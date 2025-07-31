from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    image_source = db.Column(db.String(100), nullable=False)  # Leonardo AI, etc.
    video_url = db.Column(db.String(500))
    video_source = db.Column(db.String(100))  # Synthesia, etc.
    audio_url = db.Column(db.String(500))
    audio_source = db.Column(db.String(100))  # AIVA, etc.
    featured = db.Column(db.Boolean, default=False)
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='cart_items')

def init_sample_data():
    """Initialize the database with Romanian ceramic products using uploaded images"""
    
    # Romanian ceramic products using uploaded images
    products = [
        # Vaze
        {
            'name': 'Vaza Ceramică Tradițională cu Motive Etnice',
            'description': 'Vază handmade din ceramică, decorată cu motive tradiționale românești. Fiecare piesă este unică, modelată și arsă manual folosind tehnici străvechi.',
            'price': 150.00,
            'category': 'Vaze',
            'image_url': '/static/images/products/vaza_1.jpg',
            'image_source': 'Leonardo AI',
            'featured': True,
            'in_stock': True,
            'stock_quantity': 3
        },
        {
            'name': 'Vaza Ceramică cu Ornamente Geometrice',
            'description': 'Vază elegantă din lut natural cu ornamente geometrice incizate manual. Perfect pentru flori sau ca obiect decorativ de sine stătător.',
            'price': 120.00,
            'category': 'Vaze',
            'image_url': '/static/images/products/vaza_2.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 2
        },
        {
            'name': 'Vaza Ceramică cu Design Celtic',
            'description': 'Vază artistică cu design inspirat din arta celtică, realizată manual din argila naturală și arsă în cuptor traditional.',
            'price': 180.00,
            'category': 'Vaze',
            'image_url': '/static/images/products/vaza_3.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 1,
            'featured': True
        },
        
        # Ghivece
        {
            'name': 'Ghiveci Ceramic Multicolor pentru Plante',
            'description': 'Ghiveci handmade din ceramică cu glazură multicoloră în nuanțe de roz, albastru și galben. Perfect pentru plantele de interior.',
            'price': 85.00,
            'category': 'Ghivece',
            'image_url': '/static/images/products/ghiveci_1.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 4
        },
        {
            'name': 'Ghiveci Ceramic cu Formă Organică',
            'description': 'Ghiveci artistic cu formă organică și glazură în nuanțe de turcoaz și teracotă. Ideal pentru succulente și plante mici.',
            'price': 95.00,
            'category': 'Ghivece',
            'image_url': '/static/images/products/ghiveci_2.jpg',
            'image_source': 'Leonardo AI',
            'featured': True,
            'in_stock': True,
            'stock_quantity': 3
        },
        {
            'name': 'Ghiveci Ceramic cu Glazură Degrade',
            'description': 'Ghiveci rotund cu efect de glazură degrade în nuanțe naturale. Realizat manual cu atenție la detalii.',
            'price': 75.00,
            'category': 'Ghivece',
            'image_url': '/static/images/products/ghiveci_3.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 5
        },
        
        # Cercei
        {
            'name': 'Cercei Ceramici cu Motive Florale',
            'description': 'Cercei handmade din ceramică cu motive florale delicate sculptate manual. Ușori și confortabili de purtat.',
            'price': 45.00,
            'category': 'Cercei',
            'image_url': '/static/images/products/cercei_1.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 6
        },
        {
            'name': 'Cercei Ceramici cu Design Abstract',
            'description': 'Cercei artistici cu design abstract modern, realizați din argila naturală și finisați cu glazură mată.',
            'price': 38.00,
            'category': 'Cercei',
            'image_url': '/static/images/products/cercei_2.jpg',
            'image_source': 'Leonardo AI',
            'featured': True,
            'in_stock': True,
            'stock_quantity': 8
        },
        {
            'name': 'Cercei Ceramici Minimali în Formă de Picătură',
            'description': 'Cercei eleganți și minimali în formă de picătură, realizați din ceramică arsă la temperaturi înalte.',
            'price': 42.00,
            'category': 'Cercei',
            'image_url': '/static/images/products/cercei_3.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 7
        },
        {
            'name': 'Cercei Ceramici cu Model Radial',
            'description': 'Cercei unici cu model radial sculptat manual, în nuanță naturală de teracotă. Design contemporan și elegant.',
            'price': 48.00,
            'category': 'Cercei',
            'image_url': '/static/images/products/cercei_4.jpg',
            'image_source': 'Leonardo AI',
            'in_stock': True,
            'stock_quantity': 4
        },
        
        # Obiecte Decorative
        {
            'name': 'Statuetă Ceramică - Înger Copil',
            'description': 'Statuetă delicată din ceramică albă reprezentând un înger copil în poziție de rugăciune. Lucrare artistică cu atenție la detalii.',
            'price': 95.00,
            'category': 'Obiecte Decorative',
            'image_url': '/static/images/products/statuie_1.jpg',
            'image_source': 'Leonardo AI',
            'featured': True,
            'in_stock': True,
            'stock_quantity': 2,
            'audio_url': '/static/audio/ceramic_ambient.mp3',
            'audio_source': 'AIVA'
        }
    ]
    
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
