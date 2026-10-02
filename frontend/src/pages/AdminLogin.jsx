import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'

export default function AdminLogin() {
  const [correo, setCorreo] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)
  const { iniciarSesionAdmin } = useAuth()
  const navegar = useNavigate()

  async function enviar(evento) {
    evento.preventDefault()
    setError('')
    setEnviando(true)
    try {
      await iniciarSesionAdmin(correo, contrasena)
      navegar('/admin/destinos')
    } catch (e) {
      setError(e.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={enviar} className="formulario">
      <h2>Acceso de administrador</h2>
      <p className="ayuda">Cuenta creada desde la consola (<code>python -m app.crear_administrador</code>); no hay registro público (S1).</p>
      <label>Correo
        <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} required />
      </label>
      <label>Contraseña
        <input type="password" value={contrasena} onChange={(e) => setContrasena(e.target.value)} required />
      </label>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={enviando}>{enviando ? 'Ingresando…' : 'Ingresar'}</button>
    </form>
  )
}
