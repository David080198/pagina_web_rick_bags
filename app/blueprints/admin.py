from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acceso denegado', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with metrics"""
    from app.models import Order, Product, User
    from app import db
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Calculate metrics
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total)).scalar() or 0
    pending_orders = Order.query.filter_by(status='pending').count()
    total_products = Product.query.count()
    total_users = User.query.count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Monthly revenue chart data
    monthly_revenue = db.session.query(
        func.date_trunc('month', Order.created_at).label('month'),
        func.sum(Order.total).label('revenue')
    ).filter(
        Order.created_at >= month_ago
    ).group_by(
        func.date_trunc('month', Order.created_at)
    ).all()
    
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         pending_orders=pending_orders,
                         total_products=total_products,
                         total_users=total_users,
                         recent_orders=recent_orders,
                         monthly_revenue=monthly_revenue)

@bp.route('/orders')
@login_required
@admin_required
def orders():
    """Order management"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    from app.models import Order
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, current_status=status)

@bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    """Order detail view"""
    from app.models import Order
    
    order = Order.query.get_or_404(order_id)
    
    return render_template('admin/order_detail.html', order=order)

@bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """Update order status"""
    from app.models import Order
    from app import db
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    tracking_number = request.form.get('tracking_number')
    
    order.status = new_status
    if tracking_number:
        order.tracking_number = tracking_number
    
    db.session.commit()
    
    # TODO: Send email notification to customer
    
    flash(f'Estado del pedido #{order.order_number} actualizado', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))

@bp.route('/products')
@login_required
@admin_required
def products():
    """Product management"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category')
    
    from app.models import Product, Category
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         current_category=category_id)

@bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():
    """Create new product"""
    if request.method == 'POST':
        from app.models import Product
        from app import db
        
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category_id=int(request.form.get('category_id')),
            brand_id=int(request.form.get('brand_id')),
            sku=request.form.get('sku'),
            stock_quantity=int(request.form.get('stock_quantity', 0)),
            active=request.form.get('active') == 'on',
            featured=request.form.get('featured') == 'on'
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Producto "{product.name}" creado exitosamente', 'success')
        return redirect(url_for('admin.products'))
    
    from app.models import Category, Brand
    categories = Category.query.all()
    brands = Brand.query.all()
    
    return render_template('admin/product_form.html', 
                         categories=categories, 
                         brands=brands)

@bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Edit existing product"""
    from app.models import Product
    from app import db
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category_id = int(request.form.get('category_id'))
        product.brand_id = int(request.form.get('brand_id'))
        product.sku = request.form.get('sku')
        product.stock_quantity = int(request.form.get('stock_quantity', 0))
        product.active = request.form.get('active') == 'on'
        product.featured = request.form.get('featured') == 'on'
        
        db.session.commit()
        
        flash(f'Producto "{product.name}" actualizado exitosamente', 'success')
        return redirect(url_for('admin.products'))
    
    from app.models import Category, Brand
    categories = Category.query.all()
    brands = Brand.query.all()
    
    return render_template('admin/product_form.html', 
                         product=product,
                         categories=categories, 
                         brands=brands)

@bp.route('/customers')
@login_required
@admin_required
def customers():
    """Customer management"""
    page = request.args.get('page', 1, type=int)
    
    from app.models import User
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/customers.html', users=users)

@bp.route('/customers/<int:user_id>')
@login_required
@admin_required
def customer_detail(user_id):
    """Customer detail view"""
    from app.models import User, Order
    
    user = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    return render_template('admin/customer_detail.html', user=user, orders=orders)

@bp.route('/reviews')
@login_required
@admin_required
def reviews():
    """Review management"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    from app.models import Review
    
    query = Review.query
    
    if status == 'pending':
        query = query.filter_by(approved=False)
    elif status == 'approved':
        query = query.filter_by(approved=True)
    
    reviews = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/reviews.html', reviews=reviews, current_status=status)

@bp.route('/reviews/<int:review_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_review(review_id):
    """Approve review"""
    from app.models import Review
    from app import db
    
    review = Review.query.get_or_404(review_id)
    review.approved = True
    db.session.commit()
    
    flash('Reseña aprobada', 'success')
    return redirect(url_for('admin.reviews'))

@bp.route('/settings')
@login_required
@admin_required
def settings():
    """Site settings"""
    return render_template('admin/settings.html')