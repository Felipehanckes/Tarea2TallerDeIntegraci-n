# API Restuful hamburguesas

## Obtener un listado de todas las hamburguesas:

Se realiza un GET a URLHEROKU/hamburguesas/
> No recibe parametros.

## Crear una hamburguesa nueva:

Se realiza un POST a URLHEROKU/hamburguesas/

 Recibe un From Data
|Key        |Value       |
|-----------|------------|
|name       | varchar: 30|
|price      | Int:       |
|description| text:      |
|image      | url:       |
|ingredients| int:       |