"""Adaptateur de stockage de fichiers : système de fichiers local (défaut) ou S3.

Interface stable utilisée par le service documents et la data room :
- put()  : stocke des octets et renvoie une `storage_key` opaque (chemin FS ou s3://…).
- get()  : relit les octets depuis une `storage_key`.
- presigned_url() : URL signée temporaire (S3 uniquement ; None en local).

`storage_provider="s3"` + `s3_bucket` active le backend S3 (AWS / Scaleway / MinIO).
Le backend S3 utilise boto3 (chaîne d'identifiants AWS standard) et chiffre côté
serveur (SSE) par défaut.
"""
from __future__ import annotations

import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger("dealiq.storage")


def object_key(company_id: str, doc_id: str, filename: str) -> str:
    return f"{company_id}/{doc_id}_{filename}"


def put(
    company_id: str, doc_id: str, filename: str, data: bytes, content_type: str | None = None
) -> str:
    key = object_key(company_id, doc_id, filename)
    if settings.storage_provider == "s3":
        return _s3_put(key, data, content_type)
    return _local_put(key, data)


def get(storage_key: str) -> bytes:
    if storage_key.startswith("s3://"):
        return _s3_get(storage_key)
    return Path(storage_key).read_bytes()


def presigned_url(storage_key: str, expires: int = 900) -> str | None:
    if not storage_key.startswith("s3://"):
        return None
    bucket, key = _split_s3(storage_key)
    return _s3_client().generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )


# --- Backend local (FS) ---
def _local_put(key: str, data: bytes) -> str:
    path = Path(settings.storage_dir) / key
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


# --- Backend S3 ---
def _s3_client():  # pragma: no cover - réseau ; monkeypatché dans les tests
    import boto3

    return boto3.client(
        "s3",
        region_name=settings.s3_region or None,
        endpoint_url=settings.s3_endpoint_url or None,
    )


def _split_s3(storage_key: str) -> tuple[str, str]:
    rest = storage_key.removeprefix("s3://")
    bucket, _, key = rest.partition("/")
    return bucket, key


def _s3_put(key: str, data: bytes, content_type: str | None) -> str:
    if not settings.s3_bucket:
        raise RuntimeError("S3 non configuré (s3_bucket vide).")
    extra: dict = {}
    if content_type:
        extra["ContentType"] = content_type
    if settings.s3_sse:
        extra["ServerSideEncryption"] = settings.s3_sse
    _s3_client().put_object(Bucket=settings.s3_bucket, Key=key, Body=data, **extra)
    return f"s3://{settings.s3_bucket}/{key}"


def _s3_get(storage_key: str) -> bytes:
    bucket, key = _split_s3(storage_key)
    obj = _s3_client().get_object(Bucket=bucket, Key=key)
    return obj["Body"].read()
