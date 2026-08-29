# Para LinkedIn

Tres versiones del mismo mensaje. LinkedIn corta a las ~140 primeras palabras
con un «ver más», así que **el gancho tiene que caber ahí** o el resto no se
lee. Publica una, mide, y si funciona reutiliza el patrón.

Un apunte que cambia el alcance más que el texto: **el enlace en el primer
comentario, no en el cuerpo**. LinkedIn penaliza los posts que sacan gente
fuera. Escribe el post limpio y pon el enlace debajo tú mismo.

---

## Versión 1 — la cifra

> Nuestra librería reportaba 98,6 % de cobertura de tests.
>
> La cifra real era 58,4 %. Y en un módulo, 8,5 %.
>
> Ninguna de las dos era mentira: ambas salían de Jest, correctamente calculadas. La diferencia estaba en *qué le pedimos medir*.
>
> Cinco mecanismos lo tapaban a la vez, y ninguno era un bug — todos eran configuración razonable:
>
> · Un patrón que excluía justo los ficheros sin probar
> · Globs con `../` que no casan con nada, y Jest no avisa cuando un patrón no casa
> · Umbrales por directorio que sacan esos ficheros del cómputo global: añadir vigilancia *subía* el número
> · Una puerta en CI donde, si no encontraba el informe, dejaba pasar
> · Una constante que cambió de significado dos veces sin cambiar de nombre
>
> Escribir los tests que faltaban destapó 34 defectos. Ocho graves.
>
> El peor: un objeto que fallaba una validación no podía volver a ser válido nunca. Corregías el error, reenviabas, y recibías la misma respuesta. Faltaba una línea.
>
> El número que te tranquiliza suele ser el que no está midiendo lo que crees.
>
> Escribí la historia completa, con los cinco mecanismos y cómo ver la verdad en dos comandos. 👇

**Primer comentario:** `https://github.com/nestjslatam/ddd` · `https://nestjslatam.dev`

---

## Versión 2 — el problema cotidiano

> `if (!dto.email.includes('@'))`
>
> Todos hemos escrito esa línea en un controlador. Funciona. Y tiene tres costes que se pagan tarde:
>
> **La regla vive donde se usó por primera vez.** Cuando ese email llegue por una cola, por un CSV o por un script de migración, la comprobación no estará. La regla no es del controlador: es del negocio.
>
> **Se detiene en el primer error.** El usuario corrige el email, reenvía, y descubre que el teléfono también estaba mal. Tres viajes para tres errores que ya conocías desde el primero.
>
> **Un string no es un email.** Para el compilador, el nombre de un producto, un identificador y una contraseña son la misma cosa. Y se pueden intercambiar.
>
> Llevamos un año construyendo librerías de Domain-Driven Design para NestJS, en español y abiertas, para resolver exactamente esto: que las reglas vivan en el tipo, y que la validación recolecte en lugar de detenerse.
>
> Cuatro paquetes en npm, licencia MIT, 1111 tests, y los números medidos en lugar de prometidos.
>
> Incluido lo que no funciona: está escrito en cada README antes de que lo descubras tú. 👇

**Primer comentario:** `https://nestjslatam.dev` · `https://github.com/nestjslatam`

---

## Versión 3 — la herramienta

> Escribimos un CLI que hace algo que no habíamos visto en otros generadores.
>
> No lleva plantillas fijas. **Parsea los .d.ts de la versión que tú tienes instalada**, con la API del compilador de TypeScript. Le preguntas por una clase y te describe *tu* versión — incluida una que nunca ha visto, o una que hayas escrito tú en tu fork.
>
> Y audita cuatro errores que compilan, pasan los tests y no producen ningún síntoma:
>
> · Una fábrica que no comprueba la validez y devuelve objetos inválidos en silencio
> · Un override que no encadena con `super` y hace desaparecer los validadores de la base
> · Leer un campo propio en un método que el constructor base llama *antes* que el tuyo
> · Un handler sin `commit()`: el comando triunfa y todos los manejadores de eventos se saltan
>
> Exit code 0 o 1. Se pone en CI tal cual.
>
> Y corre como servidor MCP, así que Claude Code o Cursor lo usan directamente **sin clave de API**: el modelo lo pone tu agente. Él decide la frontera del agregado, que es criterio; la herramienta lee las declaraciones con exactitud, que es lo que un modelo hace mal.
>
> Abierto, MIT, en español. 👇

**Primer comentario:** `https://github.com/nestjslatam/ddd-cli` · `https://docs.nestjslatam.dev`

---

## Etiquetas

Cinco como mucho; más reparte el alcance en lugar de sumarlo.

`#NestJS` `#TypeScript` `#DomainDrivenDesign` `#OpenSource` `#DesarrolloDeSoftware`

Y menciona a **@NestJS Latam** si la página existe en LinkedIn: las menciones a páginas
aparecen en el feed de sus seguidores, que es alcance que no pagas.

## Cuándo publicar

Martes a jueves, entre las 8 y las 10 de la mañana en tu zona. Y responde a
**todos** los comentarios en la primera hora: la conversación temprana es lo
que decide si LinkedIn lo sigue mostrando.
