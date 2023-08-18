from datetime import datetime
from typing import Annotated, List, Literal, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel


class ListCredentials(BaseModel):
    credentials_list: List[
        Annotated[
            Union[
                "ListCredentialsCredentialsListCredential",
                "ListCredentialsCredentialsListAwsCredential",
                "ListCredentialsCredentialsListAwsAthenaCredential",
                "ListCredentialsCredentialsListAwsRedshiftCredential",
                "ListCredentialsCredentialsListPostgreSqlCredential",
                "ListCredentialsCredentialsListSnowflakeCredential",
                "ListCredentialsCredentialsListKafkaSSLCredential",
                "ListCredentialsCredentialsListKafkaSaslSSLPlainCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialsList")


class ListCredentialsCredentialsListCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential", "GcpCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListCredentialsCredentialsListAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsCredentialConfig"


class ListCredentialsCredentialsListAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class ListCredentialsCredentialsListAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsAthenaCredentialConfig"


class ListCredentialsCredentialsListAwsAthenaCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class ListCredentialsCredentialsListAwsRedshiftCredential(BaseModel):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsRedshiftCredentialConfig"


class ListCredentialsCredentialsListAwsRedshiftCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListPostgreSqlCredential(BaseModel):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListPostgreSqlCredentialConfig"


class ListCredentialsCredentialsListPostgreSqlCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListSnowflakeCredentialConfig"


class ListCredentialsCredentialsListSnowflakeCredentialConfig(BaseModel):
    account: str
    user: str


class ListCredentialsCredentialsListKafkaSSLCredential(BaseModel):
    typename__: Literal["KafkaSSLCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSSLCredentialConfig"


class ListCredentialsCredentialsListKafkaSSLCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class ListCredentialsCredentialsListKafkaSaslSSLPlainCredential(BaseModel):
    typename__: Literal["KafkaSaslSSLPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSaslSSLPlainCredentialConfig"


class ListCredentialsCredentialsListKafkaSaslSSLPlainCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


ListCredentials.update_forward_refs()
ListCredentialsCredentialsListCredential.update_forward_refs()
ListCredentialsCredentialsListAwsCredential.update_forward_refs()
ListCredentialsCredentialsListAwsCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListAwsAthenaCredential.update_forward_refs()
ListCredentialsCredentialsListAwsAthenaCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListAwsRedshiftCredential.update_forward_refs()
ListCredentialsCredentialsListAwsRedshiftCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListPostgreSqlCredential.update_forward_refs()
ListCredentialsCredentialsListPostgreSqlCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListSnowflakeCredential.update_forward_refs()
ListCredentialsCredentialsListSnowflakeCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListKafkaSSLCredential.update_forward_refs()
ListCredentialsCredentialsListKafkaSSLCredentialConfig.update_forward_refs()
ListCredentialsCredentialsListKafkaSaslSSLPlainCredential.update_forward_refs()
ListCredentialsCredentialsListKafkaSaslSSLPlainCredentialConfig.update_forward_refs()
