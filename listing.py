# Listing Routes (CRUD operations for Listings)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity # Assuming flask_jwt_extended for JWT
from sqlalchemy import or_, and_
import os
import sys
from datetime import datetime # Added for payment_date and tier_expiry_date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.user import User
from src.models.listing import Listing
# from main import db # db will be imported from main.py to avoid circular imports

# Placeholder for db.session, will be properly linked from main.py
class DBPlaceholder:
    session = None # This will be replaced by the actual db.session
    # Adding a query attribute to the placeholder for Listing.query to work
    query = None 

    # Adding a Model attribute for Listing.query to work
    Model = None

db_placeholder = DBPlaceholder()

# Simulate SQLAlchemy query capabilities for the placeholder
class QueryPlaceholder:
    def __init__(self, model):
        self.model = model
        self._filters = []
        self._order_by = None

    def filter(self, *criterion):
        self._filters.extend(criterion)
        return self
    
    def filter_by(self, **kwargs):
        for key, value in kwargs.items():
            self._filters.append(getattr(self.model, key) == value)
        return self

    def order_by(self, *criterion):
        self._order_by = criterion
        return self

    def paginate(self, page, per_page, error_out=True):
        # This is a very simplified mock pagination
        print(f"Simulating pagination for model {self.model.__name__} with filters {self._filters}")
        class PaginatedResult:
            def __init__(self, items, total, pages, page):
                self.items = items
                self.total = total
                self.pages = pages
                self.page = page
        # Return empty for placeholder
        return PaginatedResult([], 0, 0, page)
    
    def get(self, ident):
        print(f"Simulating get for model {self.model.__name__} with id {ident}")
        # Simulate finding a mock listing for placeholder to_dict() call
        if self.model == Listing and ident is not None: # Basic check
            mock_listing_data = {
                'id': ident, 'title': 'Simulated Listing for Get',
                'price': '120000.00', 'address': '456 Simulated Ave',
                'user_id': 1 # Assuming a user_id for ownership checks
            }
            class MockListing: 
                def __init__(self, **kwargs): self.__dict__.update(kwargs)
                def to_dict(self): return self.__dict__
                user = None; date_posted = None; date_updated = None; bathrooms = None; user_id = 1 # Ensure user_id is present
            return MockListing(**mock_listing_data)
        return None # Simulate not found for other cases
    
    def all(self):
        print(f"Simulating all for model {self.model.__name__} with filters {self._filters}")
        return []

# Assign the placeholder query to Listing if db is not fully initialized
if not hasattr(Listing, 'query'):
    Listing.query = QueryPlaceholder(Listing)


listing_bp = Blueprint("listing_bp", __name__)

@listing_bp.route("/listings/my-listings", methods=["GET"])
@jwt_required()
def get_my_listings():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if db_placeholder.session: # In a real app, this would be `db.session`
        query = Listing.query.filter_by(user_id=current_user_id).order_by(Listing.date_posted.desc())
        paginated_listings = query.paginate(page=page, per_page=per_page, error_out=False)
        results = [listing.to_dict() for listing in paginated_listings.items]
        return jsonify({
            "message": "User listings retrieved successfully",
            "listings": results,
            "total_pages": paginated_listings.pages,
            "current_page": paginated_listings.page,
            "total_listings": paginated_listings.total
        }), 200
    else:
        print(f"Simulating fetching listings for user_id: {current_user_id}")
        # Simulate some listings for the current user
        simulated_listings = [
            {'id': 101, 'title': 'My Simulated Home', 'price': '500000.00', 'address': '1 User Lane', 'user_id': current_user_id, 'listing_tier': 'premium'},
            {'id': 102, 'title': 'My Other Place', 'price': '750000.00', 'address': '2 User Avenue', 'user_id': current_user_id, 'listing_tier': 'standard'}
        ]
        return jsonify({
            "message": "User listings retrieval simulated (DB not fully initialized)", 
            "listings": simulated_listings,
            "total_pages": 1,
            "current_page": 1,
            "total_listings": len(simulated_listings)
            }), 200

