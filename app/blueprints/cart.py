from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user

bp = Blueprint('cart', __name__)

@bp.route('/')
def view_cart():
    """View cart contents"""
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    return render_template('cart/view.html', cart=cart, total=total)

@bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    from app.models import Product
    
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    product_key = str(product_id)
    
    if product_key in cart:
        cart[product_key]['quantity'] += quantity
    else:
        cart[product_key] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.main_image,
            'quantity': quantity
        }
    
    session['cart'] = cart
    flash(f'{product.name} agregado al carrito', 'success')
    
    if request.is_json:
        return jsonify({
            'message': 'Producto agregado al carrito',
            'cart_count': len(cart)
        })
    
    return redirect(url_for('products.detail', product_id=product_id))

@bp.route('/update/<product_key>', methods=['POST'])
def update_cart(product_key):
    """Update cart item quantity"""
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 0))
    
    if product_key in cart:
        if quantity > 0:
            cart[product_key]['quantity'] = quantity
        else:
            del cart[product_key]
        
        session['cart'] = cart
        flash('Carrito actualizado', 'success')
    
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove/<product_key>')
def remove_from_cart(product_key):
    """Remove item from cart"""
    cart = session.get('cart', {})
    
    if product_key in cart:
        del cart[product_key]
        session['cart'] = cart
        flash('Producto eliminado del carrito', 'success')
    
    return redirect(url_for('cart.view_cart'))

@bp.route('/clear')
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    flash('Carrito vaciado', 'info')
    return redirect(url_for('cart.view_cart'))

@bp.route('/checkout')
@login_required
def checkout():
    """Checkout process - step 1: shipping"""
    cart = session.get('cart', {})
    
    if not cart:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    return render_template('cart/checkout_shipping.html', cart=cart, total=total)

@bp.route('/checkout/payment', methods=['POST'])
@login_required
def checkout_payment():
    """Checkout process - step 2: payment"""
    cart = session.get('cart', {})
    
    if not cart:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # Save shipping info to session
    session['shipping'] = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'address': request.form.get('address'),
        'city': request.form.get('city'),
        'state': request.form.get('state'),
        'zip_code': request.form.get('zip_code'),
        'country': request.form.get('country'),
        'phone': request.form.get('phone')
    }
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    shipping_cost = 15.0  # Fixed shipping cost
    tax = total * 0.08  # 8% tax
    final_total = total + shipping_cost + tax
    
    return render_template('cart/checkout_payment.html', 
                         cart=cart, 
                         total=total,
                         shipping_cost=shipping_cost,
                         tax=tax,
                         final_total=final_total)

@bp.route('/checkout/process', methods=['POST'])
@login_required
def process_checkout():
    """Process the order"""
    from app.models import Order, OrderItem
    from app import db
    import uuid
    
    cart = session.get('cart', {})
    shipping = session.get('shipping', {})
    
    if not cart or not shipping:
        flash('Error en el proceso de compra', 'error')
        return redirect(url_for('cart.view_cart'))
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    shipping_cost = 15.0
    tax = subtotal * 0.08
    total = subtotal + shipping_cost + tax
    
    # Create order
    order = Order(
        user_id=current_user.id,
        order_number=str(uuid.uuid4())[:8].upper(),
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax=tax,
        total=total,
        status='pending',
        shipping_address=f"{shipping['address']}, {shipping['city']}, {shipping['state']} {shipping['zip_code']}, {shipping['country']}",
        shipping_phone=shipping['phone']
    )
    
    db.session.add(order)
    db.session.flush()  # Get the order ID
    
    # Create order items
    for item in cart.values():
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['id'] if isinstance(item['id'], int) else None,
            product_name=item['name'],
            price=item['price'],
            quantity=item['quantity'],
            custom_specs=item.get('custom_specs')
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    # Clear cart and shipping info
    session['cart'] = {}
    session.pop('shipping', None)
    
    flash(f'Pedido #{order.order_number} creado exitosamente', 'success')
    return redirect(url_for('cart.order_confirmation', order_id=order.id))

@bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    from app.models import Order
    
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    return render_template('cart/order_confirmation.html', order=order)