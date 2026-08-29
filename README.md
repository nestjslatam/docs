# Documentación de NestJS Latam

El sitio publicado en **[docs.nestjslatam.dev](https://docs.nestjslatam.dev)**.

Construido con [VitePress](https://vitepress.dev). Todo el contenido es Markdown.

## En local

```bash
npm install
npm run dev      # http://localhost:5173
```

```bash
npm run build    # a .vitepress/dist
npm run preview
```

## Estructura

```
guia/             la guía de ddd-lib
cli/              ddd-cli y su servidor MCP
valueobjects/     el catálogo de ddd-valueobjects
event-sourcing/   ddd-es-lib
articulos/        artículos de fondo
.vitepress/       configuración y tema
```

## Colaborar

Cada página tiene un enlace **«Editar esta página en GitHub»** al final. Si algo está mal, mal explicado o simplemente te costó entenderlo, corrígelo — no hace falta pedir permiso.

Dos cosas que pedimos:

**Que las afirmaciones sean ciertas.** Si una página dice que algo funciona, es porque alguien lo ejecutó. Los bloques de código de la guía salen del [repositorio de ejemplo](https://github.com/nestjslatam/ddd), donde corren en CI.

**Español llano.** El público es hispanohablante y de nivel muy variado. Prefiere la frase corta y el ejemplo concreto a la precisión terminológica.

Los commits siguen [Conventional Commits](https://www.conventionalcommits.org/).

---

Hecho en Perú 🇵🇪 · Impulsado por [BeyondNetCode](https://beyondnet.info/)
