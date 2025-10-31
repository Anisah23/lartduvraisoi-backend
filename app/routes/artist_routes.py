from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..extensions import db
from ..models.artwork import Artwork, ArtworkSchema
from ..models.order import Order, OrderItem
from ..models.user import User
from ..utils.decorators import role_required, handle_api_errors
from ..utils.cloudinary_service import CloudinaryService
from ..utils.helpers import paginate_query

artwork_schema = ArtworkSchema()
artworks_schema = ArtworkSchema(many=True)

class ArtistArtworkResource(Resource):
    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def get(self):
        """Get artist's artworks with pagination"""
        artist_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        query = Artwork.query.filter_by(artist_id=artist_id).order_by(Artwork.created_at.desc())
        pagination = paginate_query(query, page, per_page)

        return {
            'items': artworks_schema.dump(pagination.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': pagination.pages
            }
        }, 200

    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def post(self):
        """Create new artwork"""
        artist_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'description', 'price', 'category']
        for field in required_fields:
            if not data.get(field):
                return {'message': f'{field} is required'}, 400

        # Create artwork
        artwork = Artwork(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            category=data['category'],
            image_url=data.get('image_url'),
            artist_id=artist_id
        )

        db.session.add(artwork)
        db.session.commit()

        return artwork_schema.dump(artwork), 201

class ArtistArtworkDetailResource(Resource):
    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def get(self, artwork_id):
        """Get specific artwork details"""
        artist_id = get_jwt_identity()
        artwork = Artwork.query.filter_by(id=artwork_id, artist_id=artist_id).first()
        
        if not artwork:
            return {'message': 'Artwork not found'}, 404

        return artwork_schema.dump(artwork), 200

    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def put(self, artwork_id):
        """Update artwork"""
        artist_id = get_jwt_identity()
        artwork = Artwork.query.filter_by(id=artwork_id, artist_id=artist_id).first()
        
        if not artwork:
            return {'message': 'Artwork not found'}, 404

        data = request.get_json()
        
        # Update fields
        updatable_fields = ['title', 'description', 'price', 'category', 'image_url', 'is_available']
        for field in updatable_fields:
            if field in data:
                setattr(artwork, field, data[field])

        db.session.commit()
        return artwork_schema.dump(artwork), 200

    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def delete(self, artwork_id):
        """Delete artwork"""
        artist_id = get_jwt_identity()
        artwork = Artwork.query.filter_by(id=artwork_id, artist_id=artist_id).first()
        
        if not artwork:
            return {'message': 'Artwork not found'}, 404

        # Delete image from Cloudinary if exists
        if artwork.image_public_id:
            CloudinaryService.delete_image(artwork.image_public_id)

        db.session.delete(artwork)
        db.session.commit()

        return {'message': 'Artwork deleted successfully'}, 200

class UploadImageResource(Resource):
    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def post(self):
        """Upload artwork image to Cloudinary"""
        if 'file' not in request.files:
            return {'message': 'No file provided'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No file selected'}, 400

        try:
            upload_result = CloudinaryService.upload_image(file)
            return {
                'image_url': upload_result['url'],
                'public_id': upload_result['public_id'],
                'message': 'Image uploaded successfully'
            }, 200
        except Exception as e:
            return {'message': f'Image upload failed: {str(e)}'}, 500

class ArtistStatsResource(Resource):
    @jwt_required()
    @role_required(['artist'])
    @handle_api_errors
    def get(self):
        """Get artist statistics"""
        artist_id = get_jwt_identity()

        # Total artworks
        total_artworks = Artwork.query.filter_by(artist_id=artist_id).count()

        # Total sales
        total_sales = db.session.query(db.func.sum(OrderItem.price)).\
            join(Order).\
            join(Artwork).\
            filter(
                Artwork.artist_id == artist_id,
                Order.status == 'delivered'
            ).scalar() or 0

        # Recent orders
        recent_orders = Order.query.\
            join(OrderItem).\
            join(Artwork).\
            filter(Artwork.artist_id == artist_id).\
            order_by(Order.created_at.desc()).\
            limit(5).all()

        return {
            'total_artworks': total_artworks,
            'total_sales': float(total_sales),
            'recent_orders_count': len(recent_orders)
        }, 200