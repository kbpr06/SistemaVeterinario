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

from app.data.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService

from app.data.atencion_repository import AtencionRepository
from app.services.atencion_service import AtencionService

from app.data.tipo_vacuna_repository import TipoVacunaRepository
from app.services.tipo_vacuna_service import TipoVacunaService

from app.data.vacuna_aplicada_repository import VacunaAplicadaRepository
from app.services.vacuna_aplicada_service import VacunaAplicadaService

from app.data.tipo_desparasitacion_repository import TipoDesparasitacionRepository
from app.services.tipo_desparasitacion_service import TipoDesparasitacionService

from app.data.desparasitacion_aplicada_repository import DesparasitacionAplicadaRepository
from app.services.desparasitacion_aplicada_service import DesparasitacionAplicadaService





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

def prueba_usuarios(usuario_service: UsuarioService):
    print("\n=== PRUEBA: USUARIOS SISTEMA ===")

    # 1) Crear admin_sistema inicial si no existe
    try:
        creado = usuario_service.crear_admin_sistema_si_no_existe("admin", "Admin123!")
        if creado:
            print(f"✅ Admin sistema creado con idUsuario={creado} (usuario: admin / clave: Admin123!)")
        else:
            print("✅ Ya existe un admin_sistema activo. No se crea otro.")
    except Exception as e:
        print(f"⚠️ No se pudo crear admin_sistema inicial: {e}")

    # 2) Probar login correcto
    try:
        user = usuario_service.login("ADMIN", "Admin123!")
        print("✅ Login OK:", user)
    except Exception as e:
        print("❌ Login falló:", e)

    # 3) Probar login incorrecto
    try:
        usuario_service.login("admin", "mala_clave")
        print("❌ Esto no debería imprimirse (login incorrecto aceptado)")
    except Exception as e:
        print("✅ Login incorrecto rechazado:", e)

def prueba_atenciones(atencion_service: AtencionService, id_animal: int, id_personal: int, id_motivo: int):
    print("\n=== PRUEBA: ATENCIONES CLÍNICAS ===")

    data_atencion = {
        "idAnimal": id_animal,
        "idPersonal": id_personal,
        "idMotivoConsulta": id_motivo,
        "fechaAtencion": "2025-12-29",
        "sintomas": "Decaimiento y poco apetito (informado por tenedor).",
        "pesoKg": 12.4,
        "diagnostico": "Se observa cuadro leve, se deja registro clínico en texto.",
        "tratamiento": "Indicaciones generales + control.",
        "observaciones": "Atención de prueba para validar módulo.",
        "fechaControlSugerida": "2026-01-10",
        "lugarAtencion": "Consulta",
    }

    try:
        new_id = atencion_service.crear_atencion(data_atencion)
        print(f"✅ Atención creada con idAtencion = {new_id}")
    except Exception as e:
        print(f"⚠️ No se pudo crear atención: {e}")

    print("\n--- HISTORIAL (Atenciones por animal) ---")
    atenciones = atencion_service.listar_por_animal(id_animal)
    for a in atenciones:
        print(f"- [{a['idAtencion']}] {a['fechaAtencion']} | motivo={a['idMotivoConsulta']} | lugar={a['lugarAtencion']} | peso={a['pesoKg']}")


def prueba_tipo_vacuna(service: TipoVacunaService):
    print("\n=== PRUEBA: TIPO VACUNA ===")

    data = {
        "nombreVacuna": "Antirrábica",
        "descripcion": "Vacuna contra la rabia.",
        "idEspecie": 1,             # perro (ajusta si tu idEspecie es otro)
        "intervaloRecMeses": 12
    }

    try:
        new_id = service.crear(data)
        print(f"✅ Tipo vacuna creado con idTipoVacuna = {new_id}")
    except Exception as e:
        print(f"⚠️ No se creó tipo vacuna: {e}")

    print("\n--- LISTADO TIPOS VACUNA ACTIVOS ---")
    for v in service.listar_activos():
        print(f"- [{v['idTipoVacuna']}] {v['nombreVacuna']} | especie={v['idEspecie']} | intervalo={v['intervaloRecMeses']}")

