from flask import Blueprint, request, jsonify, redirect, url_for
from app.models import add_user, check_user_exists, add_canteen_profile, get_user_by_phone
import bcrypt
import logging
import jwt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import re



    
def signup_api():
    try:
        # Fetch form data
        name = request.form.get("name")
        phone_number = request.form.get("phone_number")
        set_password = request.form.get("set_password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")
        email = request.form.get("email")

        if not all([name, phone_number, set_password, confirm_password, role]):
            return jsonify({"message": "Missing required fields"}), 400
        
         # Validate phone number format (10 digits)
        if not re.match(r"^[6-9]\d{9}$", phone_number):
            return jsonify({"message": "Invalid format for phone number"}), 400

        # Validate email format
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            return jsonify({"message": "Invalid format for email"}), 400

        role = role.lower()
        if role not in ["general", "canteen_owner"]:
            return jsonify({"message": "Invalid role provided"}), 400

        # Check if user already exists
        if check_user_exists(phone_number, role):
            return jsonify({"message": "Account already exists"}), 400

        if set_password != confirm_password:
            return jsonify({"message": "Passwords do not match"}), 400

        hashed_password = bcrypt.hashpw(set_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user_data = {
            "name": name,
            "phone_number": phone_number,
            "password": hashed_password,
            "role": role,
            "email": email
        }

        user_id = add_user(user_data)

        # Always return user_id for frontend
        response_data = {"message": "Signup successful", "user": {"user_id": user_id}}

        # Generate token only for general users
        if role == "general":
            token = create_access_token(
                identity={"user_id": user_id, "role": role},
                expires_delta=timedelta(hours=24)
            )
            response_data["token"] = token
        return jsonify(response_data), 201

    except Exception as e:
        logging.error(f"Error during signup: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500


def create_canteen_profile_api():
    try:
        owner_id = request.form.get("owner_id")
        data = request.form

        
        canteen_name = data.get("canteen_name")
        location = data.get("location")
        description = data.get("description")
        contact_number = data.get("contact_number")
        days_open = data.get("days_open")
        opening_time = data.get("opening_time")
        closing_time = data.get("closing_time")
        peak_hr_start_time = data.get("peak_hr_start_time")
        peak_hr_end_time = data.get("peak_hr_end_time")
        required_fields = [
            canteen_name, location, description, contact_number,
            days_open, opening_time, closing_time,
            peak_hr_start_time, peak_hr_end_time
        ]
        if not all(required_fields):
         return jsonify({"message": "All fields are required"}), 400
        
        if len(contact_number) != 10 or not contact_number.isdigit():
            return jsonify({"message": "Invalid phone number format"}), 400

        profile_data = {
            "owner_id": owner_id,
            
            "canteen_name": canteen_name,
            "location": location,
            "description": description,
            "contact_number": contact_number,
            "days_open": days_open,
            "opening_time": opening_time,
            "closing_time": closing_time,
            "peak_hr_start_time": peak_hr_start_time,
            "peak_hr_end_time": peak_hr_end_time
        }

        canteen_id, response = add_canteen_profile(profile_data)
        if canteen_id is None:
            return jsonify({"message": response.get("message", "Failed to create canteen profile")}), 500

        access_token = create_access_token(
            identity={"user_id": owner_id, "role": "canteen_owner"},
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            "message": response.get("message", "Canteen profile created successfully"),
            "token": access_token,
            "canteen_id": canteen_id,
            "redirect_url": f"http://localhost:5173/canteenpage?canteen_id={canteen_id}"
        }), 201

    except Exception as e:
        logging.error(f"Error creating canteen profile: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500

    
def login_api():
    try:
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")

        
        if not phone_number or not password:
            return jsonify({"message": "Phone number and password are required"}), 400
        
        if len(phone_number) != 10 or not phone_number.isdigit():
            return jsonify({"message": "Invalid phone number format"}), 400
       
        user = get_user_by_phone(phone_number)
        if not user:
            return jsonify({"message": "Invalid phone number or password"}), 401

        logging.debug(f"Attempting login for phone: {phone_number}, hash: {user['password']}")

        if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            return jsonify({"message": "Invalid phone number or password"}), 401

        access_token = create_access_token(
            identity=user["user_id"],
            
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "name": user["name"],
                "phone_number": user["phone_number"],
                "role": user["role"],
                "email": user["email"]
            },
            "token": access_token
        }), 200
    
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
