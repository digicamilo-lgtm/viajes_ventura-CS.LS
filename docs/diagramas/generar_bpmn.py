"""Genera los diagramas BPMN 2.0 del Informe Técnico como SVG.

Cada proceso se define como datos (carriles, nodos en una grilla y flujos);
este script dibuja la notación BPMN (pool, lanes, eventos, tareas,
compuertas exclusivas, almacén de datos) y enruta los flujos de forma
ortogonal. Uso:  py generar_bpmn.py   -> escribe bpmn-*.svg en esta carpeta.
"""
from pathlib import Path
from xml.sax.saxutils import escape

CW, RH = 175, 104          # ancho de columna y alto de fila de la grilla
TW, TH = 146, 72          # tamaño de una tarea
POOL_BAND, LANE_BAND = 34, 34
PAD = 14
FONT = "Arial, Helvetica, sans-serif"


class Proceso:
    def __init__(self, pool, lanes, cols):
        self.pool, self.lanes, self.cols = pool, lanes, cols  # lanes: [(nombre, filas)]
        self.nodos, self.flujos = {}, []
        self.lane_y, y = {}, PAD
        for nombre, filas in lanes:
            self.lane_y[nombre] = (y, filas)
            y += filas * RH
        self.alto = y + PAD
        self.x0 = PAD + POOL_BAND + LANE_BAND
        self.ancho = self.x0 + cols * CW + PAD

    def centro(self, lane, fila, col):
        y, _ = self.lane_y[lane]
        return self.x0 + col * CW + CW / 2, y + fila * RH + RH / 2

    def nodo(self, id, tipo, lane, fila, col, texto="", pos="arriba"):
        cx, cy = self.centro(lane, fila, col)
        self.nodos[id] = dict(tipo=tipo, cx=cx, cy=cy, texto=texto, pos=pos)

    def flujo(self, a, b, ps="r", pt="l", etiqueta="", via=None, asociacion=False):
        self.flujos.append(dict(a=a, b=b, ps=ps, pt=pt, et=etiqueta, via=via, asoc=asociacion))

    # --- geometría -------------------------------------------------------
    def medio(self, n):
        return {"start": (18, 18), "end": (18, 18), "gw": (26, 26),
                "store": (26, 22)}.get(n["tipo"], (TW / 2, TH / 2))

    def puerto(self, id, p):
        n = self.nodos[id]
        hw, hh = self.medio(n)
        return {"r": (n["cx"] + hw, n["cy"]), "l": (n["cx"] - hw, n["cy"]),
                "t": (n["cx"], n["cy"] - hh), "b": (n["cx"], n["cy"] + hh)}[p]

    def ruta(self, f):
        (sx, sy), (tx, ty) = self.puerto(f["a"], f["ps"]), self.puerto(f["b"], f["pt"])
        if f["via"]:
            return [(sx, sy), *f["via"], (tx, ty)]
        hs, ht = f["ps"] in "rl", f["pt"] in "rl"
        if abs(sy - ty) < 1 and hs and ht or abs(sx - tx) < 1 and not hs and not ht:
            return [(sx, sy), (tx, ty)]
        if hs and ht:
            if f["ps"] == "r" and f["pt"] == "l" and tx > sx:
                mx = (sx + tx) / 2
            else:
                mx = max(sx, tx) + 28 if f["ps"] == "r" else min(sx, tx) - 28
            return [(sx, sy), (mx, sy), (mx, ty), (tx, ty)]
        if not hs and not ht:
            if f["ps"] == "b" and f["pt"] == "t" and ty > sy or f["ps"] == "t" and f["pt"] == "b" and ty < sy:
                my = (sy + ty) / 2
            else:
                my = max(sy, ty) + 24 if f["ps"] == "b" else min(sy, ty) - 24
            return [(sx, sy), (sx, my), (tx, my), (tx, ty)]
        return [(sx, sy), (tx, sy), (tx, ty)] if hs else [(sx, sy), (sx, ty), (tx, ty)]

    # --- dibujo ----------------------------------------------------------
    def texto(self, x, y, lineas, size=12.5, peso="normal", color="#1F2933", anchor="middle"):
        lineas = lineas.split("\n")
        y0 = y - (len(lineas) - 1) * (size + 2) / 2
        return "".join(
            f'<text x="{x:.1f}" y="{y0 + i * (size + 2):.1f}" font-size="{size}" font-weight="{peso}" '
            f'fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" font-family="{FONT}">'
            f"{escape(l)}</text>" for i, l in enumerate(lineas))

    def svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.ancho}" height="{self.alto}" '
             f'viewBox="0 0 {self.ancho} {self.alto}">',
             '<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
             'markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker>'
             '<marker id="abierta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
             'orient="auto"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#666"/></marker></defs>',
             f'<rect width="100%" height="100%" fill="white"/>']
        x1, y1, x2, y2 = PAD, PAD, self.ancho - PAD, self.alto - PAD
        o.append(f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" fill="white" stroke="#333" stroke-width="1.6"/>')
        o.append(f'<line x1="{x1 + POOL_BAND}" y1="{y1}" x2="{x1 + POOL_BAND}" y2="{y2}" stroke="#333" stroke-width="1.6"/>')
        cy = (y1 + y2) / 2
        o.append(f'<g transform="translate({x1 + POOL_BAND / 2},{cy}) rotate(-90)">{self.texto(0, 0, self.pool, 14, "bold")}</g>')
        colores = ["#F4F8FC", "#FBF7F0", "#F3F8F3"]
        for i, (nombre, filas) in enumerate(self.lanes):
            ly, _ = self.lane_y[nombre]
            h = filas * RH
            lx = x1 + POOL_BAND
            o.append(f'<rect x="{lx}" y="{ly}" width="{x2 - lx}" height="{h}" fill="{colores[i % 3]}" stroke="#333" stroke-width="1"/>')
            o.append(f'<line x1="{lx + LANE_BAND}" y1="{ly}" x2="{lx + LANE_BAND}" y2="{ly + h}" stroke="#333"/>')
            o.append(f'<g transform="translate({lx + LANE_BAND / 2},{ly + h / 2}) rotate(-90)">{self.texto(0, 0, nombre, 13.5, "bold")}</g>')
        for f in self.flujos:
            pts = self.ruta(f)
            d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            if f["asoc"]:
                o.append(f'<polyline points="{d}" fill="none" stroke="#666" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#abierta)"/>')
            else:
                o.append(f'<polyline points="{d}" fill="none" stroke="#333" stroke-width="1.4" marker-end="url(#flecha)"/>')
            if f["et"]:
                (ax, ay), (bx, by) = pts[0], pts[1]
                if abs(ay - by) < 1:   # primer tramo horizontal
                    lx, ly, anc = ax + (8 if bx > ax else -8), ay - 9, "start" if bx > ax else "end"
                else:
                    lx, ly, anc = ax + 6, ay + (12 if by > ay else -12), "start"
                o.append(self.texto(lx, ly, f["et"], 11.5, "bold", "#0B5394", anc))
        for n in self.nodos.values():
            x, y, t = n["cx"], n["cy"], n["texto"]
            if n["tipo"] == "task":
                o.append(f'<rect x="{x - TW / 2}" y="{y - TH / 2}" width="{TW}" height="{TH}" rx="10" fill="white" stroke="#1F4E79" stroke-width="1.6"/>')
                o.append(self.texto(x, y, t, 12))
            elif n["tipo"] in ("start", "end"):
                ancho, color = (1.8, "#2E7D32") if n["tipo"] == "start" else (4, "#B71C1C")
                o.append(f'<circle cx="{x}" cy="{y}" r="17" fill="white" stroke="{color}" stroke-width="{ancho}"/>')
                if t:
                    o.append(self.texto(x, y + 32, t, 11, "normal", "#333"))
            elif n["tipo"] == "gw":
                o.append(f'<polygon points="{x},{y - 26} {x + 26},{y} {x},{y + 26} {x - 26},{y}" fill="#FFF8E1" stroke="#9A7B00" stroke-width="1.6"/>')
                o.append(f'<path d="M{x - 8},{y - 8} L{x + 8},{y + 8} M{x + 8},{y - 8} L{x - 8},{y + 8}" stroke="#333" stroke-width="2.6"/>')
                if t:
                    lx, ly, anc = {"arriba": (x, y - 42, "middle"), "izq": (x - 32, y, "end"),
                                   "noroeste": (x - 22, y - 36, "end")}[n["pos"]]
                    o.append(self.texto(lx, ly, t, 11.5, "bold", "#5C4A00", anc))
            elif n["tipo"] == "store":
                o.append(f'<path d="M{x - 24},{y - 14} v30 a24,7 0 0 0 48,0 v-30" fill="white" stroke="#333" stroke-width="1.4"/>')
                o.append(f'<ellipse cx="{x}" cy="{y - 14}" rx="24" ry="7" fill="white" stroke="#333" stroke-width="1.4"/>')
                o.append(self.texto(x, y + 36, t, 11, "normal", "#333"))
        o.append("</svg>")
        return "".join(o)


# ======================================================================
# BPMN 1 — Gestión del catálogo de destinos (FR-01 a FR-04)
# ======================================================================
def bpmn_destinos():
    A, S = "Administrador", "Sistema"
    p = Proceso("Viajes Aventura", [(A, 3), (S, 4)], 9)
    p.nodo("ini", "start", A, 1, 0, "Necesita actualizar\nel catálogo")
    p.nodo("login", "task", A, 1, 1, "Iniciar sesión\ncomo administrador")
    p.nodo("listar", "task", S, 0, 2, "Listar catálogo:\ndisponibles y\nno disponibles [FR-04]")
    p.nodo("op", "gw", A, 1, 3, "¿Operación?", "noroeste")
    p.nodo("ingresar", "task", A, 0, 4, "Ingresar nombre, zona,\ndescripción, duración\ny costo base [FR-01]")
    p.nodo("editar", "task", A, 1, 4, "Editar datos del\ndestino [FR-02]")
    p.nodo("selec", "task", A, 2, 4, "Seleccionar destino\na dar de baja [FR-03]")
    p.nodo("corregir", "task", A, 2, 6, "Corregir datos")
    p.nodo("validar", "task", S, 0, 5, "Validar: nombre único,\ncosto base > 0,\nduración > 0 (R1, R2)")
    p.nodo("ok", "gw", S, 0, 6, "¿Datos válidos?")
    p.nodo("guardar", "task", S, 0, 7, "Guardar destino\n[FR-01 / FR-02]")
    p.nodo("fin1", "end", S, 0, 8, "Destino\nguardado")
    p.nodo("error", "task", S, 1, 6, "Informar campo inválido\n(sin exponer datos)")
    p.nodo("bd", "store", S, 1, 7, "Base de datos")
    p.nodo("parte", "gw", S, 2, 4, "¿Pertenece a algún\npaquete? (R8)", "izq")
    p.nodo("marcar", "task", S, 2, 5, "Marcar destino\nno disponible [FR-03]")
    p.nodo("fin2", "end", S, 2, 6, "Destino\nno disponible")
    p.nodo("eliminar", "task", S, 3, 4, "Eliminar destino\ndel catálogo [FR-03]")
    p.nodo("fin3", "end", S, 3, 5, "Destino\neliminado")
    p.flujo("ini", "login")
    p.flujo("login", "listar", "r", "t")
    p.flujo("listar", "op", "r", "l")
    p.flujo("op", "ingresar", "t", "l", "Registrar")
    p.flujo("op", "editar", "r", "l", "Modificar")
    p.flujo("op", "selec", "b", "l", "Dar de baja")
    p.flujo("ingresar", "validar", "r", "t")
    p.flujo("editar", "validar", "r", "t")
    p.flujo("corregir", "validar", "l", "t")
    p.flujo("validar", "ok")
    p.flujo("ok", "guardar", "r", "l", "Sí")
    p.flujo("guardar", "fin1")
    p.flujo("ok", "error", "b", "t", "No")
    p.flujo("error", "corregir", "r", "r")
    p.flujo("guardar", "bd", "b", "t", asociacion=True)
    p.flujo("selec", "parte", "b", "t")
    p.flujo("parte", "marcar", "r", "l", "Sí")
    p.flujo("marcar", "fin2")
    p.flujo("parte", "eliminar", "b", "t", "No")
    p.flujo("eliminar", "fin3")
    return p


# ======================================================================
# BPMN 2 — Armado y publicación de un paquete (FR-05 a FR-07)
# ======================================================================
def bpmn_paquetes():
    A, S = "Administrador", "Sistema"
    p = Proceso("Viajes Aventura", [(A, 2), (S, 2)], 9)
    p.nodo("ini", "start", A, 0, 0, "Nueva temporada\no paquete")
    p.nodo("datos", "task", A, 0, 1, "Ingresar nombre,\nfechas, cupo y\nmargen [FR-05]")
    p.nodo("disp", "task", S, 0, 2, "Ofrecer solo destinos\ndisponibles (R8)")
    p.nodo("selec", "task", A, 0, 3, "Seleccionar\n2 a 5 destinos\n[FR-05]")
    p.nodo("validar", "task", S, 0, 4, "Validar: 2–5 destinos\nsin repetir, regreso >\nsalida, cupo > 0,\nmargen ≥ 0 (R3, R5, R6)")
    p.nodo("ok", "gw", S, 0, 5, "¿Válido?")
    p.nodo("error", "task", S, 1, 5, "Informar regla\nincumplida")
    p.nodo("calc", "task", S, 0, 6, "Calcular precio =\nΣ costos base ×\n(1 + margen) [FR-06]")
    p.nodo("revisar", "task", A, 0, 6, "Revisar precio\ncalculado")
    p.nodo("pub", "gw", A, 0, 7, "¿Publicar?")
    p.nodo("borr", "end", A, 1, 7, "Queda en\nborrador")
    p.nodo("fijar", "task", S, 0, 8, "Publicar: fijar precio\ny estado PUBLICADO\n[FR-07]")
    p.nodo("fin", "end", S, 1, 8, "Paquete\npublicado")
    p.nodo("bd", "store", S, 1, 7, "Base de datos")
    p.flujo("ini", "datos")
    p.flujo("datos", "disp", "r", "t")
    p.flujo("disp", "selec", "r", "b")
    p.flujo("selec", "validar", "r", "t")
    p.flujo("validar", "ok")
    p.flujo("ok", "calc", "r", "l", "Sí")
    p.flujo("ok", "error", "b", "t", "No")
    p.flujo("error", "datos", "l", "b", via=[(p.nodos["datos"]["cx"], p.nodos["error"]["cy"])])
    p.flujo("calc", "revisar", "t", "b")
    p.flujo("revisar", "pub")
    p.flujo("pub", "fijar", "r", "t", "Sí")
    p.flujo("pub", "borr", "b", "t", "No")
    p.flujo("fijar", "fin", "b", "t")
    p.flujo("fijar", "bd", "l", "t", asociacion=True)
    return p


# ======================================================================
# BPMN 3 — Reserva de un paquete (FR-08 a FR-15)
# ======================================================================
def bpmn_reservas():
    C, S = "Cliente", "Sistema"
    p = Proceso("Viajes Aventura", [(C, 3), (S, 3)], 11)
    p.nodo("ini", "start", C, 0, 0, "Quiere viajar")
    p.nodo("ver", "task", S, 0, 1, "Mostrar paquetes\npublicados con precio\ny cupo disponible\n[FR-08]")
    p.nodo("elige", "task", C, 0, 2, "Seleccionar paquete")
    p.nodo("aut", "gw", C, 0, 3, "¿Autenticado?")
    p.nodo("cuenta", "gw", C, 1, 3, "¿Tiene cuenta?", "izq")
    p.nodo("reg", "task", C, 2, 3, "Registrarse: nombre,\nRUT, correo, teléfono,\ncontraseña [FR-09]")
    p.nodo("guardaC", "task", S, 0, 3, "Validar datos, correo\núnico y guardar\ncontraseña como hash\n[RNF-01]")
    p.nodo("login", "task", C, 1, 4, "Iniciar sesión con\ncorreo y contraseña\n[FR-10]")
    p.nodo("cred", "gw", S, 0, 5, "¿Credenciales\ncorrectas?", "izq")
    p.nodo("errC", "task", S, 1, 5, "Mensaje genérico\n(no indica qué\ncampo falló)")
    p.nodo("pers", "task", C, 0, 6, "Indicar cantidad\nde personas")
    p.nodo("fecha", "gw", S, 0, 7, "¿Salida ya\npasó? (R15)", "izq")
    p.nodo("rechF", "task", S, 1, 7, "Rechazar reserva:\npaquete vencido\n[FR-14]")
    p.nodo("cupo", "gw", S, 0, 8, "¿1 ≤ personas ≤ cupo?")
    p.nodo("rechC", "task", S, 1, 8, "Rechazar reserva:\ncupo insuficiente\n[FR-13]")
    p.nodo("finR", "end", S, 2, 8, "Reserva\nrechazada")
    p.nodo("reservar", "task", S, 0, 9, "Registrar reserva:\ntotal = precio × personas\ny fecha de emisión\n[FR-11, FR-12]")
    p.nodo("bd", "store", S, 1, 10, "Base de datos")
    p.nodo("hist", "task", C, 0, 9, "Consultar historial\nde mis reservas\n[FR-15]")
    p.nodo("fin", "end", C, 0, 10, "Reserva\nregistrada")
    p.flujo("ini", "ver", "r", "t")
    p.flujo("ver", "elige", "r", "b")
    p.flujo("elige", "aut")
    p.flujo("aut", "pers", "r", "l", "Sí")
    p.flujo("aut", "cuenta", "b", "t", "No")
    p.flujo("cuenta", "login", "r", "l", "Sí")
    p.flujo("cuenta", "reg", "b", "t", "No")
    p.flujo("reg", "guardaC", "b", "t")
    p.flujo("guardaC", "login", "r", "b")
    p.flujo("login", "cred", "r", "t")
    p.flujo("cred", "pers", "r", "b", "Sí")
    p.flujo("cred", "errC", "b", "t", "No")
    p.flujo("errC", "login", "l", "b")
    p.flujo("pers", "fecha", "r", "t")
    p.flujo("fecha", "rechF", "b", "t", "Sí")
    p.flujo("fecha", "cupo", "r", "l", "No")
    p.flujo("cupo", "rechC", "b", "t", "No")
    p.flujo("cupo", "reservar", "r", "l", "Sí")
    p.flujo("rechF", "finR", "b", "l")
    p.flujo("rechC", "finR", "b", "t")
    p.flujo("reservar", "hist", "t", "b")
    p.flujo("hist", "fin")
    p.flujo("reservar", "bd", "r", "t", asociacion=True)
    return p


if __name__ == "__main__":
    aqui = Path(__file__).parent
    for nombre, fn in [("bpmn-1-gestion-destinos", bpmn_destinos),
                       ("bpmn-2-publicar-paquete", bpmn_paquetes),
                       ("bpmn-3-reservar-paquete", bpmn_reservas)]:
        (aqui / f"{nombre}.svg").write_text(fn().svg(), encoding="utf-8")
        print("escrito", nombre + ".svg")
