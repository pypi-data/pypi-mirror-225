from sgqlc.types import Type, Field, Union, list_of, non_null, ArgDict, Input, Enum, Scalar
from sgqlc.types.datetime import DateTime


class Base64String(Scalar):
    converter = str


class ScalarBoolean(Type):
    boolValue = non_null(bool)


class ScalarInt(Type):
    intValue = non_null(int)


class ScalarString(Type):
    stringValue = non_null(str)


class TableColumnInfoValue(Union):
    __types__ = (ScalarInt, ScalarBoolean, ScalarString)


class TableColumnInfo(Type):
    name = non_null(str)
    value = TableColumnInfoValue


class TableColumnDescription(Type):
    name = non_null(str)
    description = str
    type = non_null(str)
    graphqlType = str
    nullable = non_null(bool)
    index = int
    extra = non_null(list_of(non_null(TableColumnInfo)))


class TableStateEnum(Enum):
    __choices__ = ("INIT", "LOADING", "READY", "ERROR", "DELETING", "PAUSED")


class TableDescription(Type):
    id = non_null(str)
    name = non_null(str)
    database = non_null(str)
    schema = non_null(str)
    type = non_null(str)
    description = str
    columns = non_null(list_of(non_null(TableColumnDescription)))
    sizeBytes = int
    rowCount = int


class SourceDescription(Type):
    id = non_null(str)
    namespace = non_null(list_of(non_null(str)))
    tables = non_null(list_of(non_null(TableDescription)))
    quota = int
    quotaUsed = int


class TableDescriptions(Type):
    sourceId = non_null(str)
    tableDescriptions = non_null(list_of(non_null(TableDescription)))


class User(Type):
    id = non_null(str)
    login = non_null(str)
    fullName = str
    loggedIn = bool
    tenantId = non_null(str)


class CurrentUser(Type):
    id = non_null(str)
    login = non_null(str)
    fullName = str
    loggedIn = bool
    tenant = non_null('Tenant')


class Tenant(Type):
    id = non_null(str)
    name = non_null(str)
    isMultiTenant = non_null(bool)
    users = non_null(list_of(non_null('User')))
    quota = int
    quotaUsed = int


class Source(Type):
    id = non_null(str)
    name = non_null(str)


class HttpMethod(Enum):
    __choices__ = ("POST", "PUT")


class HttpHeader(Type):
    name = non_null(str)


class DestinationType(Enum):
    __choices__ = ("DATASET_API", "BATCH_API")


class BatchApiDestination(Type):
    retentionDays = non_null(int)


class BatchApiDestinationInput(Input):
    retentionDays = int


class WebhookDestination(Type):
    url = non_null(str)
    method = non_null(HttpMethod)
    headers = non_null(list_of(non_null(HttpHeader)))
    maxBatchSize = non_null(int)
    retentionDays = non_null(int)


class Destination(Type):
    name = non_null(str)
    type = non_null(DestinationType)
    batchApi = BatchApiDestination


class DatasetTableColumn(Type):
    name = non_null(str)

class DatasetTableColumnMetadata(Type):
    name = non_null(str)
    graphqlType = str

class TableEdgeOnColumns(Type):
    fromColumnName = non_null(str)
    toColumnName = non_null(str)


class TableEdge(Type):
    name = non_null(str)
    fromTableId = non_null(str)
    toTableId = non_null(str)
    onColumns = non_null(list_of(non_null(TableEdgeOnColumns)))
    unique = bool


class ColumnMappingInput(Input):
    sourceColumn = non_null(str)
    destinationField = non_null(str)


class TableMappingInput(Input):
    tableId = non_null(str)
    mappedTableName = str
    columnMappings = list_of(non_null(ColumnMappingInput))


class TableMapping(Type):
    tableId = non_null(str)
    mappedTableName = str
    mapping = list_of(non_null(TableMappingInput))


class DatasetTable(Type):
    id = non_null(str)
    qualifiedTableIdentifier = non_null(str)
    name = non_null(str)
    columns = non_null(list_of(non_null(DatasetTableColumnMetadata)))
    primaryKey = non_null(list_of(non_null(DatasetTableColumn)))
    tableState = non_null(TableStateEnum)
    lastRowCount = int
    edges = list_of(non_null(TableEdge))
    lastSyncAt = DateTime
    lastCdcSuccessTimeAgo = str


class DatasetDestination(Type):
    name = non_null(str)
    mapping = list_of(non_null(TableMapping))
    destination = non_null(Destination)


class DatasetDestinationInput(Input):
    name = non_null(str)
    mapping = list_of(non_null(TableMappingInput))

class DatasetVersion(Type):
    version = non_null(int)
    tables = non_null(list_of(non_null(DatasetTable)))

class Dataset(Type):
    id = non_null(str)
    name = non_null(str)
    versions = non_null(list_of(non_null(DatasetVersion)))
    tables = non_null(list_of(non_null('DatasetTable')))
    destinations = non_null(list_of(non_null(DatasetDestination)))
    latestVersion = non_null(int)


