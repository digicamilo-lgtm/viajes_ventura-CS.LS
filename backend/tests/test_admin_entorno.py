"""La cuenta de administrador se crea desde variables de entorno al arrancar (despliegue)."""
from app.crear_administrador import crear_administrador_desde_entorno
from app.database import conectar, crear_esquema
from app.repositorios import AdministradorRepositorio


def test_crea_el_administrador_desde_el_entorno_sin_duplicarlo(tmp_path, monkeypatch):
    monkeypatch.setenv("VIAJES_DB", str(tmp_path / "prueba.db"))
    monkeypatch.setenv("ADMIN_CORREO", "demo@viajesaventura.cl")
    monkeypatch.setenv("ADMIN_CONTRASENA", "contrasena-de-demo-larga")
    conexion = conectar()
    crear_esquema(conexion)
    crear_administrador_desde_entorno(conexion)
    crear_administrador_desde_entorno(conexion)
    repo = AdministradorRepositorio(conexion)
    admin = repo.buscar_por_correo("demo@viajesaventura.cl")
    assert admin is not None
    assert admin.hash_contrasena != "contrasena-de-demo-larga"
    assert admin.verificar_contrasena("contrasena-de-demo-larga")
    conexion.close()


def test_sin_variables_no_crea_nada(tmp_path, monkeypatch):
    monkeypatch.setenv("VIAJES_DB", str(tmp_path / "prueba.db"))
    monkeypatch.delenv("ADMIN_CORREO", raising=False)
    monkeypatch.delenv("ADMIN_CONTRASENA", raising=False)
    conexion = conectar()
    crear_esquema(conexion)
    crear_administrador_desde_entorno(conexion)
    assert AdministradorRepositorio(conexion).listar() == []
    conexion.close()
