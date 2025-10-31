from app import create_app
from app.extensions import db
from sqlalchemy import inspect
from app.models.user import User
from app.models.artwork import Artwork
from app.models.order import Order
from app.models.payment import Payment
from app.models.delivery import Delivery
from app.models.notification import Notification
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist, WishlistItem

app = create_app()

def show_tables():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("=== DATABASE TABLES ===")
        for table in tables:
            print(table)

def show_database_contents():
    with app.app_context():
        print("=== USERS ===")
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Full Name: {user.full_name}, Role: {user.role}, Active: {user.is_active}")

        print("\n=== ARTWORKS ===")
        artworks = Artwork.query.all()
        for artwork in artworks:
            print(f"ID: {artwork.id}, Title: {artwork.title}, Price: {artwork.price}, Category: {artwork.category}, Artist: {artwork.artist_id}, Available: {artwork.is_available}")

        print("\n=== ORDERS ===")
        orders = Order.query.all()
        for order in orders:
            print(f"ID: {order.id}, Customer: {order.customer_id}, Total: {order.total_amount}, Status: {order.status}")

        print("\n=== PAYMENTS ===")
        payments = Payment.query.all()
        for payment in payments:
            print(f"ID: {payment.id}, Order: {payment.order_id}, Amount: {payment.amount}, Status: {payment.status}")

        print("\n=== DELIVERIES ===")
        deliveries = Delivery.query.all()
        for delivery in deliveries:
            print(f"ID: {delivery.id}, Order: {delivery.order_id}, Status: {delivery.status}")

        print("\n=== NOTIFICATIONS ===")
        notifications = Notification.query.all()
        for notification in notifications:
            print(f"ID: {notification.id}, User: {notification.user_id}, Message: {notification.message}, Read: {notification.read}")

        print("\n=== CART ITEMS ===")
        cart_items = CartItem.query.all()
        for item in cart_items:
            print(f"ID: {item.id}, Cart: {item.cart_id}, Artwork: {item.artwork_id}, Quantity: {item.quantity}")

        print("\n=== WISHLIST ITEMS ===")
        wishlist_items = WishlistItem.query.all()
        for item in wishlist_items:
            print(f"ID: {item.id}, Wishlist: {item.wishlist_id}, Artwork: {item.artwork_id}")

if __name__ == "__main__":
    show_database_contents()
