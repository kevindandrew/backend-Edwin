"""
Script para aplicar autenticación a TODOS los routers
Este script muestra cómo proteger cada endpoint con require_admin

Para aplicar la protección manualmente:
1. Importar: from app.auth import require_admin
2. Agregar a cada función: current_user = Depends(require_admin)

ROUTERS A PROTEGER:
"""

INSTRUCCIONES = """
╔════════════════════════════════════════════════════════════════╗
║  🔐 CÓMO PROTEGER TUS ENDPOINTS CON AUTENTICACIÓN             ║
╚════════════════════════════════════════════════════════════════╝

📋 PASO 1: Importar require_admin
─────────────────────────────────────
En cada archivo de router (app/routers/*.py), agregar:

    from app.auth import require_admin


📋 PASO 2: Agregar dependencia a cada endpoint
─────────────────────────────────────────────
Cambiar TODAS las funciones de:

    @router.post("/")
    def crear_item(item: ItemCreate, db: Session = Depends(get_db)):
        ...

A:

    @router.post("/")
    def crear_item(
        item: ItemCreate,
        db: Session = Depends(get_db),
        current_user = Depends(require_admin)  # ✅ AGREGAR ESTA LÍNEA
    ):
        ...


📋 EJEMPLO COMPLETO - Antes y Después
─────────────────────────────────────

❌ ANTES (Sin protección):

    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from app.database import get_db

    @router.get("/")
    def listar_items(db: Session = Depends(get_db)):
        return db.query(Item).all()

✅ DESPUÉS (Con protección):

    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.auth import require_admin  # ✅ 1. Importar

    @router.get("/")
    def listar_items(
        db: Session = Depends(get_db),
        current_user = Depends(require_admin)  # ✅ 2. Agregar dependencia
    ):
        return db.query(Item).all()


╔════════════════════════════════════════════════════════════════╗
║  📁 ARCHIVOS QUE NECESITAS MODIFICAR                          ║
╚════════════════════════════════════════════════════════════════╝

🔐 MÓDULO 1: Seguridad y Roles
───────────────────────────────
✅ app/routers/rol.py              (YA PROTEGIDO - Ejemplo)
⏳ app/routers/usuario.py          (PENDIENTE)

👥 MÓDULO 2: Clientes y Ubicaciones
───────────────────────────────────────
⏳ app/routers/cliente.py          (PENDIENTE)
⏳ app/routers/ubicacion.py        (PENDIENTE)

📦 MÓDULO 3: Catálogos
──────────────────────
⏳ app/routers/categoria_equipo.py (PENDIENTE)
⏳ app/routers/nivel_riesgo.py     (PENDIENTE)
⏳ app/routers/fabricante.py       (PENDIENTE)
⏳ app/routers/tipo_tecnologia.py  (PENDIENTE)

🏥 MÓDULO 4: Inventario
──────────────────────
⏳ app/routers/equipo_biomedico.py (PENDIENTE)
⏳ app/routers/datos_tecnicos.py   (PENDIENTE)

🔧 MÓDULO 5: Mantenimiento
─────────────────────────
⏳ app/routers/mantenimiento.py    (PENDIENTE)
⏳ app/routers/repuesto.py         (PENDIENTE)
⏳ app/routers/uso_repuesto.py     (PENDIENTE)

🛒 MÓDULO 6: Compras
───────────────────
⏳ app/routers/compra_adquisicion.py (PENDIENTE)
⏳ app/routers/detalle_compra.py     (PENDIENTE)

💰 MÓDULO 7: Ventas
──────────────────
⏳ app/routers/venta.py            (PENDIENTE)
⏳ app/routers/detalle_venta.py    (PENDIENTE)

📊 ESTADÍSTICAS
──────────────
⏳ app/routers/estadisticas.py     (PENDIENTE)


╔════════════════════════════════════════════════════════════════╗
║  ⚡ EJEMPLO RÁPIDO - Proteger un router completo              ║
╚════════════════════════════════════════════════════════════════╝

Supongamos que tienes app/routers/cliente.py con 5 endpoints.

1️⃣ Agregar import al inicio del archivo:

    from app.auth import require_admin

2️⃣ Modificar cada función agregando el parámetro:

    # Endpoint 1
    @router.post("/")
    def crear_cliente(
        cliente: ClienteCreate,
        db: Session = Depends(get_db),
        current_user = Depends(require_admin)  # ✅
    ):
        ...

    # Endpoint 2
    @router.get("/")
    def listar_clientes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user = Depends(require_admin)  # ✅
    ):
        ...

    # Y así con los 5 endpoints...

3️⃣ Actualizar docstrings (opcional):

    def crear_cliente(...):
        \"\"\"
        Crear cliente (Solo Administrador)
        \"\"\"


╔════════════════════════════════════════════════════════════════╗
║  🎯 CHECKLIST DE VERIFICACIÓN                                 ║
╚════════════════════════════════════════════════════════════════╝

Para cada archivo en app/routers/:

[ ] 1. Importar: from app.auth import require_admin
[ ] 2. Agregar a TODAS las funciones: current_user = Depends(require_admin)
[ ] 3. Verificar que compile sin errores
[ ] 4. Probar en /docs que pide autenticación (🔒 aparece en el endpoint)


╔════════════════════════════════════════════════════════════════╗
║  🔍 VERIFICAR QUE FUNCIONÓ                                    ║
╚════════════════════════════════════════════════════════════════╝

1. Inicia el servidor: uvicorn app.main:app --reload

2. Abre http://localhost:8000/docs

3. Verifica que cada endpoint tenga un candado 🔒

4. Intenta ejecutar un endpoint SIN autenticarte:
   ❌ Debería dar error 401: Not authenticated

5. Haz clic en "Authorize", ingresa token, y vuelve a intentar:
   ✅ Debería funcionar correctamente


╔════════════════════════════════════════════════════════════════╗
║  📌 NOTAS IMPORTANTES                                         ║
╚════════════════════════════════════════════════════════════════╝

⚠️  NO proteger el router de autenticación (app/routers/auth_router.py)
    porque necesita estar público para que los usuarios puedan hacer login.

⚠️  El endpoint /auth/me SÍ está protegido (necesita token para ver tu perfil).

⚠️  Recuerda crear un usuario administrador ANTES de proteger todo:
    python crear_admin.py


╔════════════════════════════════════════════════════════════════╗
║  🚀 SIGUIENTE PASO                                            ║
╚════════════════════════════════════════════════════════════════╝

Una vez protegidos todos los endpoints:

1. ✅ Crea usuario administrador: python crear_admin.py
2. ✅ Inicia el servidor: uvicorn app.main:app --reload
3. ✅ Prueba login en /docs con tus credenciales
4. ✅ Verifica que puedas acceder a todos los endpoints autenticado
5. ✅ Verifica que sin autenticación obtengas error 401

¡Listo! Tu API está completamente protegida 🎉

"""

if __name__ == "__main__":
    print(INSTRUCCIONES)
