# Referencia

Las piezas públicas de `@nestjslatam/ddd-lib@4.0.0`.

## Value objects

| Clase | Notas |
|---|---|
| `DddValueObject<TProps>` | Base genérica; para valores compuestos |
| `StringValueObject` | Registra «no vacío» y «no sólo espacios» en `addValidators()` |
| `NumberValueObject` | |
| `DateValueObject` | |
| `BooleanValueObject` | |
| `IdValueObject` | UUID; `IdValueObject.create()` genera uno nuevo |
| `DddEnum` | Miembros estáticos que son **instancias**; usa `fromValue()` para buscar |

**Miembros comunes**

```ts
vo.getValue();                    // el valor primitivo
vo.isValid;                       // getter, no método (desde 3.0.0)
vo.brokenRules.getBrokenRules();  // BrokenRule[]
vo.equals(other);                 // comparación por valor
vo.validate();                    // vuelve a derivar; limpia primero
```

## Agregados y entidades

| Clase | |
|---|---|
| `DddAggregateRoot<TAggregate, TProps>` | **Dos** argumentos de tipo |
| `DddEntity<TEntity, TProps>` | Para entidades hijas dentro de un agregado |

```ts
super(props, { id });      // el id va en la bolsa de opciones, no como 2.º argumento
```

**Miembros**

```ts
aggregate.id;                        // IdValueObject
aggregate.props;                     // TProps
aggregate.isValid;                   // getter
aggregate.brokenRules;
aggregate.apply(event);              // recolecta; NO despacha
aggregate.trackingState;             // markAsNew / markAsDirty / markAsDeleted
aggregate.getStateSnapshot();
```

## Validación

```ts
abstract class AbstractRuleValidator<TSubject> {
  protected subject: TSubject;
  abstract addRules(): void;
  protected addBrokenRule(property: string, message: string, severity?: string): void;
}
```

Cada condición dentro de `addRules()` es verdadera **cuando la regla está rota**.

```ts
class BrokenRule {
  constructor(
    public readonly property: string,
    public readonly message: string,
    public readonly severity: string = 'Error',
  ) {}
}
```

## Excepciones

| | Se traduce a |
|---|---|
| `BrokenRulesException` | 422 |
| `ArgumentNullException` | 400 |
| `InvalidFormatException` | 400 |
| `InvalidStateTransitionException` | 409 |
| `InvalidOperationException` | 409 |
| `DomainException` | base de las anteriores |

Ver [Mapear errores a HTTP](/guia/errores-http).

## Eventos

```ts
class EventBase {
  readonly aggregateId: string;
  readonly occurredOn: Date;
}
```

El despacho es de `@nestjs/cqrs`:

```ts
publisher.mergeObjectContext(aggregate).commit();
```

Síncrono y sin espera: entrega al bus y vuelve.

## Cambios entre versiones

| Versión | Cambio |
|---|---|
| **3.0.0** | `isValid` pasa de método a **getter**. `obj.isValid()` deja de compilar |
| **3.0.0** | `DddAggregateRoot` toma **dos** argumentos de tipo |
| **4.0.0** | `validate()` limpia las reglas antes de re-derivarlas |
| **4.0.0** | Se corrige el orden de construcción en `NumberValueObject` |

::: tip
`npx ddd audit` compara tu código contra los `.d.ts` de la versión que tienes **instalada**, así que detecta estos desfases sin que tengas que leer el CHANGELOG. Ver [el CLI](/cli/).
:::
