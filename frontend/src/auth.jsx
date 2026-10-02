import { useCallback, useMemo, useState } from 'react'
import { api } from './api'
import { AuthContext } from './auth-context'

// Una sola sesión a la vez, de cliente o de administrador (R11, sección 7.1).
// El backend ya incluye el rol en el token (app/seguridad/tokens.py); aquí solo
// se recuerda para mostrar la pantalla correcta, nunca para decidir permisos.
const CLAVE = 'viajes-aventura-sesion'
function cargarSesion() {
  try {
    const guardada = localStorage.getItem(CLAVE)
    return guardada ? JSON.parse(guardada) : null
  } catch {
    return null               // almacenamiento no disponible (ej. navegación privada)
  }
}

function guardarSesion(sesion) {
  try {
    if (sesion) localStorage.setItem(CLAVE, JSON.stringify(sesion))
    else localStorage.removeItem(CLAVE)
  } catch {
    // la sesión sigue funcionando en memoria aunque no se pueda persistir
  }
}

export function AuthProvider({ children }) {
  const [sesion, setSesion] = useState(cargarSesion)

  const establecer = useCallback((nueva) => {
    guardarSesion(nueva)
    setSesion(nueva)
  }, [])

  const iniciarSesionCliente = useCallback(async (correo, contrasena) => {
    const { token } = await api.post('/clientes/sesiones', { correo, contrasena })
    const perfil = await api.get('/clientes/yo', token)
    establecer({ token, rol: 'cliente', perfil })
  }, [establecer])

  const iniciarSesionAdmin = useCallback(async (correo, contrasena) => {
    const { token } = await api.post('/administradores/sesiones', { correo, contrasena })
    const perfil = await api.get('/administradores/yo', token)
    establecer({ token, rol: 'administrador', perfil })
  }, [establecer])

  const cerrarSesion = useCallback(() => establecer(null), [establecer])
  const valor = useMemo(() => ({ sesion, iniciarSesionCliente, iniciarSesionAdmin, cerrarSesion }),
    [sesion, iniciarSesionCliente, iniciarSesionAdmin, cerrarSesion])

  return (
    <AuthContext.Provider value={valor}>
      {children}
    </AuthContext.Provider>
  )
}

