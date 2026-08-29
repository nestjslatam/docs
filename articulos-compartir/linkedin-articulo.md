# NestJS Latam: herramientas de Domain-Driven Design en español, abiertas y para todos

### Qué construimos, qué problema resuelve y cómo participar

---

Hay una línea que casi todos hemos escrito:

```
if (!dto.email.includes('@')) throw new BadRequestException('Email inválido');
```

Funciona. Y tiene tres costes que no se pagan el día que la escribes, sino meses después.

**El primero: la regla se queda donde nació.** Cuando ese mismo email llegue por una cola de mensajes, por la importación de un CSV o por un script de migración, la comprobación no estará. La regla no pertenece al controlador: pertenece al negocio, y debería viajar con el dato allá donde vaya.

**El segundo: se detiene en el primer error.** El usuario corrige el email, vuelve a enviar, y descubre que el teléfono también estaba mal. Tres viajes para tres problemas que ya conocíamos desde el primero.

**El tercero: para el compilador, un email es un texto cualquiera.** El nombre de un producto, un identificador y una contraseña son los tres `string`. Se pueden intercambiar sin que nada proteste, y el día que ocurre no hay ningún error: hay un dato en el sitio equivocado.

Domain-Driven Design lleva veinte años ofreciendo una respuesta a esto. Lo que faltaba, en nuestro entorno, era una implementación cómoda para NestJS **y documentación seria en español**.

Eso es lo que llevamos un año construyendo en **NestJS Latam**.

---

## Lo que hacen las librerías

### `ddd-lib` — los bloques de construcción

El paquete principal. Da cuatro cosas que si no tendrías que escribir a mano en cada proyecto: **value objects** que se validan solos, **agregados** que protegen las reglas que abarcan a más de un dato, **seguimiento de estado** y **eventos de dominio**, todo sobre `@nestjs/cqrs`.

Su decisión de diseño más característica es que **la validación recolecta en lugar de detenerse**:

```
product.isValid;                        // false
product.brokenRules.getBrokenRules();   // las tres, con el campo de cada una
```

Eso cambia lo que puedes devolverle a quien llama. En lugar de un error genérico, una respuesta que un formulario sabe usar: dos campos marcados a la vez, cada uno con su motivo, en un solo viaje.

Y trae consigo una distinción que ordena toda la API:

**400** es un tipo equivocado y lo rechaza el transporte antes de llegar al dominio. **422** es un valor equivocado — `0` es un número perfectamente válido; que no pueda ser un precio es conocimiento de negocio, y sólo el agregado puede juzgarlo. **409** es un estado que no permite la operación: nada está mal formado, simplemente no se puede confirmar un pedido vacío.

Esa separación, sostenida en el tiempo, es la diferencia entre una API que se puede consumir y una que hay que adivinar.

### `ddd-valueobjects` — doce ya escritos

Email, dinero, teléfono, URL, porcentajes, rangos de fechas, coordenadas, y documentos de identidad latinoamericanos como DNI y RUC. Cada uno con sus reglas, sus formateadores y su comparación por valor.

El que mejor ilustra la idea es el dinero:

```
precio.add(envio);   // lanza si uno está en soles y el otro en dólares
```

Sumar monedas distintas deja de ser un error silencioso que aparece en una conciliación tres semanas después, y pasa a ser algo que **no se puede escribir**.

La validación de documentos es enchufable: registras una estrategia para tu país y sustituye a la que viene. Escribir una para un formato con el que convives a diario es, probablemente, la contribución más fácil y más útil de todo el proyecto.

### `ddd-es-lib` — event sourcing sobre MongoDB

Para cuando no quieres guardar el estado actual sino **todo lo que pasó**, y derivar el estado de ahí. Trae event store con control de concurrencia, snapshots, upcasting para cuando el esquema de tus eventos evolucione, proyecciones y sagas.

Es el paquete menos maduro de los cuatro y lo decimos en su portada, no en la letra pequeña.

### `ddd-cli` — la pieza que nos parece distinta

La mayoría de los generadores llevan una plantilla fija y confían en que siga cuadrando con la librería. Éste **lee los tipos de la versión que tú tienes instalada**, con la API del compilador de TypeScript. Le preguntas por una clase y te describe *tu* versión — incluida una que nunca ha visto, o una que hayas escrito tú en tu propio fork.

Eso le permite hacer algo que una plantilla no puede: **auditar**.

```
npx ddd validate
```

