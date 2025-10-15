from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
import secrets

bp = Blueprint('products', __name__)

@bp.route('/catalog')
def catalog():
    """Product catalog with filtering"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category')
    brand = request.args.get('brand')
    material = request.args.get('material')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'name')
    
    from models import Product, Category, Brand
    
    # Base query
    query = Product.query.filter_by(active=True)
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if brand:
        query = query.join(Brand).filter(Brand.name == brand)
    
    if material:
        query = query.filter(Product.materials.any(name=material))
    
    if min_price:
        query = query.filter(Product.price >= min_price)
    
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    
    # Get filter options
    categories = Category.query.all()
    brands = Brand.query.all()
    from models import Material
    materials = Material.query.all()
    
    return render_template('products/catalog.html',
                         products=products,
                         categories=categories,
                         brands=brands,
                         materials=materials,
                         current_filters={
                             'category_id': category_id,
                             'brand': brand,
                             'material': material,
                             'min_price': min_price,
                             'max_price': max_price,
                             'sort': sort_by
                         })

@bp.route('/<int:product_id>')
def detail(product_id):
    """Product detail page"""
    from models import Product, Review
    
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id, approved=True).order_by(Review.created_at.desc()).limit(10).all()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.active == True
    ).limit(4).all()
    
    return render_template('products/detail.html',
                         product=product,
                         reviews=reviews,
                         related_products=related_products)

@bp.route('/custom-case')
def custom_case():
    """Custom case designer"""
    from models import Material, CaseType
    
    materials = Material.query.filter_by(available_for_custom=True).all()
    case_types = CaseType.query.all()
    
    return render_template('products/custom_case.html',
                         materials=materials,
                         case_types=case_types)

@bp.route('/calculate-custom-price', methods=['POST'])
def calculate_custom_price():
    """Calculate price for custom case"""
    data = request.get_json()
    
    width = float(data.get('width', 0))
    height = float(data.get('height', 0))
    depth = float(data.get('depth', 0))
    material_id = data.get('material_id')
    case_type_id = data.get('case_type_id')
    extra_pockets = int(data.get('extra_pockets', 0))
    
    from models import Material, CaseType
    
    material = Material.query.get(material_id)
    case_type = CaseType.query.get(case_type_id)
    
    if not material or not case_type:
        return jsonify({'error': 'Material o tipo de funda inválido'}), 400
    
    # Calculate base price
    volume = width * height * depth / 1000  # Convert to liters
    base_price = volume * material.price_per_unit * case_type.price_multiplier
    
    # Add extras
    pocket_price = extra_pockets * 15.0  # $15 per extra pocket
    
    total_price = base_price + pocket_price
    
    return jsonify({
        'base_price': round(base_price, 2),
        'pocket_price': round(pocket_price, 2),
        'total_price': round(total_price, 2),
        'volume': round(volume, 2)
    })

@bp.route('/add-custom-to-cart', methods=['POST'])
def add_custom_to_cart():
    """Add custom case to cart"""
    data = request.get_json()
    
    # Validate data
    required_fields = ['width', 'height', 'depth', 'material_id', 'case_type_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # Calculate price
    price_data = calculate_custom_price()
    if price_data.status_code != 200:
        return price_data
    
    price_info = price_data.get_json()
    
    # Create custom product data
    custom_product = {
        'id': 'custom_' + secrets.token_urlsafe(8),
        'name': 'Funda Personalizada',
        'price': price_info['total_price'],
        'image': '/static/images/custom-case-placeholder.jpg',
        'custom_specs': {
            'width': data['width'],
            'height': data['height'],
            'depth': data['depth'],
            'material_id': data['material_id'],
            'case_type_id': data['case_type_id'],
            'extra_pockets': data.get('extra_pockets', 0),
            'border_color': data.get('border_color', 'black')
        },
        'quantity': 1
    }
    
    # Add to session cart
    cart = session.get('cart', {})
    cart[custom_product['id']] = custom_product
    session['cart'] = cart
    
    return jsonify({'message': 'Funda personalizada agregada al carrito', 'cart_count': len(cart)})

@bp.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    """Add product review"""
    from models import Review, Product
    from models import db
    
    product = Product.query.get_or_404(product_id)
    
    # Check if user already reviewed this product
    existing_review = Review.query.filter_by(
        product_id=product_id,
        user_id=current_user.id
    ).first()
    
    if existing_review:
        flash('Ya has dejado una reseña para este producto', 'warning')
        return redirect(url_for('products.detail', product_id=product_id))
    
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    
    review = Review(
        product_id=product_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash('Reseña enviada. Será revisada antes de ser publicada.', 'success')
    return redirect(url_for('products.detail', product_id=product_id))