import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'

const VACIO = { nombre: '', zona: '', descripcion: '', duracion_dias: 1, costo_base: 0 }

export default function AdminDestinos() {
  const { sesion } = useAuth()
  const [destinos, setDestinos] = useState(null)
  const [nuevo, setNuevo] = useState(VACIO)
  const [error, setError] = useState('')

  function cargar() {
    return api.get('/destinos', sesion.token).then(setDestinos)
  }

  useEffect(() => { cargar().catch((e) => setError(e.message)) }, [])

  function cambiar(campo) {
    return (evento) => setNuevo((d) => ({ ...d, [campo]: evento.target.value }))
  }

  async function crear(evento) {
    evento.preventDefault()
    setError('')
    try {
      await api.post('/destinos', {
        ...nuevo,
        duracion_dias: Number(nuevo.duracion_dias),
        costo_base: Number(nuevo.costo_base),
      }, sesion.token)                                // FR-01
      setNuevo(VACIO)
      await cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  async function darDeBaja(id) {
    setError('')
    try {
      await api.del(`/destinos/${id}`, sesion.token)   // FR-03
      await cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  if (destinos === null) return <p>Cargando…</p>

  return (
    <section>
      <h2>Destinos</h2>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr><th>Nombre</th><th>Zona</th><th>Días</th><th>Costo base</th><th>Disponible</th><th></th></tr>
        </thead>
        <tbody>
          {destinos.map((d) => (
            <tr key={d.id}>
              <td>{d.nombre}</td>
              <td>{d.zona}</td>
              <td>{d.duracion_dias}</td>
              <td>${d.costo_base.toLocaleString('es-CL')}</td>
              <td>{d.disponible ? 'Sí' : 'No'}</td>
              <td>{d.disponible && <button onClick={() => darDeBaja(d.id)}>Dar de baja</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Nuevo destino</h3>
      <form onSubmit={crear} className="formulario">
        <label>Nombre <input value={nuevo.nombre} onChange={cambiar('nombre')} required /></label>
        <label>Zona <input value={nuevo.zona} onChange={cambiar('zona')} required /></label>
        <label>Descripción <input value={nuevo.descripcion} onChange={cambiar('descripcion')} /></label>
        <label>Duración (días)
          <input type="number" min="1" value={nuevo.duracion_dias} onChange={cambiar('duracion_dias')} required />
        </label>
        <label>Costo base
          <input type="number" min="1" value={nuevo.costo_base} onChange={cambiar('costo_base')} required />
        </label>
        <button type="submit">Registrar destino</button>
      </form>
    </section>
  )
}
