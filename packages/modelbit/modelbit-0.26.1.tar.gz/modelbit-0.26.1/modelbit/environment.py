from typing import List, Tuple, Dict, Optional, Set
import os, sys, json, time, re
import urllib.request

ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11']

PipListCache: Tuple[float, List[Dict[str, str]]] = (0, [])
PipListCacheTimeoutSeconds = 5


def listInstalledPackages():
  return [f'{p["name"]}=={p["version"]}' for p in getPipList()]


def listInstalledPackageNames():
  return [p["name"] for p in getPipList()]


# Returns List[(desiredPackage, installedPackage|None)]
def listMissingPackagesFromPipList(
    deploymentPythonPackages: Optional[List[str]]) -> List[Tuple[str, Optional[str]]]:
  missingPackages: List[Tuple[str, Optional[str]]] = []

  if deploymentPythonPackages is None or len(deploymentPythonPackages) == 0:
    return missingPackages

  installedPackages = listInstalledPackages()
  lowerInstalledPackages = [p.lower() for p in installedPackages]

  for dpp in deploymentPythonPackages:
    if "+" in dpp:
      continue
    if dpp.lower() not in lowerInstalledPackages:
      similarPackage: Optional[str] = None
      dppNoVersion = dpp.split("=")[0].lower()
      for ip in lowerInstalledPackages:
        if ip.split("=")[0] == dppNoVersion:
          similarPackage = ip
      missingPackages.append((dpp, similarPackage))

  return missingPackages


def getInstalledPythonVersion():
  installedVer = f"{sys.version_info.major}.{sys.version_info.minor}"
  return installedVer


def guessGitPackageName(gitUrl: str) -> str:
  return gitUrl.split("/")[-1].replace(".git", "")


def packagesToIgnoreFromImportCheck(deploymentPythonPackages: Optional[List[str]]) -> List[str]:
  ignorablePackages: List[str] = ["modelbit"]
  if deploymentPythonPackages is None:
    return ignorablePackages

  for p in deploymentPythonPackages:
    if p.endswith(".git"):
      ignorablePackages.append(guessGitPackageName(p))
    elif "=" in p and "+" in p:
      ignorablePackages.append(p.split("=")[0])

  missingPackages = listMissingPackagesFromPipList(deploymentPythonPackages)
  for mp in missingPackages:
    if mp[1] is not None:
      ignorablePackages.append(mp[1].split("=")[0])

  return ignorablePackages


# Mostly to prevent adding packages that were installed with git and now have a foo==bar name
def scrubUnwantedPackages(deploymentPythonPackages: List[str]) -> List[str]:

  def normalizeName(s: str) -> str:  # meant to increase matching between guessed git names and package names
    return re.sub(r"[^a-z0-9]+", "", s.lower())

  packagesToScrub: Set[str] = set(["modelbit"])
  for p in deploymentPythonPackages:
    if p.endswith(".git"):
      packagesToScrub.add(normalizeName(guessGitPackageName(p)))

  scrubbedPackageList: List[str] = []
  for p in deploymentPythonPackages:
    if "==" in p:
      packageName = normalizeName(p.split("==")[0])
      if packageName in packagesToScrub:
        continue
    scrubbedPackageList.append(p)

  return scrubbedPackageList


def addDependentPackages(deploymentPythonPackages: List[str]) -> List[str]:
  allPackages: List[str] = []

  def appendIfExists(importName: str, packageName: Optional[str] = None):
    pkg = pipPackageIfInstalled(importName, packageName)
    if pkg is not None:
      allPackages.append(pkg)

  for p in deploymentPythonPackages:
    allPackages.append(p)
    if p.startswith("xgboost="):
      appendIfExists("sklearn", "scikit-learn")
    elif p.startswith("transformers="):
      appendIfExists("keras")
      appendIfExists("tensorflow")
    elif p.startswith("segment-anything="):
      appendIfExists("torch")
      appendIfExists("torchvision")
  return allPackages


