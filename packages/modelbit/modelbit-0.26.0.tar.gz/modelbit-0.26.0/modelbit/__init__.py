__version__ = "0.26.0"
__author__ = 'Modelbit'
from . import helpers as m_helpers

m_helpers.pkgVersion = __version__

import os, sys, yaml, pickle, logging
from typing import cast, Union, Callable, Any, Dict, List, Optional, TYPE_CHECKING

# aliasing since some of these overlap with functions we want to expose to users

from . import runtime as m_runtime
from . import utils as m_utils
from . import model_wrappers as m_model_wrappers
from . import collect_dependencies as m_collect_dependencies
from . import jobs as m_jobs
from . import telemetry as m_telemetry

from modelbit.internal.auth import mbApi as _mbApi, mbApiReadOnly, isAuthenticated as isAuthenticated
from modelbit.error import ModelbitError as ModelbitError, UserFacingError as UserFacingError

if TYPE_CHECKING:
  import pandas
  import modelbit.internal.datasets as m_datasets
  import modelbit.internal.warehouses as m_warehouses
  import modelbit.internal.deployments as m_deployments

m_telemetry.initLogging()
logger = logging.getLogger(__name__)


# Nicer UX for customers: from modelbit import Deployment
class Deployment(m_runtime.Deployment):
  ...


errorHandler = lambda msg: m_telemetry.eatErrorAndLog(mbApiReadOnly(), msg)  # type: ignore


def __str__():
  return "Modelbit Client"


def _repr_html_():  # type: ignore
  return ""


@errorHandler("Failed to add job.")
def add_job(
    func: Callable[..., Any],
    deployment_name: str,
    name: Optional[str] = None,
    store_result_as: Optional[str] = None,
    python_version: Optional[str] = None,
    python_packages: Optional[List[str]] = None,
    system_packages: Optional[List[str]] = None,
    extra_files: Union[List[str], Dict[str, str], None] = None,
    redeploy_on_success: bool = True,
    email_on_failure: Optional[str] = None,
    schedule: Optional[str] = None,
    refresh_datasets: Optional[List[str]] = None,
    size: Optional[str] = None,
    timeout_minutes: Optional[int] = None,
    default_arguments: Optional[List[Any]] = None,
) -> 'm_jobs.ModelbitJobWrapper':
  """Adds a job to a new or existing deployment.
     For more details, see https://doc.modelbit.com/jobs/notebooks

    Jobs are a way to automate workflows you do manually in a notebook.

    Jobs run python functions in Modelbit and create artifacts that
    can be accessed in both notebooks and inference functions.

    A job's output can be accessed using `modelbit.get_latest_job_output(deployment_name, job_name)`
    To access output for previous job runs, use `modelbit.get_job_runs(deployment_name, job_name)`

    Behind the scenes, modelbit saves the result of this function and loads it when your deployment is called.

    You'll be able to re-run that function and update the value used in your deployment without having to
    redeploy from your notebook.


    Args:
      func: Training function that returns a model.
      deployment_name: Name of a deployment for this job. Will be created if missing.
          Jobs share an environment with the attached deployment.
      name: Name of the job
      store_result_as: Name of job result file. Defaults to the job name. Job results are stored as
          files accessible via git in the `data/` directory of a deployment.
      redeploy_on_success: By default, the output from this job is available when the job finishes.
          When false, output must be manually promoted before it is accessible from `get_latest_job_output`.
      schedule: Modelbit jobs can be run on any schedule you can define with a cron string.
          You can also use the simpler schedules of hourly, daily, weekly and monthly.
      refresh_datasets: Jobs usually require fresh data to retrain their models. This is a list
          of datasets to refresh before executing the job.
      size: See https://doc.modelbit.com/jobs#runner-sizes
      timeout_minutes: Timeout before job is stopped. Integers between 5 and 1440 (1 day)
      email_on_failure: Modelbit can email you if your job fails. Set to your email address.
      For the rest, see https://doc.modelbit.com/custom-python-environments/


    Returns:
      A `modelbit.jobs.ModelbitJobWrapper` object.

      This can be passed to `modelbit.run_job()` to run the newly created job.

    Raises:
      modelbit.error.ModelbitError: An error occurred creating the job.
  """
  return m_jobs.add_job(_mbApi(), func, deployment_name, name, store_result_as, python_version,
                        python_packages, system_packages, extra_files, redeploy_on_success, email_on_failure,
                        schedule, refresh_datasets, size, timeout_minutes, default_arguments)


