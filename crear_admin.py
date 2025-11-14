"""
Script para crear el primer usuario Administrador
Ejecutar con: python crear_admin.py
"""
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.auth import get_password_hash


def crear_usuario_administrador():
    db = SessionLocal()

    try:
        # 1. Buscar o crear rol Administrador
        print("🔍 Buscando rol 'Administrador'...")
        rol_admin = db.query(Rol).filter(
            Rol.nombre_rol == "Administrador").first()

        if not rol_admin:
            print("📝 Creando rol 'Administrador'...")
            rol_admin = Rol(nombre_rol="Administrador")
            db.add(rol_admin)
            db.commit()
            db.refresh(rol_admin)
            print(f"✅ Rol creado con ID: {rol_admin.id_rol}")
        else:
            print(f"✅ Rol encontrado con ID: {rol_admin.id_rol}")

        # 2. Verificar si ya existe el usuario admin
        usuario_existente = db.query(Usuario).filter(
            Usuario.nombre_usuario == "admin"
        ).first()

        if usuario_existente:
            print("⚠️  Ya existe un usuario 'admin'")
            respuesta = input("¿Deseas actualizar su contraseña? (s/n): ")

            if respuesta.lower() == 's':
                nueva_password = input("Ingresa la nueva contraseña: ")
                usuario_existente.contrasena_hash = get_password_hash(
                    nueva_password)
                db.commit()
                print("✅ Contraseña actualizada exitosamente")
            return

        # 3. Crear usuario administrador
        print("\n📝 Creando usuario administrador...")

        # Solicitar datos
        username = input(
            "Nombre de usuario (default: admin): ").strip() or "admin"
        password = input(
            "Contraseña (default: admin123): ").strip() or "admin123"
        nombre_completo = input(
            "Nombre completo (default: Administrador): ").strip() or "Administrador"

        usuario_admin = Usuario(
            nombre_usuario=username,
            contrasena_hash=get_password_hash(password),
            nombre_completo=nombre_completo,
            id_rol=rol_admin.id_rol
        )

        db.add(usuario_admin)
        db.commit()
        db.refresh(usuario_admin)

        print("\n" + "="*50)
        print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
        print("="*50)
        print(f"ID: {usuario_admin.id_usuario}")
        print(f"Usuario: {usuario_admin.nombre_usuario}")
        print(f"Nombre: {usuario_admin.nombre_completo}")
        print(f"Rol: {rol_admin.nombre_rol}")
        print("="*50)
        print("\n🎉 Ahora puedes iniciar sesión en /docs con POST /auth/login")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    print("="*50)
    print("🔐 CREADOR DE USUARIO ADMINISTRADOR")
    print("="*50)
    print()
    crear_usuario_administrador()
