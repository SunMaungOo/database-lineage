from decouple import config

OUTPUT_FILE_PATH = config("OUTPUT_FILE_PATH",cast=str)

HOST_NAME = config("HOST_NAME",cast=str)

DATABASE_NAME = config("DATABASE_NAME",cast=str)

PORT = config("PORT",cast=int,default=1433)

USER_NAME = config("USER_NAME",cast=str)

PASSWORD = config("PASSWORD",cast=str)

IS_USE_FQN  = config("IS_USE_FQN",default=True,cast=bool)

GET_VIEW_LINEAGE = """

SELECT schemas.name AS view_schema,
views.name AS view_name,
dependencies.referenced_schema_name  AS used_schema_name,
dependencies.referenced_entity_name AS used_table_name
FROM sys.sql_expression_dependencies AS dependencies
INNER JOIN sys.views AS views
ON dependencies.referencing_id = views.object_id
INNER JOIN sys.schemas AS schemas
ON views.schema_id = schemas.schema_id

"""


GET_PROCEDURE_LINEAGE = """

SELECT routines.routine_schema,
routines.routine_name,
sql_modules.definition AS routines_definition
FROM
(
	SELECT routine_schema,
	routine_name,
	OBJECT_ID(CONCAT(routine_schema,'.',routine_name)) AS object_id
	FROM INFORMATION_SCHEMA.ROUTINES
	WHERE routine_type = 'PROCEDURE'
) AS routines
INNER JOIN sys.sql_modules
ON routines.object_id = sql_modules.object_id
ORDER BY routines.routine_schema,
routines.routine_name;

"""