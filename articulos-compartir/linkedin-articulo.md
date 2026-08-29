# El número que nos tranquilizaba era el que no estaba mirando

### Lo que aprendí midiendo de verdad la cobertura de una librería que llevaba un año en producción

---

Durante meses miré el mismo número y me quedé tranquilo: **98,6 % de cobertura de tests**.

Es el tipo de cifra que cierra conversaciones. Aparece en el README, en el pipeline, en la diapositiva cuando alguien pregunta por la calidad del código. Nadie discute un 98,6 %.

La cifra real era **58,4 %**. Y en uno de los módulos, **8,5 %**.

Lo que más me costó asimilar no fue el error. Fue que **ninguna de las dos cifras era mentira**. Las dos salían de la misma herramienta, correctamente calculadas. La diferencia estaba en algo que yo nunca había pensado en revisar: *qué le habíamos pedido medir*.

Esta es la historia de cómo lo encontramos, los cinco mecanismos que lo escondían —ninguno de ellos un fallo, todos configuración perfectamente razonable— y por qué creo que le está pasando a más equipos de los que imaginamos.

---

## Cómo se esconde un 40 %

### 1. El patrón que excluía justo lo que faltaba probar

```json
"collectCoverageFrom": ["src/**/*.ts", "!src/**/*.spec.ts"]
```

Inofensivo. Hasta que alguien añade un directorio **fuera** de `src/`.

Esos ficheros no aparecían en el informe. Y aquí está el detalle que lo cambia todo: **no aparecían como 0 %. No aparecían.**

Un fichero sin cubrir baja la media. Un fichero ausente, no. El promedio se calcula sobre lo que decidiste mirar, y esos ficheros no estaban en la lista.

### 2. Un patrón que no casaba con nada, en silencio

El intento de arreglo fue el evidente:

```json
"collectCoverageFrom": ["../libs/ddd/src/**/*.ts"]
```

No funciona. Los patrones se resuelven contra el directorio raíz del proyecto y no atraviesan `../`.

Pero lo importante no es eso: **la herramienta no avisa cuando un patrón no casa con ningún fichero**. Dos configuraciones distintas, el mismo informe, cero mensajes. Cambiamos algo, el número no se movió, y concluimos que ya estaba bien.

### 3. Añadir vigilancia subía el número

Este es el que más me sorprendió.

Los umbrales de cobertura se pueden poner por directorio. Y hay un efecto de segundo orden que casi nadie conoce: **los ficheros que casan con un umbral específico salen del cómputo global**.

Consecuencia: pones un umbral estricto a tu módulo mejor probado, y el porcentaje global de todo lo demás **sube**, porque acabas de sacar del promedio a los buenos.

El número mejora exactamente cuando empeoras la vigilancia. Es difícil diseñar una trampa mejor.

### 4. Un guardián que dejaba pasar cuando no encontraba la puerta

En el pipeline teníamos una comprobación que abortaba si la cobertura bajaba del umbral. Leía el informe, comparaba, y fallaba si no llegaba.

Si el informe **no existía** —porque el paso anterior falló, o porque faltaba configurar el formato— la variable quedaba vacía. Y comparar una cadena vacía con un número, en Bash, no es un error de sintaxis: devuelve **falso**.

La puerta pasaba.

Un guardián que, cuando no encuentra la puerta, concluye que está cerrada.

### 5. Una constante que cambió de significado dos veces

`COVERAGE_THRESHOLD` empezó valiendo 80 y refiriéndose a la librería. Se movió a otro pipeline, donde medía la aplicación de ejemplo. Y después a un tercero, donde medía las dos juntas.

**El nombre nunca cambió. El valor tampoco.**

El mismo 80 significó «exigente», «laxo» y «trivial» según el mes, y en ningún momento hubo un commit que dijera «estamos bajando el listón», porque técnicamente nadie lo bajó.

---

## Lo que apareció debajo

Escribir las pruebas que faltaban destapó **34 defectos**. Ocho de ellos graves. Los tres que me parecen más instructivos:

**Un objeto que fallaba una validación no podía volver a ser válido nunca.** El método que validaba sólo *añadía* errores; nunca limpiaba los de la pasada anterior. Corregías el problema, volvías a enviar, y recibías exactamente la misma respuesta. Faltaba una línea.

