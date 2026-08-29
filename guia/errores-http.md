# Mapear errores a HTTP

Sin un filtro, un precio rechazado le llega al cliente como `500 Internal Server Error` sin cuerpo: exactamente la misma respuesta que si al proceso se le hubiera acabado la memoria. Un filtro de excepciones arregla eso en un solo sitio.

## El filtro

```ts
@Catch(DomainException, BrokenRulesException)
export class DomainExceptionFilter implements ExceptionFilter {
  catch(exception: DomainException | BrokenRulesException, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse();

    if (exception instanceof BrokenRulesException) {
      return response.status(HttpStatus.UNPROCESSABLE_ENTITY).json({
        statusCode: 422,
        error: 'Unprocessable Entity',
        message: `${exception.subject} is invalid`,
        brokenRules: exception.brokenRules.map((rule) => ({
          property: rule.property,
          message: rule.message,
          severity: rule.severity,
        })),
      });
    }

    const { status, error } = MAP[exception.constructor.name] ?? {
      status: HttpStatus.INTERNAL_SERVER_ERROR,
      error: 'Internal Server Error',
    };

    return response.status(status).json({ statusCode: status, error, message: exception.message });
  }
}
```

```ts
// main.ts
app.useGlobalFilters(new DomainExceptionFilter());
```

## La tabla

| Excepción | Código | Por qué |
|---|---|---|
| `BrokenRulesException` | **422** | El cuerpo está bien formado y el dominio lo rechazó |
| `ArgumentNullException` | **400** | Falta un valor obligatorio |
| `InvalidFormatException` | **400** | La forma del dato no es la esperada |
| `InvalidStateTransitionException` | **409** | El agregado no está en un estado que lo permita |
| `InvalidOperationException` | **409** | La operación no procede ahora mismo |
| Cualquier otra | **500** | Un fallo de verdad, y debe seguir siendo un 500 |

Esa última fila es importante: **el filtro no debe tragarse lo que no entiende.** Un `TypeError` convertido en 400 es un bug de producción que nadie va a encontrar.

## Por qué 422 y no 400

Es la distinción que organiza toda la librería:

```bash
# estructura — el pipe lo rechaza antes de que el dominio lo vea
-d '{"name":"X","description":"Suficientemente larga","price":"cuarenta"}'   → 400

# significado — el cuerpo es correcto y el agregado lo rechaza
-d '{"name":"X","description":"Suficientemente larga","price":0}'            → 422
```

`0` es un número perfectamente válido. Ningún validador de transporte puede saber que un precio no puede serlo — eso es conocimiento de negocio, y vive en el agregado.

## La respuesta que esto habilita

```json
{
  "statusCode": 422,
  "error": "Unprocessable Entity",
  "message": "Product is invalid",
  "brokenRules": [
    { "property": "props.price", "message": "Price must be greater than 0", "severity": "Error" },
    { "property": "props.description", "message": "Description must be longer than the name", "severity": "Error" }
  ]
}
```

`property` es lo que permite a un formulario resaltar los dos campos correctos a la vez, en vez de mostrar un aviso genérico y hacer que el usuario adivine.

Y ése es todo el sentido de que la validación recolecte en lugar de lanzar. Si aplanas las reglas a una cadena en el handler —`throw new Error(rules.join(', '))`— tiras esa estructura, y ya no hay forma de recuperarla cuando llega al transporte.

## Siguiente

- [Referencia de API](/guia/api)