class QueryAuth(Type):
    accessToken = non_null(str)


class DataAccessKey(Type):
    id = non_null(str)
    name = non_null(str)
    sourceId = non_null(str)
    datasetName = non_null(str)
    createdAt = non_null(str)
    accessKey = non_null(str)


class SourceDisconnectInput(Input):
    name = non_null(str)


class CreateDatasetTableIngestModeEnum(Enum):
    __choices__ = ("ONCE", "CONTINUOUS")


class CreateDatasetTableColumnInput(Input):
    columnName = non_null(str)


class CreateObjectStorageTableInput(Input):
    prefix = str
    filePattern = str


class CreateDatasetTableInput(Input):
    tableId = non_null(str)
    primaryKey = list_of(non_null(CreateDatasetTableColumnInput))
    primaryKeys = list_of(non_null(CreateDatasetTableColumnInput))
    ingestMode = CreateDatasetTableIngestModeEnum
    objectStorage = CreateObjectStorageTableInput

class UpdateDatasetTableInput(Input):
    tableId = non_null(str)
    ingestMode = CreateDatasetTableIngestModeEnum
    primaryKey = list_of(non_null(CreateDatasetTableColumnInput))
    objectStorage = CreateObjectStorageTableInput

class UpdateDatasetPayload(Type):
    ok = non_null(bool)
    createdVersion = non_null(int)

class CreateDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    tables = non_null(list_of(non_null(CreateDatasetTableInput)))
    destinations = list_of(non_null(DatasetDestinationInput))

class UpdateDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    tables = non_null(list_of(non_null(UpdateDatasetTableInput)))
    version = non_null(int)

class DestinationInput(Input):
    name = non_null(str)
    type = non_null(DestinationType)
    batchApi = BatchApiDestinationInput


class TableDescriptionsInput(Input):
    sourceId = non_null(str)
    tableIds = non_null(list_of(non_null(str)))


class RemoveDestinationInput(Input):
    name = non_null(str)


class TableEdgeOnColumnsInput(Input):
    fromColumnName = non_null(str)
    toColumnName = non_null(str)


class TableEdgeInput(Input):
    name = non_null(str)
    fromTableId = non_null(str)
    toTableId = non_null(str)
    onColumns = non_null(list_of(non_null(TableEdgeOnColumnsInput)))
    unique = bool


class GetSourceStatusInput(Input):
    name = non_null(str)


class AuthenticationMethodEnum(Enum):
    __choices__ = ("PASSWORD", "RSA")


class SourceConnectionSnowflakeInput(Input):
    name = non_null(str)
    user = non_null(str)
    password = str
    authenticationMethod = AuthenticationMethodEnum
    host = non_null(str)
    warehouse = non_null(str)
    database = non_null(str)
    schema = non_null(str)
    stagingDatabase = str


class GetSourceListInput(Input):
    sourceName = str


class SourceConnectionAzureBlobInput(Input):
    name = non_null(str)
    containerName = non_null(str)
    accountName = non_null(str)
    sasToken = str
    sharedKey = str


class SourceConnectionDatabricksInput(Input):
    name = non_null(str)
    hostname = non_null(str)
    httpPath = non_null(str)
    token = non_null(str)


class SourceConnectionBigQueryInput(Input):
    name = non_null(str)
    credentialsKey = non_null(str)
    projectId = non_null(str)
    location = str
    dataset = str
    stagingProjectId = non_null(str)


class RegisterUserInput(Input):
    phone = str
    email = str
    tenantId = str
    fullName = str
    isMultiTenant = non_null(bool)


class UnregisterUserInput(Input):
    userId = non_null(str)


class UpdateUserInput(Input):
    userId = non_null(str)
    fullName = str


class UpdateTenantInput(Input):
    tenantId = non_null(str)
    name = str
    quota = int


class CreateTenantInput(Input):
    name = str
    quota = int


class DeleteTenantInput(Input):
    tenantId = non_null(str)


class GetTenantsInput(Input):
    pass


class DatasetByNameInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)


class SyncDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = str
    datasetId = str
    tableName = str


class DatasetsInput(Input):
    sourceId = non_null(str)


class DataAccessKeysInput(Input):
    showKey = bool
    sourceId = str
    datasetName = str


class RemoveDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)


class PauseDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)


class GenerateQueryAuthFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class GenerateQueryAuthInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    filters = list_of(non_null(GenerateQueryAuthFilterInput))


class RevokeDataAccessKeyInput(Input):
    dataAccessKeyId = non_null(str)


class GenerateDataAccessKeyFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class GenerateDataAccessKeyInput(Input):
    name = non_null(str)
    sourceId = non_null(str)
    datasetName = non_null(str)
    filters = list_of(non_null(GenerateDataAccessKeyFilterInput))


class CustomSigningTemplateFilter(Type):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class CustomSigningTemplateJwk(Type):
    kid = non_null(str)


