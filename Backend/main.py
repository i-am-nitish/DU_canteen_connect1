from app import create_app
import uuid
from datetime import datetime, timedelta, timezone
import requests
from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
import os 
from apis.signup import signup_api, create_canteen_profile_api, login_api
from flask_jwt_extended import jwt_required, get_jwt_identity
from apis.no_login import all_canteens_api, fetch_canteen_info, get_canteen_review_ratings_api, get_canteen_menu_details_api
from apis.need_login import display_user_info_api, display_user_reviews_api, give_app_feedback_api, report_app_issue_api, fetch_canteen_info_handler, add_food_item_handler, report_issue_by_canteen_owner_api, fetch_canteen_reviews_owner_handler
from flask_cors import CORS
from app.models import get_user_by_id_db
import logging
app = create_app()
CORS(app)




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
    
@app.route('/display_user_info', methods=['GET'])
def display_user_info_route():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "user_id is required"}), 400
        return display_user_info_api(user_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500
    
@app.route('/display_user_reviews', methods=['GET'])
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

@app.route('/give_app_feedback', methods=['POST'])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
