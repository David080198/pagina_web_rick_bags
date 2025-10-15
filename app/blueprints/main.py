from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page with hero banner and featured products"""
    from models import Product, Category
    
    # Get featured products
    featured_products = Product.query.filter_by(featured=True).limit(8).all()
    
    # Get main categories
    categories = Category.query.filter_by(parent_id=None).all()
    
    return render_template('main/index.html', 
                         featured_products=featured_products,
                         categories=categories)

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@bp.route('/faq')
def faq():
    """FAQ page"""
    return render_template('main/faq.html')

@bp.route('/terms')
def terms():
    """Terms and conditions"""
    return render_template('main/terms.html')

@bp.route('/privacy')
def privacy():
    """Privacy policy"""
    return render_template('main/privacy.html')

@bp.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('products.catalog'))
    
    from models import Product
    products = Product.query.filter(
        Product.name.contains(query) | 
        Product.description.contains(query)
    ).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('main/search_results.html', 
                         products=products, 
                         query=query)