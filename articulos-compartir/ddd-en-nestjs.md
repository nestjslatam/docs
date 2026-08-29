# Encontramos 34 errores en una librería con 98,6 % de cobertura

Y el más grave hacía que un objeto que fallaba una validación no pudiera volver a ser válido nunca.

Esta es la historia corta de por qué construimos **[`@nestjslatam/ddd-lib`](https://github.com/nestjslatam/ddd)**, qué problema resuelve y qué aprendimos midiéndolo de verdad. Si trabajas con NestJS y alguna vez has escrito `if (!user.email.includes('@'))` en un controlador, esto va de eso.

---

## El problema, en tres líneas

```ts
async createProduct(dto: CreateProductDto) {
  if (!dto.name || dto.name.length < 3) throw new BadRequestException('Nombre inválido');
  if (dto.price <= 0) throw new BadRequestException('Precio inválido');
  // ...y catorce comprobaciones más, repartidas por seis ficheros
}
```

Todos hemos escrito esto. Funciona. Y tiene tres costes que se pagan tarde:

**La regla vive donde se usó por primera vez.** Cuando el precio llegue por una cola, por un CSV o por un script de migración, esa comprobación no estará. La regla no es del controlador; es del negocio.

**Se detiene en el primer error.** El usuario corrige el precio, reenvía, y descubre que el nombre también estaba mal. Tres viajes para tres errores que ya conocías desde el primero.

**Un `string` no es un email.** El compilador no distingue entre el nombre de un producto, un identificador y una contraseña: los tres son `string`, y los tres se pueden pasar donde va cualquiera de los otros.

## Lo que proponemos

Que las reglas vivan en el tipo, y que la validación **recolecte en lugar de detenerse**.

```ts
const product = new Product({ name, description, price });

product.isValid;                        // false
product.brokenRules.getBrokenRules();   // las TRES, con el campo de cada una
```

Eso permite una respuesta que el formulario puede usar de verdad:

```json
{
  "statusCode": 422,
  "brokenRules": [
    { "property": "props.price", "message": "Price must be greater than 0" },
    { "property": "props.description", "message": "Description must be longer than the name" }
  ]
}
```

Dos campos marcados a la vez, en lugar de un aviso genérico y un usuario adivinando.

Y trae consigo una distinción que ordena toda la API:

| | Significa | Lo juzga |
|---|---|---|
| **400** | Un tipo equivocado | El transporte, antes de llegar al dominio |
| **422** | Un valor equivocado | El agregado — `0` es un número válido; que no pueda ser un precio es negocio |
| **409** | Un estado que no lo permite | El agregado — confirmar un pedido vacío |

## Las cuatro piezas

| | |
|---|---|
| **[`ddd-lib`](https://github.com/nestjslatam/ddd)** | Los bloques: agregados, value objects, validadores, seguimiento de estado y eventos de dominio, sobre `@nestjs/cqrs` |
| **[`ddd-cli`](https://github.com/nestjslatam/ddd-cli)** | Entiende y audita tu dominio. Lee los `.d.ts` de **tu** versión instalada |
| **[`ddd-valueobjects`](https://github.com/nestjslatam/ddd-valueobjects)** | Doce ya hechos: email, dinero, teléfono, DNI, RUC, rangos de fechas |
| **[`ddd-es-lib`](https://github.com/nestjslatam/ddd-event-sourcing)** | Event sourcing sobre MongoDB: event store, snapshots, upcasting, sagas |

Sólo el primero es obligatorio.

## El CLI hace algo que no habíamos visto

La mayoría de los generadores llevan una plantilla fija y confían en que siga cuadrando con la librería. Éste **parsea los `.d.ts` instalados en tu proyecto** con la API del compilador de TypeScript. Le preguntas por `DddAggregateRoot` y te describe *tu* versión — incluida una que nunca ha visto.

```bash
npx ddd validate
```

Aplica cuatro reglas. Cada una es un error que **compila, pasa los tests y no produce ningún síntoma**:

1. **Una fábrica que no comprueba `isValid`.** La validación recolecta y no lanza, así que devuelve objetos inválidos en silencio.
2. **Un `addValidators` que no llama a `super`.** Los validadores de la clase base desaparecen. Sin error.
3. **Leer un campo propio dentro de `addValidators`.** El constructor base lo llama *antes* que el tuyo. Revienta en cada construcción — así publicamos rota una clase durante dos versiones.
4. **Un handler sin `commit()`.** El comando triunfa y todos tus `@EventsHandler` se saltan. Sin aviso.

Exit code `0` o `1`. Se pone en CI tal cual.

Y corre como **servidor MCP**, así que Claude Code o Cursor lo usan directamente, **sin clave de API** — el modelo lo pone tu agente:

```bash
claude mcp add ddd -- npx -y @nestjslatam/ddd-cli mcp
```

El reparto es lo interesante: el agente decide la frontera del agregado y las invariantes, que es criterio. El CLI lee las declaraciones con exactitud y audita contra el idioma, que es lo que un modelo hace mal.

---

## Lo que aprendimos midiéndolo

La librería reportaba **98,6 % de cobertura**. La cifra real era **58,4 %**, y en un módulo, **8,5 %**.

Ninguna de las dos era mentira: ambas salían de Jest, correctamente calculadas. La diferencia estaba en *qué se le pidió medir*. Cinco mecanismos lo tapaban a la vez, y ninguno era un bug — todos eran configuración razonable:

- Un patrón `collectCoverageFrom` que **excluía** los ficheros sin probar
- Globs con `../` que **no casan con nada**, y Jest no avisa cuando un patrón no casa
- Umbrales por directorio que **sacan esos ficheros del cómputo global** — añadir vigilancia *subía* el número
- Una puerta en CI donde `[ "" -lt "80" ]` devuelve **falso**: si no encuentra el informe, deja pasar
- Una constante que cambió de significado dos veces sin cambiar de nombre

Escribir las pruebas que faltaban destapó **34 defectos**, ocho graves. El peor: `validate()` sólo añadía reglas rotas y nunca las limpiaba, así que un agregado que fallaba una vez arrastraba el error para siempre. Corregías el precio, reenviabas, y recibías la misma respuesta.

**El número que te tranquiliza suele ser el que no está midiendo lo que crees.**

Hoy: 98,76 % medido, 1111 pruebas, y el ejemplo del README es un fichero `.spec.ts` que corre en CI — si deja de compilar, el build se pone rojo antes de que nadie lo copie.

## Lo que no te vamos a vender

**La API todavía se mueve.** Ha roto entre versiones mayores y el compilador no detecta la mayoría de los cambios. **Clava una versión exacta.** Cada repositorio dice en su README qué está probado y qué no, con cifras que salen de ejecutar y no de prometer.

`ddd-es-lib` es el menos maduro: sus pruebas cubren las piezas, no el cableado entre ellas, que es justo donde estaban sus defectos. Está escrito en su README, en mayúsculas, antes de que lo descubras tú.

Preferimos que lo sepas antes.

---

## La comunidad

**[nestjslatam.dev](https://nestjslatam.dev)** — artículos, guías y tutoriales en español.
**[docs.nestjslatam.dev](https://docs.nestjslatam.dev)** — la documentación completa.
**[github.com/nestjslatam](https://github.com/nestjslatam)** — todo abierto, licencia MIT.

No hace falta pedir permiso para participar. Cada repositorio tiene una sección *Contributing* con tareas concretas: no «se aceptan contribuciones», sino qué falta exactamente y cómo comprobar que lo arreglaste. Algunas se verifican en cinco minutos.

Y hay algo que valoramos por encima del código: **que las afirmaciones sean ciertas**. Si un README dice que algo funciona, es porque alguien lo ejecutó. Un reporte que documenta con precisión algo roto vale tanto como el arreglo.

---

*Construido por [BeyondNetCode](https://beyondnet.info/) con la comunidad NestJS Latam.*
*Proyecto de comunidad no oficial, sin afiliación con NestJS ni sus autores.*