def pipPackageIfInstalled(importName: str, packageName: Optional[str] = None) -> Optional[str]:
  version = getVersionIfInstalled(importName)
  if version is not None:
    return f"{packageName or importName}=={version}"
  return None


def getVersionIfInstalled(importName: str) -> Optional[str]:
  try:
    import importlib
    mod = importlib.import_module(importName)
    return mod.__version__
  except:
    return None


def normalizeModuleName(name: str) -> str:
  return name.replace("_", "-")


# Returns List[(importedModule, pipPackageInstalled)]
def listMissingPackagesFromImports(importedModules: Optional[List[str]],
                                   deploymentPythonPackages: Optional[List[str]]) -> List[Tuple[str, str]]:
  missingPackages: List[Tuple[str, str]] = []
  ignorablePackages = packagesToIgnoreFromImportCheck(deploymentPythonPackages)
  if importedModules is None:
    return missingPackages
  if deploymentPythonPackages is None:
    deploymentPythonPackages = []

  installedModules = listInstalledPackagesByModule()
  for im in importedModules:
    baseModule = im.split(".")[0]
    baseModuleNorm = normalizeModuleName(baseModule)
    baseModuleInst = sys.modules.get(baseModule)
    if baseModuleInst is None:
      continue
    if baseModuleNorm not in installedModules:
      continue  # from stdlib or a local file, not an installed package
    pipInstalls = installedModules[baseModuleNorm]
    missingPip = True
    for pipInstall in pipInstalls:
      pipPackage = pipInstall.split("=")[0]
      if pipInstall in deploymentPythonPackages or pipPackage in ignorablePackages:
        missingPip = False
    if missingPip:
      missingPackages.append((im, guessRecommendedPackage(baseModule, pipInstalls)))

  return missingPackages


def listLocalModulesFromImports(importedModules: Optional[List[str]]) -> List[str]:
  installedModules = listInstalledPackagesByModule()
  localModules: List[str] = []
  if importedModules is None:
    return []
  for im in importedModules:
    baseModule = im.split(".")[0]
    if normalizeModuleName(baseModule) not in installedModules:
      baseModuleInst = sys.modules.get(baseModule)
      if baseModuleInst is None or not hasattr(baseModuleInst, "__file__"):
        continue
      bmf = baseModuleInst.__file__
      if bmf is None or bmf.startswith((sys.base_prefix, sys.prefix)):
        continue
      localModules.append(baseModule)
  return localModules


def guessRecommendedPackage(baseModule: str, pipInstalls: List[str]):
  if len(pipInstalls) == 0:
    return pipInstalls[0]

  # pandas-stubs==1.2.0.19 adds itself to the pandas module (other type packages seem to have their own base module)
  for pi in pipInstalls:
    if "types" not in pi.lower() and "stubs" not in pi.lower():
      return pi

  return pipInstalls[0]


def getModuleNames(distInfoPath: str) -> List[str]:
  moduleNames: List[str] = []
  try:
    topLevelPath = os.path.join(distInfoPath, "top_level.txt")
    metadataPath = os.path.join(distInfoPath, "METADATA")
    if os.path.exists(topLevelPath):
      with open(topLevelPath) as f:
        moduleNames = f.read().strip().split("\n")
    elif os.path.exists(metadataPath):
      with open(metadataPath) as f:
        lines = f.read().strip().split("\n")
        for line in lines:
          if line.startswith("Name: "):
            moduleNames.append(line.split(":")[1].strip())
            break
  except:
    pass
  return moduleNames


def getPipInstallAndModuleFromDistInfo(distInfoPath: str) -> Dict[str, List[str]]:
  try:
    moduleNames = getModuleNames(distInfoPath)
    if len(moduleNames) == 0:
      return {}

    mPath = os.path.join(distInfoPath, "METADATA")
    if not os.path.exists(mPath):
      return {}

    pipName = None
    pipVersion = None
    with open(mPath) as f:
      metadata = f.read().split("\n")
      for mLine in metadata:
        if mLine.startswith("Name: "):
          pipName = mLine.split(":")[1].strip()
        if mLine.startswith("Version: "):
          pipVersion = mLine.split(":")[1].strip()
        if pipName is not None and pipVersion is not None:
          break

    if pipName is None or pipVersion is None:
      return {}

    modulesToPipVersions: Dict[str, List[str]] = {}
    for moduleName in moduleNames:
      if moduleName not in modulesToPipVersions:
        modulesToPipVersions[moduleName] = []
      modulesToPipVersions[moduleName].append(f"{pipName}=={pipVersion}")
    return modulesToPipVersions
  except Exception as err:
    print(f"Warning, unable to check module '{distInfoPath}': {err}")
    return {}


