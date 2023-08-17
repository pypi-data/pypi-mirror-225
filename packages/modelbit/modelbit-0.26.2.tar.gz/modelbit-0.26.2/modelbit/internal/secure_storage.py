import base64
import logging
import os
import sys
from io import BytesIO, StringIO
from typing import Any, Dict, TextIO

import boto3
import requests

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from modelbit.internal.cache import objectCacheFilePath
from modelbit.utils import inNotebook
from tqdm import tqdm
from abc import ABCMeta, abstractmethod
from modelbit.internal.describe import calcHash

logger = logging.getLogger(__name__)

defaultRequestTimeout = 10


class UploadableObjectInfo:

  def __init__(self, data: Dict[str, Any]):
    self.bucket: str = data["bucket"]
    self.s3Key: str = data["s3Key"]
    self.awsCreds: Dict[str, str] = data["awsCreds"]
    self.metadata: Dict[str, str] = data["metadata"]
    self.fileKey64: str = data["fileKey64"]
    self.fileIv64: str = data["fileIv64"]
    self.objectExists: bool = data["objectExists"]


class DownloadableObjectInfo(metaclass=ABCMeta):

  def __init__(self, data: Dict[str, Any]):
    self.workspaceId: str = data["workspaceId"]
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]

  @abstractmethod
  def cachekey(self) -> str:
    raise Exception("NYI")


def putSecureData(uploadInfo: UploadableObjectInfo, obj: bytes, desc: str) -> None:
  if uploadInfo.objectExists:
    return
  import zstd
  cipher = AES.new(  # type: ignore
      mode=AES.MODE_CBC,
      key=base64.b64decode(uploadInfo.fileKey64),
      iv=base64.b64decode(uploadInfo.fileIv64))
  body = cipher.encrypt(pad(zstd.compress(obj, 10), AES.block_size))
  _uploadFile(uploadInfo, body, desc)


def getSecureData(dri: DownloadableObjectInfo, desc: str) -> bytes:
  if not dri:
    raise Exception("Download info missing from API response.")
  filepath = objectCacheFilePath(dri.workspaceId, dri.cachekey())

  if os.path.exists(filepath):  # Try cache
    try:
      return _readAndDecryptFile(filepath, dri)
    except Exception as e:
      logger.info("Failed to read from cache", exc_info=e)

  _downloadFile(dri, filepath, desc)
  return _readAndDecryptFile(filepath, dri)


def _uploadFile(uploadInfo: UploadableObjectInfo, body: bytes, desc: str) -> None:
  s3Client = boto3.client('s3', **uploadInfo.awsCreds)  # type: ignore
  outputStream: TextIO = sys.stdout
  if not inNotebook():  # printing to stdout breaks git's add file flow
    outputStream = sys.stderr
  if os.getenv('MB_TXT_MODE'):
    outputStream = StringIO()
  with BytesIO(body) as b, tqdm(total=len(body),
                                unit='B',
                                unit_scale=True,
                                miniters=1,
                                desc=f"Uploading '{desc}'",
                                file=outputStream) as t:
    s3Client.upload_fileobj(  # type: ignore
        b,
        uploadInfo.bucket,
        uploadInfo.s3Key,
        ExtraArgs={"Metadata": uploadInfo.metadata},
        Callback=lambda bytes_transferred: t.update(bytes_transferred))  # type: ignore


def _downloadFile(dri: DownloadableObjectInfo, filepath: str, desc: str) -> None:
  logger.info(f"Downloading to {filepath}")
  outputStream: TextIO = sys.stdout
  if not inNotebook():  # printing to stdout breaks git's add file flow
    outputStream = sys.stderr
  if os.getenv('MB_TXT_MODE'):
    outputStream = StringIO()
  resp = requests.get(dri.signedDataUrl, stream=True, timeout=defaultRequestTimeout)
  total = int(resp.headers.get('content-length', 0))
  with open(filepath, "wb") as f, tqdm(total=total,
                                       unit='B',
                                       unit_scale=True,
                                       miniters=1,
                                       desc=f"Downloading '{desc}'",
                                       file=outputStream) as t:
    for data in resp.iter_content(chunk_size=32 * 1024):
      size = f.write(data)
      t.update(size)


def _readAndDecryptFile(filepath: str, dri: DownloadableObjectInfo) -> bytes:
  with open(filepath, "rb") as f:
    data = f.read()
  return _decryptAndValidate(dri, data)


ZSTD_MAGIC_NUMBER = b"\x28\xB5\x2F\xFD"
GZIP_MAGIC_NUMBER = b"\x1f\x8b"


def _isLikelyZstd(data: bytes) -> bool:
  return data[0:4] == ZSTD_MAGIC_NUMBER


def _isLikelyGzip(data: bytes) -> bool:
  return data[0:2] == GZIP_MAGIC_NUMBER


def _decompress(data: bytes) -> bytes:
  if _isLikelyZstd(data):
    import zstd
    return zstd.decompress(data)
  elif _isLikelyGzip(data):
    import zlib
    return zlib.decompress(data, zlib.MAX_WBITS | 32)
  else:
    raise Exception("Unknown compression format")


def _decryptAndValidate(dri: DownloadableObjectInfo, data: bytes) -> bytes:
  cipher = AES.new(base64.b64decode(dri.key64), AES.MODE_CBC, iv=base64.b64decode(dri.iv64))  # type: ignore
  data = unpad(cipher.decrypt(data), AES.block_size)
  data = _decompress(data)
  actualHash = calcHash(data)
  if hasattr(dri, "contentHash"):
    if actualHash != dri.contentHash:  #type: ignore
      raise ValueError(
          f"Hash mismatch. Tried to fetch {dri.contentHash}, calculated {actualHash}")  #type: ignore
  return data
