# Un agregado que no podía volver a ser válido

De los 34 bugs que encontramos, éste era el más grave, y también el más corto de explicar.

## El síntoma

Un usuario envía un formulario con el precio a `0`. Recibe, correctamente:

```json
{ "brokenRules": [{ "property": "props.price", "message": "Price must be greater than 0" }] }
```

Lo corrige. Pone `49.99`. Reenvía.

Recibe **exactamente la misma respuesta**.

## La causa

```ts
public validate(): void {
  this._guardStrategy();
  // ...ejecuta todos los validadores, que van llamando a addBrokenRule()
}
```

Falta una línea. `validate()` **sólo añadía**. Nunca limpiaba.

Cada pasada acumulaba sobre la anterior. Un agregado que falló una vez arrastraba esa regla rota para siempre, aunque la condición que la produjo ya no se cumpliera.

## El arreglo

```ts
public validate(): void {
  // Descarta los hallazgos de la pasada anterior antes de re-derivarlos.
  // Sin esto, las reglas rotas se acumulan para siempre y un agregado que
  // falló una vez no puede volver a ser válido nunca.
  this.brokenRules.clear();

  this._guardStrategy();
  // ...
}
```

Una línea.

## Por qué nadie lo vio

Porque el patrón de uso dominante lo esconde. Mira el flujo normal:

```ts
const product = Product.create(name, description, price);   // valida UNA vez
```

Se construye el objeto, se valida, y si falla se lanza una excepción y el objeto se descarta. **Nunca se valida dos veces el mismo objeto.** En ese camino, el bug no existe.

Sólo aparece cuando algo revalida: un agregado de vida larga que se modifica y se vuelve a comprobar, un formulario que reintenta contra la misma instancia, un test que llama a `validate()` dos veces.

Y los tests no lo hacían, porque los tests se escribieron imitando el flujo normal.

## El patrón de test que lo caza

Es corto y vale para cualquier cosa que acumule estado:

```ts
it('vuelve a ser válido cuando se corrige el problema', () => {
  const product = new Product({ name, description, price: Price.create(0), status });

  expect(product.isValid).toBe(false);

  product.changePrice(Price.create(49.99));

  expect(product.isValid).toBe(true);                        // ← el que fallaba
  expect(product.brokenRules.getBrokenRules()).toHaveLength(0);
});
```

La primera aserción pasa siempre. Es la **segunda** la que tiene valor, y es la que casi nunca se escribe, porque comprobar que algo *deja* de estar mal se siente redundante cuando ya comprobaste que estaba mal.

No lo es. **Un test que sólo verifica el camino de fallo no distingue entre «detecta el error» y «se queda atascado en el error».**

## Una regla general

Si tienes un método que deriva un resultado a partir del estado actual —validación, cálculo de totales, resolución de permisos— hazte una pregunta:

> ¿Qué pasa si lo llamo dos veces?

Debería dar lo mismo si el estado no cambió, y algo distinto si cambió. Si el segundo resultado depende de que hubo un primero, tienes un acumulador donde querías una función.

Y busca `.clear()`, `= []`, `.reset()` al principio de esos métodos. Cuando falta uno, casi nunca es a propósito.
