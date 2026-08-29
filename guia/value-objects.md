# Value objects

Un value object es un tipo definido por su valor, no por su identidad. Dos `Money` de 10 € son el mismo `Money`; dos pedidos con los mismos datos son pedidos distintos.

## Bases disponibles

| Base | Para |
|---|---|
| `StringValueObject` | Texto con reglas |
| `NumberValueObject` | Números con rango o precisión |
| `DateValueObject` | Fechas con reglas temporales |
| `BooleanValueObject` | Banderas con significado de dominio |
| `IdValueObject` | Identidades (UUID) |
| `DddEnum` | Conjuntos cerrados de valores |
| `DddValueObject<T>` | Cualquier otra forma, incluidas las compuestas |

## Compuestos

Cuando el valor tiene varias partes que sólo tienen sentido juntas:

```ts
interface IMoneyProps {
  amount: number;
  currency: string;
}

export class Money extends DddValueObject<IMoneyProps> {
  static create(amount: number, currency = 'USD'): Money {
    const money = new Money({ amount, currency });
    if (!money.isValid) {
      throw new BrokenRulesException('Money', money.brokenRules.getBrokenRules());
    }
    return money;
  }

  add(other: Money): Money {
    if (other.props.currency !== this.props.currency) {
      throw new InvalidOperationException(
        `Cannot add ${other.props.currency} to ${this.props.currency}`,
      );
    }
    return Money.create(this.props.amount + other.props.amount, this.props.currency);
  }
}
```

`add()` devuelve un `Money` **nuevo**. Los value objects son inmutables: si necesitas otro valor, construyes otro objeto. Mutar uno compartido cambiaría el valor bajo los pies de quien lo tuviera guardado.

Y fíjate en lo que hace ese guard: sumar dólares y euros deja de ser un bug silencioso de producción y pasa a ser imposible de escribir.

## Comparación por valor

```ts
Money.create(10, 'USD').equals(Money.create(10, 'USD'));  // true
Money.create(10, 'USD') === Money.create(10, 'USD');      // false
```

Usa siempre `.equals()`. La igualdad por referencia sobre un value object es casi siempre un bug.

## `DddEnum` no es un enum de TypeScript

Es la fuente de un error concreto que costó tiempo encontrar:

```ts
export class ProductStatus extends DddEnum {
  static readonly ACTIVE = new ProductStatus('ACTIVE');
  static readonly INACTIVE = new ProductStatus('INACTIVE');
  static readonly DELETED = new ProductStatus('DELETED');
}
```

Los miembros estáticos son **instancias**, no cadenas. Así que esto no funciona nunca:

```ts
Object.values(ProductStatus).includes(dto.status);   // siempre false
```

Estás comparando instancias con un `string`. El endpoint que hacía esto rechazaba *todas* las llamadas —incluidas las correctas— con el mensaje maravillosamente contradictorio `Expected: ACTIVE, INACTIVE or DELETED. Provided value: 'INACTIVE'`.

Usa la búsqueda propia del enum:

```ts
const status = ProductStatus.fromValue(dto.status);   // devuelve la instancia, o lanza
```

## El orden de construcción

Ya está en [Reglas rotas](/guia/reglas-rotas) como error 3, pero es específico de los value objects y vale la pena verlo aquí:

```ts
export class Price extends NumberValueObject {
  private readonly max = 9_999_999.99;      // ← se asigna DESPUÉS

  override addValidators(): void {
    super.addValidators();
    this.validatorRules.add(new MaxValidator(this, this.max));   // ← undefined
  }
}
```

El constructor base llama a `addValidators()` antes de que corra el cuerpo del tuyo. Saca el valor a una constante de módulo o a un `static readonly` y desaparece.

## ¿Y si ya está hecho?

Antes de escribir un `Email`, un `Money` o un `Phone`, mira [`ddd-valueobjects`](/valueobjects/): son doce, con sus reglas y sus formateadores, y ya están probados.

## Siguiente

- [Reglas rotas](/guia/reglas-rotas)
