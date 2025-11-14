# 🔐 Sistema de Autenticación JWT con RBAC

## 📋 Descripción General

Este proyecto implementa autenticación JWT (JSON Web Tokens) con control de acceso basado en roles (RBAC - Role-Based Access Control).

## 🚀 Uso Rápido

### 1. **Iniciar sesión** (Obtener Token JWT)

**Endpoint:** `POST /auth/login`

**Body:**

```json
{
  "username": "admin",
  "password": "tu_password"
}
```

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "nombre_usuario": "admin",
    "rol": "Administrador"
  }
}
```

### 2. **Usar el Token en Swagger UI** (`/docs`)

1. Haz clic en el botón **"Authorize"** 🔓 (esquina superior derecha)
2. En el campo **Value**, escribe: `Bearer tu_token_aqui`
3. Haz clic en **"Authorize"**
4. ¡Listo! Ahora puedes probar todos los endpoints protegidos

### 3. **Usar el Token en código/Postman/Insomnia**

Agrega el header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🛠️ Configuración Inicial

### Variables de Entorno (`.env`)

```env
# Autenticación JWT
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiala
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANTE:** Cambia `SECRET_KEY` en producción. Genera una con:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔑 Endpoints de Autenticación

### 1. Login Principal

- **Endpoint:** `POST /auth/login`
- **Uso:** Login desde frontend, devuelve información del usuario
- **Response:** Token + datos del usuario

### 2. Login OAuth2 (Swagger)

- **Endpoint:** `POST /auth/token`
- **Uso:** Compatible con OAuth2, usado automáticamente por Swagger UI
- **Response:** Solo token

### 3. Usuario Actual

- **Endpoint:** `GET /auth/me`
- **Uso:** Obtener información del usuario autenticado
- **Requiere:** Token válido

---

## 🎯 Cómo Proteger tus Endpoints

### Opción 1: Solo Administradores ✅ **(RECOMENDADO AHORA)**

```python
from app.auth import require_admin

@router.post("/equipos/")
def crear_equipo(
    equipo: EquipoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # ✅ Solo Administrador
):
    """Crear equipo - Solo Administrador"""
    # ... tu código ...
```

### Opción 2: Administrador O Técnico

```python
from app.auth import require_admin_or_tecnico

@router.get("/mantenimientos/")
def listar_mantenimientos(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_tecnico)  # ✅ Admin o Técnico
):
    """Listar mantenimientos - Administrador o Técnico"""
    # ... tu código ...
```

### Opción 3: Cualquier Usuario Autenticado

```python
from app.auth import require_any_authenticated

@router.get("/mi-perfil/")
def obtener_perfil(
    current_user = Depends(require_any_authenticated)  # ✅ Cualquier usuario
):
    """Ver perfil - Cualquier usuario autenticado"""
    return current_user
```

### Opción 4: Roles Personalizados (Para el futuro)

```python
from app.auth import RoleChecker

# Crear un checker personalizado
require_admin_or_vendedor = RoleChecker(["Administrador", "Vendedor"])

@router.post("/ventas/")
def crear_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_vendedor)  # ✅ Admin o Vendedor
):
    """Crear venta - Administrador o Vendedor"""
    # ... tu código ...
```

---

## 📊 Ejemplo Completo - Router Protegido

```python
"""
Router de Equipos - Ejemplo con autenticación
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import require_admin, require_admin_or_tecnico
from app.models.equipo_biomedico import EquipoBiomedico
from app.schemas.equipo_biomedico import Equipo, EquipoCreate, EquipoUpdate

router = APIRouter(
    prefix="/equipos",
    tags=["🏥 Módulo 4: Inventario y Equipos"]
)

# Solo Administrador puede crear
@router.post("/", response_model=Equipo, status_code=status.HTTP_201_CREATED)
def crear_equipo(
    equipo: EquipoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # 🔒 Solo Admin
):
    """Crear equipo - Solo Administrador"""
    # ... código ...

# Admin o Técnico pueden listar
@router.get("/", response_model=List[Equipo])
def listar_equipos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_tecnico)  # 🔒 Admin o Técnico
):
    """Listar equipos - Administrador o Técnico"""
    # ... código ...

# Solo Admin puede eliminar
@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # 🔒 Solo Admin
):
    """Eliminar equipo - Solo Administrador"""
    # ... código ...
```

---

## 🎨 Estrategia de Implementación (Tu Proyecto)

### **Fase 1 - ACTUAL: Todo protegido con Admin** 🔥

```python
# TODOS los endpoints actuales:
current_user = Depends(require_admin)
```

**Ventaja:** Máxima seguridad mientras desarrollas el frontend.

### **Fase 2 - Asignar permisos según rol**

Cuando crees nuevos roles en la base de datos, puedes ir cambiando los endpoints:

```python
# Ejemplo: Técnicos pueden ver mantenimientos
@router.get("/mantenimientos/")
def listar_mantenimientos(
    current_user = Depends(require_admin_or_tecnico)  # ✅ Cambiado
):
    pass

# Ejemplo: Vendedores pueden crear ventas
require_admin_or_vendedor = RoleChecker(["Administrador", "Vendedor"])

@router.post("/ventas/")
def crear_venta(
    current_user = Depends(require_admin_or_vendedor)  # ✅ Nuevo checker
):
    pass
```

