# Advertisement Routes (CRUD operations for Advertisements)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required # Assuming admin/staff role for ad management
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.advertisement import Advertisement

# Placeholder for db.session, will be properly linked from main.py
class DBPlaceholder:
    session = None
    query = None
    Model = None

db_placeholder = DBPlaceholder()

advertisement_bp = Blueprint("advertisement_bp", __name__)

@advertisement_bp.route("/advertisements", methods=["POST"])
@jwt_required() # Add role checks if needed, e.g., @admin_required
def create_advertisement():
    data = request.get_json()
    required_fields = ["title", "advertiser_name", "image_url", "target_url", "placement_area", "start_date", "end_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": f"Missing required fields: {", ".join(required_fields)}"}), 400

    try:
        start_date = datetime.fromisoformat(data["start_date"])
        end_date = datetime.fromisoformat(data["end_date"])
        if start_date >= end_date:
            return jsonify({"message": "Start date must be before end date"}), 400
    except ValueError:
        return jsonify({"message": "Invalid date format for start_date or end_date. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400

    new_ad = Advertisement(
        title=data["title"],
        advertiser_name=data["advertiser_name"],
        image_url=data["image_url"],
        target_url=data["target_url"],
        placement_area=data["placement_area"],
        start_date=start_date,
        end_date=end_date,
        is_active=data.get("is_active", True)
    )

    if db_placeholder.session:
        db_placeholder.session.add(new_ad)
        db_placeholder.session.commit()
        return jsonify({"message": "Advertisement created successfully", "advertisement": new_ad.to_dict()}), 201
    else:
        print(f"Simulating advertisement creation: {new_ad.to_dict()}")
        return jsonify({"message": "Advertisement creation simulated (DB not fully initialized)", "advertisement": new_ad.to_dict()}), 201

@advertisement_bp.route("/advertisements", methods=["GET"])
def get_advertisements():
    placement_area = request.args.get("placement_area")
    active_only = request.args.get("active_only", "true").lower() == "true"
    now = datetime.utcnow()

    if db_placeholder.session:
        query = Advertisement.query
        if placement_area:
            query = query.filter_by(placement_area=placement_area)
        if active_only:
            query = query.filter(Advertisement.is_active == True, Advertisement.start_date <= now, Advertisement.end_date >= now)
        
        ads = query.order_by(Advertisement.date_created.desc()).all()
        results = [ad.to_dict() for ad in ads]
        return jsonify({"message": "Advertisements retrieved successfully", "advertisements": results}), 200
    else:
        print(f"Simulating fetching advertisements with placement: {placement_area}, active_only: {active_only}")
        # Simulate some ads
        simulated_ads = [
            {"id": 1, "title": "Simulated Ad 1", "advertiser_name": "Advertiser A", "image_url": "http://example.com/ad1.jpg", "target_url": "http://example.com", "placement_area": "homepage_banner", "start_date": now.isoformat(), "end_date": (now + timedelta(days=30)).isoformat(), "is_active": True},
            {"id": 2, "title": "Simulated Ad 2", "advertiser_name": "Advertiser B", "image_url": "http://example.com/ad2.jpg", "target_url": "http://example.com/product", "placement_area": "sidebar_listing", "start_date": now.isoformat(), "end_date": (now + timedelta(days=60)).isoformat(), "is_active": True}
        ]
        if placement_area:
            simulated_ads = [ad for ad in simulated_ads if ad["placement_area"] == placement_area]
        
        return jsonify({"message": "Advertisements retrieval simulated (DB not fully initialized)", "advertisements": simulated_ads}), 200

@advertisement_bp.route("/advertisements/<int:ad_id>", methods=["GET"])
def get_advertisement_detail(ad_id):
    if db_placeholder.session:
        ad = Advertisement.query.get(ad_id)
        if ad:
            return jsonify({"message": "Advertisement found", "advertisement": ad.to_dict()}), 200
        return jsonify({"message": "Advertisement not found"}), 404
    else:
        print(f"Simulating fetching ad detail for ID: {ad_id}")
        return jsonify({"message": "Ad detail simulated (DB not fully initialized)", "advertisement": {"id": ad_id, "title": "Simulated Ad Detail"}}), 200

@advertisement_bp.route("/advertisements/<int:ad_id>", methods=["PUT"])
@jwt_required() # Add role checks if needed
def update_advertisement(ad_id):
    if db_placeholder.session:
        ad = Advertisement.query.get(ad_id)
        if not ad:
            return jsonify({"message": "Advertisement not found"}), 404

        data = request.get_json()
        for field in ["title", "advertiser_name", "image_url", "target_url", "placement_area", "is_active"]:
            if field in data:
                setattr(ad, field, data[field])
        
        if "start_date" in data:
            try:
                ad.start_date = datetime.fromisoformat(data["start_date"])
            except ValueError:
                return jsonify({"message": "Invalid start_date format"}), 400
        if "end_date" in data:
            try:
                ad.end_date = datetime.fromisoformat(data["end_date"])
            except ValueError:
                return jsonify({"message": "Invalid end_date format"}), 400
        
        if ad.start_date and ad.end_date and ad.start_date >= ad.end_date:
            return jsonify({"message": "Start date must be before end date"}), 400

        db_placeholder.session.commit()
        return jsonify({"message": "Advertisement updated successfully", "advertisement": ad.to_dict()}), 200
    else:
        print(f"Simulating update for ad ID: {ad_id}")
        return jsonify({"message": "Ad update simulated (DB not fully initialized)"}), 200

@advertisement_bp.route("/advertisements/<int:ad_id>", methods=["DELETE"])
@jwt_required() # Add role checks if needed
def delete_advertisement(ad_id):
    if db_placeholder.session:
        ad = Advertisement.query.get(ad_id)
        if not ad:
            return jsonify({"message": "Advertisement not found"}), 404

        db_placeholder.session.delete(ad)
        db_placeholder.session.commit()
        return jsonify({"message": "Advertisement deleted successfully"}), 200
    else:
        print(f"Simulating delete for ad ID: {ad_id}")
        return jsonify({"message": "Ad deletion simulated (DB not fully initialized)"}), 200

@advertisement_bp.route("/advertisements/<int:ad_id>/track-click", methods=["POST"])
def track_ad_click(ad_id):
    if db_placeholder.session:
        ad = Advertisement.query.get(ad_id)
        if not ad:
            return jsonify({"message": "Advertisement not found"}), 404
        ad.clicks = (ad.clicks or 0) + 1
        db_placeholder.session.commit()
        # In a real app, you might redirect to ad.target_url or return a 204 No Content
        return jsonify({"message": "Click tracked successfully", "target_url": ad.target_url}), 200 
    else:
        print(f"Simulating click tracking for ad ID: {ad_id}")
        return jsonify({"message": "Click tracking simulated", "target_url": "http://example.com/simulated-target"}), 200

@advertisement_bp.route("/advertisements/<int:ad_id>/track-impression", methods=["POST"])
def track_ad_impression(ad_id):
    # This would typically be called via JS when an ad is displayed
    if db_placeholder.session:
        ad = Advertisement.query.get(ad_id)
        if not ad:
            return jsonify({"message": "Advertisement not found"}), 404
        ad.impressions = (ad.impressions or 0) + 1
        db_placeholder.session.commit()
        return jsonify({"message": "Impression tracked successfully"}), 200
    else:
        print(f"Simulating impression tracking for ad ID: {ad_id}")
        return jsonify({"message": "Impression tracking simulated"}), 200

