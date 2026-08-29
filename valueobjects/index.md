# ddd-valueobjects

```bash
npm i @nestjslatam/ddd-valueobjects
```

Doce value objects ya escritos y probados, para que no vuelvas a implementar la validación de un email.

## El catálogo

| Value object | Valida | Extra |
|---|---|---|
| `Email` | Formato RFC, longitud | `domain`, `localPart` |
| `Money` | Importe y moneda | Aritmética que **se niega a mezclar monedas** |
| `PhoneNumber` | Formato internacional | Normaliza a E.164 |
| `Url` | Esquema y autoridad | |
| `PostalCode` | Por país | |
| `DateRange` | Inicio ≤ fin | `contains()`, `overlaps()` |
| `Percentage` | 0–100 | |
| `Latitude` / `Longitude` | Rango geográfico | |
| `Dni` | Documento peruano, 8 dígitos | |
| `Ruc` | Documento peruano, dígito verificador | Distingue persona de empresa |
| `CreditCard` | Luhn | Detecta la marca; **no almacena el número completo** |

## Uso

```ts
import { Email, Money } from '@nestjslatam/ddd-valueobjects';

const email = Email.create('ada@example.com');
email.domain;        // 'example.com'

const price = Money.create(49.99, 'PEN');
const total = price.add(Money.create(10, 'PEN'));   // Money(59.99, 'PEN')

price.add(Money.create(10, 'USD'));   // InvalidOperationException
```

Ese último caso es la razón de ser de la librería: sumar soles y dólares deja de ser un bug silencioso y pasa a ser imposible de escribir.

## Se integran igual que los tuyos

Extienden las mismas bases de `ddd-lib`, así que recolectan reglas rotas de la misma forma y el mismo `DomainExceptionFilter` los traduce a 400 y 422 sin configuración adicional.

```ts
interface ICustomerProps {
  name: Name;          // tuyo
  email: Email;        // de la librería
  phone: PhoneNumber;  // de la librería
}
```

## Fuente

[github.com/nestjslatam/ddd-valueobjects](https://github.com/nestjslatam/ddd-valueobjects)