@errorHandler("Failed to run job.")
def run_job(deployment_name: str,
            job_name: Optional[str] = None,
            arguments: Optional[List[Any]] = None,
            branch: Optional[str] = None) -> 'm_jobs.ModelbitJobRun':
  """Run a job in Modelbit.
     For more details, run help(modelbit.add_job) and see https://doc.modelbit.com/jobs/notebooks.

    Args:
      deployment_name_or_job: Deployment name containing the job to run.
          Can also be a ModelbitJobWrapper returned from `modelbit.add_job`.
      job_name: The name of the job to run. Required if deployment_name_or_job is a string.
      arguments: Optional. A list of arguments passed to the deployment function. Must be JSON serializable.
            A value of None uses the defaults. Pass an empty list to override the default with no arguments.
      branch: Optional. Branch to find the job. Defaults to the current branch.

    Returns:
      A `modelbit.jobs.ModelbitJobRun` object.

      This has a `wait()` function to wait for the job to complete.

      job = modelbit.run_job('doubler', 'train')
      job.wait()
      model = modelbit.get_job_output('doubler', 'train', run_id=job.run_id)

    Raises:
      modelbit.error.ModelbitError: An error occurred running the job.
  """
  if type(deployment_name) is str and job_name is not None:
    return m_jobs.runJob(runtimeName=deployment_name,
                         jobName=job_name,
                         args=arguments,
                         mbApi=_mbApi(),
                         branch=branch or m_helpers.getCurrentBranch())
  else:
    raise TypeError("missing job_name")


@errorHandler("Failed to get job output.")
def get_job_output(deployment_name: str,
                   job_name: str,
                   branch: Optional[str] = None,
                   run_id: Optional[int] = None,
                   result_stored_as: Optional[str] = None,
                   file_name: Optional[str] = None):
  """Get the latest output from a job. Works both in notebooks and inference functions.

    For more details on jobs, run help(modelbit.add_job) and see https://doc.modelbit.com/jobs/notebooks.

    Args:
      deployment_name: Deployment name containing the job.
      job_name: The name of the job.
      branch: Optional. Branch to find the job. Defaults to the current branch.
      run_id: Optional. The ID of the recent job run, visible in the Web UI.
      file_name: Optional. The name of the file written during the job

    Returns:
      The result of the job run.

    Raises:
      modelbit.error.ModelbitError: An error occurred finding the job output.

    Note:
      This function is designed to work with jobs created with modelbit.add_job() in the notebook.
      For more details on using jobs with git, see https://doc.modelbit.com/jobs/git
  """
  if result_stored_as is not None:
    file_name = f"data/{result_stored_as}.pkl"
  return m_jobs.getJobOutput(runtimeName=deployment_name,
                             jobName=job_name,
                             branch=branch or m_helpers.getCurrentBranch(),
                             userFacingId=run_id,
                             fileName=file_name,
                             mbApi=_mbApi())


@errorHandler("Failed to list datasets.")
def datasets() -> 'm_datasets.DatasetList':
  import modelbit.internal.datasets as m_datasets
  return m_datasets.list(_mbApi())


@errorHandler("Failed to load dataset.")
def get_dataset(dsName: str,
                filters: Optional[Dict[str, List[Any]]] = None,
                filter_column: Optional[str] = None,
                filter_values: Optional[List[Any]] = None,
                optimize: Optional[bool] = None,
                legacy: Optional[bool] = None,
                branch: Optional[str] = None) -> Optional['pandas.DataFrame']:
  if filter_column is not None and filter_values is not None:
    print("Deprecated: filter_column= & filter_values= will be removed soon. Use filters= instead.")
    if filters is None:
      filters = {}
    filters[filter_column] = filter_values
  if optimize is not None:
    print("Deprecated: optimize= will be removed soon.")

  import modelbit.internal.feature_store as m_feature_store
  return m_feature_store.getDataFrame(_mbApi(),
                                      branch=branch or m_helpers.getCurrentBranch(),
                                      dsName=dsName,
                                      filters=filters)