Nadie lo había visto porque el uso normal valida **una vez**: se construye el objeto, se comprueba, y si falla se descarta. El fallo sólo aparece cuando algo revalida — y las pruebas se habían escrito imitando el uso normal.

**Un método que devolvía un alias en lugar de una copia.** Se llamaba `clone()`. Modificabas la «copia» y cambiabas el original.

**Una comprobación de seguridad que no se ejecutaba jamás.** Un método pasó a ser una propiedad entre dos versiones. El código antiguo, `if (!objeto.esValido)`, seguía compilando — pero ahora evaluaba *la función*, que siempre es verdadera. La condición nunca se cumplía.

Sin error. Sin aviso. Sin nada en ningún log. La validación llevaba dos versiones sin ejecutarse.

---

## Las tres cosas que me llevo

**Una cobertura alta responde a una pregunta más estrecha de lo que parece.** Responde «de lo que decidí medir, ¿cuánto se ejecuta?». Nunca responde «¿decidí medir lo correcto?». Y esa segunda pregunta no te la va a hacer ninguna herramienta.

**El fallo casi nunca es un porcentaje bajo: es un fichero ausente.** Antes de mirar el número, cuenta cuántos ficheros hay en el informe y compáralo con cuántos esperabas. Son dos comandos. Si esperabas 120 y salen 74, ya sabes por dónde empezar.

**Cuando un número te sorprenda por bueno, averigua qué está contando.** Un resultado mejor de lo esperado merece la misma investigación que uno peor. Instintivamente auditamos las malas noticias y celebramos las buenas, y ahí es donde se esconden estas cosas.

---

## Qué hicimos con eso

Los 34 defectos llevaban ahí todo el tiempo. Lo único que cambió fue que alguien miró.

Hoy la librería está en **98,76 % medido**, con 1111 pruebas. Pero el cambio que más valoro no es ese: es que **el ejemplo del README es ahora un fichero de test que se ejecuta en cada push**. Si deja de compilar contra la versión publicada, el build se pone rojo antes de que nadie lo copie y pierda una tarde.

Los ejemplos a los que sustituyó tenían siete errores de tipos y no habían compilado nunca contra ninguna versión publicada. Nadie los ejecutaba, así que nadie lo sabía.

Y escribimos una herramienta que audita el código contra **la versión que tú tienes instalada**, leyendo sus declaraciones de tipos en lugar de llevar una tabla de compatibilidad que alguien tendría que mantener al día. Detecta los cuatro errores que aquella librería hace fáciles y silenciosos: los que compilan, pasan los tests y no producen ningún síntoma.

Todo eso —cuatro paquetes, la herramienta y la documentación— está abierto con licencia MIT, en español, en **[NestJS Latam](https://nestjslatam.dev)**. Lo construimos porque nos hacía falta a nosotros.

Con una advertencia que también está escrita en cada README, antes de que la descubras tú: **la API todavía se mueve y ha roto entre versiones**. Clava una versión exacta. Y uno de los cuatro paquetes es claramente el menos maduro, y lo decimos en mayúsculas en su portada.

Preferimos perder alguna instalación a que alguien se lleve una sorpresa en producción.

---

## Por qué lo cuento

Porque sospecho que no somos un caso raro.

Si mides cobertura en tu equipo, te propongo un ejercicio de cinco minutos: ejecuta el informe **sin ninguna configuración**, sobre todos los ficheros, y compara el número de ficheros con el que esperabas.

No el porcentaje. **El número de ficheros.**

Si coinciden, enhorabuena: tu número significa lo que crees. Si no, acabas de encontrar algo — y me gustaría que me lo contaras.

---

**Alberto Arroyo** — [BeyondNetCode](https://beyondnet.info/)

Construimos librerías de Domain-Driven Design para NestJS con la comunidad hispanohablante.
**[nestjslatam.dev](https://nestjslatam.dev)** · **[docs.nestjslatam.dev](https://docs.nestjslatam.dev)** · **[github.com/nestjslatam](https://github.com/nestjslatam)**

*Proyecto de comunidad no oficial, sin afiliación con NestJS ni sus autores.*
