# Tu primer agregado

De cero a un `Product` que valida sus propias reglas. Todo el código de esta página está tomado del [repositorio de ejemplo](https://github.com/nestjslatam/ddd), donde se ejecuta en cada CI.

## 1. Un value object

Empieza por lo más pequeño. Un `Name` no es un `string`: es un `string` con reglas.

```ts
import {
  StringValueObject,
  BrokenRulesException,
  AbstractRuleValidator,
} from '@nestjslatam/ddd-lib';

class NameLengthValidator extends AbstractRuleValidator<Name> {
  public addRules(): void {
    const value = this.subject.getValue();

    if (value.length < 3) {
      this.addBrokenRule('value', 'Name must be at least 3 characters');
    }
    if (value.length > 100) {
      this.addBrokenRule('value', 'Name must be at most 100 characters');
    }
  }
}

export class Name extends StringValueObject {
  static create(value: string): Name {
    const name = new Name(value);

    if (!name.isValid) {
      throw new BrokenRulesException('Name', name.brokenRules.getBrokenRules());
    }

    return name;
  }

  override addValidators(): void {
    super.addValidators();
    this.validatorRules.add(new NameLengthValidator(this));
  }
}
```

::: danger La condición va al revés de como se lee una aserción
`if (value.length < 3)` significa **«la regla está rota»**, no «la regla se cumple». Cada condición dentro de `addRules()` es verdadera cuando algo va *mal*.

Es el error más fácil de cometer y el más difícil de ver: un validador con la condición invertida pasa exactamente cuando debería fallar, y sus tests pasan si los escribiste con la misma confusión.
:::

## 2. El agregado

```ts
import { DddAggregateRoot, IdValueObject } from '@nestjslatam/ddd-lib';

interface IProductProps {
  name: Name;
  description: Description;
  price: Price;
  status: ProductStatus;
}

export class Product extends DddAggregateRoot<Product, IProductProps> {
  private constructor(props: IProductProps, id?: IdValueObject) {
    super(props, { id });
    this.trackingState.markAsNew();
  }

  static create(name: Name, description: Description, price: Price): Product {
    const product = new Product({
      name,
      description,
      price,
      status: ProductStatus.ACTIVE,
    });

    if (!product.isValid) {
      throw new BrokenRulesException(
        'Product',
        product.brokenRules.getBrokenRules(),
      );
    }

    product.apply(new ProductCreatedEvent(product.id.getValue()));

    return product;
  }

  override addValidators(): void {
    super.addValidators();
    this.validatorRules.add(new ProductPriceValidator(this));
    this.validatorRules.add(new ProductBusinessRulesValidator(this));
  }
}
```

Fíjate en tres detalles que cuestan una tarde si los descubres solo:

**Dos argumentos de tipo, no uno.** `DddAggregateRoot<Product, IProductProps>` — el agregado y sus props.

**El id va en la bolsa de opciones.** La firma del constructor base es `(props, options?)`, con `{ id }` dentro del segundo argumento. Pasarlo como `super(props, id)` compila en algunas versiones y te deja el id a `undefined`.

**`markAsNew()` es tuyo.** El seguimiento de estado no adivina; se lo dices. Un repositorio lo lee después para decidir entre `INSERT`, `UPDATE` y `DELETE` sin que nadie se lo cuente.

## 3. Cargar sin validar

Junto a `create()` va `load()`, y hace algo deliberadamente distinto:

```ts
static load(props: IProductProps, id: IdValueObject): Product {
  const product = new Product(props, id);
  product.trackingState.markAsDirty();
  return product;   // sin comprobar isValid
}
```

**Rehidratar algo que ya está en la base de datos no es lo mismo que crearlo.** Si las reglas cambiaron desde que se guardó, `load()` debe devolverte la fila tal como está — para que puedas leerla, migrarla o corregirla. Un `load()` que valida convierte un cambio de reglas en una base de datos que no se puede abrir.

## 4. Una regla que sólo el agregado puede ver

Éste es el momento en que el patrón empieza a pagar:

```ts
export class ProductBusinessRulesValidator extends AbstractRuleValidator<Product> {
  public addRules(): void {
    const { name, description } = this.subject.props;

    if (description.getValue().length <= name.getValue().length) {
      this.addBrokenRule(
        'props.description',
        'Description must be longer than the name',
      );
    }
  }
}
```

`name` es válido. `description` es válida. La **combinación** no lo es, y ningún value object puede saberlo por sí mismo porque ninguno de los dos ve al otro.

Para esto existe la raíz de agregado: es el único sitio del sistema desde donde esa frase se puede escribir.

## 5. Probarlo

```ts
describe('Product', () => {
  it('recolecta todas las reglas rotas, no sólo la primera', () => {
    const product = Product.create(
      Name.create('Ab'),                    // demasiado corto
      Description.create('X'),              // más corta que el nombre
      Price.create(0),                      // no positivo
    );
  }); // ← esto lanza en Name.create, antes de llegar al agregado
});
```

Ese test está mal, y de una forma instructiva: **los value objects lanzan en su fábrica**, así que nunca llegas al agregado con tres cosas rotas a la vez. Para ver la recolección en acción tienes que construir con value objects válidos y romper una regla *de agregado*:

```ts
it('recolecta todas las reglas rotas, no sólo la primera', () => {
  const product = new Product({
    name: Name.create('Wireless Keyboard'),
    description: Description.create('Corta'),  // más corta que el nombre
    price: Price.create(49.99),
    status: ProductStatus.ACTIVE,
  });

  expect(product.isValid).toBe(false);
  expect(product.brokenRules.getBrokenRules()).toHaveLength(1);
});
```

## Siguiente

- [Agregados](/guia/agregados) — ciclo de vida, entidades hijas, transiciones de estado
- [Reglas rotas](/guia/reglas-rotas) — los tres errores clásicos, con su síntoma
