from flask_restx import Api, Resource, fields
from flask import Blueprint

# Create blueprint for Swagger
swagger_bp = Blueprint('swagger', __name__)

# Initialize Flask-RESTX API
api = Api(
    swagger_bp,
    version='1.0',
    title='ArtMarket API',
    description='A comprehensive REST API for the ArtMarket digital art platform',
    doc='/docs/',
    security='Bearer Auth',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    }
)

# Namespaces
auth_ns = api.namespace('auth', description='Authentication operations')
artworks_ns = api.namespace('artworks', description='Artworks operations')
artists_ns = api.namespace('artists', description='Artist-specific operations')
collectors_ns = api.namespace('collectors', description='Collector-specific operations')
orders_ns = api.namespace('orders', description='Order management operations')
payments_ns = api.namespace('payments', description='Payment processing operations')
cart_ns = api.namespace('cart', description='Cart operations')
wishlist_ns = api.namespace('wishlist', description='Wishlist operations')

# Common Models
pagination_model = api.model('Pagination', {
    'page': fields.Integer(description='Current page number'),
    'per_page': fields.Integer(description='Number of items per page'),
    'total': fields.Integer(description='Total number of items'),
    'total_pages': fields.Integer(description='Total number of pages')
})

# Auth Models
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'fullName': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(required=True, description='User role (artist or collector)', enum=['artist', 'collector'])
})

auth_response_model = api.model('AuthResponse', {
    'user': fields.Raw(description='User object'),
    'access_token': fields.String(description='JWT access token'),
    'message': fields.String(description='Response message')
})