@listing_bp.route("/listings", methods=["POST"])
@jwt_required()
def create_listing():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401

    required_fields = ["title", "price", "address"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": f"Missing required fields: {', '.join(required_fields)}"}), 400
    
    try:
        price = float(data["price"])
        if price <= 0:
            return jsonify({"message": "Price must be a positive number"}), 400
    except ValueError:
        return jsonify({"message": "Invalid price format"}), 400

    new_listing = Listing(
        title=data["title"],
        price=price,
        address=data["address"],
        user_id=current_user_id,
        description=data.get("description"),
        city=data.get("city"),
        province=data.get("province"),
        postal_code=data.get("postal_code"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        bedrooms=data.get("bedrooms"),
        bathrooms=data.get("bathrooms"),
        property_type=data.get("property_type"),
        area_sqm=data.get("area_sqm"),
        main_image_url=data.get("main_image_url"),
        source='manual',
        status=data.get("status", "active"),
        # Monetization fields
        is_charged_listing=data.get("is_charged_listing", False),
        listing_tier=data.get("listing_tier"), # e.g., standard, premium
        payment_status=data.get("payment_status"),
        transaction_id=data.get("transaction_id"),
        payment_date=datetime.fromisoformat(data["payment_date"]) if data.get("payment_date") else None,
        tier_expiry_date=datetime.fromisoformat(data["tier_expiry_date"]) if data.get("tier_expiry_date") else None
    )

    if db_placeholder.session: # In a real app, this would be `db.session`
        db_placeholder.session.add(new_listing)
        db_placeholder.session.commit()
        return jsonify({"message": "Listing created successfully", "listing": new_listing.to_dict()}), 201
    else:
        print(f"Simulating listing creation: {new_listing.to_dict()}")
        return jsonify({"message": "Listing creation simulated (DB not fully initialized)", "listing": new_listing.to_dict()}), 201

@listing_bp.route("/listings", methods=["GET"])
def get_listings():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    filters = []
    if request.args.get("city"):
        filters.append(Listing.city.ilike(f"%{request.args.get('city')}%" ) )
    if request.args.get("province"):
        filters.append(Listing.province.ilike(f"%{request.args.get('province')}%" ) )
    if request.args.get("property_type"):
        filters.append(Listing.property_type == request.args.get("property_type"))
    if request.args.get("min_price"):
        try:
            filters.append(Listing.price >= float(request.args.get("min_price")))
        except ValueError:
            return jsonify({"message": "Invalid min_price format"}), 400
    if request.args.get("max_price"):
        try:
            filters.append(Listing.price <= float(request.args.get("max_price")))
        except ValueError:
            return jsonify({"message": "Invalid max_price format"}), 400
    if request.args.get("bedrooms"):
        try:
            filters.append(Listing.bedrooms == int(request.args.get("bedrooms")))
        except ValueError:
            return jsonify({"message": "Invalid bedrooms format"}), 400
    if request.args.get("listing_tier"):
        filters.append(Listing.listing_tier == request.args.get("listing_tier"))
    
    search_query = request.args.get("search")
    if search_query:
        search_term = f"%{search_query}%"
        filters.append(or_(Listing.title.ilike(search_term), Listing.description.ilike(search_term)))

    if db_placeholder.session: # In a real app, this would be `db.session`
        query = Listing.query
        if filters:
            query = query.filter(*filters) 
            
        query = query.order_by(Listing.date_posted.desc())
        paginated_listings = query.paginate(page=page, per_page=per_page, error_out=False)
        
        results = [listing.to_dict() for listing in paginated_listings.items]
        return jsonify({
            "message": "Listings retrieved successfully",
            "listings": results,
            "total_pages": paginated_listings.pages,
            "current_page": paginated_listings.page,
            "total_listings": paginated_listings.total
        }), 200
    else:
        print(f"Simulating fetching listings with filters: {filters}")
        return jsonify({"message": "Listing retrieval simulated (DB not fully initialized)", "listings": []}), 200

@listing_bp.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing_detail(listing_id):
    if db_placeholder.session: # In a real app, this would be `db.session`
        listing = Listing.query.get(listing_id)
        if listing:
            return jsonify({"message": "Listing found", "listing": listing.to_dict()}), 200
        return jsonify({"message": "Listing not found"}), 404
    else:
        print(f"Simulating fetching listing detail for ID: {listing_id}")
        mock_listing_data = {
            'id': listing_id, 'title': 'Simulated Listing Detail', 'price': '100000.00',
            'address': '123 Simulated St', 'user_id': 1, 'listing_tier': 'premium' 
        }
        class MockListing: 
            def __init__(self, **kwargs): self.__dict__.update(kwargs)
            def to_dict(self): return self.__dict__
            user = None; date_posted = None; date_updated = None; bathrooms = None; user_id = 1

        return jsonify({"message": "Listing detail simulated (DB not fully initialized)", "listing": MockListing(**mock_listing_data).to_dict()}), 200

@listing_bp.route("/listings/<int:listing_id>", methods=["PUT"])
@jwt_required()
def update_listing(listing_id):
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401

    if db_placeholder.session: # In a real app, this would be `db.session`
        listing = Listing.query.get(listing_id)
        if not listing:
            return jsonify({"message": "Listing not found"}), 404

        if listing.user_id != current_user_id:
            return jsonify({"message": "Forbidden: You do not own this listing"}), 403

        data = request.get_json()
        
        for field in ["title", "description", "address", "city", "province", "postal_code", "latitude", "longitude", "property_type", "main_image_url", "status", "listing_tier", "payment_status", "transaction_id"]:
            if field in data:
                setattr(listing, field, data[field])
        if "price" in data:
            try:
                listing.price = float(data["price"])
                if listing.price <= 0:
                    return jsonify({"message": "Price must be a positive number"}), 400
            except ValueError:
                return jsonify({"message": "Invalid price format"}), 400
        if "bedrooms" in data:
            listing.bedrooms = data.get("bedrooms")
        if "bathrooms" in data:
            listing.bathrooms = data.get("bathrooms")
        if "area_sqm" in data:
            listing.area_sqm = data.get("area_sqm")
        if "is_charged_listing" in data:
            listing.is_charged_listing = data.get("is_charged_listing", False)
        if "payment_date" in data:
            listing.payment_date = datetime.fromisoformat(data["payment_date"]) if data["payment_date"] else None
        if "tier_expiry_date" in data:
            listing.tier_expiry_date = datetime.fromisoformat(data["tier_expiry_date"]) if data["tier_expiry_date"] else None

        db_placeholder.session.commit()
        return jsonify({"message": "Listing updated successfully", "listing": listing.to_dict()}), 200
    else:
        print(f"Simulating update for listing ID: {listing_id}")
        # Simulate finding the listing to check ownership for placeholder
        listing_owner_id = 1 # Assume listing with ID listing_id is owned by user 1 for simulation
        if listing_owner_id != current_user_id:
             return jsonify({"message": "Forbidden: You do not own this listing (Simulated)"}), 403
        return jsonify({"message": "Listing update simulated (DB not fully initialized)"}), 200

@listing_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
@jwt_required()
def delete_listing(listing_id):
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401

    if db_placeholder.session: # In a real app, this would be `db.session`
        listing = Listing.query.get(listing_id)
        if not listing:
            return jsonify({"message": "Listing not found"}), 404

        if listing.user_id != current_user_id:
            return jsonify({"message": "Forbidden: You do not own this listing"}), 403

        db_placeholder.session.delete(listing)
        db_placeholder.session.commit()
        return jsonify({"message": "Listing deleted successfully"}), 200
    else:
        print(f"Simulating delete for listing ID: {listing_id}")
        # Simulate finding the listing to check ownership for placeholder
        listing_owner_id = 1 # Assume listing with ID listing_id is owned by user 1 for simulation
        if listing_owner_id != current_user_id:
             return jsonify({"message": "Forbidden: You do not own this listing (Simulated)"}), 403
        return jsonify({"message": "Listing deletion simulated (DB not fully initialized)"}), 200

