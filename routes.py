from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import Product, Contact, CartItem
import uuid

def get_or_create_session_id():
    """Get or create a session ID for cart functionality"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_cart_count():
    """Get the current cart item count"""
    session_id = session.get('session_id')
    if not session_id:
        return 0
    try:
        result = db.session.query(db.func.sum(CartItem.quantity)).filter_by(session_id=session_id).scalar()
        return result or 0
    except:
        return 0

@app.route('/')
def index():
    """Pagina principală cu produsele recomandate"""
    featured_products = Product.query.filter_by(featured=True).limit(3).all()
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    cart_count = get_cart_count()
    return render_template('index.html', featured_products=featured_products, 
                         latest_products=latest_products, cart_count=cart_count)

@app.route('/produse')
def products():
    """Pagina cu toate produsele cu filtrare și căutare"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    cart_count = get_cart_count()
    
    return render_template('products.html', products=products, categories=categories, 
                         selected_category=category, search_term=search, cart_count=cart_count)

@app.route('/vaze')
def vaze():
    """Pagina dedicată vazelor"""
    products = Product.query.filter_by(category='Vaze').all()
    cart_count = get_cart_count()
    return render_template('category.html', products=products, category='Vaze', cart_count=cart_count)

@app.route('/ghivece')
def ghivece():
    """Pagina dedicată ghivecelor"""
    products = Product.query.filter_by(category='Ghivece').all()
    cart_count = get_cart_count()
    return render_template('category.html', products=products, category='Ghivece', cart_count=cart_count)

@app.route('/cercei')
def cercei():
    """Pagina dedicată cerceilor"""
    products = Product.query.filter_by(category='Cercei').all()
    cart_count = get_cart_count()
    return render_template('category.html', products=products, category='Cercei', cart_count=cart_count)

@app.route('/obiecte-decorative')
def obiecte_decorative():
    """Pagina dedicată obiectelor decorative"""
    products = Product.query.filter_by(category='Obiecte Decorative').all()
    cart_count = get_cart_count()
    return render_template('category.html', products=products, category='Obiecte Decorative', cart_count=cart_count)

@app.route('/produs/<int:product_id>')
def product_detail(product_id):
    """Pagina de detalii a produsului"""
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.in_stock == True
    ).limit(3).all()
    cart_count = get_cart_count()
    
    return render_template('product_detail.html', product=product, 
                         related_products=related_products, cart_count=cart_count)

@app.route('/adauga-in-cos/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adaugă produs în coș"""
    product = Product.query.get_or_404(product_id)
    
    if not product.in_stock or product.stock_quantity <= 0:
        flash('Produsul nu este disponibil în stoc.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    session_id = get_or_create_session_id()
    quantity = int(request.form.get('quantity', 1))
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(session_id=session_id, product_id=product_id).first()
    
    if cart_item:
        # Update quantity if already in cart
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            flash(f'Nu putem adăuga mai mult de {product.stock_quantity} bucăți.', 'error')
            return redirect(url_for('product_detail', product_id=product_id))
        cart_item.quantity = new_quantity
    else:
        # Add new item to cart
        if quantity > product.stock_quantity:
            flash(f'Nu putem adăuga mai mult de {product.stock_quantity} bucăți.', 'error')
            return redirect(url_for('product_detail', product_id=product_id))
        cart_item = CartItem(session_id=session_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    try:
        db.session.commit()
        flash(f'{product.name} a fost adăugat în coș!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('A apărut o eroare. Vă rugăm să încercați din nou.', 'error')
        app.logger.error(f'Cart error: {e}')
    
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cos')
def cart():
    """Pagina coșului de cumpărături"""
    session_id = session.get('session_id')
    cart_items = []
    total = 0
    
    if session_id:
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    
    cart_count = get_cart_count()
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)

@app.route('/actualizeaza-cos/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """Actualizează cantitatea unui produs din coș"""
    cart_item = CartItem.query.get_or_404(item_id)
    new_quantity = int(request.form.get('quantity', 1))
    
    if new_quantity <= 0:
        db.session.delete(cart_item)
        flash('Produsul a fost eliminat din coș.', 'success')
    elif new_quantity > cart_item.product.stock_quantity:
        flash(f'Nu avem suficiente bucăți în stoc. Maximum: {cart_item.product.stock_quantity}', 'error')
        return redirect(url_for('cart'))
    else:
        cart_item.quantity = new_quantity
        flash('Coșul a fost actualizat.', 'success')
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('A apărut o eroare. Vă rugăm să încercați din nou.', 'error')
        app.logger.error(f'Cart update error: {e}')
    
    return redirect(url_for('cart'))

@app.route('/elimina-din-cos/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """Elimină produs din coș"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Produsul a fost eliminat din coș.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('A apărut o eroare. Vă rugăm să încercați din nou.', 'error')
        app.logger.error(f'Cart removal error: {e}')
    
    return redirect(url_for('cart'))

@app.route('/despre')
def about():
    """Pagina despre noi"""
    cart_count = get_cart_count()
    return render_template('about.html', cart_count=cart_count)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Pagina de contact cu formularul de trimitere"""
    cart_count = get_cart_count()
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Basic validation
        if not all([name, email, subject, message]):
            flash('Vă rugăm să completați toate câmpurile.', 'error')
            return render_template('contact.html', cart_count=cart_count)
        
        # Save contact form submission
        contact_entry = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        try:
            db.session.add(contact_entry)
            db.session.commit()
            flash('Mulțumim pentru mesaj! Vă vom răspunde în curând.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            flash('A apărut o eroare la trimiterea mesajului. Vă rugăm să încercați din nou.', 'error')
            app.logger.error(f'Contact form error: {e}')
    
    return render_template('contact.html', cart_count=cart_count)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
