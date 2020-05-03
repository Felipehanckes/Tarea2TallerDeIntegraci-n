# API Restuful hamburguesas

## Busca hamburguesas:

Se realiza un GET a URLHEROKU/hamburguesa
> No recibe parámetros.

## Crear una hamburguesa nueva:

Se realiza un POST a URLHEROKU/hamburguesa

>_En Postman_\
Protocolo: POST\
body: From data


Para añadir multiples ingreidentes, se debe realizar entregando un string, separando los id de los ingredientes por una ",".

>key: Ingredientes\
values: 1,3,8
## Encontrar hamburguesa por ID

Se realiza un GET a URLHEROKU/hamburguesa/:int

> No recibe parámetros.

## Elimina una hamburguesa por ID
Se realiza un DELETE a URLHEROKU/hamburguesa/:int

> No recibe parámetros.

## Edita una hamburguesa por ID
Se realiza un PATCH a URLHEROKU/hamburguesa/:int

>_En Postman_\
Protocolo: PATCH\
body: From data

## Busca ingrediente
Se realiza un GET a URLHEROKU/ingrediente

> No recibe parámetros.

## Crea un nuevo ingrediente

Se realiza un POST a URLHEROKU/ingrediente

>_En Postman_\
Protocolo: POST\
body: From data

## Encontrar un ingrediente por ID

Se realiza un GET a URLHEROKU/ingrediente/:int

> No recibe parámetros.

## Elimina un ingrediente por ID

Se realiza un DELETE a URLHEROKU/ingrediente/:int

>No recibe parámetros

## Agrega un ingrediente a una hamburguesa

Se realiza un PATCH a URLHEROKU/hamburguesa/:int/ingrediente/:int

>No recibe parámetros

## Retira un ingrediente de una hamburguesa

Se realiza un PATCH a URLHEROKU/hamburguesa/:int/ingrediente/:int

>No recibe parámetros


# Modelos

## Hamburguesa
|Key        |Value       |
|-----------|------------|
|nombre     | varchar: 30|
|precio     | Int:       |
|descripcion| text:      |
|image      | url:       |
|ingredients| str:       |

## Ingrediente
|Key        |Value       |
|-----------|------------|
|nombre     | varchar: 30|
|descripcion| text:      |

## Relación Ingrediente-Hamburguesa

|Key          |Value       |
|-----------  |------------|
|burguer_id   | int:       |
|ingredient_id| int:       |