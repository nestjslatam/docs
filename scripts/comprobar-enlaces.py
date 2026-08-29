#!/usr/bin/env python3
"""
Comprueba los enlaces del sitio construido.

    npm run build && python3 scripts/comprobar-enlaces.py [--externos]

Los INTERNOS se comprueban siempre y fallan el proceso: un ancla rota o una
ruta que no existe son fallos nuestros y deterministas.

Los EXTERNOS sólo con --externos, y NO fallan el proceso. Dependen de la red y
de terceros, y hay sitios que responden 403 a cualquier cosa que no parezca un
navegador —beyondnet.info es uno— y funcionan perfectamente para una persona.
Ponerlos en CI daría rojos que no significan nada.
"""
import pathlib
import re
import sys
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIST = RAIZ / '.vitepress' / 'dist'

if not DIST.exists():
    sys.exit('No hay build. Ejecuta `npm run build` primero.')

en_disco = {'/' + str(f.relative_to(DIST)) for f in DIST.rglob('*') if f.is_file()}
paginas = sorted(DIST.rglob('*.html'))


def existe(ruta: str) -> bool:
    ruta = ruta.split('?')[0]
    if ruta in en_disco:
        return True
    limpia = ruta.rstrip('/')
    return (f'{limpia}.html' in en_disco
            or f'{limpia}/index.html' in en_disco
            or (ruta == '/' and '/index.html' in en_disco))


rotos, externos = [], {}

for f in paginas:
    html = f.read_text(encoding='utf-8', errors='replace')
    pag = '/' + str(f.relative_to(DIST)).removesuffix('index.html').removesuffix('.html')
    pag = pag or '/'

    ids = set(re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', html))

    # Sólo el artículo: la barra lateral repite los enlaces de todo el sitio.
    cuerpo = re.search(r'<main[^>]*>.*?</main>', html, re.S)
    cuerpo = cuerpo.group(0) if cuerpo else html

    for u in set(re.findall(r'href="([^"]+)"', html)):
        if u.startswith('#'):
            a = u[1:]
            if a and a != 'VPContent' and a not in ids:
                rotos.append(f'{pag} -> {u}   (ancla inexistente)')
        elif u.startswith('/') and not u.startswith('//'):
            if not existe(u.split('#')[0]):
                rotos.append(f'{pag} -> {u}   (ruta inexistente)')

    for u in set(re.findall(r'href="(https?://[^"]+)"', cuerpo)):
        externos.setdefault(u.split('#')[0], set()).add(pag)

print(f'  {len(paginas)} páginas · {len(en_disco)} ficheros publicados')
print(f'  enlaces internos rotos: {len(set(rotos))}')
for r in sorted(set(rotos)):
    print(f'    ✗ {r}')

if '--externos' in sys.argv:
    print(f'\n  comprobando {len(externos)} enlaces externos…')
    for u in sorted(externos):
        try:
            req = urllib.request.Request(u, method='HEAD', headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131 Safari/537.36'
            })
            codigo = urllib.request.urlopen(req, timeout=20).status
        except urllib.error.HTTPError as e:
            codigo = e.code
        except Exception as e:
            codigo = type(e).__name__

        marca = ' ' if codigo == 200 else '·'
        nota = ''
        if codigo == 403:
            nota = '   (403 suele ser antibots; comprueba en un navegador antes de tocar nada)'
        print(f'    {marca} {codigo}  {u}{nota}')

sys.exit(1 if rotos else 0)
