// Cliente de la API REST/JSON del backend (sección 5.1 del Informe Técnico).
const BASE = '/api'

export class ApiError extends Error {
  constructor(status, detail, errores) {
    super(detail)
    this.status = status
    this.errores = errores
  }
}

async function solicitud(ruta, { metodo = 'GET', cuerpo, token } = {}) {
  const encabezados = {}
  if (cuerpo !== undefined) encabezados['Content-Type'] = 'application/json'
  if (token) encabezados['Authorization'] = `Bearer ${token}`

  const respuesta = await fetch(`${BASE}${ruta}`, {
    method: metodo,
    headers: encabezados,
    body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
  })

  if (respuesta.status === 204) return null

  const datos = await respuesta.json().catch(() => null)
  if (!respuesta.ok) {
    throw new ApiError(respuesta.status, datos?.detail ?? 'Error inesperado.', datos?.errores)
  }
  return datos
}

export const api = {
  get: (ruta, token) => solicitud(ruta, { token }),
  post: (ruta, cuerpo, token) => solicitud(ruta, { metodo: 'POST', cuerpo, token }),
  put: (ruta, cuerpo, token) => solicitud(ruta, { metodo: 'PUT', cuerpo, token }),
  del: (ruta, token) => solicitud(ruta, { metodo: 'DELETE', token }),
}
