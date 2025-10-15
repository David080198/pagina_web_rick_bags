"""Sample data for RickBags"""

from app import create_app, db
from app.models import Category, Brand, Material, CaseType, Product, User
from datetime import datetime
import json

def seed_database():
    """Populate database with sample data"""
    
    # Create categories
    categories_data = [
        {
            'name': 'Fundas para Amplificadores',
            'slug': 'fundas-amplificadores',
            'description': 'Fundas protectoras para amplificadores de guitarra, bajo y teclado',
            'sort_order': 1
        },
        {
            'name': 'Fundas para Guitarras',
            'slug': 'fundas-guitarras',
            'description': 'Fundas y estuches para guitarras eléctricas y acústicas',
            'sort_order': 2
        },
        {
            'name': 'Fundas para Teclados',
            'slug': 'fundas-teclados',
            'description': 'Fundas protectoras para teclados y pianos digitales',
            'sort_order': 3
        },
        {
            'name': 'Accesorios',
            'slug': 'accesorios',
            'description': 'Accesorios y complementos para músicos',
            'sort_order': 4
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories.append(category)
    
    db.session.flush()
    
    # Create brands
    brands_data = [
        {'name': 'Marshall', 'slug': 'marshall', 'description': 'Amplificadores icónicos de rock'},
        {'name': 'Fender', 'slug': 'fender', 'description': 'Amplificadores clásicos americanos'},
        {'name': 'Vox', 'slug': 'vox', 'description': 'Amplificadores británicos vintage'},
        {'name': 'Orange', 'slug': 'orange', 'description': 'Amplificadores con carácter distintivo'},
        {'name': 'Mesa Boogie', 'slug': 'mesa-boogie', 'description': 'Amplificadores de alta gama'},
        {'name': 'Yamaha', 'slug': 'yamaha', 'description': 'Instrumentos y amplificadores versátiles'},
        {'name': 'Roland', 'slug': 'roland', 'description': 'Tecnología musical innovadora'}
    ]
    
    brands = []
    for brand_data in brands_data:
        brand = Brand(**brand_data)
        db.session.add(brand)
        brands.append(brand)
    
    db.session.flush()
    
    # Create materials
    materials_data = [
        {
            'name': 'Nylon Balístico 1680D',
            'description': 'Material ultra resistente con excelente protección contra impactos',
            'price_per_unit': 25.00,
            'properties': {
                'waterproof': True,
                'padding_thickness': 15,
                'tear_resistance': 'high',
                'weight': 'medium'
            }
        },
        {
            'name': 'Vinilo Negro Premium',
            'description': 'Vinilo de alta calidad con acabado profesional',
            'price_per_unit': 18.00,
            'properties': {
                'waterproof': True,
                'padding_thickness': 10,
                'tear_resistance': 'medium',
                'weight': 'light'
            }
        },
        {
            'name': 'Cordura 500D',
            'description': 'Material ligero pero resistente, ideal para uso frecuente',
            'price_per_unit': 20.00,
            'properties': {
                'waterproof': False,
                'padding_thickness': 12,
                'tear_resistance': 'medium',
                'weight': 'light'
            }
        },
        {
            'name': 'Cuero Sintético',
            'description': 'Acabado elegante con gran durabilidad',
            'price_per_unit': 30.00,
            'properties': {
                'waterproof': True,
                'padding_thickness': 8,
                'tear_resistance': 'high',
                'weight': 'heavy'
            }
        }
    ]
    
    materials = []
    for mat_data in materials_data:
        material = Material(**mat_data)
        db.session.add(material)
        materials.append(material)
    
    db.session.flush()
    
    # Create case types
    case_types_data = [
        {
            'name': 'Funda Básica',
            'description': 'Protección estándar con acolchado básico',
            'price_multiplier': 1.0
        },
        {
            'name': 'Funda Premium',
            'description': 'Protección superior con acolchado extra y bolsillos',
            'price_multiplier': 1.3
        },
        {
            'name': 'Funda de Viaje',
            'description': 'Máxima protección para transporte profesional',
            'price_multiplier': 1.6
        },
        {
            'name': 'Flight Case',
            'description': 'Protección industrial con estructura rígida',
            'price_multiplier': 2.0
        }
    ]
    
    case_types = []
    for ct_data in case_types_data:
        case_type = CaseType(**ct_data)
        db.session.add(case_type)
        case_types.append(case_type)
    
    db.session.flush()
    
    # Create sample products
    products_data = [
        {
            'name': 'Funda Marshall JCM800 Head',
            'slug': 'funda-marshall-jcm800-head',
            'description': 'Funda premium para cabezal Marshall JCM800. Fabricada en nylon balístico 1680D con acolchado de 15mm. Incluye bolsillo frontal para cables y accesorios.',
            'short_description': 'Funda premium para cabezal Marshall JCM800',
            'price': 89.99,
            'compare_price': 119.99,
            'sku': 'RICK-MAR-JCM800',
            'stock_quantity': 25,
            'weight': 800,
            'dimensions': {'width': 68, 'height': 26, 'depth': 24},
            'compatibility': ['Marshall JCM800 2203', 'Marshall JCM800 2204'],
            'main_image': '/static/images/products/marshall-jcm800-cover.jpg',
            'images': [
                '/static/images/products/marshall-jcm800-cover.jpg',
                '/static/images/products/marshall-jcm800-cover-2.jpg'
            ],
            'features': [
                'Nylon balístico 1680D ultra resistente',
                'Acolchado de 15mm de grosor',
                'Bolsillo frontal con cierre',
                'Asas reforzadas',
                'Bordes en color rojo característico'
            ],
            'specifications': {
                'material': 'Nylon balístico 1680D',
                'padding': '15mm foam',
                'color': 'Negro con detalles rojos',
                'closure': 'Velcro heavy duty',
                'handles': '2 asas laterales reforzadas'
            },
            'category_id': 1,
            'brand_id': 1,
            'featured': True,
            'active': True
        },
        {
            'name': 'Funda Fender Twin Reverb Combo',
            'slug': 'funda-fender-twin-reverb-combo',
            'description': 'Funda profesional para amplificador combo Fender Twin Reverb. Protección completa con material de alta calidad.',
            'short_description': 'Funda profesional para Fender Twin Reverb',
            'price': 129.99,
            'sku': 'RICK-FEN-TWIN',
            'stock_quantity': 15,
            'weight': 1200,
            'dimensions': {'width': 66, 'height': 61, 'depth': 26},
            'compatibility': ['Fender Twin Reverb 85W', 'Fender Twin Reverb Reissue'],
            'main_image': '/static/images/products/fender-twin-cover.jpg',
            'features': [
                'Material premium resistente al agua',
                'Acolchado extra grueso',
                'Acceso trasero para cables',
                'Bolsillos laterales',
                'Diseño ergonómico'
            ],
            'category_id': 1,
            'brand_id': 2,
            'featured': True,
            'active': True
        },
        {
            'name': 'Funda Vox AC30 Combo',
            'slug': 'funda-vox-ac30-combo',
            'description': 'Funda especializada para el icónico amplificador Vox AC30. Diseñada específicamente para las dimensiones exactas del AC30.',
            'short_description': 'Funda especializada para Vox AC30',
            'price': 109.99,
            'sku': 'RICK-VOX-AC30',
            'stock_quantity': 20,
            'weight': 1000,
            'dimensions': {'width': 70, 'height': 55, 'depth': 28},
            'compatibility': ['Vox AC30C2', 'Vox AC30CC2', 'Vox AC30VR'],
            'main_image': '/static/images/products/vox-ac30-cover.jpg',
            'category_id': 1,
            'brand_id': 3,
            'active': True
        }
    ]
    
    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        db.session.add(product)
        products.append(product)
    
    db.session.flush()
    
    # Create admin user
    admin_user = User(
        email='admin@rickbags.com',
        first_name='Admin',
        last_name='RickBags',
        is_admin=True,
        is_active=True
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Create sample customer
    customer = User(
        email='customer@example.com',
        first_name='Juan',
        last_name='Pérez',
        phone='+34 600 123 456',
        is_admin=False,
        is_active=True
    )
    customer.set_password('customer123')
    db.session.add(customer)
    
    db.session.commit()
    
    print("Database seeded successfully!")
    print("Admin user: admin@rickbags.com / admin123")
    print("Customer user: customer@example.com / customer123")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed data
        seed_database()