@errorHandler("Failed to load warehouses.")
def warehouses() -> 'm_warehouses.WarehousesList':
  import modelbit.internal.warehouses as m_warehouses
  return m_warehouses.list(_mbApi())


@errorHandler("Failed to load deployments.")
def deployments() -> 'm_deployments.DeploymentsList':
  import modelbit.internal.deployments as m_deployments
  return m_deployments.list(_mbApi())


@errorHandler("Failed to add files.")
def add_files(deployment: str,
              files: Union[List[str], Dict[str, str]],
              modelbit_file_prefix: Optional[str] = None,
              strip_input_path: Optional[bool] = False):
  return m_runtime.add_files(_mbApi(), deployment, files, modelbit_file_prefix, strip_input_path)


@errorHandler("Failed to add objects.")
def add_objects(deployment: str, values: Dict[str, Any]):
  return m_runtime.add_objects(_mbApi(), deployment, values)


@errorHandler("Failed to load secret.")
def get_secret(name: str,
               deployment: Optional[str] = None,
               branch: Optional[str] = None,
               encoding: str = "utf8") -> str:
  import modelbit.internal.secrets as m_secrets
  return m_secrets.get_secret(name, deployment, branch, encoding, _mbApi())


@errorHandler("Failed to add package.")
def add_package(path: str, force: bool = False):
  import modelbit.internal.package as m_package
  return m_package.add_package(path, force, _mbApi())


@errorHandler("Failed to delete package.")
def delete_package(name: str, version: str):
  import modelbit.internal.package as m_package
  return m_package.delete_package(name, version, _mbApi())


@errorHandler("Failed to add common files.")
def add_common_files(files: Union[List[str], Dict[str, str], str]):
  import modelbit.internal.common_files as m_common_files
  m_common_files.addFiles(_mbApi(), files)


@errorHandler("Failed to delete common files.")
def delete_common_files(names: Union[List[str], str]):
  import modelbit.internal.common_files as m_common_files
  m_common_files.deleteFiles(_mbApi(), names)


@errorHandler("Failed to list common files.")
def common_files(prefix: Optional[str] = None):
  import modelbit.internal.common_files as m_common_files
  return m_common_files.listFiles(_mbApi(), prefix)


@errorHandler("Failed to deploy.")
def deploy(deployableObj: Union[Callable[..., Any], 'm_runtime.Deployment'],
           name: Optional[str] = None,
           python_version: Optional[str] = None,
           python_packages: Optional[List[str]] = None,
           system_packages: Optional[List[str]] = None,
           dataframe_mode: bool = False,
           example_dataframe: Optional['pandas.DataFrame'] = None,
           extra_files: Union[List[str], Dict[str, str], None] = None,
           require_gpu: bool = False):
  if type(deployableObj) is m_jobs.ModelbitJobWrapper:
    raise UserFacingError("Cannot deploy a job. Use modelbit.add_job()")

  if _objIsDeployment(deployableObj):
    deployableObj = cast(Deployment, deployableObj)
    return deployableObj.deploy()
  elif callable(deployableObj) and deployableObj.__name__ == "<lambda>":
    return m_model_wrappers.LambdaWrapper(deployableObj,
                                          name=name,
                                          python_version=python_version,
                                          python_packages=python_packages,
                                          system_packages=system_packages,
                                          dataframe_mode=dataframe_mode,
                                          example_dataframe=example_dataframe,
                                          extra_files=extra_files,
                                          require_gpu=require_gpu).makeDeployment(_mbApi()).deploy()
  elif callable(deployableObj):
    return Deployment(api=_mbApi(),
                      name=name,
                      deploy_function=deployableObj,
                      python_version=python_version,
                      python_packages=python_packages,
                      system_packages=system_packages,
                      dataframe_mode=dataframe_mode,
                      example_dataframe=example_dataframe,
                      extra_files=extra_files,
                      require_gpu=require_gpu).deploy()
  elif hasattr(deployableObj, "__module__") and "sklearn" in deployableObj.__module__ and hasattr(
      deployableObj, "predict"):
    return m_model_wrappers.SklearnPredictor(deployableObj,
                                             name=name,
                                             python_version=python_version,
                                             python_packages=python_packages,
                                             system_packages=system_packages,
                                             dataframe_mode=dataframe_mode,
                                             example_dataframe=example_dataframe,
                                             extra_files=extra_files,
                                             require_gpu=require_gpu).makeDeployment(_mbApi()).deploy()
  else:
    raise Exception("First argument must be a function or Deployment object.")


