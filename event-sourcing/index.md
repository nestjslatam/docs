# ddd-es-lib

```bash
npm i @nestjslatam/ddd-es-lib
```

Event sourcing sobre MongoDB para agregados de `ddd-lib`. En vez de guardar el estado actual, guardas **todo lo que pasó** y el estado se deriva.

## Qué trae

| | |
|---|---|
| **Event store** | Persistencia de eventos con control de concurrencia optimista |
| **Snapshots** | Para no releer diez mil eventos en cada carga |
| **Upcasting** | Migrar eventos viejos a esquemas nuevos, al leerlos |
| **Proyecciones** | Vistas materializadas que se reconstruyen desde el flujo |
| **Sagas** | Coordinación entre agregados |

## Configuración

```ts
@Module({
  imports: [
    EsModule.forRoot({
      connectionUri: process.env.MONGODB_URI,
      snapshotFrequency: 100,
    }),
  ],
})
export class AppModule {}
```

::: warning MongoDB necesita un conjunto de réplicas
El event store escribe eventos y snapshots en una transacción, y **las transacciones de MongoDB exigen un replica set**. Un `mongod` suelto falla al primer commit.

Para desarrollo, un nodo único en modo réplica basta:

```bash
docker run -d -p 27017:27017 mongo:7 --replSet rs0
docker exec <id> mongosh --eval 'rs.initiate()'
```

Y un detalle que cuesta encontrar: **no se puede crear una colección dentro de una transacción multi-documento.** Si la base está vacía, la primera escritura falla con un error que no menciona nada de esto. Crea las colecciones al arrancar.
:::

## Rehidratar

```ts
const order = await this.rehydrator.rehydrate(Order, orderId);
```

Lee el snapshot más reciente, aplica los eventos posteriores y te devuelve el agregado. Internamente:

```ts
aggregate.loadFromHistory(events);   // el array entero, de una vez
```

`loadFromHistory` recibe **toda** la historia e itera por dentro. Llamarlo evento a evento en un bucle parece equivalente y no lo es.

## Publicar

El publicador de `ddd-es-lib` se instala sobre el bus de eventos de CQRS y persiste todo lo que pasa por él, antes de reenviarlo al publicador que hubiera.

```ts
await this.publisher.flush();
```

`flush()` existe porque `commit()` de CQRS es **síncrono y sin espera**. En un test necesitas un punto en el que saber que los proyectores terminaron; en producción, para vaciar antes de un apagado ordenado.

## Fuente

[github.com/nestjslatam/ddd-event-sourcing](https://github.com/nestjslatam/ddd-event-sourcing)
