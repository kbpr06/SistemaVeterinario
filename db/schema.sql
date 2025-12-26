-- -------------------------
-- TENEDOR_RESPONSABLE
-- -------------------------
CREATE TABLE IF NOT EXISTS tenedor_responsable (
  idTenedor          INTEGER PRIMARY KEY AUTOINCREMENT,
  rut                TEXT NOT NULL UNIQUE,
  nombres            TEXT NOT NULL,
  apellidos          TEXT NOT NULL,
  fechaNacimiento    TEXT,                 -- ISO: YYYY-MM-DD (puede ser NULL)
  telefono           TEXT,
  direccion          TEXT,
  sector             TEXT,
  correo             TEXT,
  observaciones      TEXT,
  estadoRegistro     INTEGER NOT NULL DEFAULT 1, -- 1=activo, 0=inactivo
  CHECK (estadoRegistro IN (0,1))
);

CREATE INDEX IF NOT EXISTS idx_tenedor_rut ON tenedor_responsable(rut);
CREATE INDEX IF NOT EXISTS idx_tenedor_nombre ON tenedor_responsable(apellidos, nombres);

-- -------------------------
-- ESPECIE
-- -------------------------
CREATE TABLE IF NOT EXISTS especie (
  idEspecie       INTEGER PRIMARY KEY AUTOINCREMENT,
  nombreEspecie   TEXT NOT NULL UNIQUE,
  estadoRegistro  INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1))
);

-- -------------------------
-- RAZA
-- -------------------------
CREATE TABLE IF NOT EXISTS raza (
  idRaza          INTEGER PRIMARY KEY AUTOINCREMENT,
  idEspecie       INTEGER NOT NULL,
  nombreRaza      TEXT NOT NULL,
  estadoRegistro  INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  FOREIGN KEY (idEspecie) REFERENCES especie(idEspecie)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  UNIQUE (idEspecie, nombreRaza)
);

CREATE INDEX IF NOT EXISTS idx_raza_especie ON raza(idEspecie);

-- -------------------------
-- MOTIVO_CONSULTA
-- -------------------------
CREATE TABLE IF NOT EXISTS motivo_consulta (
  idMotivoConsulta  INTEGER PRIMARY KEY AUTOINCREMENT,
  nombreMotivo      TEXT NOT NULL UNIQUE,
  descripcion       TEXT,
  estadoRegistro    INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1))
);

-- -------------------------
-- PERSONAL_VETERINARIO
-- -------------------------
CREATE TABLE IF NOT EXISTS personal_veterinario (
  idPersonal       INTEGER PRIMARY KEY AUTOINCREMENT,
  rut              TEXT NOT NULL UNIQUE,
  nombres          TEXT NOT NULL,
  apellidos        TEXT NOT NULL,
  cargo            TEXT NOT NULL,
  areaTrabajo      TEXT,
  telefono         TEXT,
  correo           TEXT,
  fechaIngreso     TEXT,  -- YYYY-MM-DD
  fechaNacimiento  TEXT,  -- YYYY-MM-DD
  observaciones    TEXT,
  estadoRegistro   INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1))
);

CREATE INDEX IF NOT EXISTS idx_personal_rut ON personal_veterinario(rut);
CREATE INDEX IF NOT EXISTS idx_personal_nombre ON personal_veterinario(apellidos, nombres);

