import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'

const VACIO = { nombre: '', fecha_salida: '', fecha_regreso: '', cupo_maximo: 1, margen: 0.2, destino_ids: [] }

export default function AdminPaquetes() {
  const { sesion } = useAuth()
  const [paquetes, setPaquetes] = useState(null)
  const [destinos, setDestinos] = useState([])
  const [nuevo, setNuevo] = useState(VACIO)
  const [error, setError] = useState('')

  async function cargar() {
    const [listaPaquetes, listaDestinos] = await Promise.all([
      api.get('/paquetes', sesion.token),
      api.get('/destinos?solo_disponibles=true', sesion.token),
    ])
    setPaquetes(listaPaquetes)
    setDestinos(listaDestinos)
  }

  useEffect(() => { cargar().catch((e) => setError(e.message)) }, [])

  function cambiar(campo) {
    return (evento) => setNuevo((d) => ({ ...d, [campo]: evento.target.value }))
  }

  function alternarDestino(id) {
    setNuevo((d) => ({
      ...d,
      destino_ids: d.destino_ids.includes(id)
        ? d.destino_ids.filter((x) => x !== id)
        : [...d.destino_ids, id],
    }))
  }

  async function crear(evento) {
    evento.preventDefault()
    setError('')
    try {
      await api.post('/paquetes', {
        ...nuevo,
        cupo_maximo: Number(nuevo.cupo_maximo),
        margen: Number(nuevo.margen),
      }, sesion.token)                                 // FR-05, FR-06
      setNuevo(VACIO)
      await cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  async function publicar(id) {
    setError('')
    try {
      await api.post(`/paquetes/${id}/publicar`, undefined, sesion.token)   // FR-07
      await cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  async function eliminar(id) {
    setError('')
    try {
      await api.del(`/paquetes/${id}`, sesion.token)
      await cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  if (paquetes === null) return <p>Cargando…</p>

  return (
    <section>
      <h2>Paquetes</h2>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr><th>Nombre</th><th>Estado</th><th>Precio</th><th>Cupo</th><th></th></tr>
        </thead>
        <tbody>
          {paquetes.map((p) => (
            <tr key={p.id}>
              <td>{p.nombre}</td>
              <td>{p.estado}</td>
              <td>${p.precio_por_persona.toLocaleString('es-CL')}</td>
              <td>{p.cupo_disponible}/{p.cupo_maximo}</td>
              <td>
                {p.estado === 'BORRADOR' && (
                  <>
                    <button onClick={() => publicar(p.id)}>Publicar</button>{' '}
                    <button onClick={() => eliminar(p.id)}>Eliminar</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Nuevo paquete</h3>
      <form onSubmit={crear} className="formulario">
        <label>Nombre <input value={nuevo.nombre} onChange={cambiar('nombre')} required /></label>
        <label>Fecha de salida
          <input type="date" value={nuevo.fecha_salida} onChange={cambiar('fecha_salida')} required />
        </label>
        <label>Fecha de regreso
          <input type="date" value={nuevo.fecha_regreso} onChange={cambiar('fecha_regreso')} required />
        </label>
        <label>Cupo máximo
          <input type="number" min="1" value={nuevo.cupo_maximo} onChange={cambiar('cupo_maximo')} required />
        </label>
        <label>Margen (ej. 0.20 = 20 %)
          <input type="number" min="0" step="0.01" value={nuevo.margen} onChange={cambiar('margen')} required />
        </label>
        <fieldset>
          <legend>Destinos disponibles (combina entre 2 y 5)</legend>
          {destinos.length === 0 && <p className="ayuda">No hay destinos disponibles; crea alguno primero.</p>}
          {destinos.map((d) => (
            <label key={d.id} className="casilla">
              <input type="checkbox" checked={nuevo.destino_ids.includes(d.id)}
                    onChange={() => alternarDestino(d.id)} />
              {d.nombre} (${d.costo_base.toLocaleString('es-CL')})
            </label>
          ))}
        </fieldset>
        <button type="submit">Crear paquete</button>
      </form>
    </section>
  )
}
