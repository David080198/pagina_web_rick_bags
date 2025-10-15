# Instrucciones de Instalación Rápida - RickBags

## 🚀 Instalación con Docker (Recomendado)

### Prerrequisitos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/David080198/pagina_web_rick_bags.git
cd pagina_web_rick_bags
```

2. **Configurar variables de entorno** (Opcional)
```bash
# Editar docker-compose.yml para personalizar:
# - SECRET_KEY (para producción)
# - Credenciales de base de datos
# - Configuración de email
```

3. **Ejecutar la aplicación**
```bash
docker-compose up --build
```

4. **Inicializar la base de datos** (En otra terminal)
```bash
docker-compose exec app python seed_data.py
```

5. **Acceder a la aplicación**
- **Sitio web**: http://localhost
- **Usuario Admin**: admin@rickbags.com / admin123
- **Usuario Cliente**: customer@example.com / customer123

## 🛠️ Instalación Local (Desarrollo)

### Prerrequisitos
- Python 3.11+
- PostgreSQL 15+
- Redis

### Pasos

1. **Clonar y configurar entorno virtual**
```bash
git clone https://github.com/David080198/pagina_web_rick_bags.git
cd pagina_web_rick_bags
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
# Crear base de datos PostgreSQL
createdb rickbags_db

# Configurar variables de entorno
export DATABASE_URL="postgresql://user:password@localhost/rickbags_db"
export SECRET_KEY="your-secret-key"
export REDIS_URL="redis://localhost:6379/0"
```

4. **Inicializar base de datos**
```bash
cd app
python seed_data.py
```

5. **Ejecutar aplicación**
```bash
python app.py
```

## 📊 Usuarios de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| Admin | admin@rickbags.com | admin123 | Administrador |
| Cliente | customer@example.com | customer123 | Cliente |

## 🔧 Configuración Adicional

### Variables de Entorno
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@localhost:5432/rickbags
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Personalización
- Editar `app/static/css/style.css` para cambios de diseño
- Modificar `app/templates/` para cambios en las plantillas
- Agregar productos en `app/seed_data.py`

## 📚 Documentación Completa

Ver [README.md](README.md) para documentación completa del proyecto.

## 🆘 Soporte

Si encuentras problemas:
1. Revisa que Docker esté ejecutándose
2. Verifica que los puertos 80, 5432 y 6379 estén disponibles
3. Consulta los logs: `docker-compose logs`
4. Crea un [Issue en GitHub](https://github.com/David080198/pagina_web_rick_bags/issues)