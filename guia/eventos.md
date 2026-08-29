# Eventos de dominio

Un agregado registra lo que le ha pasado. Otro código reacciona. La librería se apoya en `@nestjs/cqrs` para el transporte.

## Aplicar

```ts
confirm(): void {
  // ...comprobaciones y cambio de estado
  this.apply(new OrderConfirmedEvent(this.id.getValue()));
}
```

`apply()` **no despacha nada**. Añade el evento a una lista interna del agregado. En este punto no ha salido de la memoria.

## Despachar

::: danger La línea que se olvida
```ts
await this.repository.save(order);

this.publisher.mergeObjectContext(order).commit();   // ← sin esto no pasa nada
```

Si falta, el comando **se ejecuta con éxito**, devuelve su respuesta, no lanza ningún error… y todos tus `@EventsHandler` se saltan en silencio. No hay aviso, no hay log, no hay nada que mirar. El correo de confirmación simplemente no se envía, y descubres por qué tres días después.

`npx ddd validate` tiene una regla para exactamente esto.
:::

`commit()` es **síncrono y sin espera**: entrega los eventos al bus y vuelve. No devuelve una promesa que puedas esperar para saber que los handlers terminaron. Si necesitas esa garantía —en un test, por ejemplo— necesitas un mecanismo aparte; en `ddd-es-lib` el publicador expone un `flush()` justamente por eso.

## El orden importa

```ts
await this.repository.save(order);              // 1. persistir
this.publisher.mergeObjectContext(order).commit();  // 2. publicar
```

Publicar antes de guardar abre una ventana en la que un handler lee un pedido que todavía no existe. Es una carrera que no se reproduce en local y sí en producción.

## Reaccionar

```ts
@EventsHandler(OrderConfirmedEvent)
export class OrderConfirmedEventHandler implements IEventHandler<OrderConfirmedEvent> {
  private readonly logger = new Logger(OrderConfirmedEventHandler.name);

  async handle(event: OrderConfirmedEvent): Promise<void> {
    try {
      await this.mailer.sendConfirmation(event.orderId);
    } catch (error) {
      // La escritura ya ocurrió. El bug de un proyector no es problema de quien llamó.
      this.logger.error(`No se pudo notificar ${event.orderId}`, error);
    }
  }
}
```

**Un manejador de eventos no debe tumbar el comando que lo produjo.** El pedido está confirmado; que el correo falle no lo desconfirma. Traga el error, regístralo, y si hace falta reintenta por tu cuenta.

## Sagas

Cuando un flujo abarca varios agregados —y por tanto varias fronteras de consistencia— la pieza que coordina es una saga:

```ts
@Injectable()
export class OrderSaga {
  @Saga()
  orderConfirmed = (events$: Observable<any>): Observable<ICommand> =>
    events$.pipe(
      ofType(OrderConfirmedEvent),
      map((event) => new ReserveStockCommand(event.orderId)),
    );
}
```

Escucha el flujo de eventos y emite nuevos comandos. Es el sitio correcto para «cuando se confirma un pedido, reserva el stock», porque pedido e inventario son agregados distintos y no pueden compartir transacción.

## Siguiente

- [Comandos y consultas](/guia/cqrs)
