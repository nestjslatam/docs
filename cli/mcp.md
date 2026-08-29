# Servidor MCP

```bash
claude mcp add ddd -- npx -y @nestjslatam/ddd-cli mcp
```

```jsonc
// cualquier otro cliente MCP
{
  "mcpServers": {
    "ddd": { "command": "npx", "args": ["-y", "@nestjslatam/ddd-cli", "mcp"] }
  }
}
```

## Siete herramientas, sin clave de API

| Herramienta | Qué hace |
|---|---|
| `ddd_list` | Inventaría cada estereotipo que exporta la librería instalada |
| `ddd_describe` | La declaración de tipos real de un estereotipo |
| `ddd_new` | Genera un estereotipo desde una plantilla determinista |
| `ddd_extend` | Anda una subclase de cualquier base, con todos los miembros abstractos |
| `ddd_validate` | Comprueba el TypeScript contra las cuatro reglas del idioma |
| `ddd_aggregate_schema` | El JSON Schema que debe cumplir el modelo de un agregado |
| `ddd_render_aggregate` | Convierte la especificación de un agregado en ficheros |

**No hace falta clave porque el agente ya tiene modelo y credenciales.** Si trabajas dentro de Claude Code, Codex o Cursor, el que razona es él; el CLI hace lo que un modelo hace mal.

::: tip Ojo con la distinción
Esto vale para el **servidor MCP**. El comando suelto `ddd generate:aggregate` sí necesita un proveedor de modelo, y `ddd explain` también salvo que uses `--raw`. Lo que no necesita clave es el camino MCP, porque ahí el modelo lo pone tu agente.
:::

## El reparto de trabajo

El agente decide la frontera del agregado, las invariantes y los nombres — **criterio**. El CLI lee las declaraciones instaladas con exactitud, renderiza de forma determinista y audita contra el idioma.

`ddd_describe` devuelve **hechos, no prosa**, a propósito: la explicación la escribe el agente, que para eso está.

`ddd_aggregate_schema` y `ddd_render_aggregate` hacen el reparto explícito: el agente produce una **especificación**, el CLI la renderiza, y una especificación que no cumple el esquema vuelve con los problemas campo por campo, así que el agente se corrige solo sin que haya nadie mirando.

## Nada toca el disco sin permiso

Ninguna llamada escribe salvo que pase `write: true`, y **aun así jamás sobrescribe un fichero existente**. Un agente trabajando sin supervisión no debe pisar código de dominio escrito a mano.

## Un prompt que funciona

> Lee el `ddd-lib` que tengo instalado y modela un agregado Cargo para un dominio de transporte marítimo: un identificador de seguimiento, una especificación de ruta con origen y destino, un peso bruto y un viaje actual. Valida lo que escribas antes de enseñármelo.

El agente llamará a `ddd_list`, `ddd_describe`, `ddd_aggregate_schema`, `ddd_render_aggregate` y `ddd_validate` en el orden que necesite.