class CustomSigningTemplate(Type):
    id = non_null(str)
    name = non_null(str)
    sourceId = str
    datasetName = str
    jwks = non_null(list_of(non_null(CustomSigningTemplateJwk)))
    filters = non_null(list_of(non_null(CustomSigningTemplateFilter)))


class CustomSigningTemplateFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class CreateCustomSigningTemplateInput(Input):
    name = non_null(str)
    jwk = non_null(str)
    sourceId = str
    datasetName = str
    filters = non_null(list_of(non_null(CustomSigningTemplateFilterInput)))


class DeleteCustomSigningTemplateInput(Input):
    customSigningTemplateId = non_null(str)


class SnowflakeSharing(Type):
    publicKey = non_null(Base64String)


class Sharing(Type):
    snowflake = non_null(SnowflakeSharing)


class Query(Type):
    getSourceList = Field(non_null(list_of(non_null(Source))), args=ArgDict({
        'input': non_null(GetSourceListInput)
    }))
    getSourceDescription = Field(non_null(SourceDescription), args=ArgDict({
        'id': non_null(str)
    }))
    getTableDescriptions = Field(non_null(TableDescriptions), args=ArgDict({
        'input': non_null(TableDescriptionsInput)
    }))
    getSourceStatus = Field(non_null(bool), args=ArgDict({
        'input': non_null(GetSourceStatusInput)
    }))
    getTenants = Field(non_null(list_of(non_null('Tenant'))))

    dataset = Field('Dataset', args=ArgDict({
        'id': non_null(str)
    }))
    datasetByName = Field('Dataset', args=ArgDict({
        'input': 'DatasetByNameInput'
    }))
    datasets = Field(non_null(list_of(non_null('Dataset'))), args=ArgDict({
        'input': 'DatasetsInput'
    }))
    destinations = Field(non_null(list_of(non_null(Destination))))
    user = Field(non_null('User'), args=ArgDict({
        'id': non_null(str)
    }))
    currentUser = Field(non_null('CurrentUser'))
    dataAccessKeys = Field(non_null(list_of(non_null('DataAccessKey'))), args=ArgDict({
        'input': 'DataAccessKeysInput'
    }))
    dataAccessKey = Field(non_null('DataAccessKey'), args=ArgDict({
        'id': non_null(str)
    }))
    listCustomSigningTemplates = Field(non_null(list_of(non_null('CustomSigningTemplate'))))

    sharing = Field(non_null('Sharing'))


class Mutation(Type):
    sourceConnectAzureBlob = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionAzureBlobInput)
    }))
    sourceConnectBigQuery = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionBigQueryInput)
    }))
    sourceConnectDatabricks = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionDatabricksInput)
    }))
    sourceConnectSnowflake = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionSnowflakeInput)
    }))
    sourceDisconnect = Field(non_null(bool), args=ArgDict({
        'input': non_null(SourceDisconnectInput)
    }))
    createDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null(CreateDatasetInput)
    }))
    createDestination = Field(non_null(Destination), args=ArgDict({
        'input': non_null(DestinationInput)
    }))
    removeDestination = Field(non_null(bool), args=ArgDict({
        'input': non_null(DestinationInput)
    }))
    createTableEdge = Field(non_null(bool), args=ArgDict({
        'input': non_null(TableEdgeInput)
    }))
    registerUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('RegisterUserInput')
    }))
    unregisterUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('UnregisterUserInput')
    }))
    updateUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('UpdateUserInput')
    }))
    updateTenant = Field(non_null('Tenant'), args=ArgDict({
        'input': non_null('UpdateTenantInput')
    }))
    pauseDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null('PauseDatasetInput')
    }))
    removeDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null('RemoveDatasetInput')
    }))
    updateDataset = Field(non_null(UpdateDatasetPayload), args=ArgDict({
        'input': non_null('UpdateDatasetInput')
    }))
    generateQueryAuth = Field(non_null(QueryAuth), args=ArgDict({
        'input': non_null('GenerateQueryAuthInput')
    }))
    generateDataAccessKey = Field(non_null(DataAccessKey), args=ArgDict({
        'input': non_null('GenerateDataAccessKeyInput')
    }))
    revokeDataAccessKey = Field(non_null(bool), args=ArgDict({
        'input': non_null('RevokeDataAccessKeyInput')
    }))
    syncDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null('SyncDatasetInput')
    }))
    createTenant = Field(non_null('Tenant'), args=ArgDict({
        'input': non_null('CreateTenantInput')
    }))
    deleteTenant = Field(non_null(bool), args=ArgDict({
        'input': non_null('DeleteTenantInput')
    }))
    createCustomSigningTemplate = Field(non_null('CustomSigningTemplate'), args=ArgDict({
        'input': non_null('CreateCustomSigningTemplateInput')
    }))
    deleteCustomSigningTemplate = Field(non_null(bool), args=ArgDict({
        'input': non_null('DeleteCustomSigningTemplateInput')
    }))
