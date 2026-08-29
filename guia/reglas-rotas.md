# Reglas rotas

Cómo funciona la recolección, y los tres errores que hace fáciles. Los tres los detecta `npx ddd validate`.

## Cómo funciona

Un agregado o value object mantiene una colección de `BrokenRule`. Al validar, cada validador registrado añade las suyas:

```ts
product.isValid;                       // boolean — hay cero reglas rotas
product.brokenRules.getBrokenRules();  // BrokenRule[]
```

Cada `BrokenRule` tiene tres campos:

```ts
{ property: 'props.price', message: 'Price must be greater than 0', severity: 'Error' }
```

`property` es la ruta, y es lo que permite a un formulario resaltar el campo correcto en vez de mostrar un aviso genérico arriba del todo.

## Se vacía en cada pasada

`validate()` limpia antes de re-derivar:

```ts
public validate(): void {
  this.brokenRules.clear();
  // ...vuelve a ejecutar todos los validadores
}
```

Parece un detalle de implementación y no lo es. **Sin ese `clear()`, un agregado que falló una vez no puede volver a ser válido nunca.** Corriges el precio, vuelves a validar, y la regla vieja sigue ahí porque sólo se añadía. La respuesta al segundo intento sería idéntica a la del primero, y el usuario concluiría, con razón, que el formulario está roto.

## Error 1 — la fábrica que no comprueba

```ts
static create(value: string): Name {
  return new Name(value);      // ← nunca comprueba isValid
}
```

**Síntoma:** ninguno. Todo funciona. Los objetos inválidos entran en tu sistema en silencio y aparecen semanas después como datos imposibles en un informe.

La validación **recolecta y no lanza**. Es una decisión de diseño deliberada —es lo que permite devolver las cinco reglas rotas de golpe— pero traslada la responsabilidad de preguntar a quien construye.

```ts
static create(value: string): Name {
  const name = new Name(value);
  if (!name.isValid) {
    throw new BrokenRulesException('Name', name.brokenRules.getBrokenRules());
  }
  return name;
}
```

## Error 2 — el `addValidators` que no encadena

```ts
override addValidators(): void {
  this.validatorRules.add(new NameLengthValidator(this));   // ← falta super
}
```

**Síntoma:** ninguno, otra vez. No hay error, no hay aviso. Los validadores que la clase base registraba —«no vacío», «no sólo espacios»— simplemente dejan de existir, y `''` pasa a ser un nombre válido.

```ts
override addValidators(): void {
  super.addValidators();
  this.validatorRules.add(new NameLengthValidator(this));
}
```

## Error 3 — leer un campo propio dentro de `addValidators`

```ts
export class Price extends NumberValueObject {
  private readonly max = 9_999_999.99;

  override addValidators(): void {
    super.addValidators();
    this.validatorRules.add(new MaxValidator(this, this.max));  // ← undefined
  }
}
```

**Síntoma:** esta vez sí lo hay, y es escandaloso — revienta en **cada** construcción.

La causa es el orden: el constructor de la clase base llama a `addValidators()` **antes** de que se ejecute el cuerpo de tu constructor, así que `this.max` todavía no existe. `NumberValueObject`, dentro de la propia librería, se publicó roto exactamente así durante dos versiones.

La solución es no depender de estado de instancia ahí: usa una constante de módulo, un `static readonly`, o pasa el valor al validador directamente.

## La condición va invertida

Ya sale en [Tu primer agregado](/guia/primer-agregado), pero se repite aquí porque es el que más veces se cuela:

```ts
public addRules(): void {
  // Esto significa "la regla ESTÁ ROTA cuando el precio es <= 0"
  if (this.subject.props.price.getValue() <= 0) {
    this.addBrokenRule('props.price', 'Price must be greater than 0');
  }
}
```

Se lee como una aserción y no lo es. Si escribes `>= 0` pensando «el precio debe ser positivo», acabas con un validador que marca como rotos justamente los precios correctos.

## Siguiente

- [Mapear errores a HTTP](/guia/errores-http) — convertir esto en 400, 422 y 409
