#!/usr/bin/env python3
"""
Importa la guía del CLI desde su repositorio y adapta sus anclas.

El mismo fichero se lee en dos sitios con reglas de anclaje distintas:

    GitHub      ## 3. Leer un contrato: `ddd explain`  ->  #3-leer-un-contrato-ddd-explain
    VitePress                                          -> #_3-leer-un-contrato-ddd-explain

VitePress antepone un guion bajo cuando el identificador empezaría por un
dígito —un id de CSS no puede— y además quita los acentos y convierte los dos
puntos en guion. Un índice escrito a mano no puede acertar en los dos, así que
el fichero del repositorio conserva las anclas de GitHub y aquí se traducen.

    python3 scripts/importar-guia.py ../ddd-cli/docs/GUIDE.md
"""
import pathlib
import re
import sys
import unicodedata

ORIGEN = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                      else '../ddd-cli/docs/GUIDE.md').resolve()
DESTINO = pathlib.Path(__file__).resolve().parent.parent / 'cli' / 'guia.md'

CABECERA = (
    '---\ntitle: Guía completa del CLI\n---\n\n'
    '::: tip Se mantiene en el repositorio\n'
    'Esta guía vive en '
    '[`nestjslatam/ddd-cli`](https://github.com/nestjslatam/ddd-cli/blob/main/docs/GUIDE.md) '
    'y se reproduce aquí. Si encuentras algo que corregir, el enlace lleva al fichero.\n'
    ':::\n\n'
)


def ancla_vitepress(titulo: str) -> str:
    """Reproduce el identificador que genera VitePress para un encabezado."""
    # Fuera el marcado en línea: `código`, **negrita**, enlaces.
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', titulo)
    t = re.sub(r'[`*_]', '', t)

    # Sin acentos: VitePress normaliza a ASCII.
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))

    t = t.lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')

    # Un id de CSS no puede empezar por dígito.
    return f'_{t}' if t and t[0].isdigit() else t


texto = ORIGEN.read_text(encoding='utf-8')

# Mapa: ancla de GitHub -> ancla de VitePress, para cada encabezado.
mapa = {}
for nivel, titulo in re.findall(r'^(#{2,4})\s+(.+)$', texto, re.M):
    limpio = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', titulo)
    limpio = re.sub(r'[`*_]', '', limpio).strip()

    # La forma de GitHub: minúsculas, se conservan los acentos, fuera la
    # puntuación y los espacios pasan a guion.
    gh = limpio.lower()
    gh = re.sub(r'[^\w\s-]', '', gh, flags=re.UNICODE)
    gh = re.sub(r'[\s]+', '-', gh).strip('-')

    mapa[gh] = ancla_vitepress(titulo)

# Se reescriben sólo los enlaces internos.
def sustituir(m):
    destino = m.group(1)
    return f'](#{mapa.get(destino, destino)})'

salida, no_resueltos = re.subn(r'\]\(#([^)]+)\)', sustituir, texto)

rotos = [a for a in re.findall(r'\]\(#([^)]+)\)', salida)
         if a not in mapa.values()]

DESTINO.write_text(CABECERA + salida, encoding='utf-8')

print(f'  {ORIGEN.name} -> {DESTINO.relative_to(DESTINO.parent.parent)}')
print(f'  encabezados mapeados : {len(mapa)}')
print(f'  enlaces reescritos   : {no_resueltos}')

if rotos:
    print('\n  ✗ enlaces internos que no apuntan a ningún encabezado:')
    for r in sorted(set(rotos)):
        print(f'      #{r}')
    sys.exit(1)

print('  ✓ todos los enlaces internos resuelven')
