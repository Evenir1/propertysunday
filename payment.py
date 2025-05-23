# Payment Routes for Charged Listings
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.user import User
from src.models.listing import Listing

# Placeholder for db.session, will be properly linked from main.py
class DBPlaceholder:
    session = None
    query = None
    Model = None

db_placeholder = DBPlaceholder()

payment_bp = Blueprint("payment_bp", __name__)

# Define pricing tiers
LISTING_TIERS = {
    "standard": {
        "price": 0,  # Free tier
        "duration_days": 30,
        "features": ["Basic listing", "Standard visibility"]
    },
    "premium": {
        "price": 199.99,  # ZAR
        "duration_days": 60,
        "features": ["Premium listing", "Higher visibility", "Featured in search results"]
    },
    "featured": {
        "price": 499.99,  # ZAR
        "duration_days": 90,
        "features": ["Top visibility", "Featured on homepage", "Social media promotion", "Professional photography"]
    }
}

@payment_bp.route("/pricing/tiers", methods=["GET"])
def get_pricing_tiers():
    """Get all available pricing tiers and their details"""
    return jsonify({
        "message": "Pricing tiers retrieved successfully",
        "tiers": LISTING_TIERS
    }), 200

@payment_bp.route("/listings/<int:listing_id>/upgrade", methods=["POST"])
@jwt_required()
def upgrade_listing(listing_id):
    """Upgrade a listing to a paid tier"""
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401
    
    data = request.get_json()
    if not data or "tier" not in data:
        return jsonify({"message": "Missing required field: tier"}), 400
    
    requested_tier = data["tier"]
    if requested_tier not in LISTING_TIERS:
        return jsonify({"message": f"Invalid tier. Available tiers: {', '.join(LISTING_TIERS.keys())}"}), 400
    
    # Simulate payment processing
    payment_successful = True  # In a real app, this would be the result of payment processing
    payment_details = {
        "transaction_id": f"TRANS-{datetime.now().strftime('%Y%m%d%H%M%S')}-{listing_id}",
        "amount": LISTING_TIERS[requested_tier]["price"],
        "currency": "ZAR",
        "payment_method": data.get("payment_method", "credit_card"),
        "status": "completed" if payment_successful else "failed"
    }
    
    if db_placeholder.session:
        listing = Listing.query.get(listing_id)
        if not listing:
            return jsonify({"message": "Listing not found"}), 404
        
        if listing.user_id != current_user_id:
            return jsonify({"message": "Forbidden: You do not own this listing"}), 403
        
        if payment_successful:
            # Update listing with new tier information
            listing.is_charged_listing = True
            listing.listing_tier = requested_tier
            listing.payment_status = "paid"
            listing.transaction_id = payment_details["transaction_id"]
            listing.payment_date = datetime.now()
            
            # Set expiry date based on tier duration
            duration_days = LISTING_TIERS[requested_tier]["duration_days"]
            listing.tier_expiry_date = datetime.now() + timedelta(days=duration_days)
            
            db_placeholder.session.commit()
            
            return jsonify({
                "message": "Listing upgraded successfully",
                "payment": payment_details,
                "listing": listing.to_dict(),
                "tier_details": LISTING_TIERS[requested_tier]
            }), 200
        else:
            return jsonify({
                "message": "Payment failed",
                "payment": payment_details
            }), 400
    else:
        print(f"Simulating listing upgrade for ID: {listing_id} to tier: {requested_tier}")
        
        if payment_successful:
            # Simulate the updated listing
            mock_listing = {
                'id': listing_id,
                'title': 'Simulated Upgraded Listing',
                'price': '100000.00',
                'address': '123 Premium St',
                'user_id': current_user_id,
                'is_charged_listing': True,
                'listing_tier': requested_tier,
                'payment_status': 'paid',
                'transaction_id': payment_details["transaction_id"],
                'payment_date': datetime.now().isoformat(),
                'tier_expiry_date': (datetime.now() + timedelta(days=LISTING_TIERS[requested_tier]["duration_days"])).isoformat()
            }
            
            return jsonify({
                "message": "Listing upgrade simulated (DB not fully initialized)",
                "payment": payment_details,
                "listing": mock_listing,
                "tier_details": LISTING_TIERS[requested_tier]
            }), 200
        else:
            return jsonify({
                "message": "Payment failed (simulated)",
                "payment": payment_details
            }), 400

@payment_bp.route("/listings/<int:listing_id>/payment-status", methods=["GET"])
@jwt_required()
def get_listing_payment_status(listing_id):
    """Get the payment status and details for a listing"""
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401
    
    if db_placeholder.session:
        listing = Listing.query.get(listing_id)
        if not listing:
            return jsonify({"message": "Listing not found"}), 404
        
        if listing.user_id != current_user_id:
            return jsonify({"message": "Forbidden: You do not own this listing"}), 403
        
        payment_info = {
            "is_charged_listing": listing.is_charged_listing,
            "listing_tier": listing.listing_tier,
            "payment_status": listing.payment_status,
            "transaction_id": listing.transaction_id,
            "payment_date": listing.payment_date.isoformat() if listing.payment_date else None,
            "tier_expiry_date": listing.tier_expiry_date.isoformat() if listing.tier_expiry_date else None
        }
        
        # Add tier details if applicable
        if listing.listing_tier and listing.listing_tier in LISTING_TIERS:
            payment_info["tier_details"] = LISTING_TIERS[listing.listing_tier]
        
        return jsonify({
            "message": "Payment status retrieved successfully",
            "payment_info": payment_info
        }), 200
    else:
        print(f"Simulating payment status retrieval for listing ID: {listing_id}")
        
        # Simulate payment info
        mock_payment_info = {
            "is_charged_listing": True,
            "listing_tier": "premium",
            "payment_status": "paid",
            "transaction_id": f"TRANS-20250501-{listing_id}",
            "payment_date": datetime.now().isoformat(),
            "tier_expiry_date": (datetime.now() + timedelta(days=60)).isoformat(),
            "tier_details": LISTING_TIERS["premium"]
        }
        
        return jsonify({
            "message": "Payment status retrieval simulated (DB not fully initialized)",
            "payment_info": mock_payment_info
        }), 200
