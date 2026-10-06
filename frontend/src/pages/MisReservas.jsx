import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../use-auth'

export default function MisReservas() {
  const { sesion } = useAuth()
  const [reservas, setReservas] = useState(null)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')
  const [edicion, setEdicion] = useState(null)

  function cargar() {
    api.get('/reservas', sesion.token).then(setReservas).catch((e) => setError(e.message))
  }

  useEffect(cargar, [sesion.token])

  async function cancelar(reserva) {
    if (!window.confirm('¿Cancelar esta reserva? Se libera su cupo.')) return
    try {
      await api.del(`/reservas/${reserva.id}`, sesion.token)
      setMensaje('Reserva cancelada.')
      cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  async function guardarModificacion(reserva) {
    try {
      await api.put(`/reservas/${reserva.id}`, { cantidad_personas: edicion.cantidad }, sesion.token)
      setEdicion(null)
      setMensaje('Reserva modificada: la anterior queda cancelada y se creó una nueva al precio vigente.')
      cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  if (error) return <p className="error">{error}</p>
  if (reservas === null) return <p>Cargando…</p>

  return (
    <section>
      <h2>Mis reservas</h2>
      {mensaje && <p>{mensaje}</p>}
      {reservas.length === 0 ? (
        <p>Todavía no tienes reservas. <a href="/">Explora el catálogo</a>.</p>
      ) : (
        <table>
          <thead>
            <tr><th>Fecha de emisión</th><th>Paquete</th><th>Personas</th><th>Total</th><th>Estado</th><th></th></tr>
          </thead>
          <tbody>
            {reservas.map((r) => (
              <tr key={r.id}>
                <td>{r.fecha_emision}</td>
                <td>#{r.paquete_id}</td>
                <td>
                  {edicion?.id === r.id ? (
                    <input type="number" min="1" value={edicion.cantidad}
                      onChange={(e) => setEdicion({ id: r.id, cantidad: Number(e.target.value) })} />
                  ) : (
                    r.cantidad_personas
                  )}
                </td>
                <td>${r.total.toLocaleString('es-CL')}</td>
                <td>{r.cancelada ? 'Cancelada' : 'Vigente'}</td>
                <td>
                  {!r.cancelada && edicion?.id === r.id && (
                    <>
                      <button type="button" onClick={() => guardarModificacion(r)}>Guardar</button>{' '}
                      <button type="button" onClick={() => setEdicion(null)}>Volver</button>
                    </>
                  )}
                  {!r.cancelada && edicion?.id !== r.id && (
                    <>
                      <button type="button" onClick={() => setEdicion({ id: r.id, cantidad: r.cantidad_personas })}>
                        Modificar
                      </button>{' '}
                      <button type="button" onClick={() => cancelar(r)}>Cancelar</button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