-- -------------------------
-- USUARIO_SISTEMA
-- -------------------------
CREATE TABLE IF NOT EXISTS usuario_sistema (
  idUsuario        INTEGER PRIMARY KEY AUTOINCREMENT,
  idPersonal       INTEGER,  -- puede ser NULL
  nombreUsuario    TEXT NOT NULL UNIQUE,
  claveEncriptada  TEXT NOT NULL, -- hash
  rol              TEXT NOT NULL, -- admin_sistema / veterinario / tecnico / administrativo
  fechaCreacion    TEXT NOT NULL DEFAULT (date('now')),
  estadoRegistro   INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  CHECK (rol IN ('admin_sistema','veterinario','tecnico','administrativo')),
  FOREIGN KEY (idPersonal) REFERENCES personal_veterinario(idPersonal)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_usuario_nombre ON usuario_sistema(nombreUsuario);

-- -------------------------
-- ANIMAL
-- -------------------------
CREATE TABLE IF NOT EXISTS animal (
  idAnimal            INTEGER PRIMARY KEY AUTOINCREMENT,
  idTenedor           INTEGER NOT NULL,
  idEspecie           INTEGER NOT NULL,
  idRaza              INTEGER, -- opcional
  nombre              TEXT NOT NULL,
  sexo                TEXT NOT NULL DEFAULT 'Desconocido', -- M/H/Desconocido
  fechaNacimientoEst  TEXT, -- YYYY-MM-DD
  color               TEXT,
  estadoReproductivo  TEXT,
  numeroMicrochip     TEXT,
  viveDentroCasa      INTEGER, -- 1/0/NULL
  conviveConOtros     TEXT,
  observaciones       TEXT,
  estadoRegistro      INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  CHECK (viveDentroCasa IN (0,1) OR viveDentroCasa IS NULL),
  CHECK (sexo IN ('M','H','Desconocido')),
  FOREIGN KEY (idTenedor) REFERENCES tenedor_responsable(idTenedor)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idEspecie) REFERENCES especie(idEspecie)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idRaza) REFERENCES raza(idRaza)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- Microchip debería ser único si se usa (pero puede venir vacío)
CREATE UNIQUE INDEX IF NOT EXISTS ux_animal_microchip
ON animal(numeroMicrochip)
WHERE numeroMicrochip IS NOT NULL AND trim(numeroMicrochip) <> '';

CREATE INDEX IF NOT EXISTS idx_animal_tenedor ON animal(idTenedor);
CREATE INDEX IF NOT EXISTS idx_animal_especie ON animal(idEspecie);
CREATE INDEX IF NOT EXISTS idx_animal_nombre ON animal(nombre);

-- -------------------------
-- ATENCION_CLINICA
-- -------------------------
CREATE TABLE IF NOT EXISTS atencion_clinica (
  idAtencion             INTEGER PRIMARY KEY AUTOINCREMENT,
  idAnimal               INTEGER NOT NULL,
  idPersonal             INTEGER NOT NULL, -- vet responsable
  idMotivoConsulta       INTEGER NOT NULL,
  fechaAtencion          TEXT NOT NULL,    -- YYYY-MM-DD
  sintomas               TEXT,
  pesoKg                 REAL,             -- NULL permitido
  diagnostico            TEXT,
  tratamiento            TEXT,
  observaciones          TEXT,
  fechaControlSugerida   TEXT,             -- YYYY-MM-DD
  lugarAtencion          TEXT NOT NULL DEFAULT 'Consulta', -- Consulta/Operativo/Domicilio
  estadoRegistro         INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  CHECK (pesoKg IS NULL OR pesoKg >= 0),
  CHECK (lugarAtencion IN ('Consulta','Operativo','Domicilio')),
  FOREIGN KEY (idAnimal) REFERENCES animal(idAnimal)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idPersonal) REFERENCES personal_veterinario(idPersonal)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idMotivoConsulta) REFERENCES motivo_consulta(idMotivoConsulta)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_atencion_animal_fecha ON atencion_clinica(idAnimal, fechaAtencion);
CREATE INDEX IF NOT EXISTS idx_atencion_fecha ON atencion_clinica(fechaAtencion);
CREATE INDEX IF NOT EXISTS idx_atencion_motivo ON atencion_clinica(idMotivoConsulta);

