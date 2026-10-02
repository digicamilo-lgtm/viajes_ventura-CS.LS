import { Link, Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './use-auth'
import AdminDestinos from './pages/AdminDestinos'
import AdminLogin from './pages/AdminLogin'
import AdminPaquetes from './pages/AdminPaquetes'
import Catalogo from './pages/Catalogo'
import ClienteLogin from './pages/ClienteLogin'
import ClienteRegistro from './pages/ClienteRegistro'
import MisReservas from './pages/MisReservas'
import PaqueteDetalle from './pages/PaqueteDetalle'

function RutaCliente({ children }) {
  const { sesion } = useAuth()
  return sesion?.rol === 'cliente' ? children : <Navigate to="/iniciar-sesion" replace />
}

function RutaAdmin({ children }) {
  const { sesion } = useAuth()
  return sesion?.rol === 'administrador' ? children : <Navigate to="/admin" replace />
}

export default function App() {
  const { sesion, cerrarSesion } = useAuth()

  return (
    <div className="app">
      <header>
        <h1><Link to="/">Viajes Aventura</Link></h1>
        <nav>
          <Link to="/">Catálogo</Link>
          {sesion?.rol === 'cliente' && <Link to="/mis-reservas">Mis reservas</Link>}
          {sesion?.rol === 'administrador' && <Link to="/admin/destinos">Destinos</Link>}
          {sesion?.rol === 'administrador' && <Link to="/admin/paquetes">Paquetes</Link>}
          {!sesion && <Link to="/iniciar-sesion">Iniciar sesión</Link>}
          {!sesion && <Link to="/admin" className="enlace-admin">Administrador</Link>}
          {sesion && (
            <span className="sesion-activa">
              {sesion.perfil.nombre} ({sesion.rol}) <button onClick={cerrarSesion}>Salir</button>
            </span>
          )}
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Catalogo />} />
          <Route path="/paquetes/:id" element={<PaqueteDetalle />} />
          <Route path="/registro" element={<ClienteRegistro />} />
          <Route path="/iniciar-sesion" element={<ClienteLogin />} />
          <Route path="/mis-reservas" element={<RutaCliente><MisReservas /></RutaCliente>} />
          <Route path="/admin" element={<AdminLogin />} />
          <Route path="/admin/destinos" element={<RutaAdmin><AdminDestinos /></RutaAdmin>} />
          <Route path="/admin/paquetes" element={<RutaAdmin><AdminPaquetes /></RutaAdmin>} />
        </Routes>
      </main>
    </div>
  )
}