---

## 🔍 Acceder a Datos del Usuario en el Endpoint

```python
@router.get("/mi-perfil/")
def obtener_perfil(current_user = Depends(require_admin)):
    # current_user es un objeto Usuario con:
    return {
        "id": current_user.id_usuario,
        "nombre": current_user.nombre_usuario,
        "email": current_user.email,
        "rol": current_user.rol.nombre_rol,  # Relación con tabla Rol
        "activo": current_user.activo
    }
```

---

## 🚫 Errores Comunes y Soluciones

### Error 401: Not authenticated

**Causa:** No enviaste el token o el token expiró.

**Solución:**

1. Obtén un nuevo token con `/auth/login`
2. Verifica que el header sea: `Authorization: Bearer tu_token`

### Error 403: Forbidden

**Causa:** Tu rol no tiene permiso para ese endpoint.

**Ejemplo:**

```json
{
  "detail": "Se requiere rol: Administrador"
}
```

**Solución:** Usa un usuario con el rol correcto o modifica el endpoint para permitir tu rol.

### Error 422: Validation Error (username/password)

**Causa:** Credenciales inválidas.

**Solución:** Verifica que el usuario existe en la tabla `Usuario`.

---

## 📝 Checklist de Seguridad

- [x] ✅ SECRET_KEY única y segura en producción
- [x] ✅ Contraseñas hasheadas con bcrypt
- [x] ✅ Tokens JWT con expiración (30 minutos)
- [x] ✅ Todos los endpoints protegidos con `Depends(require_admin)` inicialmente
- [ ] ⏳ Verificar usuarios activos (`activo = True`)
- [ ] ⏳ Implementar refresh tokens (opcional, para tokens de larga duración)
- [ ] ⏳ Rate limiting en `/auth/login` (prevenir fuerza bruta)
- [ ] ⏳ HTTPS en producción

---

## 🔄 Flujo de Autenticación

```mermaid
graph TD
    A[Usuario envía username + password] --> B[POST /auth/login]
    B --> C{Credenciales válidas?}
    C -->|No| D[Error 401]
    C -->|Sí| E[Verificar rol del usuario]
    E --> F[Generar Token JWT]
    F --> G[Devolver token + info usuario]
    G --> H[Frontend guarda token]
    H --> I[Cada request envía: Authorization: Bearer token]
    I --> J{Token válido?}
    J -->|No| K[Error 401]
    J -->|Sí| L{Rol correcto?}
    L -->|No| M[Error 403]
    L -->|Sí| N[Ejecutar endpoint]
```

---

## 🎓 Crear tu Primer Usuario Administrador

**⚠️ IMPORTANTE:** Necesitas al menos un usuario administrador en la base de datos.

### Opción 1: Script Python

```python
# crear_admin.py
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.auth import get_password_hash

db = SessionLocal()

# Buscar o crear rol Administrador
rol_admin = db.query(Rol).filter(Rol.nombre_rol == "Administrador").first()
if not rol_admin:
    rol_admin = Rol(nombre_rol="Administrador", descripcion="Acceso total")
    db.add(rol_admin)
    db.commit()
    db.refresh(rol_admin)

# Crear usuario admin
usuario_admin = Usuario(
    nombre_usuario="admin",
    contrasena_hash=get_password_hash("admin123"),  # ⚠️ Cambiar en producción
    email="admin@empresa.com",
    id_rol=rol_admin.id_rol,
    activo=True
)
db.add(usuario_admin)
db.commit()
print("✅ Usuario administrador creado")
```

### Opción 2: SQL Directo

```sql
-- 1. Crear rol
INSERT INTO "Rol" (nombre_rol, descripcion)
VALUES ('Administrador', 'Acceso total al sistema');

-- 2. Crear usuario (contraseña: admin123)
INSERT INTO "Usuario" (nombre_usuario, contrasena_hash, email, id_rol, activo)
VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQw7mH7UK',  -- Hash de "admin123"
    'admin@empresa.com',
    1,  -- id_rol del Administrador
    true
);
```

---

## 📚 Recursos Adicionales

- **JWT.io:** https://jwt.io/ - Decodificar y verificar tokens
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/
- **OAuth2 Password Flow:** https://oauth.net/2/grant-types/password/

---

## 🎉 ¡Listo!

Ahora tienes un sistema completo de autenticación. Pasos siguientes:

1. ✅ Todos los endpoints están protegidos con `require_admin`
2. 🔄 Crea un usuario administrador en la BD
3. 🧪 Prueba el login en `/docs` con tus credenciales
4. 🚀 Según vayas creando roles, ajusta los permisos con `RoleChecker`

**¿Dudas?** Revisa este documento o los archivos:

- `app/auth.py` - Lógica de autenticación
- `app/routers/auth_router.py` - Endpoints de login
- `app/routers/rol.py` - Ejemplo de router protegido
