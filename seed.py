#!/usr/bin/env python3
"""
Database seeding script for ArtGallery project.
Populates the database with initial data for artists, collectors, artworks, etc.
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.artwork import Artwork
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.delivery import Delivery
from app.models.notification import Notification
from app.models.wishlist import Wishlist, WishlistItem
from app.models.cart import Cart, CartItem

def seed_database():
    """Seed the database with initial data."""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        print("🌱 Seeding database...")

        # Create artists
        artists_data = [
            {
                'email': 'elena.chen@example.com',
                'full_name': 'Elena Chen',
                'role': 'artisan',
                'address': '123 Artist Lane, Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'marcus.rivera@example.com',
                'full_name': 'Marcus Rivera',
                'role': 'artisan',
                'address': '456 Sculpture St, Mombasa, Kenya',
                'city': 'Mombasa',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'sarah.blake@example.com',
                'full_name': 'Sarah Blake',
                'role': 'artisan',
                'address': '789 Photo Ave, Kisumu, Kenya',
                'city': 'Kisumu',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'alex.kim@example.com',
                'full_name': 'Alex Kim',
                'role': 'artisan',
                'address': '321 Digital Dr, Nakuru, Kenya',
                'city': 'Nakuru',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'maya.johnson@example.com',
                'full_name': 'Maya Johnson',
                'role': 'artisan',
                'address': '654 Urban Rd, Eldoret, Kenya',
                'city': 'Eldoret',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'david.chen@example.com',
                'full_name': 'David Chen',
                'role': 'artisan',
                'address': '987 Cosmic Way, Thika, Kenya',
                'city': 'Thika',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'jamie.wong@example.com',
                'full_name': 'Jamie Wong',
                'role': 'artisan',
                'address': '147 Nature Ln, Naivasha, Kenya',
                'city': 'Naivasha',
                'country': 'Kenya',
                'password': 'password123'
            }
        ]

        # Create collectors
        collectors_data = [
            {
                'email': 'john.collector@example.com',
                'full_name': 'John Smith',
                'role': 'collector',
                'address': '111 Collector St, Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'emma.artlover@example.com',
                'full_name': 'Emma Johnson',
                'role': 'collector',
                'address': '222 Art Ave, Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya',
                'password': 'password123'
            },
            {
                'email': 'michael.galleries@example.com',
                'full_name': 'Michael Brown',
                'role': 'collector',
                'address': '333 Museum Rd, Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya',
                'password': 'password123'
            }
        ]

        # Create users
        all_users = artists_data + collectors_data
        users = {}

        for user_data in all_users:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                users[user_data['email']] = existing_user
                continue

            user = User(
                username=user_data['email'].split('@')[0],  # Use email prefix as username
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                address=user_data.get('address'),
                city=user_data.get('city'),
                country=user_data.get('country'),
                password_hash=generate_password_hash(user_data['password'])
            )
            db.session.add(user)
            users[user_data['email']] = user

        db.session.commit()
        print(f"✅ Created {len(users)} users")

        # Create artworks
        artworks_data = [
            {
                'title': 'Abstract Harmony',
                'description': 'A vibrant exploration of color and movement in abstract form',
                'price': 1250.00,
                'category': 'painting',
                'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'elena.chen@example.com'
            },
            {
                'title': 'Bronze Guardian',
                'description': 'A powerful bronze sculpture that embodies strength and protection',
                'price': 3500.00,
                'category': 'sculpture',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'marcus.rivera@example.com'
            },
            {
                'title': 'Soul in Shadows',
                'description': 'An evocative portrait that captures the depth of human emotion',
                'price': 850.00,
                'category': 'photography',
                'image_url': 'https://images.unsplash.com/photo-1605721911519-3dfeb3be25e7?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'sarah.blake@example.com'
            },
            {
                'title': 'Neon Dreams',
                'description': 'A stunning digital artwork that merges technology and imagination',
                'price': 650.00,
                'category': 'digital',
                'image_url': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'alex.kim@example.com'
            },
            {
                'title': 'Urban Reflections',
                'description': 'A cityscape captured in moments of rain and neon lights',
                'price': 950.00,
                'category': 'photography',
                'image_url': 'https://images.unsplash.com/photo-1514539079130-25950c84af65?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'maya.johnson@example.com'
            },
            {
                'title': 'Celestial Dance',
                'description': 'An abstract interpretation of cosmic movements',
                'price': 1800.00,
                'category': 'painting',
                'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'david.chen@example.com'
            },
            {
                'title': 'Digital Wilderness',
                'description': 'A fusion of natural elements and digital manipulation',
                'price': 750.00,
                'category': 'digital',
                'image_url': 'https://images.unsplash.com/photo-1563089145-599997674d42?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'jamie.wong@example.com'
            },
            {
                'title': 'Ancient Whispers',
                'description': 'A bronze sculpture inspired by ancient mythology',
                'price': 4200.00,
                'category': 'sculpture',
                'image_url': 'https://images.unsplash.com/photo-1570288685280-7802a8f8c4fa?q=80&w=1000&auto=format&fit=crop',
                'artist_email': 'marcus.rivera@example.com'
            }
        ]

        artworks = []
        for artwork_data in artworks_data:
            artist = users[artwork_data['artist_email']]
            artwork = Artwork(
                title=artwork_data['title'],
                description=artwork_data['description'],
                price=artwork_data['price'],
                category=artwork_data['category'],
                image_url=artwork_data['image_url'],
                artist_id=artist.id
            )
            db.session.add(artwork)
            artworks.append(artwork)

        db.session.commit()
        print(f"✅ Created {len(artworks)} artworks")

        # Create some sample orders and related data
        collector = users['john.collector@example.com']
        artwork = artworks[0]  # Abstract Harmony

        # Create an order
        order = Order(
            customer_id=collector.id,
            total_amount=artwork.price,
            status='delivered',
            shipping_address=collector.address or '123 Collector St, Nairobi, Kenya',
            shipping_city=collector.city or 'Nairobi',
            shipping_country=collector.country or 'Kenya',
            shipping_postal_code='00100'
        )
        db.session.add(order)
        db.session.flush()

        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            artwork_id=artwork.id,
            quantity=1,
            price=artwork.price
        )
        db.session.add(order_item)

        # Create payment
        payment = Payment(
            order_id=order.id,
            amount=artwork.price,
            provider='stripe',
            status='completed'
        )
        db.session.add(payment)

        # Create delivery
        delivery = Delivery(
            order_id=order.id,
            status='delivered',
            tracking_number='BOLT-DEL-001'
        )
        db.session.add(delivery)

        # Create notification
        notification = Notification(
            user_id=collector.id,
            title='Order Delivered',
            message=f'Your order for "{artwork.title}" has been delivered successfully!'
        )
        db.session.add(notification)

        db.session.commit()
        print("✅ Created sample order with payment and delivery")

        # Add some items to wishlist
        wishlist_items = [
            (users['emma.artlover@example.com'], artworks[1]),  # Bronze Guardian
            (users['emma.artlover@example.com'], artworks[3]),  # Neon Dreams
            (users['michael.galleries@example.com'], artworks[7])  # Ancient Whispers
        ]

        for user, artwork in wishlist_items:
            # First create or get the user's wishlist
            wishlist = Wishlist.query.filter_by(user_id=user.id).first()
            if not wishlist:
                wishlist = Wishlist(user_id=user.id)
                db.session.add(wishlist)
                db.session.flush()

            # Then add the item to the wishlist
            wishlist_item = WishlistItem(
                wishlist_id=wishlist.id,
                artwork_id=artwork.id
            )
            db.session.add(wishlist_item)

        db.session.commit()
        print("✅ Added sample wishlist items")

        print("🎉 Database seeding completed successfully!")
        print("\n📋 Sample accounts created:")
        print("Artists:")
        for artist in artists_data:
            print(f"  - {artist['email']} (password: {artist['password']})")
        print("\nCollectors:")
        for collector in collectors_data:
            print(f"  - {collector['email']} (password: {collector['password']})")

if __name__ == '__main__':
    seed_database()