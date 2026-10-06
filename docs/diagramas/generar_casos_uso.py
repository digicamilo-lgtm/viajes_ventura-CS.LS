"""Genera el diagrama UML de casos de uso del Informe Técnico como SVG.

Uso:  py generar_casos_uso.py   -> escribe casos-de-uso.svg en esta carpeta.
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

FONT = "Arial, Helvetica, sans-serif"
W, H = 1150, 800
RX, RY = 108, 31
IZQ, MED, DER = 330, 600, 855

# id: (x, y, texto)
CASOS = {
    "consultar": (IZQ, 110, "CU-01 Consultar paquetes\ny cupo disponible"),
    "registrarse": (IZQ, 215, "CU-02 Registrarse"),
    "reservar": (IZQ, 380, "CU-04 Reservar paquete"),
    "historial": (IZQ, 700, "CU-05 Consultar historial\nde mis reservas"),
    "login": (MED, 700, "CU-03 Iniciar sesión"),
    "verificar": (MED, 380, "CU-12 Verificar cupo y\nfecha de salida"),
    "calcular": (MED, 110, "CU-11 Calcular precio\ndel paquete"),
    "cancelar": (IZQ, 540, "CU-14 Cancelar reserva"),
    "modificar": (MED, 540, "CU-15 Modificar reserva"),
    "crear": (DER, 90, "CU-10 Crear paquete"),
    "publicar": (DER, 170, "CU-13 Publicar paquete"),
    "listar": (DER, 250, "CU-06 Listar destinos"),
    "regdest": (DER, 330, "CU-07 Registrar destino"),
    "moddest": (DER, 410, "CU-08 Modificar destino"),
    "bajadest": (DER, 490, "CU-09 Dar de baja destino"),
}
ACTORES = {"Cliente": (75, 380), "Administrador": (1075, 470)}
ASOCIACIONES = [("Cliente", c) for c in ("consultar", "registrarse", "reservar", "historial", "login", "cancelar", "modificar")] + [("Administrador", c) for c in ("crear", "publicar", "listar", "regdest", "moddest", "bajadest", "login")]
INCLUDES = [("reservar", "verificar"), ("reservar", "login"), ("historial", "login"), ("crear", "calcular"),
            ("modificar", "verificar"), ("cancelar", "login")]


def borde(caso, hacia):
    """Punto del borde de la elipse en dirección a otro punto."""
    x, y, _ = CASOS[caso]
    dx, dy = hacia[0] - x, hacia[1] - y
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    return x + dx * t, y + dy * t


def texto(x, y, t, size=12.5, peso="normal", color="#1F2933", anchor="middle"):
    lineas = t.split("\n")
    y0 = y - (len(lineas) - 1) * (size + 2) / 2
    return "".join(f'<text x="{x:.1f}" y="{y0 + i * (size + 2):.1f}" font-size="{size}" font-weight="{peso}" '
                   f'fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" font-family="{FONT}">'
                   f"{escape(l)}</text>" for i, l in enumerate(lineas))


def actor(x, y, nombre):
    return (f'<g stroke="#1F2933" stroke-width="2" fill="none">'
            f'<circle cx="{x}" cy="{y - 38}" r="12" fill="white"/>'
            f'<line x1="{x}" y1="{y - 26}" x2="{x}" y2="{y + 8}"/>'
            f'<line x1="{x - 20}" y1="{y - 14}" x2="{x + 20}" y2="{y - 14}"/>'
            f'<line x1="{x}" y1="{y + 8}" x2="{x - 16}" y2="{y + 34}"/>'
            f'<line x1="{x}" y1="{y + 8}" x2="{x + 16}" y2="{y + 34}"/></g>'
            + texto(x, y + 52, nombre, 13.5, "bold"))


def dibujar_asociaciones(o):
    for a, c in ASOCIACIONES:
        ax, ay = ACTORES[a]
        ax += 22 if a == "Cliente" else -22
        cx, cy, _ = CASOS[c]
        if a == "Cliente" and c == "login":   # caso compartido: entra por arriba para no tapar el «include»
            bx, by = borde(c, (ax, ay))
        else:
            bx, by = (cx - RX, cy) if a == "Cliente" else (cx + RX, cy)
        o.append(f'<line x1="{ax}" y1="{ay - 10}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#333" stroke-width="1.3"/>')


def dibujar_includes(o):
    for base, inc in INCLUDES:
        p1 = borde(base, CASOS[inc][:2])
        p2 = borde(inc, CASOS[base][:2])
        o.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#333" '
                 f'stroke-width="1.3" stroke-dasharray="6,4" marker-end="url(#abierta)"/>')
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        if abs(p1[1] - p2[1]) < 30:   # tramo casi horizontal: etiqueta bajo la línea
            o.append(texto(mx, my + 14, "«include»", 11, "normal", "#0B5394"))
        else:
            o.append(f'<rect x="{mx - 30}" y="{my - 9}" width="60" height="16" fill="#F7F9FC"/>')
            o.append(texto(mx, my - 1, "«include»", 11, "normal", "#0B5394"))


def dibujar_casos(o):
    for x, y, t in CASOS.values():
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" fill="white" stroke="#1F4E79" stroke-width="1.6"/>')
        o.append(texto(x, y, t, 12))


def dibujar_actores(o):
    for nombre, (x, y) in ACTORES.items():
        o.append(actor(x, y, nombre))


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><marker id="abierta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
         'orient="auto"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#333" stroke-width="1.4"/></marker></defs>',
         '<rect width="100%" height="100%" fill="white"/>',
         f'<rect x="190" y="20" width="790" height="{H - 40}" rx="6" fill="#F7F9FC" stroke="#333" stroke-width="1.6"/>',
         texto(585, 42, "Sistema de gestión Viajes Aventura", 14, "bold")]
    dibujar_asociaciones(o)
    dibujar_includes(o)
    dibujar_casos(o)
    dibujar_actores(o)
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    (Path(__file__).parent / "casos-de-uso.svg").write_text(svg(), encoding="utf-8")
    print("escrito casos-de-uso.svg")
