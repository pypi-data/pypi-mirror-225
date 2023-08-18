from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel


class GetCredentialByResourceName(BaseModel):
    credential_by_resource_name: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential",
                "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialByResourceName")


class GetCredentialByResourceNameCredentialByResourceNameCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential", "GcpCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig(
    BaseModel
):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential(
    BaseModel
):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential(
    BaseModel
):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig(
    BaseModel
):
    account: str
    user: str


class GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredential(BaseModel):
    typename__: Literal["KafkaSSLCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredential(
    BaseModel
):
    typename__: Literal["KafkaSaslSSLPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


GetCredentialByResourceName.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameKafkaSSLCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSSLPlainCredentialConfig.update_forward_refs()
