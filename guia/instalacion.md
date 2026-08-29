# Instalación

```bash
npm i @nestjslatam/ddd-lib @nestjs/cqrs
```

`@nestjs/cqrs` es una **dependencia par**: la librería la necesita pero no la instala por ti, para que no acabes con dos copias distintas en tu árbol de dependencias. Si te la saltas, el error aparece al arrancar y no al compilar.

## Clava la versión

::: warning Esto no es una recomendación de estilo
La API ha roto entre versiones mayores más de una vez. En tu `package.json`:

```json
{
  "dependencies": {
    "@nestjslatam/ddd-lib": "4.0.0"
  }
}
```

Sin `^` y sin `~`. Cuando quieras subir, lees el CHANGELOG y subes a propósito.
:::

Un ejemplo real de por qué: `isValid` pasó de ser **método** a ser **getter** en la 3.0.0. El código viejo era `if (!name.isValid())`. Con un getter, `name.isValid` devuelve un booleano — pero `name.isValid()` intenta *invocar* ese booleano y revienta. Y al revés es peor: si escribes `if (!obj.isValid)` sobre una versión donde es un método, estás evaluando la **función**, que siempre es truthy, así que `!fn` es siempre `false` y **el guard nunca se dispara**. Compila, pasa los tests y no valida nada.

## Configuración del módulo

No hay `DddModule.forRoot()`. La librería son clases que importas. Lo único que tienes que registrar es CQRS, como en cualquier proyecto NestJS:

```ts
import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';

@Module({
  imports: [CqrsModule],
})
export class ProductsModule {}
```

## TypeScript

La librería se distribuye con sus propios `.d.ts`. Necesitas `strict` activado — o al menos `strictNullChecks` — porque varias firmas dependen de ello para ser útiles:

```json
{
  "compilerOptions": {
    "strict": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "target": "ES2023"
  }
}
```

## Comprueba que funciona

```ts
import { StringValueObject } from '@nestjslatam/ddd-lib';

class Foo extends StringValueObject {}

console.log(new Foo('hola').isValid);  // true
console.log(new Foo('').isValid);      // false
```

Si la segunda línea imprime `true`, tienes una versión donde `isValid` es un método. Revisa la versión instalada con `npm ls @nestjslatam/ddd-lib`.

## Siguiente

[Tu primer agregado](/guia/primer-agregado)
