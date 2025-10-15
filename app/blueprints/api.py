from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user

bp = Blueprint('api', __name__)

@bp.route('/cart/count')
def cart_count():
    """Get current cart count"""
    from flask import session
    cart = session.get('cart', {})
    return jsonify({'count': len(cart)})

@bp.route('/products/search')
def search_products():
    """AJAX product search"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify([])
    
    from app.models import Product
    
    products = Product.query.filter(
        Product.name.contains(query),
        Product.active == True
    ).limit(limit).all()
    
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.main_image,
            'url': url_for('products.detail', product_id=product.id)
        })
    
    return jsonify(results)

@bp.route('/products/filters')
def product_filters():
    """Get available filter options"""
    from app.models import Brand, Material, Category
    
    brands = [{'id': b.id, 'name': b.name} for b in Brand.query.all()]
    materials = [{'id': m.id, 'name': m.name} for m in Material.query.all()]
    categories = [{'id': c.id, 'name': c.name} for c in Category.query.all()]
    
    return jsonify({
        'brands': brands,
        'materials': materials,
        'categories': categories
    })

@bp.route('/contact', methods=['POST'])
def contact_form():
    """Handle contact form submission"""
    from app import mail
    from flask_mail import Message
    
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject', 'Consulta desde el sitio web')
    message = request.form.get('message')
    
    if not all([name, email, message]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400
    
    # Send email
    msg = Message(
        f'Contacto: {subject}',
        recipients=['info@rickbags.com']
    )
    msg.body = f'''
Nuevo mensaje de contacto:

Nombre: {name}
Email: {email}
Asunto: {subject}

Mensaje:
{message}
'''
    
    try:
        mail.send(msg)
        return jsonify({'message': 'Mensaje enviado exitosamente'})
    except Exception as e:
        return jsonify({'error': 'Error al enviar el mensaje'}), 500

@bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Newsletter subscription"""
    from app.models import NewsletterSubscriber
    from app import db
    
    email = request.form.get('email')
    
    if not email:
        return jsonify({'error': 'Email requerido'}), 400
    
    # Check if already subscribed
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': 'Ya estás suscrito a nuestro newsletter'})
    
    subscriber = NewsletterSubscriber(email=email)
    db.session.add(subscriber)
    db.session.commit()
    
    return jsonify({'message': 'Suscripción exitosa'})

@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add product to wishlist"""
    from app.models import Wishlist, Product
    from app import db
    
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing:
        return jsonify({'message': 'Producto ya está en tu lista de deseos'})
    
    wishlist_item = Wishlist(
        user_id=current_user.id,
        product_id=product_id
    )
    
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({'message': 'Producto agregado a tu lista de deseos'})

@bp.route('/wishlist/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(product_id):
    """Remove product from wishlist"""
    from app.models import Wishlist
    from app import db
    
    wishlist_item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first_or_404()
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    return jsonify({'message': 'Producto eliminado de tu lista de deseos'})