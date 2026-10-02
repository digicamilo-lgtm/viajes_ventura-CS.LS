import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../use-auth'

export default function MisReservas() {
  const { sesion } = useAuth()
  const [reservas, setReservas] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/reservas', sesion.token).then(setReservas).catch((e) => setError(e.message))
  }, [sesion.token])

  if (error) return <p className="error">{error}</p>
  if (reservas === null) return <p>Cargando…</p>

  return (
    <section>
      <h2>Mis reservas</h2>
      {reservas.length === 0 ? (
        <p>Todavía no tienes reservas. <a href="/">Explora el catálogo</a>.</p>
      ) : (
        <table>
          <thead>
            <tr><th>Fecha de emisión</th><th>Paquete</th><th>Personas</th><th>Total</th></tr>
          </thead>
          <tbody>
            {reservas.map((r) => (
              <tr key={r.id}>
                <td>{r.fecha_emision}</td>
                <td>#{r.paquete_id}</td>
                <td>{r.cantidad_personas}</td>
                <td>${r.total.toLocaleString('es-CL')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
