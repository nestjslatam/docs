---
layout: home

hero:
  name: NestJS Latam
  text: Domain-Driven Design para NestJS
  tagline: Agregados que acumulan sus propias reglas rotas, value objects que se validan solos y un CLI que lee tu código. En español, con el fuente a la vista.
  image:
    src: /logo-large.svg
    alt: NestJS Latam
  actions:
    - theme: brand
      text: Empezar
      link: /guia/
    - theme: alt
      text: La guía del CLI
      link: /cli/guia
    - theme: alt
      text: GitHub
      link: https://github.com/nestjslatam

features:
  - icon: 🧱
    title: ddd-lib
    details: Los bloques de construcción. Agregados, value objects, validadores, seguimiento de estado y eventos de dominio, sobre @nestjs/cqrs.
    link: /guia/
    linkText: Leer la guía
  - icon: 🤖
    title: ddd-cli
    details: Entiende, genera y audita tu dominio. Lee los .d.ts de la versión que tú tienes instalada, y corre como servidor MCP sin API key.
    link: /cli/
    linkText: Ver comandos
  - icon: 💎
    title: ddd-valueobjects
    details: Doce value objects ya hechos — email, dinero, teléfono, documentos de identidad, fechas — con sus reglas y sus formateadores.
    link: /valueobjects/
    linkText: Ver el catálogo
  - icon: 📼
    title: ddd-es-lib
    details: Event sourcing sobre MongoDB. Event store, snapshots, upcasting, sagas y vistas materializadas.
    link: /event-sourcing/
    linkText: Empezar
---

## Cinco minutos

```bash
npm i @nestjslatam/ddd-lib @nestjs/cqrs
```

```ts
import { StringValueObject, BrokenRulesException } from '@nestjslatam/ddd-lib';

export class Name extends StringValueObject {
  static create(value: string): Name {
    const name = new Name(value);

    // La validación RECOLECTA reglas rotas y nunca lanza.
    // Si no compruebas aquí, create() te devuelve un objeto inválido.
    if (!name.isValid) {
      throw new BrokenRulesException('Name', name.brokenRules.getBrokenRules());
    }

    return name;
  }

  override addValidators(): void {
    super.addValidators(); // sin esta línea los validadores base desaparecen
    this.validatorRules.add(new NameLengthValidator(this));
  }
}
```

Esas dos líneas comentadas son el 80 % de los errores que verás al empezar. La [guía](/guia/) explica por qué.

## Una advertencia honesta

La API todavía se mueve y ha roto en más de una versión: **clava una versión exacta** en tu `package.json`. Cada repositorio dice en su README qué está probado y qué no, con números medidos y no prometidos.

Preferimos que lo sepas antes y no después.

## Esto es una comunidad

La documentación vive en [`nestjslatam/docs`](https://github.com/nestjslatam/docs) y cada página tiene un enlace **«Editar esta página en GitHub»** al final. Si algo está mal, mal explicado o simplemente te costó entenderlo, corrígelo — no hace falta pedir permiso.

Las conversaciones, artículos y novedades de la comunidad están en **[nestjslatam.dev](https://nestjslatam.dev)**.
