# ddd-cli

```bash
npm install -D @nestjslatam/ddd-cli
```

Una herramienta que **lee la librería que tú tienes instalada**. No lleva una idea propia de cómo es la API: parsea los `.d.ts` de tu `node_modules`, así que lo que te dice describe tu proyecto y no una plantilla.

## Los comandos

| Comando | Alias | ¿Necesita modelo? |
|---|---|---|
| `ddd list` | `ls` | No |
| `ddd explain <símbolo>` | `why` | Sólo sin `--raw` |
| `ddd new <tipo> <Nombre>` | `n` | No |
| `ddd extend <Base> <Nombre>` | `x` | No |
| `ddd validate [ruta]` | `check` | No |
| `ddd generate:aggregate "<prosa>"` | `ga` | **Sí** |
| `ddd mcp` | — | No |

Estereotipos de `new`: `value-object`, `validator`, `event`, `exception`, `aggregate`, `enum`.

Códigos de salida: `0` limpio, `1` violaciones o fallo. **`validate` se puede poner en CI tal cual.**

## Por qué lee tus `.d.ts`

Porque la alternativa es mentir. Una herramienta con su propia tabla de compatibilidad da avisos falsos en cuanto la librería cambia — y ésta ha cambiado.

Leyendo los tipos instalados, `ddd validate` detecta que tu `if (!name.isValid())` ya no compila **contra tu versión concreta**, sin que nadie tenga que mantener esa tabla al día.

## Las cuatro reglas de `validate`

Son los errores que el compilador no puede ver:

1. Una fábrica que no comprueba `isValid`
2. Un `addValidators` que no llama a `super`
3. Un handler que no llama a `commit()`
4. Un validador que lee un campo de instancia dentro de `addValidators`

Los cuatro compilan. Los cuatro pasan los tests. Los cuatro rompen algo en silencio.

## Siguiente

- **[La guía completa](/cli/guia)** — construye un dominio de carga marítima desde cero, comando a comando
- [Servidor MCP](/cli/mcp) — usarlo desde Claude Code o Cursor
