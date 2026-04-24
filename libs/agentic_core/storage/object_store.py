"""Thin S3-compatible object store. Tenant-prefixed keys for isolation."""

from dataclasses import dataclass
from functools import lru_cache
from uuid import UUID

import boto3
from botocore.client import BaseClient

from ..config import get_settings


def _tenant_key(tenant_id: UUID, key: str) -> str:
    return f"tenants/{tenant_id}/{key.lstrip('/')}"


@dataclass
class ObjectStore:
    client: BaseClient
    bucket: str

    def put(self, tenant_id: UUID, key: str, body: bytes, content_type: str = "application/octet-stream") -> str:
        full_key = _tenant_key(tenant_id, key)
        self.client.put_object(Bucket=self.bucket, Key=full_key, Body=body, ContentType=content_type)
        return full_key

    def get(self, tenant_id: UUID, key: str) -> bytes:
        full_key = _tenant_key(tenant_id, key)
        response = self.client.get_object(Bucket=self.bucket, Key=full_key)
        return response["Body"].read()

    def presigned_url(self, tenant_id: UUID, key: str, expires_in: int = 3600) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": _tenant_key(tenant_id, key)},
            ExpiresIn=expires_in,
        )

    def ensure_bucket(self) -> None:
        existing = {b["Name"] for b in self.client.list_buckets().get("Buckets", [])}
        if self.bucket not in existing:
            self.client.create_bucket(Bucket=self.bucket)


@lru_cache
def get_object_store() -> ObjectStore:
    s = get_settings()
    client = boto3.client(
        "s3",
        endpoint_url=s.s3_endpoint_url,
        region_name=s.s3_region,
        aws_access_key_id=s.s3_access_key,
        aws_secret_access_key=s.s3_secret_key,
    )
    return ObjectStore(client=client, bucket=s.s3_bucket)
