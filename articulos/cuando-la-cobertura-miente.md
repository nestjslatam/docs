# Cuando la cobertura miente

`@nestjslatam/ddd-lib` reportaba **98,6 % de cobertura**. La cifra real era **58,4 %**, y en un módulo concreto, **8,5 %**.

Ninguna de las dos cifras era mentira. Ambas salían de Jest, correctamente calculadas. La diferencia estaba en qué se le pidió medir.

## Mecanismo 1 — `collectCoverageFrom` excluía lo no probado

```json
{
  "collectCoverageFrom": ["src/**/*.ts", "!src/**/*.spec.ts"]
}
```

Se ve inofensivo. El problema es qué pasa cuando alguien añade un directorio nuevo **fuera** de `src/`. Los ficheros de `libs/ddd/src/` no encajaban con el patrón, así que no aparecían en el informe. No como 0 %: **no aparecían**.

Un fichero sin cubrir baja la media. Un fichero ausente, no.

## Mecanismo 2 — los globs no siguen `../`

El intento de arreglo fue éste:

```json
{
  "collectCoverageFrom": ["../libs/ddd/src/**/*.ts"]
}
```

No funciona, y sin decirlo. **`collectCoverageFrom` resuelve contra `rootDir` y no atraviesa `../`.** El patrón no casa con nada, Jest no avisa de que un patrón no casó con nada, y el informe sale idéntico al anterior.

Dos configuraciones distintas, mismo resultado, cero mensajes.

## Mecanismo 3 — la clave de directorio vs. la clave de glob

`coverageThreshold` se comporta de dos maneras según cómo escribas la clave, y la diferencia no está en el nombre:

```json
{
  "coverageThreshold": {
    "global": { "lines": 80 },
    "./src/valueobjects/": { "lines": 95 },        // AGREGA el directorio
    "./src/valueobjects/**/*.ts": { "lines": 95 }  // se aplica a CADA fichero
  }
}
```

La primera forma permite que un fichero al 20 % se esconda detrás de nueve al 99 %. La segunda no.

Y hay un efecto de segundo orden que casi nadie conoce: **los ficheros que casan con una clave de ruta salen del cómputo de `global`.** Añadir un umbral estricto a un directorio bien probado *sube* el `global` de los demás, porque quita del promedio a los buenos. El número mejora justo cuando empeoras la vigilancia.

## Mecanismo 4 — la puerta de CI que se saltaba a sí misma

```yaml
- name: Coverage gate
  run: |
    COVERAGE=$(node -p "require('./coverage/coverage-summary.json').total.lines.pct")
    if [ "$COVERAGE" -lt "$COVERAGE_THRESHOLD" ]; then exit 1; fi
```

Si `coverage-summary.json` no existe —porque el paso anterior falló, o porque el reporter `json-summary` no estaba configurado—, `node -p` escribe en stderr, `COVERAGE` queda vacío, y `[ "" -lt "80" ]` en bash no es un error de sintaxis: devuelve **falso**. La puerta pasa.

Un guardián que, cuando no encuentra la puerta, decide que está cerrada.

## Mecanismo 5 — el umbral que cambió de significado dos veces

`COVERAGE_THRESHOLD` empezó valiendo 80 y refiriéndose a la librería. Se movió a un workflow donde medía la aplicación de ejemplo. Después se movió otra vez, a uno que medía ambas juntas. **El nombre nunca cambió y el valor tampoco.**

Tres cosas distintas vigiladas por la misma constante, y el mismo 80 significaba «exigente», «laxo» y «trivial» según el mes.

## Cómo se ve la verdad

```bash
npx jest --coverage --collectCoverageFrom='**/*.ts' --coverageReporters=text
```

Sin filtros, sin exclusiones, sin config. Lo que salga es lo que hay.

Y la segunda comprobación, la que realmente cierra el asunto:

```bash
# ¿el informe contiene los ficheros que crees que contiene?
node -p "Object.keys(require('./coverage/coverage-final.json')).length"
```

Si esperabas 120 ficheros y salen 74, ya sabes por dónde empezar. **El fallo casi nunca es un porcentaje bajo: es un fichero ausente.**

## Unir informes en lugar de mirarlos por separado

El último hallazgo fue de otro tipo. La capa de aplicación de la app de ejemplo marcaba **0 %**, y llevábamos tiempo tratándola como deuda pendiente.

No lo era. Diecisiete tests e2e la recorrían entera — pero los e2e escribían su informe en otro directorio, y nadie los sumaba.

```js
const libCoverage = require('istanbul-lib-coverage');

const map = libCoverage.createCoverageMap({});
map.merge(require('./coverage/coverage-final.json'));
map.merge(require('./coverage-e2e/coverage-final.json'));
```

`istanbul-lib-coverage` viene con Jest; no hay dependencia nueva que instalar. La cobertura real de la aplicación pasó de un 64 % aparente a un **85,11 %** medido.

**Un fichero está cubierto si un test lo recorre.** Cuál de los dos ejecutores lo hizo es un accidente de cómo repartiste las suites.

## El resultado

| | Antes | Después |
|---|---|---|
| Cobertura de la librería | 98,6 % *(declarada)* / 58,4 % *(real)* | **98,76 %** *(medida)* |
| Cobertura de la app | 64 % | **85,11 %** |
| Tests | 308 | **1111** |
| Bugs encontrados al subir la cobertura | — | **34 confirmados** |

Esos 34 bugs llevaban ahí todo el tiempo. Lo único que cambió fue que alguien miró.

## Lo que nos llevamos

**El número que te tranquiliza suele ser el que no está midiendo lo que crees.**

Una cobertura alta responde a la pregunta «de lo que decidí medir, ¿cuánto se ejecuta?». Nunca responde «¿decidí medir lo correcto?». Y esa segunda pregunta no te la va a hacer ninguna herramienta.

Cuando un número te sorprenda por bueno, no lo celebres: averigua qué está contando.
