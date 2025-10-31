#!/usr/bin/env python3
"""
Development startup script for ArtMarket backend
"""
import os
import sys
from app import create_app
from app.extensions import db

def setup_environment():
    """Setup development environment variables"""
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('SECRET_KEY', 'dev-secret-key-change-in-production')
    os.environ.setdefault('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:artowner@localhost:5432/artgallery')
    os.environ.setdefault('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')

def main():
    """Main startup function"""
    print("🎨 Starting ArtMarket Backend...")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Create Flask app
    app = create_app()
    
    # Check database connection
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Make sure PostgreSQL is running and database exists")
            sys.exit(1)
        
        # Check if database needs seeding
        from app.models.user import User
        if User.query.count() == 0:
            print("🌱 Database is empty, running seed script...")
            try:
                from seed import seed_database
                seed_database()
                print("✅ Database seeded successfully!")
            except Exception as e:
                print(f"⚠️  Seeding failed: {e}")
    
    print("=" * 50)
    print("🚀 Server starting on http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/docs/")
    print("🔍 Health Check: http://localhost:5000/health")
    print("=" * 50)
    
    # Start the server
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()