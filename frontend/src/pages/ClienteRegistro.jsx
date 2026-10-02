import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'

const VACIO = { nombre: '', rut: '', correo: '', telefono: '', contrasena: '' }

export default function ClienteRegistro() {
  const [datos, setDatos] = useState(VACIO)
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)
  const { iniciarSesionCliente } = useAuth()
  const navegar = useNavigate()

  function cambiar(campo) {
    return (evento) => setDatos((d) => ({ ...d, [campo]: evento.target.value }))
  }

  async function enviar(evento) {
    evento.preventDefault()
    setError('')
    setEnviando(true)
    try {
      await api.post('/clientes', datos)             // FR-09
      await iniciarSesionCliente(datos.correo, datos.contrasena)   // FR-10
      navegar('/mis-reservas')
    } catch (e) {
      setError(e.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={enviar} className="formulario">
      <h2>Crear cuenta</h2>
      <label>Nombre
        <input value={datos.nombre} onChange={cambiar('nombre')} required />
      </label>
      <label>RUT
        <input value={datos.rut} onChange={cambiar('rut')} placeholder="12345678-9" required />
      </label>
      <label>Correo
        <input type="email" value={datos.correo} onChange={cambiar('correo')} required />
      </label>
      <label>Teléfono
        <input value={datos.telefono} onChange={cambiar('telefono')} required />
      </label>
      <label>Contraseña
        <input type="password" value={datos.contrasena} onChange={cambiar('contrasena')} minLength={8} required />
      </label>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={enviando}>{enviando ? 'Creando…' : 'Registrarme'}</button>
    </form>
  )
}
