# Qué es esto

`@nestjslatam/ddd-lib` es una librería de bloques de construcción para escribir dominios ricos en NestJS. No es un framework: no te obliga a una estructura de carpetas, no genera código en tiempo de ejecución y no toca tu base de datos.

Te da cuatro cosas:

| | |
|---|---|
| **Value objects** | Tipos que se validan a sí mismos y se comparan por valor, no por referencia |
| **Agregados** | Raíces de consistencia que **acumulan sus propias reglas rotas** en vez de lanzar en la primera |
| **Validadores** | Una clase por regla de negocio, testeable por separado |
| **Eventos de dominio** | Recolectados por el agregado, despachados por el handler sobre `@nestjs/cqrs` |

## La idea que hay que entender primero

La mayoría de las librerías de validación lanzan una excepción en cuanto encuentran el primer problema. Ésta **no**.

```ts
const product = new Product({ name, description, price });

product.isValid;                        // false
product.brokenRules.getBrokenRules();   // [ {...}, {...}, {...} ]  ← las TRES
```

Eso cambia lo que puedes devolverle a quien llama. En vez de «el precio es inválido», y que arregle eso, lo reenvíe y descubra que el nombre también lo era, le devuelves las tres de golpe:

```json
{
  "statusCode": 422,
  "error": "Unprocessable Entity",
  "message": "Product is invalid",
  "brokenRules": [
    { "property": "props.price", "message": "Price must be greater than 0", "severity": "Error" },
    { "property": "props.name", "message": "Name must be at least 3 characters", "severity": "Error" }
  ]
}
```

La contrapartida es que **tú tienes que preguntar**. Como la validación no lanza, una fábrica que no comprueba `isValid` devuelve tan tranquila un objeto que incumple sus propias invariantes. Es el error número uno, y tiene su propia sección en [Reglas rotas](/guia/reglas-rotas).

## Estructura vs. significado

Es la distinción que organiza toda la librería, y merece la pena tenerla clara desde el principio:

| | Quién lo juzga | Respuesta |
|---|---|---|
| `price: "cuarenta"` | El `ValidationPipe` de NestJS, antes de llegar al dominio | **400** |
| `price: 0` | El agregado — es un número perfectamente válido | **422** |
| Confirmar un pedido vacío | El agregado — nada está mal formado, el estado no lo permite | **409** |

Un **tipo** equivocado es estructura. Un **valor** equivocado es significado, y sólo el agregado puede juzgarlo.

## Requisitos

- Node `>=20.11`
- NestJS 11
- `@nestjs/cqrs` como dependencia par

## Siguiente

- [Instalación](/guia/instalacion)
- [Tu primer agregado](/guia/primer-agregado) — de cero a un `Product` que valida
