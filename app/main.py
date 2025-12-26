from app.data.db_connection import DBConnection
from app.data.tenedor_repository import TenedorRepository
from app.services.tenedor_service import TenedorService


def main():
    # 1) Ruta a la base de datos
    # Como main.py está dentro de /app, subimos un nivel para llegar a /db
    db_path = "../db/veterinaria.db"

    # 2) Armamos la cadena: DB -> Repository -> Service
    db = DBConnection(db_path)
    repo = TenedorRepository(db)
    service = TenedorService(repo)

    # 3) Datos de prueba (hardcodeados)
    data_tenedor = {
        "rut": "12.345.678-9",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "telefono": "987654321",
        "correo": None,
        "direccion": None,
        "sector": "Hanga Roa",
        "observaciones": "Registro de prueba"
    }

    print("=== PRUEBA SISTEMA VETERINARIO: TENEDORES ===")

    # 4) Crear solo si NO existe por RUT
    existente = service.obtener_por_rut(data_tenedor["rut"])
    if existente is None:
        print(f"No existe el RUT {data_tenedor['rut']}. Creando tenedor...")
        new_id = service.crear_tenedor(data_tenedor)
        print(f"✅ Tenedor creado con idTenedor = {new_id}")
    else:
        print(f"ℹ️ Ya existe un tenedor activo con RUT {data_tenedor['rut']}. No se crea nuevamente.")
        print(f"   idTenedor existente: {existente.get('idTenedor')}")

    # 5) Listar tenedores activos
    print("\n--- LISTADO DE TENEDORES ACTIVOS ---")
    tenedores = service.listar_activos()

    if not tenedores:
        print("No hay tenedores activos registrados.")
    else:
        for t in tenedores:
            print(f"- [{t.get('idTenedor')}] {t.get('apellidos')}, {t.get('nombres')} | RUT: {t.get('rut')} | Sector: {t.get('sector')}")

    # 6) Buscar nuevamente por RUT y mostrar detalle
    print("\n--- BÚSQUEDA POR RUT ---")
    buscado = service.obtener_por_rut(data_tenedor["rut"])
    if buscado is None:
        print("No se encontró el tenedor por RUT (algo falló).")
    else:
        print("✅ Encontrado:")
        print(f"   ID: {buscado.get('idTenedor')}")
        print(f"   RUT: {buscado.get('rut')}")
        print(f"   Nombre: {buscado.get('nombres')} {buscado.get('apellidos')}")
        print(f"   Teléfono: {buscado.get('telefono')}")
        print(f"   Sector: {buscado.get('sector')}")


if __name__ == "__main__":
    main()
