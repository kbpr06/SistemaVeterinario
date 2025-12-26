from pathlib import Path

from app.data.db_connection import DBConnection

from app.data.tenedor_repository import TenedorRepository
from app.services.tenedor_service import TenedorService

from app.data.animal_repository import AnimalRepository
from app.services.animal_service import AnimalService


def prueba_tenedores(tenedor_service: TenedorService) -> int:
    """
    Crea (si no existe) un tenedor de prueba y retorna su idTenedor.
    """
    print("\n=== PRUEBA: TENEDORES ===")

    data_tenedor = {
        "rut": "12.345.678-9",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "telefono": "987654321",
        "correo": None,
        "direccion": None,
        "sector": "Hanga Roa",
        "observaciones": None
    }

    existente = tenedor_service.obtener_por_rut(data_tenedor["rut"])
    if existente:
        print(f"✅ Ya existe el RUT {data_tenedor['rut']}. No se crea de nuevo.")
        id_tenedor = existente.get("idTenedor")
    else:
        print(f"No existe el RUT {data_tenedor['rut']}. Creando tenedor...")
        id_tenedor = tenedor_service.crear_tenedor(data_tenedor)
        print(f"✅ Tenedor creado con idTenedor = {id_tenedor}")

    print("\n--- LISTADO DE TENEDORES ACTIVOS ---")
    for t in tenedor_service.listar_activos():
        print(
            f"- [{t.get('idTenedor')}] {t.get('apellidos','')} , {t.get('nombres','')} "
            f"| RUT: {t.get('rut')} | Sector: {t.get('sector')}"
        )

    print("\n--- BÚSQUEDA POR RUT ---")
    encontrado = tenedor_service.obtener_por_rut(data_tenedor["rut"])
    if encontrado:
        print("✅ Encontrado:")
        print(f"   ID: {encontrado.get('idTenedor')}")
        print(f"   RUT: {encontrado.get('rut')}")
        print(f"   Nombre: {encontrado.get('nombres','')} {encontrado.get('apellidos','')}")
        print(f"   Teléfono: {encontrado.get('telefono')}")
        print(f"   Sector: {encontrado.get('sector')}")
    else:
        print("❌ No encontrado (o desactivado).")

    return int(id_tenedor)


def prueba_animales(animal_service: AnimalService, id_tenedor: int) -> None:
    """
    Crea (si no existe por microchip) un animal de prueba y lista animales del tenedor.
    """
    print("\n=== PRUEBA: ANIMALES ===")

    data_animal = {
        "idTenedor": id_tenedor,
        "idEspecie": 1,  # 1=perro (según tu seed)
        "idRaza": None,
        "nombre": "Firulais",
        "sexo": "M",

        # usar SOLO uno:
        "edadEstimadaMeses": 36,
        "fechaNacimientoEst": None,

        "color": "Café",
        "estadoReproductivo": "Entero",
        "numeroMicrochip": "MC-0001",

        "viveDentroCasa": 1,
        "conviveConOtros": ["Perros", "Gatos"],
        "observaciones": "Animal de prueba para validar módulo Animal."
    }

    try:
        new_id = animal_service.crear_animal(data_animal)
        print(f"✅ Animal creado con idAnimal = {new_id}")
    except Exception as e:
        print("⚠️ No se creó el animal (probable duplicado o validación):", e)

    print("\n--- LISTADO DE ANIMALES DEL TENEDOR ---")
    animales = animal_service.listar_por_tenedor(id_tenedor)
    if not animales:
        print("No hay animales activos asociados a este tenedor.")
        return

    for a in animales:
        print(
            f"- [{a.get('idAnimal')}] {a.get('nombre')} | idEspecie={a.get('idEspecie')} "
            f"| sexo={a.get('sexo')} | microchip={a.get('numeroMicrochip')} "
            f"| edadMeses={a.get('edadEstimadaMeses')}"
        )

    # buscar por id (ejemplo)
    id_busqueda = animales[0]["idAnimal"]
    encontrado = animal_service.obtener_por_id(id_busqueda)
    print("\n--- BÚSQUEDA ANIMAL POR ID ---")
    if encontrado:
        print("✅ Encontrado:", encontrado)
    else:
        print("❌ No encontrado (o desactivado).")


def main():
    print("=== PRUEBA SISTEMA VETERINARIO (BACKEND) ===")

    # Ruta absoluta al archivo DB (robusta)
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_path = str(BASE_DIR / "db" / "veterinaria.db")
    print("Usando BD en:", db_path)

    db = DBConnection(db_path)

    # Servicios / repos
    tenedor_repo = TenedorRepository(db)
    tenedor_service = TenedorService(tenedor_repo)

    animal_repo = AnimalRepository(db)
    animal_service = AnimalService(animal_repo)

    # Ejecutar pruebas
    id_tenedor = prueba_tenedores(tenedor_service)
    prueba_animales(animal_service, id_tenedor)


if __name__ == "__main__":
    main()