-- -------------------------
-- TIPO_VACUNA
-- -------------------------
CREATE TABLE IF NOT EXISTS tipo_vacuna (
  idTipoVacuna       INTEGER PRIMARY KEY AUTOINCREMENT,
  nombreVacuna       TEXT NOT NULL UNIQUE,
  descripcion        TEXT,
  idEspecie          INTEGER,  -- opcional
  intervaloRecMeses  INTEGER,  -- opcional
  estadoRegistro     INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  CHECK (intervaloRecMeses IS NULL OR intervaloRecMeses >= 0),
  FOREIGN KEY (idEspecie) REFERENCES especie(idEspecie)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- -------------------------
-- VACUNA_APLICADA
-- -------------------------
CREATE TABLE IF NOT EXISTS vacuna_aplicada (
  idVacunaAplicada  INTEGER PRIMARY KEY AUTOINCREMENT,
  idAtencion        INTEGER NOT NULL,
  idTipoVacuna      INTEGER NOT NULL,
  fechaAplicacion   TEXT NOT NULL, -- YYYY-MM-DD
  fechaProximaDosis TEXT,
  dosis             TEXT,
  lote              TEXT,
  observaciones     TEXT,
  estadoRegistro    INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  FOREIGN KEY (idAtencion) REFERENCES atencion_clinica(idAtencion)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idTipoVacuna) REFERENCES tipo_vacuna(idTipoVacuna)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_vacuna_atencion ON vacuna_aplicada(idAtencion);

-- -------------------------
-- TIPO_DESPARASITACION
-- -------------------------
CREATE TABLE IF NOT EXISTS tipo_desparasitacion (
  idTipoDesparasitacion INTEGER PRIMARY KEY AUTOINCREMENT,
  nombreDesparasitacion TEXT NOT NULL UNIQUE,
  tipo                 TEXT NOT NULL DEFAULT 'Mixta', -- Interna/Externa/Mixta
  idEspecie            INTEGER,
  intervaloRecMeses    INTEGER,
  estadoRegistro       INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  CHECK (tipo IN ('Interna','Externa','Mixta')),
  CHECK (intervaloRecMeses IS NULL OR intervaloRecMeses >= 0),
  FOREIGN KEY (idEspecie) REFERENCES especie(idEspecie)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- -------------------------
-- DESPARASITACION_APLICADA
-- -------------------------
CREATE TABLE IF NOT EXISTS desparasitacion_aplicada (
  idDesparasitacion     INTEGER PRIMARY KEY AUTOINCREMENT,
  idAtencion            INTEGER NOT NULL,
  idTipoDesparasitacion INTEGER NOT NULL,
  fechaAplicacion       TEXT NOT NULL,
  fechaProximaDosis     TEXT,
  dosis                 TEXT,
  lote                  TEXT,
  observaciones         TEXT,
  estadoRegistro        INTEGER NOT NULL DEFAULT 1,
  CHECK (estadoRegistro IN (0,1)),
  FOREIGN KEY (idAtencion) REFERENCES atencion_clinica(idAtencion)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (idTipoDesparasitacion) REFERENCES tipo_desparasitacion(idTipoDesparasitacion)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_desparasitacion_atencion ON desparasitacion_aplicada(idAtencion);


-- Evita borrar ANIMAL si tiene atenciones
CREATE TRIGGER IF NOT EXISTS trg_no_delete_animal_con_atenciones
BEFORE DELETE ON animal
FOR EACH ROW
BEGIN
  SELECT CASE
    WHEN EXISTS (SELECT 1 FROM atencion_clinica WHERE idAnimal = OLD.idAnimal)
    THEN RAISE(ABORT, 'No se puede eliminar el animal: tiene atenciones registradas.')
  END;
END;

-- Evita borrar ATENCION si tiene vacuna/desparasitación asociada
CREATE TRIGGER IF NOT EXISTS trg_no_delete_atencion_con_procedimientos
BEFORE DELETE ON atencion_clinica
FOR EACH ROW
BEGIN
  SELECT CASE
    WHEN EXISTS (SELECT 1 FROM vacuna_aplicada WHERE idAtencion = OLD.idAtencion)
      OR EXISTS (SELECT 1 FROM desparasitacion_aplicada WHERE idAtencion = OLD.idAtencion)
    THEN RAISE(ABORT, 'No se puede eliminar la atención: tiene procedimientos asociados.')
  END;
END;