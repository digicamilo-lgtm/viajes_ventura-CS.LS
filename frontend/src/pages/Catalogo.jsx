import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

export default function Catalogo() {
  const [paquetes, setPaquetes] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/paquetes/publicados').then(setPaquetes).catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="error">{error}</p>
  if (paquetes === null) return <p>Cargando catálogo…</p>
  if (paquetes.length === 0) return <p>No hay paquetes publicados por ahora.</p>

  return (
    <section>
      <h2>Paquetes disponibles</h2>
      <ul className="tarjetas">
        {paquetes.map((p) => (
          <li key={p.id} className="tarjeta">
            <h3>{p.nombre}</h3>
            <p>{p.destinos.map((d) => d.nombre).join(' · ')}</p>
            <p>{p.fecha_salida} → {p.fecha_regreso}</p>
            <p className="precio">${p.precio_por_persona.toLocaleString('es-CL')} por persona</p>
            <p>Cupo disponible: {p.cupo_disponible}</p>
            <Link to={`/paquetes/${p.id}`}>Ver detalle</Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
