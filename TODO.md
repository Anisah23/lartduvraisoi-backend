# TODO List for Art Marketplace Backend Fixes

## 1. Implement Missing Routes
- [x] Create `backend/app/routes/artist_routes.py` for CRUD operations on artworks (artisans only).
- [x] Create `backend/app/routes/customer_routes.py` for viewing orders, artworks, etc. (collectors only).
- [x] Implement full CRUD routes for orders, payments, deliveries, notifications.

## 2. Add Image Upload Logic
- [x] Integrate Cloudinary for image uploads in artwork routes.

## 3. Add Email Notifications
- [x] Integrate SendGrid for email notifications (e.g., on order creation).

## 4. Improve Validations
- [x] Use Marshmallow schemas for input validation in all routes.

## 5. Enhance Error Handling
- [x] Add try-except blocks and human-readable error messages.

## 6. Add Date Formatting
- [x] Format dates in responses using datetime.isoformat.

## 7. Implement API Documentation
- [ ] Add Flask-Swagger for API documentation.

## 8. Test the Fixes
- [ ] Run the app and test endpoints with curl.
- [ ] Check DB relationships once DB is created.

## 9. Create Migrations
- [ ] Create database migrations if needed.
