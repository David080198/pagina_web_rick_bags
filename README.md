# RickBags E-commerce Platform

RickBags es una plataforma de e-commerce especializada en fundas protectoras premium para equipos musicales, desarrollada con Flask, Docker y tecnologías modernas.

## Características Principales

### 🎯 Especialización

- **Fundas para Amplificadores**: Prioridad en cubiertas para amplificadores de guitarra, bajo y teclado
- **Marcas Compatibles**: Marshall, Fender, Vox, Orange, Mesa Boogie, Yamaha, Roland
- **Personalización**: Sistema de diseño interactivo para fundas a medida

### 🎨 Diseño Profesional

- **Tema Negro y Rojo**: Paleta de colores formal y elegante (#000000, #CC0000)
- **Tipografía Premium**: Montserrat y Poppins para un look profesional
- **Responsive Design**: Optimizado para todos los dispositivos
- **Texturas Sutiles**: Efectos visuales que evocan calidad premium

### ⚡ Funcionalidades Técnicas

- **Autenticación Completa**: Login, registro, recuperación de contraseña
- **Sistema de Roles**: Usuarios regulares y administradores
- **Carrito Avanzado**: Sesiones persistentes con Redis
- **Personalización en Tiempo Real**: Calculadora de precios dinámica
- **Panel de Administración**: CRUD completo para productos, pedidos y usuarios
- **API REST**: Endpoints para búsqueda, carrito y wishlist

## Stack Tecnológico

### Backend

- **Flask 3.0**: Framework web principal
- **PostgreSQL**: Base de datos principal
- **Redis**: Cache y sesiones
- **SQLAlchemy**: ORM
- **Flask-Login**: Autenticación
- **Flask-Mail**: Sistema de emails
- **Gunicorn**: Servidor WSGI

### Frontend

- **HTML5/CSS3**: Estructura y estilos
- **JavaScript Vanilla**: Interactividad
- **Font Awesome**: Iconografía
- **Google Fonts**: Tipografías premium

### DevOps

- **Docker**: Contenedorización
- **Docker Compose**: Orquestación
- **Nginx**: Reverse proxy y servir archivos estáticos

## Estructura del Proyecto

```
rickbags/
├── app/
│   ├── blueprints/          # Módulos de la aplicación
│   │   ├── main.py         # Páginas principales
│   │   ├── auth.py         # Autenticación
│   │   ├── products.py     # Catálogo y productos
│   │   ├── cart.py         # Carrito y checkout
│   │   ├── admin.py        # Panel de administración
│   │   └── api.py          # API endpoints
│   ├── static/             # Archivos estáticos
│   │   ├── css/           # Estilos
│   │   ├── js/            # JavaScript
│   │   └── images/        # Imágenes
│   ├── templates/          # Plantillas HTML
│   ├── models.py          # Modelos de base de datos
│   ├── app.py            # Configuración principal
│   └── seed_data.py      # Datos de ejemplo
├── nginx/
│   └── nginx.conf        # Configuración de Nginx
├── db/
│   └── init.sql         # Scripts de inicialización
├── docker-compose.yml    # Configuración de contenedores
├── Dockerfile           # Imagen de la aplicación
└── requirements.txt     # Dependencias Python
```

## Instalación y Configuración

### Prerrequisitos

- Docker y Docker Compose
- Git

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd rickbags
```

2. **Configurar variables de entorno**

```bash
# Editar docker-compose.yml para actualizar:
# - SECRET_KEY: Clave secreta para la aplicación
# - Credenciales de base de datos
# - Configuración de email (opcional)
# - Keys de Stripe/PayPal (opcional)
```

3. **Construir y ejecutar**

```bash
docker-compose up --build
```

4. **Inicializar la base de datos**

```bash
# En otro terminal
docker-compose exec app python seed_data.py
```

5. **Acceder a la aplicación**

- **Sitio web**: http://localhost
- **Admin**: admin@rickbags.com / admin123
- **Cliente**: customer@example.com / customer123

## Configuración de Desarrollo

### Variables de Entorno

```env
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/rickbags
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Base de Datos

#### Modelos Principales

- **User**: Usuarios del sistema
- **Product**: Catálogo de productos
- **Category**: Categorías de productos
- **Brand**: Marcas de amplificadores
- **Material**: Materiales para fundas
- **Order**: Pedidos de clientes
- **Review**: Reseñas de productos

#### Relaciones Clave

- Productos pueden tener múltiples materiales (many-to-many)
- Usuarios pueden tener múltiples pedidos (one-to-many)
- Pedidos contienen múltiples items (one-to-many)
- Productos pueden tener reseñas (one-to-many)

## Funcionalidades Implementadas

### 🏠 Frontend Público

- [x] Página de inicio con hero banner
- [x] Catálogo de productos con filtros avanzados
- [x] Página de detalle de producto
- [x] Sistema de carrito de compras
- [x] Proceso de checkout en 3 pasos
- [x] Diseñador de fundas personalizadas
- [x] Sistema de búsqueda
- [x] Lista de deseos
- [x] Reseñas de productos

### 👤 Sistema de Usuarios

- [x] Registro y login
- [x] Recuperación de contraseña
- [x] Perfil de usuario
- [x] Historial de pedidos
- [x] Perfiles de equipos guardados

### 🛠️ Panel de Administración

- [x] Dashboard con métricas
- [x] Gestión de productos (CRUD)
- [x] Gestión de pedidos
- [x] Gestión de clientes
- [x] Moderación de reseñas
- [x] Configuración del sitio

### 🔧 API y Servicios

- [x] API REST para carrito
- [x] Búsqueda de productos
- [x] Calculadora de precios personalizada
- [x] Sistema de notificaciones
- [x] Newsletter

## Personalización de Fundas

El sistema incluye un diseñador interactivo que permite:

1. **Selección de Dimensiones**: Ancho, alto, profundidad
2. **Materiales Disponibles**:
   - Nylon Balístico 1680D
   - Vinilo Negro Premium
   - Cordura 500D
   - Cuero Sintético
3. **Opciones de Personalización**:
   - Color de bordes (rojo/negro)
   - Bolsillos adicionales
   - Tipo de funda (básica, premium, viaje, flight case)
4. **Cálculo de Precio en Tiempo Real**

## Seguridad

- **Autenticación**: Flask-Login con hash de contraseñas
- **Validación**: Validación de formularios del lado servidor
- **Rate Limiting**: Nginx con límites por IP
- **CORS**: Configuración segura
- **Headers de Seguridad**: X-Frame-Options, CSP, etc.
- **Sanitización**: Prevención de XSS y SQL injection

## Optimización y Performance

- **Nginx**: Compresión gzip, cache de archivos estáticos
- **Redis**: Cache de sesiones y datos temporales
- **Lazy Loading**: Carga diferida de imágenes
- **Minificación**: CSS y JS optimizados
- **Índices de BD**: Optimización de consultas

## Próximas Funcionalidades

- [ ] Integración de pagos (Stripe/PayPal)
- [ ] Sistema de envíos con tracking
- [ ] Chat de soporte en vivo
- [ ] Programa de fidelidad
- [ ] API móvil
- [ ] PWA (Progressive Web App)
- [ ] Análisis avanzado con gráficos
- [ ] Sistema de cupones y descuentos

## Contacto y Soporte

Para consultas técnicas o soporte:

- Email: tech@rickbags.com
- GitHub Issues: [Crear Issue]
- Documentación: [Wiki del proyecto]

## Licencia

Este proyecto está licenciado bajo [MIT License] - ver el archivo LICENSE para detalles.

---

**RickBags** - Protección Premium para tu Equipo Musical 🎸🎵
