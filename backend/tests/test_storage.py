"""Tests de l'adaptateur de stockage : backend local (FS) et S3 (boto3 monkeypatché)."""
from __future__ import annotations

import io

import pytest

from app.services import storage


class _FakeS3:
    """Faux client S3 capturant les objets en mémoire (aucun accès réseau)."""

    def __init__(self) -> None:
        self.objects: dict[tuple[str, str], bytes] = {}
        self.put_kwargs: list[dict] = []

    def put_object(self, Bucket, Key, Body, **kwargs):  # noqa: N803
        self.objects[(Bucket, Key)] = Body
        self.put_kwargs.append(kwargs)

    def get_object(self, Bucket, Key):  # noqa: N803
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}

    def generate_presigned_url(self, op, Params, ExpiresIn):  # noqa: N803
        return f"https://{Params['Bucket']}.s3.example/{Params['Key']}?e={ExpiresIn}"


def test_local_roundtrip(monkeypatch, tmp_path):
    monkeypatch.setattr(storage.settings, "storage_provider", "local")
    monkeypatch.setattr(storage.settings, "storage_dir", str(tmp_path))
    key = storage.put("c1", "d1", "file.pdf", b"%PDF-data")
    assert key.startswith(str(tmp_path))
    assert storage.get(key) == b"%PDF-data"
    assert storage.presigned_url(key) is None  # pas d'URL signée en local


def test_s3_roundtrip_with_sse(monkeypatch):
    fake = _FakeS3()
    monkeypatch.setattr(storage, "_s3_client", lambda: fake)
    monkeypatch.setattr(storage.settings, "storage_provider", "s3")
    monkeypatch.setattr(storage.settings, "s3_bucket", "dealiq-docs")
    monkeypatch.setattr(storage.settings, "s3_sse", "AES256")

    key = storage.put("c1", "d1", "file.pdf", b"%PDF-data", "application/pdf")
    assert key == "s3://dealiq-docs/c1/d1_file.pdf"
    assert fake.put_kwargs[-1]["ServerSideEncryption"] == "AES256"  # chiffrement
    assert fake.put_kwargs[-1]["ContentType"] == "application/pdf"

    assert storage.get(key) == b"%PDF-data"
    url = storage.presigned_url(key)
    assert url and "dealiq-docs" in url and "c1/d1_file.pdf" in url


def test_s3_requires_bucket(monkeypatch):
    monkeypatch.setattr(storage.settings, "storage_provider", "s3")
    monkeypatch.setattr(storage.settings, "s3_bucket", "")
    with pytest.raises(RuntimeError):
        storage.put("c1", "d1", "f.pdf", b"x")
