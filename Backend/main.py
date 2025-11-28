from app import create_app
import uuid
from datetime import datetime, timedelta, timezone
import requests
from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
import os 
from apis.signup import signup_api, create_canteen_profile_api, login_api
from flask_jwt_extended import jwt_required, get_jwt_identity
from apis.no_login import all_canteens_api, get_canteen_review_ratings_api, get_canteen_menu_details_api,  search_canteens_handler, search_food_items_handler
from apis.need_login import submit_canteen_review_handler, admin_get_open_issues_handler, admin_get_app_feedbacks_handler
import logging
from apis.no_login import all_canteens_api, get_canteen_review_ratings_api, get_canteen_menu_details_api, fetch_daywise_menu_handler, update_daywise_menu_handler, fetch_canteen_info
from apis.need_login import display_user_info_api, display_user_reviews_api, give_app_feedback_api, report_app_issue_api, fetch_canteen_info_handler, add_food_item_handler, report_issue_by_canteen_owner_api, fetch_canteen_reviews_owner_handler, fetch_food_items_owner_handler, update_user_info_handler, update_canteen_profile_handler
from flask_cors import CORS
from app.models import get_user_by_id_db, update_menu_images, update_canteen_images
import bcrypt
import logging
from app.cloudinary_setup import cloudinary
import cloudinary.uploader
from app.models import _upload_to_cloudinary

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

def upload_files_to_cloudinary(files_in_order):
    
    urls = []
    for f in files_in_order:
        if f:
            url = _upload_to_cloudinary(f)
            urls.append(url)
    return urls



@app.route('/check_jwt_status', methods=['POST'])
@jwt_required()
def check_jwt_status():
    jwt_data = get_jwt()
    exp_timestamp = jwt_data['exp']
    now = datetime.now(timezone.utc)
    exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    remaining = exp - now

    return jsonify({'message': 'JWT is valid.','remaining_time': str(remaining), 'status': 'success'}), 200

@app.route('/signup', methods=['POST'])
def signup_route(): 
    return signup_api()

@app.route("/create_canteen_profile", methods=["POST"])
def create_profile_route():
    return create_canteen_profile_api()

@app.route("/login", methods=["POST"])
def login_route():
    return login_api()
@app.route('/canteens', methods=['GET'])
def canteens_route():
    return all_canteens_api()

