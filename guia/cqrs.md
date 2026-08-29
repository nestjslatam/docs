# Comandos y consultas

Cuatro ficheros por caso de uso, siempre los mismos. Quien entiende uno entiende todos.

```
create-product/
  create-product-dto.ts              el contrato de transporte
  create-product.command.ts          el comando
  create-product.command-handler.ts  donde se conduce el dominio
  create-product.service.ts          lo que llama el controlador
  index.ts
```

## El DTO

```ts
export class CreateProductDto {
  @IsString() name: string;
  @IsString() description: string;
  @IsNumber() price: number;
}
```

::: warning Los decoradores no son decoración
Si tu `main.ts` instala `ValidationPipe({ whitelist: true })` —y debería—, `whitelist` **conserva únicamente las propiedades que llevan un decorador de `class-validator`**.

Un DTO sin ninguno se reduce a `{}` y el handler recibe un objeto vacío. El síntoma es un `500` desconcertante en un endpoint cuyo cuerpo se ve perfectamente bien en el `curl`.
:::

Los decoradores declaran **estructura**: que el campo esté y sea del tipo correcto. No repiten las invariantes del dominio a propósito — que `Name` tenga entre 3 y 100 caracteres es asunto del agregado, y se cumple llegue el dato por HTTP, por una cola o por un script de migración.

## El servicio

Existe para que el controlador dependa de una cosa por caso de uso, y no del bus:

```ts
@Injectable()
export class CreateProductService {
  constructor(private readonly commandBus: CommandBus) {}

  async execute(dto: CreateProductDto): Promise<string> {
    return this.commandBus.execute(new CreateProductCommand(dto));
  }
}
```

## El handler

```ts
@CommandHandler(CreateProductCommand)
export class CreateProductCommandHandler
  implements ICommandHandler<CreateProductCommand, string>
{
  constructor(
    private readonly publisher: EventPublisher,
    private readonly repository: ProductRepository,
  ) {}

  async execute(command: CreateProductCommand): Promise<string> {
    const product = Product.create(
      Name.create(command.name),
      Description.create(command.description),
      Price.create(command.price),
    );

    if (!product.isValid) {
      throw new BrokenRulesException('Product', product.brokenRules.getBrokenRules());
    }

    await this.repository.save(product);
    this.publisher.mergeObjectContext(product).commit();

    return product.id.getValue();
  }
}
```

Las tres líneas que hay que mirar dos veces:

| | Si falta |
|---|---|
| `if (!product.isValid)` | Guardas un objeto que incumple sus propias invariantes, sin error |
| `BrokenRulesException`, no `new Error(...)` | Las reglas se aplanan a texto y el filtro no puede responder 422: el cliente recibe un `500` pelado |
| `.commit()` | El comando triunfa y todos los manejadores de eventos se saltan en silencio |

## Consultas

Las lecturas van por su propio camino, con DTOs propios, para que la forma de lectura pueda diferir de la del dominio sin arrastrar a nadie:

```ts
@QueryHandler(GetProductsQuery)
export class GetProductsQueryHandler implements IQueryHandler<GetProductsQuery> {
  async execute(query: GetProductsQuery): Promise<ProductResponseDto[]> {
    const products = await this.repository.findAll();
    return products.map(ProductResponseDto.fromDomain);
  }
}
```

Una consulta **no** debe cambiar estado ni emitir eventos. Si te hace falta, es un comando.

## Siguiente

- [Mapear errores a HTTP](/guia/errores-http)
