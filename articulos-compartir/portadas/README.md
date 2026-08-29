# Portadas

Generadas desde `portada.html` con Chrome en modo headless, para poder
regenerarlas cuando cambien las cifras o el mensaje.

| Fichero | Medida | Para |
|---|---|---|
| `portada-linkedin-articulo.png` | 1280×720 | La portada del artículo de LinkedIn |
| `portada-linkedin-enlace.png` | 1200×627 | Vista previa cuando se comparte el enlace |

## Regenerar

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --window-size=1280,720 --screenshot=portada-linkedin-articulo.png \
  --virtual-time-budget=6000 "file://$PWD/portada.html"
```

Para el otro tamaño, cambia `width`/`height` en el `<style>` del HTML y el
`--window-size` a `1200,627`.

## Por qué así y no una foto

En el feed compite con fotos de personas, y ahí una imagen bonita pierde
contra un titular legible en miniatura. La portada tiene el titular en grande,
las cifras —que son el argumento— y el dominio abajo. Se lee incluso al tamaño
de la vista previa.

Las cifras son las medidas, no redondeadas. Es lo que hace que se lean.
