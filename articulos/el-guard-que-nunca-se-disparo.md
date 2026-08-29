# El guard que nunca se disparó

Durante dos versiones, `@nestjslatam/ddd-lib` tuvo una validación que no validaba nada. Compilaba, los tests pasaban en verde, y la causa cabe en una línea.

## El cambio

En la 3.0.0, `isValid` pasó de método a getter:

```ts
// 2.x
public isValid(): boolean { ... }

// 3.x
public get isValid(): boolean { ... }
```

Un cambio razonable. `isValid` describe un estado, no una acción, y un getter lo dice mejor. El CHANGELOG lo anunciaba como cambio incompatible.

## El código que quedó

```ts
static create(value: string): Name {
  const name = new Name(value);

  if (!name.isValid) {
    throw new BrokenRulesException('Name', name.brokenRules.getBrokenRules());
  }

  return name;
}
```

Correcto en 3.x. Ahora mira la versión anterior, escrita cuando `isValid` era un método, pero **sin los paréntesis**:

```ts
if (!name.isValid) {   // ← sobre 2.x, esto evalúa la FUNCIÓN
```

En 2.x, `name.isValid` es una referencia a función. Una función es siempre *truthy*. Así que `!name.isValid` es **siempre `false`**, y el cuerpo del `if` no se ejecuta jamás.

La fábrica devuelve todos los objetos que le pidas, válidos o no. Sin error. Sin aviso. Sin nada que aparezca en un log.

## Por qué no lo cogió el compilador

Porque `!fn` es TypeScript perfectamente legal. Negar una función da un booleano; el tipo es correcto. El compilador no tiene forma de saber que querías negar el *resultado* de llamarla.

Con `strictNullChecks` tampoco salta: no hay nada nulo. Con ESLint tampoco, salvo que tengas activada `@typescript-eslint/no-unnecessary-condition`, que es una regla que requiere información de tipos y que casi nadie enciende porque es lenta.

## Por qué no lo cogieron los tests

Ésta es la parte que duele.

```ts
it('rechaza un nombre demasiado corto', () => {
  expect(() => Name.create('Ab')).toThrow();
});
```

Este test **falla** cuando el bug está presente, y efectivamente lo hacía. Pero el bug no estaba en `Name` — estaba en value objects que nadie había cubierto todavía. Las clases con tests estaban bien; las que no, tenían el guard muerto y nadie preguntaba.

Y la cobertura decía 98,6 %, lo cual nos lleva a [otro artículo](/articulos/cuando-la-cobertura-miente).

## La simetría del error

Lo peor es que falla en las dos direcciones, y de formas distintas:

| Escribes | Sobre 2.x (método) | Sobre 3.x (getter) |
|---|---|---|
| `if (!obj.isValid)` | **Nunca se dispara**, en silencio | Correcto |
| `if (!obj.isValid())` | Correcto | **`TypeError`** al arrancar |

La migración de 2.x a 3.x rompe ruidosamente: intentas invocar un booleano y revienta en cuanto se ejecuta esa línea. Eso es bueno — un fallo escandaloso es un fallo que se arregla.

La dirección peligrosa es la otra: código escrito con la sintaxis de getter corriendo sobre una versión de método. Ahí no revienta nada. Simplemente deja de validar.

## Qué hicimos

**Un `validate` que lee tus tipos instalados.** `npx ddd validate` no lleva una tabla de compatibilidad; parsea los `.d.ts` de tu `node_modules` y comprueba tu código contra la API que realmente tienes. Es una de sus cuatro reglas.

**Convertimos el README en un test.** El ejemplo de inicio rápido del README es ahora un fichero `.spec.ts` que corre en CI. Si el ejemplo deja de compilar contra la versión publicada, el build se pone rojo antes de que nadie lo copie.

## Lo que nos llevamos

Un tipo booleano y una función que devuelve booleano son **intercambiables en un contexto de verdad**, y ésa es la trampa. El lenguaje no distingue «el valor» de «la cosa que produce el valor» cuando lo único que haces es preguntar si es cierto.

Cada vez que un cambio de API convierte un método en propiedad —o al revés— estás creando esta trampa para todos tus consumidores. Merece la pena una regla de lint, un `validate`, o como mínimo un párrafo en mayúsculas en el CHANGELOG.
