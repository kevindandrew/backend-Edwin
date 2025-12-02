# 🏥 Sistema de Gestión de Equipos Biomédicos (Edwin Backend)

Este proyecto es una API robusta y escalable construida con **FastAPI** para la gestión integral de equipos biomédicos, mantenimiento, ventas y control de inventario. Está diseñado siguiendo las mejores prácticas de desarrollo moderno en Python, con un fuerte enfoque en la seguridad, modularidad y rendimiento.

---

## 🛠️ Tecnologías Utilizadas

El proyecto utiliza un stack tecnológico moderno y eficiente:

### Core Framework

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno y de alto rendimiento para construir APIs con Python 3.8+.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para producción, rápido y ligero.
- **[Pydantic](https://docs.pydantic.dev/)**: Validación de datos y gestión de configuraciones mediante anotaciones de tipo.

### Base de Datos & ORM

- **[PostgreSQL](https://www.postgresql.org/)**: Sistema de gestión de bases de datos relacional robusto y potente.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Toolkit SQL y ORM (Object Relational Mapper) para Python.
- **[Psycopg2](https://www.psycopg.org/)**: Adaptador de base de datos PostgreSQL para Python.

### Seguridad & Autenticación

- **[PyJWT](https://pyjwt.readthedocs.io/)**: Implementación de JSON Web Tokens (JWT) para autenticación segura sin estado.
- **[Passlib (con Bcrypt)](https://passlib.readthedocs.io/)**: Hashing seguro de contraseñas.
- **[Python-Jose](https://python-jose.readthedocs.io/)**: Implementación de estándares JOSE (Javascript Object Signing and Encryption).
- **[Python-Multipart](https://github.com/Kludex/python-multipart)**: Soporte para streaming de formularios multipart (necesario para OAuth2).

### Utilidades

- **[Python-Dotenv](https://saurabh-kumar.com/python-dotenv/)**: Gestión de variables de entorno desde archivos `.env`.
- **[Email-Validator](https://pypi.org/project/email-validator/)**: Validación robusta de direcciones de correo electrónico.

---

## 🔐 Seguridad y Autenticación

La seguridad es un pilar fundamental de este proyecto. Implementamos un esquema de seguridad en profundidad:

### 1. Autenticación JWT (JSON Web Tokens)

El sistema utiliza autenticación basada en tokens **Bearer JWT**.

- **Sin Estado (Stateless)**: El servidor no necesita almacenar sesiones, lo que facilita la escalabilidad.
- **Flujo**:
  1. El usuario envía credenciales (`username`, `password`) al endpoint `/auth/login`.
  2. Si son válidas, el servidor devuelve un `access_token` firmado.
  3. El cliente debe enviar este token en el header `Authorization: Bearer <token>` en cada petición subsiguiente.

### 2. Control de Acceso Basado en Roles (RBAC)

Implementamos un sistema granular de permisos:

- **Roles Definidos**: Administrador, Técnico, Vendedor, etc.
- **Protección de Endpoints**: Cada ruta puede requerir un rol específico o un conjunto de ellos.
- **Decoradores Personalizados**: Utilizamos dependencias de FastAPI (`Depends`) para verificar roles antes de ejecutar la lógica del endpoint (ej. `require_admin`, `require_admin_or_tecnico`).

### 3. Hashing de Contraseñas

- **Nunca** almacenamos contraseñas en texto plano.
- Utilizamos **Bcrypt**, un algoritmo de hashing adaptativo diseñado para ser lento y resistente a ataques de fuerza bruta.

### 4. Variables de Entorno

- La configuración sensible (como `SECRET_KEY`, `DATABASE_URL`) se gestiona exclusivamente a través de variables de entorno, evitando exponer secretos en el código fuente.

---

## 🏗️ Arquitectura y Estructura del Proyecto

El proyecto sigue una arquitectura **Modular Monolith**, organizando el código por dominios funcionales para facilitar el mantenimiento y la escalabilidad.

### Estructura de Directorios

```plaintext
edwin-backend/
├── app/
│   ├── models/          # Modelos ORM (SQLAlchemy) - Representan las tablas de la BD
│   │   ├── usuario.py
│   │   ├── equipo_biomedico.py
│   │   └── ...
│   ├── routers/         # Controladores (Endpoints) - Manejan las peticiones HTTP
│   │   ├── auth_router.py
│   │   ├── equipo_biomedico_router.py
│   │   └── ...
│   ├── schemas/         # Esquemas Pydantic - Validación y serialización de datos (DTOs)
│   │   ├── usuario.py
│   │   ├── equipo.py
│   │   └── ...
│   ├── auth.py          # Lógica central de autenticación y seguridad
│   ├── database.py      # Configuración de conexión a BD y sesión
│   └── main.py          # Punto de entrada de la aplicación
├── .env                 # Variables de entorno (no commitear)
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

### Patrones de Diseño

- **Separación de Responsabilidades**:
  - **Routers**: Solo manejan la capa HTTP (request/response).
  - **Schemas**: Definen qué datos entran y salen (Validación).
  - **Models**: Definen la estructura de datos persistente.
  - **Database**: Gestiona la conexión y el ciclo de vida de la sesión.
- **Inyección de Dependencias**: FastAPI inyecta la sesión de base de datos (`db: Session`) y el usuario actual (`current_user`) en cada endpoint, facilitando el testing y la modularidad.

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.8 o superior
- PostgreSQL instalado y corriendo

### Pasos

1.  **Clonar el repositorio**

    ```bash
    git clone <url-del-repo>
    cd edwin-backend
    ```

2.  **Crear entorno virtual**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Instalar dependencias**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**
    Crea un archivo `.env` en la raíz basado en el ejemplo:

    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/edwin_db
    SECRET_KEY=tu_clave_secreta_super_segura
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Ejecutar la aplicación**

    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Acceder a la documentación**
    Abre tu navegador en:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

---

## 📚 Documentación de API

La API es autodocumentada gracias a OpenAPI (Swagger).

- **Interactivo**: Puedes probar los endpoints directamente desde `/docs`.
- **Autenticación en Docs**: Usa el botón "Authorize" en la parte superior derecha de Swagger UI e ingresa tu token (o credenciales si usas el flujo OAuth2) para probar endpoints protegidos.

---

## 👥 Contribución

1.  Haz un Fork del proyecto.
2.  Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`).
3.  Committea tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Push a la rama (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.