def prueba_vacuna_aplicada(service: VacunaAplicadaService):
    print("\n=== PRUEBA: VACUNA APLICADA ===")

    data = {
        "id_atencion" : 1,
        "id_tipo_vacuna" : 1,
        "fecha_aplicacion" :"2025-12-29",
        "fecha_proxima_dosis" : "2026-01-29",
        "dosis" : "1 dosis",
        "lote" : "L-001",
        "observaciones" : "Vacuna aplicada en control sano"
    }

    try:
        new_id = service.crear(**data)
        print(f"✅ Vacuna aplicada creada con idVacunaAplicada = {new_id}")
    except Exception as e:
        print(f"⚠️ No se creó vacuna aplicada: {e}")

    print("\n--- VACUNAS DE LA ATENCIÓN ---")
    vacunas = service.listar_por_atencion(data["id_atencion"])
    for v in vacunas:
        print(
            f"- [{v['idVacunaAplicada']}] "
            f"fecha={v['fechaAplicacion']} "
            f"tipo={v['idTipoVacuna']} "
            f"próxima={v['fechaProximaDosis']}"
        )

def prueba_tipo_desparasitacion(service: TipoDesparasitacionService):
    print("\n=== PRUEBA: TIPO DESPARASITACION ===")

    try:
        new_id = service.crear(
            nombre_desparasitacion="Antiparasitario Externo",
            tipo="Interna",
            id_especie=1,            # perro (ajusta si corresponde)
            intervalo_rec_meses=3
        )
        print(f"✅ Tipo desparasitación creado con idTipoDesparasitacion = {new_id}")
    except Exception as e:
        print(f"⚠️ No se creó tipo desparasitación: {e}")

    print("\n--- LISTADO TIPOS DESPARASITACION ACTIVOS ---")
    for d in service.listar_activos():
        print(f"- [{d['idTipoDesparasitacion']}] {d['nombreDesparasitacion']} | tipo={d['tipo']} | especie={d['idEspecie']} | intervalo={d['intervaloRecMeses']}")

def prueba_desparasitacion_aplicada(service: DesparasitacionAplicadaService):
    print("\n=== PRUEBA: DESPARASITACION APLICADA ===")

    try:
        new_id = service.crear(
            id_atencion=1,                 # ajusta según tu BD
            id_tipo_desparasitacion=1,     # ajusta según tu BD
            fecha_aplicacion="2025-12-29",
            fecha_proxima_dosis="2026-03-29",
            dosis="1 pipeta",
            lote="D-001",
            observaciones="Desparasitación aplicada en control sano"
        )
        print(f"✅ Desparasitación aplicada creada con idDesparasitacion = {new_id}")
    except Exception as e:
        print(f"⚠️ No se creó desparasitación aplicada: {e}")

    print("\n--- DESPARASITACIONES DE LA ATENCIÓN ---")
    desps = service.listar_por_atencion(1)
    for d in desps:
        print(f"- [{d['idDesparasitacion']}] fecha={d['fechaAplicacion']} tipo={d['idTipoDesparasitacion']} próxima={d['fechaProximaDosis']}")

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

    usuario_repo = UsuarioRepository(db)
    usuario_service = UsuarioService(usuario_repo)

    atencion_repo = AtencionRepository(db)
    atencion_service = AtencionService(atencion_repo, animal_repo, personal_repo, motivo_repo)

    tipo_vacuna_repo = TipoVacunaRepository(db)
    tipo_vacuna_service = TipoVacunaService(tipo_vacuna_repo, especie_repo)

    vacuna_aplicada_repo = VacunaAplicadaRepository(db)
    vacuna_aplicada_service = VacunaAplicadaService(vacuna_aplicada_repo)

    tipo_des_repo = TipoDesparasitacionRepository(db)
    tipo_des_service = TipoDesparasitacionService(tipo_des_repo)

    desparasitacion_aplicada_repo = DesparasitacionAplicadaRepository(db)
    desparasitacion_aplicada_service = DesparasitacionAplicadaService(desparasitacion_aplicada_repo)


    # Ejecutar pruebas
    id_tenedor = prueba_tenedores(tenedor_service)
    id_animales = prueba_animales(animal_service, id_tenedor)
    id_personal = prueba_personal(personal_service)
    id_motivo = prueba_motivos(motivo_service)
    id_especies = prueba_especies(especie_service)
    id_razas = prueba_razas(especie_service, raza_service)
    id_usuarios = prueba_usuarios(usuario_service)
    id_atenciones = prueba_atenciones(atencion_service, id_animal=1, id_personal=1, id_motivo=1)
    id_tipo_vacuna = prueba_tipo_vacuna(tipo_vacuna_service)
    id_vacuna_aplicada = prueba_vacuna_aplicada(vacuna_aplicada_service)
    id_tipo_desparasitacion = prueba_tipo_desparasitacion(tipo_des_service)
    id_desparasitacion_aplicada = prueba_desparasitacion_aplicada(desparasitacion_aplicada_service)


if __name__ == "__main__":
    main()
