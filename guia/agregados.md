# Agregados

Una raíz de agregado es la frontera de consistencia: el único sitio desde donde se puede afirmar una regla que involucra a más de un valor.

## Ciclo de vida

El ejemplo canónico es un pedido, porque tiene estados y las transiciones entre ellos son reglas de negocio:

```
DRAFT ──→ CONFIRMED ──→ PROCESSING ──→ SHIPPED ──→ DELIVERED
  │            │             │
  └────────────┴─────────────┴──→ CANCELLED
```

```ts
confirm(): void {
  if (!this.isDraft()) {
    throw new InvalidStateTransitionException(this.props.status.getValue(), 'CONFIRMED');
  }
  if (this.props.items.length === 0) {
    throw new InvalidOperationException('Cannot confirm order without items');
  }

  this.props.status = OrderStatus.CONFIRMED;
  this.trackingState.markAsDirty();
  this.apply(new OrderConfirmedEvent(this.id.getValue()));
}
```

Aquí sí se lanza, y a propósito. Una transición ilegal no es «un dato inválido que quiero listar junto a otros»: es una operación que no procede. Se traduce a un **409**, no a un 422.

## Un borrador es un carrito, y un carrito empieza vacío

Éste es el error de modelado más caro que cometimos, y merece explicarlo entero.

`Order.create()` construye un pedido con `items: []`. Si escribes las reglas «al menos un artículo» y «mínimo 10 $» sin condición, ocurre esto:

```ts
const order = Order.create(customer, address);
order.isValid;   // false  ← recién creado por su propia fábrica
```

El agregado rechaza el objeto que él mismo acababa de construir. Y como la fábrica comprueba `isValid`, **crear un pedido era imposible**.

La corrección no es quitar las reglas, es fecharlas:

```ts
export class OrderItemsValidator extends AbstractRuleValidator<Order> {
  public addRules(): void {
    // Un borrador puede estar vacío; a partir de CONFIRMED, no.
    if (this.subject.isDraft()) return;

    if (this.subject.props.items.length === 0) {
      this.addBrokenRule('props.items', 'Order must have at least one item');
    }
  }
}
```

La lección general: **una invariante no siempre es válida en todo el ciclo de vida.** «Un pedido tiene artículos» es verdad para un pedido confirmado y falsa para un carrito, y son el mismo agregado en dos momentos distintos.

## Entidades hijas

Un `Order` contiene `OrderItem`. Son **entidades**, no value objects: tienen identidad propia dentro del agregado.

```ts
addItem(productId: string, productName: string, quantity: number, unitPrice: Money): void {
  if (!this.canModifyItems()) {
    throw new InvalidOperationException(`Cannot modify items of a ${this.props.status.getValue()} order`);
  }

  const item = OrderItem.create(productId, productName, quantity, unitPrice);
  this.props.items.push(item);
  this.recalculateTotal();

  this.apply(new OrderItemAddedEvent(this.id.getValue(), item.id.getValue()));
}
```

Tres propiedades que definen lo que es una entidad hija:

- **No se guardan solas.** No hay `OrderItemRepository`. Se persisten con el pedido.
- **No se cargan solas.** Llegas a un artículo a través de su pedido, siempre.
- **No se modifican desde fuera.** `order.items` es de sólo lectura; para cambiar una cantidad llamas a `order.changeItemQuantity(...)`, que puede recalcular el total y comprobar el estado.

Si te descubres queriendo un repositorio para la entidad hija, casi siempre significa que debería ser un agregado por derecho propio.

## `create()` vs. `load()`

```ts
static create(...): Order   // valida — es un objeto nuevo
static load(...): Order     // NO valida — ya existía
```

Ya sale en [Tu primer agregado](/guia/primer-agregado), pero conviene repetirlo: si `load()` validara, cualquier endurecimiento de una regla dejaría filas históricas ilegibles. No podrías ni leerlas para migrarlas.

## Seguimiento de estado

```ts
order.trackingState.markAsNew();
order.trackingState.markAsDirty();
order.trackingState.markAsDeleted();
```

El repositorio lo consulta y decide la operación. Es lo que permite que un handler llame siempre a `save()` sin saber si está insertando o actualizando.

## Siguiente

- [Eventos de dominio](/guia/eventos) — cómo salen del agregado
- [Comandos y consultas](/guia/cqrs) — quién conduce todo esto