@app.route('/canteen_info', methods=['GET'])
def canteen_info_route():
    try:
        canteen_id = request.args.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return fetch_canteen_info(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500   
    
@app.route('/canteen_review_ratings', methods=['GET'])
def get_canteen_reviews_and_ratings_route():
    try:
        canteen_id = request.args.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return get_canteen_review_ratings_api(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500
    

@app.route('/canteen_menu_details', methods=['GET'])
def canteen_menu_details_route():
    try:
        canteen_id = request.args.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return get_canteen_menu_details_api(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500
    


@app.route('/add_review_rating', methods=['POST'])
@jwt_required()
def submit_review_route():
    
    try:
        
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        # form fields
        canteen_id = request.form.get("canteen_id")
        overall_rating = request.form.get("overall_rating")
        food_rating = request.form.get("food_rating")
        hygiene_rating = request.form.get("hygiene_rating")
        staff_rating = request.form.get("staff_rating")
        facilities_rating = request.form.get("facilities_rating")
        review_text = request.form.get("review_text", "").strip()

        # files
        image_1 = request.files.get("image_1")
        image_2 = request.files.get("image_2")
        image_3 = request.files.get("image_3")

        return submit_canteen_review_handler(
            user_id=user_id,
            canteen_id=canteen_id,
            overall_rating=overall_rating,
            food_rating=food_rating,
            hygiene_rating=hygiene_rating,
            staff_rating=staff_rating,
            facilities_rating=facilities_rating,
            review_text=review_text
        )

    except Exception as e:
        logging.exception("Unexpected error in submit_review_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/display_user_reviews', methods=['GET'])
@jwt_required()
def display_user_reviews_route():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "user_id is required"}), 400
        user_info = get_user_by_id_db(user_id)
        if not user_info:
            return jsonify({"message": "User not found"}), 404

        role = user_info.get("role")
        if not role or str(role).lower() != "general":
            return jsonify({"message": "Access denied. Only general users can access this page."}), 403

        return display_user_reviews_api(user_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500    


# for the admin panel 



@app.route('/admin/app_issues/open', methods=['GET'])
@jwt_required()
def admin_get_open_issues_route():
    
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        # delegate to handler (handler will verify role either via token or DB)
        return admin_get_open_issues_handler(user_id)

    except Exception as e:
        logging.exception("Unexpected error in admin_get_open_issues_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/admin/app_feedbacks', methods=['GET'])
@jwt_required()
def admin_get_app_feedbacks_route():
    
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        return admin_get_app_feedbacks_handler(user_id)
    except Exception as e:
        logging.exception("Unexpected error in admin_get_app_feedbacks_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
# search apis 

@app.route('/search/canteens', methods=['GET'])
def search_canteens_route():
    
    try:
        q = (request.args.get('q') or "").strip()
        if not q:
            return jsonify({"message": "q parameter is required", "results": []}), 400

        return search_canteens_handler(q)
    except Exception as e:
        logging.exception("Unexpected error in search_canteens_route")
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/search/food_items', methods=['GET'])
def search_food_items_route():
    
    try:
        q = (request.args.get('q') or "").strip()
        if not q:
            return jsonify({"message": "q parameter is required", "results": []}), 400

        available_only = str(request.args.get("available_only") or "").lower() in ("1", "true", "yes")
        return search_food_items_handler(q, available_only=available_only)
    except Exception as e:
        logging.exception("Unexpected error in search_food_items_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/display_user_info', methods=['GET'])
@jwt_required()
def display_user_info_route():
    try:
        user_id = get_jwt_identity()
        logging.info(f"Got user_id from JWT: {user_id}")
        if not user_id:
            return jsonify({"message": "Invalid token"}), 401

        return display_user_info_api(user_id)
    except Exception as e:
        logging.error(f" Error in display_user_info_route: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/give_app_feedback', methods=['POST'])
@jwt_required()
def give_app_feedback_route():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "user_id is required"}), 400
        
        user_info = get_user_by_id_db(user_id)
        if not user_info:
            return jsonify({"message": "User not found"}), 404

        role = user_info.get("role")
        if not role or str(role).lower() != "general":
            return jsonify({"message": "Access denied. Only general users can access this page."}), 403
        return give_app_feedback_api(user_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500

@app.route('/report_app_issue', methods=['POST'])
@jwt_required()
#to be reveiwed - Allow all authenticated users to report issues
def report_app_issue_route():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "user_id is required"}), 400
        
        user_info = get_user_by_id_db(user_id)
        if not user_info:
            return jsonify({"message": "User not found"}), 404

        role = user_info.get("role")
        if not role or str(role).lower() != "general":
            return jsonify({"message": "Access denied. Only general users can access this page."}), 403
        return report_app_issue_api(user_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/get_canteen_info_owner', methods=['GET'])
@jwt_required()
def get_canteen_info_owner_route():
    try:
        owner_id = get_jwt_identity()
        if not owner_id:
            return jsonify({"message": "owner_id is required"}), 400
        
    
        return fetch_canteen_info_handler(owner_id)

    except Exception as e:
        logging.exception("Unexpected error in canteen_info_route")
        return jsonify({"message": "Internal Server Error"}), 500
    

@app.route('/add_food_item', methods=['POST'])
@jwt_required()
def add_food_item_route():
    try:
        owner_id = get_jwt_identity()
        if not owner_id:
            return jsonify({"message": "owner_id is required"}), 400
        
        item_name = request.form.get("item_name", "").strip()
        item_price = request.form.get("item_price")

        description = request.form.get("description", "").strip()
        status = request.form.get("status")  # optional; we normalize in handler

        return add_food_item_handler(owner_id, item_name, item_price, description, status)
    except Exception as e:
        logging.exception("Unexpected error in add_food_item_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/report_issue_canteen_owner', methods=['POST'])
@jwt_required()
def report_issue_canteen_owner_route():
    try:
        owner_id = get_jwt_identity()
        if not owner_id:
            return jsonify({"message": "owner_id is required"}), 400
        
        issue_text = request.form.get("issue_text")
        if not issue_text:
            return jsonify({"message": "Issue description is required"}), 400

        return report_issue_by_canteen_owner_api(owner_id, issue_text)

    except Exception as e:
        logging.exception("Unexpected error in report_issue_route")
        return jsonify({"message": "Internal Server Error"}), 500

@app.route('/canteen_reviews_owner', methods=['GET'])
@jwt_required()
def canteen_reviews_Owner_route():
    """
    GET /canteen_reviews
    Returns canteen_info + reviews for the canteen owned by the logged-in canteen_owner.
    """
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        return fetch_canteen_reviews_owner_handler(user_id)

    except Exception as e:
        logging.exception("Unexpected error in canteen_reviews_route")
        return jsonify({"message": "Internal Server Error"}), 500
    
 
@app.route('/food_items_owner', methods=['GET'])
@jwt_required()
def food_items_owner_route():
    """
    GET /food_items_owner
    Returns all food items for the canteen owned by the logged-in canteen_owner.
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        return fetch_food_items_owner_handler(user_id)

    except Exception as e:
        logging.exception("Unexpected error in food_items_owner_route")
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/menu/daywise', methods=['POST'])
@jwt_required()
def menu_daywise_route():
    """
    Expects form-data: canteen_id (required)
    Returns day-wise menu mapping (Monday..Sunday) with list of {item_name, price}.
    """
    try:
        canteen_id = request.form.get("canteen_id")
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400

        return fetch_daywise_menu_handler(canteen_id)

    except Exception as e:
        logging.exception("Unexpected error in /menu/daywise")
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route("/menu/update_day", methods=["POST"])
@jwt_required()
def update_daywise_menu_route():
    """
    Form-data:
      canteen_id: required
      day: required (Monday..Sunday)
      food_ids: repeated form field OR comma-separated string
    """
    try:
        identity = get_jwt_identity()
        user_id = identity.get("user_id") if isinstance(identity, dict) else identity
        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        canteen_id = request.form.get("canteen_id")
        day = (request.form.get("day") or "").strip()
        # Accept multiple food_ids
        food_ids = request.form.getlist("food_ids")
        if not food_ids:
            # maybe comma separated in a single field
            s = request.form.get("food_ids")
            if s:
                food_ids = [p.strip() for p in s.split(",") if p.strip()]

        return update_daywise_menu_handler(user_id=user_id, canteen_id=canteen_id, day=day, food_ids=food_ids)

    except Exception as e:
        logging.exception("Unexpected error in update_daywise_menu_route")
        return jsonify({"message": "Internal Server Error"}), 500
    

@app.route("/user_profile_update", methods=["POST"])
@jwt_required()
def update_user_info_route():
    
    try:
        identity = get_jwt_identity()
        user_id = identity.get("user_id") if isinstance(identity, dict) else identity
        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        name = request.form.get("name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        new_password = request.form.get("password")

        hashed_password = None
        if new_password:
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

        return update_user_info_handler(
            user_id=user_id,
            name=name,
            phone_number=phone_number,
            email=email,
            password_hash=hashed_password
        )

    except Exception as e:
        logging.exception("Error in /user/update route")
        return jsonify({"message": "Internal Server Error"}), 500

@app.route("/canteen_profile_update", methods=["POST"])
@jwt_required()
def update_canteen_profile_route():
   
    try:
        identity = get_jwt_identity()
        user_id = identity.get("user_id") if isinstance(identity, dict) else identity
        if not user_id:
            return jsonify({"message": "Invalid token / user identity"}), 401

        # Read form fields (all optional)
        payload = {
            "name": request.form.get("name"),
            "location": request.form.get("location"),
            "description": request.form.get("description"),
            "contact_no": request.form.get("contact_no"),
            "days_open": request.form.get("days_open"),
            "opening_time": request.form.get("opening_time"),
            "closing_time": request.form.get("closing_time"),
            "peak_hr_start_time": request.form.get("peak_hr_start_time"),
            "peak_hr_end_time": request.form.get("peak_hr_end_time"),
        }

        # Remove None values (only update provided fields)
        update_payload = {k: v for k, v in payload.items() if v is not None}

        return update_canteen_profile_handler(user_id=user_id, update_payload=update_payload)

    except Exception as e:
        logging.exception("Unexpected error in /canteen/update")
        return jsonify({"message": "Internal Server Error"}), 500
    

@app.route("/upload_menu_image", methods=["POST"])
def upload_menu_image_route():
    try:
        canteen_id = request.form.get("canteen_id")
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400

        # Accept either menu_file_1/menu_file_2 or arbitrary files in order
        menu_file_1 = request.files.get("menu_file_1")
        menu_file_2 = request.files.get("menu_file_2")

        if not menu_file_1 and not menu_file_2:
            return jsonify({"message": "No files provided"}), 400

        
        uploaded_urls = upload_files_to_cloudinary([menu_file_1, menu_file_2])

        
        updated = update_menu_images(canteen_id, uploaded_urls)

        return jsonify({"message": "Menu images updated", "data": updated}), 200

    except Exception as e:
        logging.exception("Error in upload_menu_image_route: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route("/upload_canteen_images", methods=["POST"])
def upload_canteen_images_route():
    try:
        canteen_id = request.form.get("canteen_id")
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400

        canteen_image_1 = request.files.get("canteen_image_1")
        canteen_image_2 = request.files.get("canteen_image_2")
        if not canteen_image_1 and not canteen_image_2:
            return jsonify({"message": "No files provided"}), 400

        uploaded_urls = upload_files_to_cloudinary([canteen_image_1, canteen_image_2])
        updated = update_canteen_images(canteen_id, uploaded_urls)

        return jsonify({"message": "Canteen images updated", "data": updated}), 200

    except Exception as e:
        logging.exception("Error in upload_canteen_images_route: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