# TODO: figure out how to recognize modules that are installed as editable
def listInstalledPackagesByModule() -> Dict[str, List[str]]:
  packages = getPipList()
  installPaths: Dict[str, int] = {}
  for package in packages:
    installPaths[package["location"]] = 1

  modulesToPipVersions: Dict[str, List[str]] = {}
  for installPath in installPaths.keys():
    try:
      for fileOrDir in os.listdir(installPath):
        if fileOrDir.endswith("dist-info"):
          dPath = os.path.join(installPath, fileOrDir)
          newModuleInfo = getPipInstallAndModuleFromDistInfo(dPath)
          for mod, pips in newModuleInfo.items():
            normMod = normalizeModuleName(mod)
            if normMod not in modulesToPipVersions:
              modulesToPipVersions[normMod] = []
            for pip in pips:
              modulesToPipVersions[normMod].append(pip)
    except Exception as err:
      # See https://gitlab.com/modelbit/modelbit/-/issues/241
      print(f"Warning, skipping module '{installPath}': {err}")
      pass

  return modulesToPipVersions


def getPipList() -> List[Dict[str, str]]:
  global PipListCache
  if time.time() - PipListCache[0] > PipListCacheTimeoutSeconds:
    PipListCache = (time.time(), _getPipList())
  return PipListCache[1]


def _getPipList() -> List[Dict[str, str]]:
  try:
    packages: List[Dict[str, str]] = []
    # need importlib_metadata imported to annotate metadata.distributions()
    import importlib_metadata  # type: ignore
    from importlib import metadata
    for i in metadata.distributions():
      dirPath = os.path.dirname(i._path)  # type: ignore
      packages.append({
          # name is added by importing importlib_metadata
          "name": i.name,  # type: ignore
          "version": i.version,
          "location": dirPath
      })
    return packages
  except Exception as err:
    print("Warning: Falling back to pip to resolve local packages.", err)
    # Some of the above isn't supported on Python 3.7, so fall back to good ol'pip
    return json.loads(os.popen("pip list -v --format json --disable-pip-version-check").read().strip())


def systemPackagesForPips(pipPackages: Optional[List[str]],
                          userSysPackages: Optional[List[str]]) -> Optional[List[str]]:
  systemPackages: Set[str] = set(userSysPackages or [])
  if pipPackages is None:
    return None
  # Add to this list as we find more dependencies that packages need
  lookups: Dict[str, List[str]] = {
      "fasttext": ["build-essential"],
      "psycopg2": ["libpq5", "libpq-dev"],
      "opencv-python": ["python3-opencv"],
      "opencv-python-headless": ["python3-opencv"],
      "xgboost": ["libgomp1"],
      "lightgbm": ["libgomp1"],
      "groundingdino-py": ["build-essential"],
  }
  for pipPackage in pipPackages:
    name = pipPackage.split("=")[0].lower()
    for sysPkg in lookups.get(name, []):
      systemPackages.add(sysPkg)
    if pipPackage.startswith("git+"):
      systemPackages.add("git")

  if (len(systemPackages)) == 0:
    return None
  return sorted(list(systemPackages))


def versionProbablyWrong(pyPackage: str) -> bool:
  if pyPackage.startswith("git") or "+" in pyPackage or "==" not in pyPackage:
    return False
  name, version = pyPackage.split("==", 1)
  with urllib.request.urlopen(f"https://pypi.org/simple/{name}/") as uf:
    return f"-{version}-" not in uf.read().decode("utf8")
