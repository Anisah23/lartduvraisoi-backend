from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Seed the database on startup if it's empty
    with app.app_context():
        from app.extensions import db
        from app.models.user import User

        # Check if database is empty
        if User.query.count() == 0:
            print("🌱 Database is empty, running seed script...")
            from seed import seed_database
            seed_database()
            print("✅ Database seeded successfully!")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)