@errorHandler("Unable to log in.")
def login(region: Optional[str] = None, branch: Optional[str] = None):
  _mbApi(region=region, branch=branch)
  return sys.modules['modelbit']


def switch_branch(branch: str):
  # See if new branch exists, but not from deployments
  if (not m_utils.inDeployment() and not mbApiReadOnly().refreshAuthentication(branch=branch)):
    raise UserFacingError(f"Branch {branch} not found.")
  m_helpers.setCurrentBranch(branch)


def get_branch() -> str:
  return m_helpers.getCurrentBranch()


def in_modelbit() -> bool:
  return m_utils.inDeployment()


def get_deployment_info() -> Dict[str, Any]:
  if not in_modelbit():
    print("get_deployment_info: Warning, not currently running in a deployment.")
  return {
      "branch": m_helpers.getCurrentBranch(),
      "name": m_helpers.getDeploymentName(),
      "version": m_helpers.getDeploymentVersion()
  }


def log_image(obj: Any):
  import modelbit.file_logging as m_file_logging
  m_file_logging.logImage(obj)


def load_value(name: str, restoreClass: Optional[type] = None):
  if name.endswith(".pkl"):
    import __main__ as main_package
    # Support finding files relative to source location
    # This doesn't work from lambda, so only use when not in a deployment
    if not os.path.exists(name):
      name = os.path.join(os.path.dirname(main_package.__file__), name)

    with open(name, "rb") as f:
      value = pickle.load(f)
      if restoreClass is not None and isinstance(value, m_helpers.InstancePickleWrapper):
        return value.restore(restoreClass)
      else:
        return value
  extractPath = os.environ['MB_EXTRACT_PATH']
  objPath = os.environ['MB_RUNTIME_OBJ_DIR']
  if not extractPath or not objPath:
    raise Exception("Missing extractPath/objPath")
  with open(f"{extractPath}/metadata.yaml", "r") as f:
    yamlData = cast(Dict[str, Any], yaml.load(f, Loader=yaml.SafeLoader))  # type: ignore
  data: Dict[str, Dict[str, str]] = yamlData["data"]
  contentHash = data[name]["contentHash"]
  with open(f"{objPath}/{contentHash}.pkl.gz", "rb") as f:
    return m_utils.deserializeGzip(contentHash, f.read)


def save_value(obj: Any, filepath: str):
  if not m_collect_dependencies.savedSpecialObj(obj, filepath):
    if not os.path.exists(os.path.dirname(filepath)):
      os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if (hasattr(obj, "__module__") and obj.__module__ == "__main__"):
      # If the object is in __main__, move it so we can load it from a source file.
      # This allows objects saved from jobs to be loaded by inference functions.
      import inspect
      callerFrame = inspect.stack()[1]
      module = inspect.getmodule(callerFrame[0])
      if module is not None and module.__file__ is not None:
        obj = m_utils.repickleFromMain(obj, module)

    with open(filepath, "wb") as f:
      pickle.dump(obj, f)


def _objIsDeployment(obj: Any):
  try:
    if type(obj) in [Deployment, m_runtime.Deployment]:
      return True
    # catch modelbit._reload() class differences
    if obj.__class__.__name__ in ['Deployment']:
      return True
  except:
    return False
  return False


def parseArg(s: str) -> Any:
  import json
  try:
    return json.loads(s)
  except json.decoder.JSONDecodeError:
    return s