Comprueba cuatro errores que tienen una propiedad en común — **compilan, pasan los tests y no producen ningún síntoma**:

- Una fábrica que no comprueba la validez y devuelve objetos inválidos en silencio
- Un método sobrescrito que no encadena con el de la clase base, y hace desaparecer sus validadores
- Leer un campo propio en un método que el constructor base llama *antes* que el tuyo
- Un manejador de comandos sin la llamada que despacha los eventos: el comando triunfa y todos los suscriptores se saltan

Devuelve `0` o `1`. Se pone en un pipeline tal cual.

Y corre como **servidor MCP**, así que Claude Code, Codex o Cursor lo usan directamente **sin necesitar una clave de API**: el modelo lo pone tu agente. El reparto de trabajo es lo interesante — el agente decide la frontera del agregado y las invariantes, que es criterio; la herramienta lee las declaraciones con exactitud y audita contra el idioma, que es justo lo que un modelo hace mal.

---

## Qué es NestJS Latam

Una comunidad hispanohablante que construye y documenta en abierto. Todo lo que hacemos está en npm, con licencia MIT y el código a la vista.

**Qué vas a encontrar:**

**Documentación completa en español**, en [docs.nestjslatam.dev](https://docs.nestjslatam.dev) — de tu primer value object a la referencia de API, con los errores típicos y su síntoma explicados donde te los vas a encontrar.

**Guías y tutoriales paso a paso**: montar tu primer agregado, probarlo bien, modelar dinero sin equivocarte, migrar entre versiones mayores, conectar el CLI a tu agente de IA.

**Artículos de fondo** sobre lo que aprendimos construyendo esto, incluidos los errores. Uno cuenta cómo una cobertura del 98,6 % convivía con un 58,4 % real y los cinco mecanismos que lo escondían. Otro, cómo una comprobación de seguridad estuvo dos versiones sin ejecutarse porque un método pasó a ser una propiedad.

**Un ejemplo completo y funcionando**: una aplicación de pedidos y productos que consume la librería, con su superficie HTTP real y sus pruebas.

**Y una norma que nos importa más que el código:** que las afirmaciones sean ciertas. Si un README dice que algo funciona, es porque alguien lo ejecutó. Si algo está roto, está escrito antes de que lo descubras tú. Cada repositorio publica sus cifras medidas, no prometidas.

Por eso también decimos lo incómodo: **la API todavía se mueve y ha roto entre versiones mayores**. Clava una versión exacta. Preferimos perder una instalación a que alguien se lleve una sorpresa en producción.

---

## Cómo participar

No hace falta pedir permiso, ni ser experto, ni escribir código.

**Pregunta.** Si algo no se entiende, casi siempre es culpa de cómo está explicado. Cada pregunta mejora la documentación para quien venga detrás.

**Corrige una página.** Cada página de la documentación tiene un enlace «Editar en GitHub» al final. Una errata arreglada es una contribución.

**Reporta lo que se rompe.** Un informe que documenta con precisión un fallo vale tanto como el arreglo. Con la versión exacta y cómo reproducirlo, ya está medio resuelto.

**Escribe.** ¿Resolviste algo que te costó una tarde? Eso es un artículo. Lo publicamos con tu firma y tu enlace.

**Manda un pull request.** Cada repositorio tiene una sección *Contributing* con tareas concretas: no un «se aceptan contribuciones», sino qué falta exactamente y cómo comprobar que lo arreglaste. Algunas se verifican en cinco minutos.

**Cuéntalo.** Si algo de esto te sirvió, decirlo ayuda a que otros lo encuentren. Es la contribución más barata y de las más útiles.

---

## Empezar

```
npm install @nestjslatam/ddd-lib @nestjs/cqrs
```

La guía completa está en **[docs.nestjslatam.dev](https://docs.nestjslatam.dev)**. La comunidad, en **[nestjslatam.dev](https://nestjslatam.dev)**. Todo el código, en **[github.com/nestjslatam](https://github.com/nestjslatam)**.

Si trabajas con NestJS y llevas tiempo con la sensación de que las reglas de tu negocio están repartidas por los controladores, esto se escribió para ese problema.

Y si te animas a mejorarlo, mejor todavía. Se construyó así.

---

**Impulsado por [BeyondNetCode](https://beyondnet.info/)** con la comunidad NestJS Latam.

*Proyecto de comunidad no oficial, sin afiliación con NestJS ni con sus autores. NestJS fue creado por Kamil Myśliwiec y se publica bajo licencia MIT.*
