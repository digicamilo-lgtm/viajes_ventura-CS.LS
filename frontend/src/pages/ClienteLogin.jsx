import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'

export default function ClienteLogin() {
  const [correo, setCorreo] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)
  const { iniciarSesionCliente } = useAuth()
  const navegar = useNavigate()

  async function enviar(evento) {
    evento.preventDefault()
    setError('')
    setEnviando(true)
    try {
      await iniciarSesionCliente(correo, contrasena)
      navegar('/mis-reservas')
    } catch (e) {
      setError(e.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={enviar} className="formulario">
      <h2>Iniciar sesión</h2>
      <label>Correo
        <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} required />
      </label>
      <label>Contraseña
        <input type="password" value={contrasena} onChange={(e) => setContrasena(e.target.value)} required />
      </label>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={enviando}>{enviando ? 'Ingresando…' : 'Ingresar'}</button>
      <p>¿No tienes cuenta? <Link to="/registro">Regístrate</Link></p>
    </form>
  )
}
