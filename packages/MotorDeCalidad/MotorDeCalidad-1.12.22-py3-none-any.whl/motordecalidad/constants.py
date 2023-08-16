##Constants
from pyspark.sql.functions import col
from pyspark.sql.types import StructType,StructField,StringType, IntegerType
class Rules:
    class Pre_Requisites:
        name  = "Prerequisitos de Validación"
        property = "Integridad de Data"
        code = "100"
    class NullRule:
        name = "Completitud de Registro"
        property = "Completitud"
        code = "101"
    class DuplicatedRule:
        name = "Riesgo de Inconsistencia por Duplicidad"
        property = "Consistencia"
        code = "102"
    class IntegrityRule:
        name = "Integridad Referencial"
        property = "Consistencia"
        code = "103"
    class FormatDate:
        name = "Exactitud de Formato de Fecha"
        property = "Exactitud Sintactica"
        code = "104"
    class RangeRule:
        name = "Exactitud de Rango de Valores"
        property = "Exactitud"
        code = "105"
    class CatalogRule:
        name = "Exactitud de Catalogo de Valores"
        property = "Exactitud"
        code = "106"
    class ForbiddenRule:
        name = "Exactitud de Caracteres Permitidos"
        property = "Exactitud Sintactica"
        code = "107"
    class Type:
        name = "Consistencia de Formato (CSV)"
        property = "Consistencia"
        code = "108"
    class Composision:
        name = "Consistencia de Composición"
        property = "Consistencia"
        code = "109"
    class LengthRule:
        name = "Consistencia de Longitud de dato"
        property = "Consistencia"
        code = "110"
    class DataTypeRule:
        name = "Consistencia de Formato"
        property = "Consistencia"
        code = "111"
    class NumericFormatRule:
        name = "Consistencia de Formato Numerico"
        property = "Consistencia"
        code = "112" 
    class OperationRule:
        name = "Exactitud de Resultado"
        property = "Exactitud"
        code = "113"
    class StatisticsResult:
        name = "Exactitud Estadistica"
        property = "Exactitud"
        code = "114"
    class validateTimeInRange:
        name = "Exactitud de rango de fecha"
        property = "Exactitud"
        code = "115"
    class validateConditional:
        name = "Exactitud de Validacion Condicional"
        property = "Exactitud"
        code = "116"
    class validatePositionValue:
        name = "Exactitud de valor de Posición Específica"
        property = "Exactitud"
        code = "117"
    class validateEmail:
        name = "Validez de la estructura del Correo Electrónico"
        property = "Validez"
        code = "118"

class JsonParts:
    Input = "INPUT"
    Output = "OUTPUT"
    Rules = "RULES"
    Header= "HEADER"
    Delimiter = "DELIMITER"
    Fields = "FIELDS"
    ReferenceFields = "REFERENCE_FIELDS"
    Country = "COUNTRY_ID"
    Entity = "ENTITY_ID"
    Project = "PROJECT"
    Path = "PATH"
    Account = "ACCOUNT"
    Key = "KEY"
    FormatDate = "FORMAT_DATE"
    Domain = "DOMAIN"
    SubDomain = "SUB_DOMAIN"
    Segment = "SEGMENT"
    Area = "AREA"
    Threshold = "THRESHOLD"
    Values = "VALUES"
    MinRange = "MIN_RANGE"
    MaxRange = "MAX_RANGE"
    DataType = "DATA_TYPE"
    RepetitionNumber = "REPETITION_NUMBER"
    ReferenceDate = "REFERENCE_DATE"
    diffUnit = "DIFFERENT_UNIT"
    includeLimitRight = "INCLUDE_LIMIT_RIGHT"
    includeLimitLeft = "INCLUDE_LIMIT_LEFT"
    inclusive = "INCLUSIVE"
    condition = "CONDITION"
    filterList = "FILTER_LIST"
    qualityFunction = "QUALITY_FUNCTION"
    initialPosition = "INITIAL_POSITION"
    finalPosition = "FINAL_POSITION"
    expectedValue = "EXPECTED_VALUE"
    expressionForbidden = "EXPRESSION_FORBIDDEN"
    Type = "TYPE"
    Write = "WRITE"
    Error = "ERROR"
    Host = "HOST"
    Port = "PORT"
    DBName = "DATABASE_NAME"
    DBTable = "DATABASE_TABLE"
    DBUser = "DATABASE_USER"
    DBPassword = "DATABASE_PASSWORD"
    MaxInt = "MAX_INT"
    Sep = "SEP"
    NumDec = "NUM_DEC"
    TempPath = "TEMPORAL_PATH"
    Filter = "FILTER"
    Input_val = "INPUT_VAL"
    Error_val = "ERROR_VAL"
    Operator = "OPERATOR"
    Scope = "SCOPE"
    Partitions = "PARTITIONS"
    DataDate = "DATA_DATE"
    ValidData = "VALID_DATA"
    Data = "DATA"
    SendEmail = "SEND_EMAIL"
    Email ="EMAIL"

