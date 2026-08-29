# Post para anunciar el artículo

Tres versiones. LinkedIn corta a las ~140 primeras palabras con un «ver más»,
así que **el gancho tiene que caber ahí** o el resto no se lee.

**El enlace va en el primer comentario, no en el cuerpo.** La plataforma
penaliza los posts que sacan gente fuera; publicas limpio y pones el enlace tú
mismo debajo, en cuanto se publique.

---

## Versión A — el problema (recomendada)

> `if (!dto.email.includes('@'))`
>
> Todos hemos escrito esa línea en un controlador. Funciona. Y tiene tres costes que no se pagan el día que la escribes, sino meses después.
>
> **La regla se queda donde nació.** Cuando ese email llegue por una cola, por un CSV o por un script de migración, la comprobación no estará. La regla no es del controlador: es del negocio.
>
> **Se detiene en el primer error.** El usuario corrige el email, reenvía, y descubre que el teléfono también estaba mal. Tres viajes para tres problemas que ya conocías desde el primero.
>
> **Para el compilador, un email es un texto cualquiera.** El nombre de un producto, un identificador y una contraseña son los tres `string`. Se pueden intercambiar sin que nada proteste.
>
> Llevamos un año construyendo librerías de Domain-Driven Design para NestJS, en español y abiertas, para resolver exactamente esto.
>
> Acabo de escribir qué hace cada una, qué problema resuelve, y cómo participar en la comunidad. Incluido lo que todavía no funciona bien, que también está escrito.
>
> Enlace en el primer comentario 👇
>
> \#NestJS \#TypeScript \#DomainDrivenDesign \#OpenSource \#DesarrolloDeSoftware

---

## Versión B — la herramienta

> Escribimos un CLI que hace algo que no habíamos visto en otros generadores.
>
> No lleva plantillas fijas. **Lee los tipos de la versión que tú tienes instalada**, con la API del compilador de TypeScript. Le preguntas por una clase y te describe *tu* versión — incluida una que nunca ha visto, o una que hayas escrito tú en tu fork.
>
> Eso le permite hacer algo que una plantilla no puede: auditar. Comprueba cuatro errores que tienen una propiedad incómoda en común — **compilan, pasan los tests y no producen ningún síntoma**.
>
> Y corre como servidor MCP, así que Claude Code o Cursor lo usan **sin clave de API**: el modelo lo pone tu agente. Él decide la frontera del agregado, que es criterio; la herramienta lee las declaraciones con exactitud, que es lo que un modelo hace mal.
>
> Escribí un artículo sobre las cuatro librerías que mantenemos, qué resuelve cada una y cómo colaborar. Todo abierto, MIT, en español.
>
> Enlace en el primer comentario 👇
>
> \#NestJS \#TypeScript \#DomainDrivenDesign \#OpenSource \#IA

---

## Versión C — la comunidad

> Hace un año no había documentación seria de Domain-Driven Design para NestJS en español.
>
> Hoy hay cuatro librerías en npm, una herramienta que audita tu dominio, guías paso a paso y una comunidad que lo mantiene. Todo con licencia MIT y el código a la vista.
>
> Lo que más me importa no es el código: es una norma que nos pusimos y sostenemos.
>
> **Que las afirmaciones sean ciertas.** Si un README dice que algo funciona, es porque alguien lo ejecutó. Si algo está roto, está escrito antes de que lo descubras tú. Cada repositorio publica sus cifras medidas, no prometidas.
>
> Por eso también decimos lo incómodo: la API todavía se mueve, y hay un paquete que es claramente el menos maduro. Está en su portada, no en la letra pequeña.
>
> Preferimos perder una instalación a que alguien se lleve una sorpresa en producción.
>
> Escribí qué hace cada librería, qué resuelve y cómo participar — no hace falta ser experto ni escribir código.
>
> Enlace en el primer comentario 👇
>
> \#NestJS \#OpenSource \#DomainDrivenDesign \#Comunidad \#TypeScript

---

## El primer comentario

Publícalo tú en cuanto salga el post:

> Artículo completo aquí 👉 [enlace del artículo de LinkedIn]
>
> Y todo el código, en github.com/nestjslatam · nestjslatam.dev

---

## Notas

**Cinco etiquetas como máximo.** Más reparte el alcance en lugar de sumarlo.
Las que rinden son las de nicho: `#DomainDrivenDesign` llega a menos gente que
`#Programación`, pero a la que le interesa.

**Menciona a la página de NestJS Latam** si existe en LinkedIn. Las menciones a
páginas aparecen en el feed de sus seguidores: es alcance que no pagas.

**Publica martes a jueves, entre las 8 y las 10 de la mañana.** Y responde a
todos los comentarios de la primera hora — la conversación temprana es lo que
decide cuánto lo sigue mostrando la plataforma.

**Sube la portada al post también.** El post con imagen rinde bastante más que
el de sólo texto, y ya la tienes generada en `portadas/`.