# Artwork Models
artwork_model = api.model('Artwork', {
    'id': fields.String(description='Artwork UUID'),
    'title': fields.String(required=True, description='Artwork title'),
    'description': fields.String(required=True, description='Artwork description'),
    'price': fields.Float(required=True, description='Artwork price'),
    'category': fields.String(required=True, description='Artwork category', 
                             enum=['painting', 'sculpture', 'photography', 'digital', 'mixed-media', 'textile']),
    'image_url': fields.String(description='Artwork image URL'),
    'artist_id': fields.String(description='Artist UUID'),
    'is_available': fields.Boolean(description='Artwork availability status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

artwork_list_model = api.model('ArtworkList', {
    'items': fields.List(fields.Nested(artwork_model)),
    'pagination': fields.Nested(pagination_model)
})

# Artist Models
upload_response_model = api.model('UploadResponse', {
    'image_url': fields.String(description='Uploaded image URL'),
    'public_id': fields.String(description='Cloudinary public ID'),
    'message': fields.String(description='Response message')
})

artist_stats_model = api.model('ArtistStats', {
    'total_artworks': fields.Integer(description='Total artworks'),
    'total_sales': fields.Float(description='Total sales'),
    'recent_orders_count': fields.Integer(description='Recent orders count')
})

# Collector Models
customer_artwork_model = api.model('CustomerArtwork', {
    'id': fields.String(description='Artwork UUID'),
    'title': fields.String(description='Artwork title'),
    'description': fields.String(description='Artwork description'),
    'price': fields.Float(description='Artwork price'),
    'category': fields.String(description='Artwork category'),
    'image_url': fields.String(description='Artwork image URL'),
    'artist_id': fields.String(description='Artist UUID'),
    'artist': fields.String(description='Artist username'),
    'is_available': fields.Boolean(description='Artwork availability status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

customer_artwork_list_model = api.model('CustomerArtworkList', {
    'items': fields.List(fields.Nested(customer_artwork_model)),
    'page': fields.Integer(description='Current page number'),
    'per_page': fields.Integer(description='Number of items per page'),
    'total': fields.Integer(description='Total number of items'),
    'total_pages': fields.Integer(description='Total number of pages')
})

customer_stats_model = api.model('CustomerStats', {
    'total_orders': fields.Integer(description='Total orders'),
    'total_spent': fields.Float(description='Total spent')
})

# Order Models
order_item_model = api.model('OrderItem', {
    'id': fields.String(description='Order item UUID'),
    'order_id': fields.String(description='Order UUID'),
    'artwork_id': fields.String(description='Artwork UUID'),
    'quantity': fields.Integer(description='Quantity'),
    'price': fields.Float(description='Item price'),
    'artwork': fields.Raw(description='Artwork details')
})

order_model = api.model('Order', {
    'id': fields.String(description='Order UUID'),
    'customer_id': fields.String(description='Customer UUID'),
    'total_amount': fields.Float(description='Total amount'),
    'status': fields.String(description='Order status', enum=['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']),
    'shipping_address': fields.String(description='Shipping address'),
    'shipping_city': fields.String(description='Shipping city'),
    'shipping_country': fields.String(description='Shipping country'),
    'shipping_postal_code': fields.String(description='Shipping postal code'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'items': fields.List(fields.Nested(order_item_model)),
    'payments': fields.Raw(description='Payment details'),
    'deliveries': fields.Raw(description='Delivery details')
})

order_list_model = api.model('OrderList', {
    'items': fields.List(fields.Nested(order_model)),
    'pagination': fields.Nested(pagination_model)
})

create_order_model = api.model('CreateOrder', {
    'items': fields.List(fields.Raw(description='Order items')),
    'shipping_details': fields.Raw(description='Shipping details')
})

update_order_status_model = api.model('UpdateOrderStatus', {
    'status': fields.String(description='New order status', enum=['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'])
})

payment_intent_request_model = api.model('PaymentIntentRequest', {
    'amount': fields.Float(required=True, description='Payment amount'),
    'currency': fields.String(description='Currency code', default='usd')
})

payment_intent_response_model = api.model('PaymentIntentResponse', {
    'client_secret': fields.String(description='Stripe client secret'),
    'payment_intent_id': fields.String(description='Stripe payment intent ID')
})

# Cart Models
cart_item_model = api.model('CartItem', {
    'id': fields.String(description='Cart item UUID'),
    'cart_id': fields.String(description='Cart UUID'),
    'artwork_id': fields.String(description='Artwork UUID'),
    'quantity': fields.Integer(description='Quantity'),
    'added_at': fields.String(description='Added timestamp'),
    'artwork': fields.Raw(description='Artwork details')
})

cart_model = api.model('Cart', {
    'id': fields.String(description='Cart UUID'),
    'user_id': fields.String(description='User UUID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'items': fields.List(fields.Nested(cart_item_model))
})

add_to_cart_model = api.model('AddToCart', {
    'artworkId': fields.String(required=True, description='Artwork UUID'),
    'quantity': fields.Integer(description='Quantity', default=1)
})

update_cart_item_model = api.model('UpdateCartItem', {
    'quantity': fields.Integer(required=True, description='New quantity')
})

# Wishlist Models
wishlist_item_model = api.model('WishlistItem', {
    'id': fields.String(description='Wishlist item UUID'),
    'wishlist_id': fields.String(description='Wishlist UUID'),
    'artwork_id': fields.String(description='Artwork UUID'),
    'added_at': fields.String(description='Added timestamp'),
    'artwork': fields.Raw(description='Artwork details')
})

wishlist_model = api.model('Wishlist', {
    'id': fields.String(description='Wishlist UUID'),
    'user_id': fields.String(description='User UUID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'items': fields.List(fields.Nested(wishlist_item_model))
})

add_to_wishlist_model = api.model('AddToWishlist', {
    'artworkId': fields.String(required=True, description='Artwork UUID')
})

# Import and register routes
from .routes import auth_routes, gallery_routes, artist_routes, customer_routes, order_routes, cart_routes, wishlist_routes

# Auth routes
@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', auth_response_model)
    @auth_ns.response(400, 'Validation error')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """User login"""
        return auth_routes.LoginResource().post()

@auth_ns.route('/signup')
class RegisterResource(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'Created', auth_response_model)
    @auth_ns.response(400, 'Validation error')
    @auth_ns.response(409, 'User already exists')
    def post(self):
        """User registration"""
        return auth_routes.RegisterResource().post()

# Artworks routes
@artworks_ns.route('/')
class GalleryResource(Resource):
    @artworks_ns.doc(params={
        'page': 'Page number',
        'per_page': 'Items per page',
        'category': 'Filter by category',
        'search': 'Search term',
        'sort': 'Sort field'
    })
    @artworks_ns.response(200, 'Success', artwork_list_model)
    def get(self):
        """Get paginated artwork gallery"""
        return gallery_routes.GalleryResource().get()

@artworks_ns.route('/<uuid:artwork_id>')
class ArtworkDetailResource(Resource):
    @artworks_ns.response(200, 'Success', artwork_model)
    @artworks_ns.response(404, 'Artwork not found')
    def get(self, artwork_id):
        """Get single artwork details"""
        return gallery_routes.GalleryResource().get(artwork_id)

# Artist routes
@artists_ns.route('/artworks')
class ArtistArtworkResource(Resource):
    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.doc(params={
        'page': 'Page number',
        'per_page': 'Items per page'
    })
    @artists_ns.response(200, 'Success', artwork_list_model)
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    def get(self):
        """Get artist's artworks with pagination"""
        return artist_routes.ArtistArtworkResource().get()

    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.expect(artwork_model)
    @artists_ns.response(201, 'Created', artwork_model)
    @artists_ns.response(400, 'Validation error')
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    def post(self):
        """Create new artwork"""
        return artist_routes.ArtistArtworkResource().post()

@artists_ns.route('/artworks/<uuid:artwork_id>')
class ArtistArtworkDetailResource(Resource):
    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.response(200, 'Success', artwork_model)
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    @artists_ns.response(404, 'Artwork not found')
    def get(self, artwork_id):
        """Get specific artwork details"""
        return artist_routes.ArtistArtworkDetailResource().get(artwork_id)

    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.expect(artwork_model)
    @artists_ns.response(200, 'Success', artwork_model)
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    @artists_ns.response(404, 'Artwork not found')
    def put(self, artwork_id):
        """Update artwork"""
        return artist_routes.ArtistArtworkDetailResource().put(artwork_id)

    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.response(200, 'Success')
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    @artists_ns.response(404, 'Artwork not found')
    def delete(self, artwork_id):
        """Delete artwork"""
        return artist_routes.ArtistArtworkDetailResource().delete(artwork_id)

@artists_ns.route('/upload-image')
class UploadImageResource(Resource):
    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.response(200, 'Success', upload_response_model)
    @artists_ns.response(400, 'Validation error')
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    @artists_ns.response(500, 'Internal server error')
    def post(self):
        """Upload artwork image to Cloudinary"""
        return artist_routes.UploadImageResource().post()

@artists_ns.route('/stats')
class ArtistStatsResource(Resource):
    @artists_ns.doc(security='Bearer Auth')
    @artists_ns.response(200, 'Success', artist_stats_model)
    @artists_ns.response(401, 'Unauthorized')
    @artists_ns.response(403, 'Forbidden')
    def get(self):
        """Get artist statistics"""
        return artist_routes.ArtistStatsResource().get()

# Collector routes
@collectors_ns.route('/artworks')
class CustomerArtworksResource(Resource):
    @collectors_ns.doc(security='Bearer Auth')
    @collectors_ns.doc(params={
        'page': 'Page number',
        'per_page': 'Items per page'
    })
    @collectors_ns.response(200, 'Success', customer_artwork_list_model)
    @collectors_ns.response(401, 'Unauthorized')
    @collectors_ns.response(403, 'Forbidden')
    def get(self):
        """Get available artworks for collectors"""
        return customer_routes.CustomerArtworksResource().get()

@collectors_ns.route('/stats')
class CustomerStatsResource(Resource):
    @collectors_ns.doc(security='Bearer Auth')
    @collectors_ns.response(200, 'Success', customer_stats_model)
    @collectors_ns.response(401, 'Unauthorized')
    @collectors_ns.response(403, 'Forbidden')
    def get(self):
        """Get collector statistics"""
        return customer_routes.CustomerStatsResource().get()

# Order routes
@orders_ns.route('/')
class OrdersResource(Resource):
    @orders_ns.doc(security='Bearer Auth')
    @orders_ns.doc(params={
        'page': 'Page number',
        'per_page': 'Items per page'
    })
    @orders_ns.response(200, 'Success', order_list_model)
    @orders_ns.response(401, 'Unauthorized')
    def get(self):
        """Get orders based on user role"""
        return order_routes.OrdersResource().get()

    @orders_ns.doc(security='Bearer Auth')
    @orders_ns.expect(create_order_model)
    @orders_ns.response(201, 'Created', order_model)
    @orders_ns.response(400, 'Validation error')
    @orders_ns.response(401, 'Unauthorized')
    def post(self):
        """Create new order"""
        return order_routes.OrdersResource().post()

@orders_ns.route('/<uuid:order_id>')
class OrderDetailResource(Resource):
    @orders_ns.doc(security='Bearer Auth')
    @orders_ns.response(200, 'Success', order_model)
    @orders_ns.response(401, 'Unauthorized')
    @orders_ns.response(403, 'Forbidden')
    @orders_ns.response(404, 'Order not found')
    def get(self, order_id):
        """Get specific order details"""
        return order_routes.OrderDetailResource().get(order_id)

    @orders_ns.doc(security='Bearer Auth')
    @orders_ns.expect(update_order_status_model)
    @orders_ns.response(200, 'Success', order_model)
    @orders_ns.response(401, 'Unauthorized')
    @orders_ns.response(403, 'Forbidden')
    @orders_ns.response(404, 'Order not found')
    def put(self, order_id):
        """Update order status"""
        return order_routes.OrderDetailResource().put(order_id)

@orders_ns.route('/payments/create-intent')
class StripePaymentIntentResource(Resource):
    @orders_ns.doc(security='Bearer Auth')
    @orders_ns.expect(payment_intent_request_model)
    @orders_ns.response(200, 'Success', payment_intent_response_model)
    @orders_ns.response(400, 'Validation error')
    @orders_ns.response(401, 'Unauthorized')
    @orders_ns.response(500, 'Internal server error')
    def post(self):
        """Create Stripe payment intent"""
        return order_routes.StripePaymentIntentResource().post()

@orders_ns.route('/payments/webhook')
class StripeWebhookResource(Resource):
    @orders_ns.response(200, 'Success')
    @orders_ns.response(400, 'Validation error')
    def post(self):
        """Handle Stripe webhooks"""
        return order_routes.StripeWebhookResource().post()

# Cart routes
@cart_ns.route('/')
class CartResource(Resource):
    @cart_ns.doc(security='Bearer Auth')
    @cart_ns.response(200, 'Success', cart_model)
    @cart_ns.response(401, 'Unauthorized')
    def get(self):
        """Get user's cart"""
        return cart_routes.CartResource().get()

    @cart_ns.doc(security='Bearer Auth')
    @cart_ns.expect(add_to_cart_model)
    @cart_ns.response(201, 'Created', cart_model)
    @cart_ns.response(400, 'Validation error')
    @cart_ns.response(401, 'Unauthorized')
    @cart_ns.response(404, 'Artwork not found')
    def post(self):
        """Add item to cart"""
        return cart_routes.CartResource().post()

@cart_ns.route('/<uuid:artwork_id>')
class CartItemResource(Resource):
    @cart_ns.doc(security='Bearer Auth')
    @cart_ns.expect(update_cart_item_model)
    @cart_ns.response(200, 'Success', cart_model)
    @cart_ns.response(400, 'Validation error')
    @cart_ns.response(401, 'Unauthorized')
    @cart_ns.response(404, 'Cart or item not found')
    def patch(self, artwork_id):
        """Update cart item quantity"""
        return cart_routes.CartItemResource().patch(artwork_id)

    @cart_ns.doc(security='Bearer Auth')
    @cart_ns.response(200, 'Success', cart_model)
    @cart_ns.response(401, 'Unauthorized')
    @cart_ns.response(404, 'Cart or item not found')
    def delete(self, artwork_id):
        """Remove item from cart"""
        return cart_routes.CartItemResource().delete(artwork_id)

# Wishlist routes
@wishlist_ns.route('/')
class WishlistResource(Resource):
    @wishlist_ns.doc(security='Bearer Auth')
    @wishlist_ns.response(200, 'Success', wishlist_model)
    @wishlist_ns.response(401, 'Unauthorized')
    def get(self):
        """Get user's wishlist"""
        return wishlist_routes.WishlistResource().get()

    @wishlist_ns.doc(security='Bearer Auth')
    @wishlist_ns.expect(add_to_wishlist_model)
    @wishlist_ns.response(201, 'Created', wishlist_model)
    @wishlist_ns.response(400, 'Validation error')
    @wishlist_ns.response(401, 'Unauthorized')
    @wishlist_ns.response(404, 'Artwork not found')
    def post(self):
        """Add item to wishlist"""
        return wishlist_routes.WishlistResource().post()

@wishlist_ns.route('/<uuid:artwork_id>')
class WishlistItemResource(Resource):
    @wishlist_ns.doc(security='Bearer Auth')
    @wishlist_ns.response(200, 'Success', wishlist_model)
    @wishlist_ns.response(401, 'Unauthorized')
    @wishlist_ns.response(404, 'Wishlist or item not found')
    def delete(self, artwork_id):
        """Remove item from wishlist"""
        return wishlist_routes.WishlistItemResource().delete(artwork_id)