class Field:
    def __init__(self,colName):
        self.name = colName
        self.column = col(colName)
    def value(self,colValue):
        return (colValue).alias(self.name)
CountryId = Field("CODIGO_DE_PAIS")
DataDate = Field("FECHA_DE_INFORMACION")
Country = Field("PAIS")
Project = Field("PROYECTO")
Entity = Field("ENTIDAD")
AuditDate = Field("FECHA_EJECUCION_REGLA")
Domain  = Field("DOMINIO_ENTIDAD")
SubDomain = Field("SUBDOMINIO_ENTIDAD")
Segment = Field("SEGMENTO_ENTIDAD")
Area = Field("AREA_FUNCIONAL_ENTIDAD")
TestedFields = Field("ATRIBUTOS")
RuleCode = Field("CODIGO_REGLA")
RuleDescription = Field("DESCRIPCION_FUNCION")
SucessRate = Field("PORCENTAJE_CALIDAD_OK")
TestedRegisterAmount = Field("TOTAL_REGISTROS_VALIDADOS")
FailedRegistersAmount = Field("TOTAL_REGISTROS_ERRONEOS")
PassedRegistersAmount = Field("TOTAL_REGISTROS_CORRECTOS")
DataRequirement = Field("REQUISITO_DATOS")
QualityRequirement = Field("REQUISITO_CALIDAD")
RiskApetite = Field("APETITO_RIESGO")
Threshold = Field("UMBRAL_ACEPTACION")
RuleGroup = Field("CARACTERISTICA_REGLA")
RuleProperty = Field("PROPIEDAD_REGLA")
FailRate = Field("PORCENTAJE_CALIDAD_KO")
FunctionCode = Field("CODIGO_FUNCION")
LibraryVersion = Field("VERSION_LIBRERIA")

# Definición de la excepción personalizada
class ExcepciónDePreRequisitos(Exception):
    pass

PreRequisitesSucessMsg = "Validación de PreRequesitos Exitosa"
RequisitesSchema = StructType(
[StructField(TestedRegisterAmount.name,IntegerType()),
StructField(FunctionCode.name,StringType()),
StructField(RuleGroup.name,StringType()),
StructField(RuleProperty.name,StringType()),
StructField(RuleCode.name,StringType()),
StructField(Threshold.name,StringType()),
StructField(DataRequirement.name,StringType()),
StructField(TestedFields.name,StringType()),
StructField(SucessRate.name,StringType()),
StructField(FailedRegistersAmount.name,IntegerType())]
)
LeftAntiType = "leftanti"
Country = "country"
Year = "year"
Month = "month"
Day = "day"
Overwrite = "overwrite"
PartitionOverwriteMode = "partitionOverwriteMode"
DynamicMode = "dynamic"
Delimiter = "delimiter"
Header = "header"
DatabricksCsv = "com.databricks.spark.csv"
One = 1
Zero = 0
OneHundred = 100
OutputDataFrameColumns = [TestedRegisterAmount.name,FunctionCode.name,RuleGroup.name,RuleProperty.name,RuleCode.name,Threshold.name,DataRequirement.name,TestedFields.name,SucessRate.name,FailedRegistersAmount.name]
PermitedFormatDate = ['yyyy-MM-dd','yyyy/MM/dd', 'yyyyMMdd', 'yyyyMM']
