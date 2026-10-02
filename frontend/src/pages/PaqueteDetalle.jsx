import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'

export default function PaqueteDetalle() {
  const { id } = useParams()
  const { sesion } = useAuth()
  const [paquete, setPaquete] = useState(null)
  const [cantidad, setCantidad] = useState(1)
  const [mensaje, setMensaje] = useState('')
  const [error, setError] = useState('')
  const [reservando, setReservando] = useState(false)

  function cargar() {
    return api.get(`/paquetes/publicados/${id}`).then(setPaquete)
  }

  useEffect(() => { cargar().catch((e) => setError(e.message)) }, [id])

  async function reservar(evento) {
    evento.preventDefault()
    setError('')
    setMensaje('')
    setReservando(true)
    try {
      const reserva = await api.post(
        '/reservas', { paquete_id: Number(id), cantidad_personas: Number(cantidad) }, sesion.token)
      setMensaje(`Reserva confirmada: ${reserva.cantidad_personas} persona(s), ` +
                `total $${reserva.total.toLocaleString('es-CL')}.`)
      await cargar()
    } catch (e) {
      setError(e.message)
    } finally {
      setReservando(false)
    }
  }

  if (error && !paquete) return <p className="error">{error}</p>
  if (!paquete) return <p>Cargando…</p>

  return (
    <article>
      <h2>{paquete.nombre}</h2>
      <p>{paquete.destinos.map((d) => `${d.nombre} (${d.zona})`).join(' · ')}</p>
      <p>Salida: {paquete.fecha_salida} — Regreso: {paquete.fecha_regreso}</p>
      <p className="precio">${paquete.precio_por_persona.toLocaleString('es-CL')} por persona</p>
      <p>Cupo disponible: {paquete.cupo_disponible} de {paquete.cupo_maximo}</p>

      {!sesion || sesion.rol !== 'cliente' ? (
        <p>Para reservar, <Link to="/iniciar-sesion">inicia sesión como cliente</Link>.</p>
      ) : (
        <form onSubmit={reservar} className="formulario">
          <label>
            Personas
            <input type="number" min="1" max={Math.max(paquete.cupo_disponible, 1)} value={cantidad}
                  onChange={(e) => setCantidad(e.target.value)} required />
          </label>
          <button type="submit" disabled={reservando || paquete.cupo_disponible < 1}>
            {reservando ? 'Reservando…' : 'Reservar'}
          </button>
        </form>
      )}
      {mensaje && <p className="exito">{mensaje}</p>}
      {error && <p className="error">{error}</p>}
    </article>
  )
}
