from pathlib import Path

from app.data.db_connection import DBConnection

from app.data.tenedor_repository import TenedorRepository
from app.services.tenedor_service import TenedorService

from app.data.animal_repository import AnimalRepository
from app.services.animal_service import AnimalService

from app.data.personal_repository import PersonalRepository
from app.services.personal_service import PersonalService

from app.data.motivo_repository import MotivoRepository
from app.services.motivo_service import MotivoService

from app.data.especie_repository import EspecieRepository
from app.services.especie_service import EspecieService

from app.data.raza_repository import RazaRepository
from app.services.raza_service import RazaService





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


def prueba_personal(personal_service: PersonalService) -> int:
    print("\n=== PRUEBA: PERSONAL VETERINARIO ===")

    data = {
        "rut": "11.111.111-1",           # puede venir con puntos, lo normaliza
        "nombres": "Mera",
        "apellidos": "Pont",
        "cargo": "Veterinario",          # en UI será combo
        "areaTrabajo": "Atención público",  # en UI será combo
        "telefono": "987654321",
        "correo": None,
        "fechaIngreso": "2025-12-01",
        "fechaNacimiento": "1998-01-26",
        "observaciones": "Registro de prueba"
    }

    try:
        new_id = personal_service.crear_personal(data)
        print(f"✅ Personal creado con idPersonal = {new_id}")
    except Exception as e:
        print("⚠️ No se creó (probable duplicado/validación):", e)

    print("\n--- LISTADO PERSONAL ACTIVO ---")
    for p in personal_service.listar_activos():
        print(f"- [{p['idPersonal']}] {p['apellidos']}, {p['nombres']} | RUT: {p['rut']} | Cargo: {p['cargo']}")

    # Retorna id para usarlo luego en atención clínica (si existe)
    # Si ya existía, lo buscamos:
    try:
        p = personal_service.obtener_por_rut("11111111-1")
        return int(p["idPersonal"]) if p else 0
    except Exception:
        return 0
    
def prueba_motivos(motivo_service: MotivoService):
    print("\n=== PRUEBA: MOTIVOS (CATÁLOGO) ===")

    motivos = [
        {"nombreMotivo": "Control sano", "descripcion": "Control general; puede incluir vacuna y desparasitación."},
        {"nombreMotivo": "Herida / trauma", "descripcion": "Herida abierta en algun sector del cuerpo"},
        {"nombreMotivo": "Problema digestivo", "descripcion": "Algun malestar en el estómago"},
    ]

    for m in motivos:
        try:
            new_id = motivo_service.crear_motivo(m)
            print(f"✅ Motivo creado idMotivoConsulta={new_id} | {m['nombreMotivo']}")
        except Exception as e:
            print(f"⚠️ No se creó '{m['nombreMotivo']}' (probable duplicado/validación): {e}")

    print("\n--- LISTADO MOTIVOS ACTIVOS ---")
    for x in motivo_service.listar_activos():
        print(f"- [{x['idMotivoConsulta']}] {x['nombreMotivo']}")

def prueba_especies(especie_service: EspecieService):
    print("\n=== PRUEBA: ESPECIES (CATÁLOGO) ===")

    especies = [
        {"nombreEspecie": "Perro"},
        {"nombreEspecie": "Gato"},
        {"nombreEspecie": "Equino"},
        {"nombreEspecie": "Ave"},
        {"nombreEspecie": "Otro"},
    ]

    for e in especies:
        try:
            new_id = especie_service.crear_especie(e)
            print(f"✅ Especie creada idEspecie={new_id} | {e['nombreEspecie']}")
        except Exception as ex:
            print(f"⚠️ No se creó '{e['nombreEspecie']}' (probable duplicado/validación): {ex}")

    print("\n--- LISTADO ESPECIES ACTIVAS ---")
    for x in especie_service.listar_activos():
        print(f"- [{x['idEspecie']}] {x['nombreEspecie']}")

def prueba_razas(especie_service, raza_service):
    print("\n=== PRUEBA: RAZAS (CATÁLOGO) ===")

    perro = especie_service.obtener_por_nombre("Perro")
    gato = especie_service.obtener_por_nombre("Gato")
    otro = especie_service.obtener_por_nombre("Otro")

    if not perro or not gato:
        print("⚠️ No existen especies Perro/Gato. Ejecuta primero prueba_especies.")
        return

    semillas = [
        {"idEspecie": perro["idEspecie"], "nombreRaza": "Mestizo"},
        {"idEspecie": gato["idEspecie"], "nombreRaza": "Mestizo"},
        {"idEspecie": perro["idEspecie"], "nombreRaza": "Poodle"},
    ]

    if otro:
        semillas.append({"idEspecie": otro["idEspecie"], "nombreRaza": "No aplica"})

    for r in semillas:
        try:
            new_id = raza_service.crear_raza(r)
            print(f"✅ Raza creada idRaza={new_id} | especie={r['idEspecie']} | {r['nombreRaza']}")
        except Exception as e:
            print(f"⚠️ No se creó '{r['nombreRaza']}' (duplicado/validación): {e}")

    print("\n--- RAZAS PERRO ---")
    for x in raza_service.listar_por_especie(perro["idEspecie"]):
        print(f"- [{x['idRaza']}] {x['nombreRaza']}")

    print("\n--- RAZAS GATO ---")
    for x in raza_service.listar_por_especie(gato["idEspecie"]):
        print(f"- [{x['idRaza']}] {x['nombreRaza']}")




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

    personal_repo = PersonalRepository(db)
    personal_service = PersonalService(personal_repo)

    motivo_repo = MotivoRepository(db)
    motivo_service = MotivoService(motivo_repo)

    especie_repo = EspecieRepository(db)
    especie_service = EspecieService(especie_repo)

    raza_repo = RazaRepository(db)
    raza_service = RazaService(raza_repo, especie_service)





    # Ejecutar pruebas
    id_tenedor = prueba_tenedores(tenedor_service)
    id_animales = prueba_animales(animal_service, id_tenedor)
    id_personal = prueba_personal(personal_service)
    id_motivo = prueba_motivos(motivo_service)
    id_especies = prueba_especies(especie_service)
    id_razas = prueba_razas(especie_service, raza_service)






if __name__ == "__main__":
    main()
