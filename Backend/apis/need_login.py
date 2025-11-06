from flask import Blueprint, request, jsonify, redirect, url_for
from app.models import get_user_by_id_db, get_reviews_by_id_db, submit_user_feedback_db, insert_issue_for_user_db, get_user_role_by_id_db, get_canteen_by_owner_db, get_canteen_id_by_owner, get_menu_id_by_canteen, insert_food_item_for_menu, insert_issue_for_canteen_owner
from app.models import get_reviews_for_canteen, recalc_canteen_aggregates, get_canteen_by_id, insert_review_for_canteen, get_open_app_issues, fetch_all_app_feedback_rows, update_user_info_db, update_canteen_profile_db
import logging
import jwt
from flask_jwt_extended import create_access_token
from datetime import timedelta

def display_user_info_api(user_id):
    try:
        user_info = get_user_by_id_db(user_id)
        if not user_info:
            return jsonify({"message": "User not found"}), 404
        
        role = user_info.get("role")
        if role.lower() != "general":
            return jsonify({"message": "Access denied. Only general users can access this page."}), 403
        
        return jsonify({
            "message": "User info fetched successfully",
            "user_info": user_info
        }), 200 
    except Exception as e:
        logging.error(f"Error fetching user info: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    
def display_user_reviews_api(user_id):
    try:
        reviews_info = get_reviews_by_id_db(user_id)
        if not reviews_info:
            return jsonify({"message": "No reviews yet"}), 404
        return jsonify({
            "message": "Top reviews fetched successfully", "reviews": reviews_info
        }), 200 
    except Exception as e:
        logging.exception(f"Error while getting top reviews for user_id {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def give_app_feedback_api(user_id):
    try:
        # Accept JSON or form-data. Prefer JSON key 'feedback' or form key 'feedback' or 'feedback_text'
        feedback_text = None
        if request.content_type and 'application/json' in request.content_type:
            payload = request.get_json(silent=True) or {}
            feedback_text = payload.get('feedback') or payload.get('feedback_text')
        else:
            feedback_text = (request.form.get('feedback') or
                             request.form.get('feedback_text') or
                             request.form.get('feedback/suggestions'))

        if not feedback_text:
            return jsonify({"message": "Feedback is required"}), 400

        logging.info(f"Feedback from user {user_id}: {feedback_text}")
        return submit_user_feedback_db(user_id, feedback_text)

    except Exception as e:
        logging.exception("Unexpected error in give_app_feedback_api")
        return jsonify({"message": "Internal Server Error"}), 500
    
def report_app_issue_api(user_id):
    try:
        # accept form or JSON
        issue_text = None
        if request.content_type and 'application/json' in request.content_type:
            payload = request.get_json(silent=True) or {}
            issue_text = payload.get('issue_text') or payload.get('issue')
        else:
            issue_text = request.form.get('issue_text') or request.form.get('issue')

        if not issue_text:
            return jsonify({"message": "Issue description is required"}), 400

        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404

        role = user_row.get("role")
        if role is None:
            logging.error(f"Role missing for user_id {user_id}")
            return jsonify({"message": "User role not available"}), 500

        # insert issue (insert_issue_for_user_db returns dict or None)
        result = insert_issue_for_user_db(user_id, role, issue_text)
        if result is None:
            logging.error(f"Failed to insert issue for user_id {user_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        issue_id = result.get("issue_id")
        return jsonify({"message": "Issue submitted successfully", "issue_id": issue_id}), 201

    except Exception as e:
        logging.exception("Unexpected error in report_app_issue_api")
        return jsonify({"message": "Internal Server Error"}), 500
    
def fetch_canteen_info_handler(owner_id):
    """
    Business logic:
      - Verify user exists and role == 'canteen_owner'
      - Fetch canteen where canteens.owner_user_id = user_id
      - Return canteen info or errors
    """
    try:
        user_row = get_user_role_by_id_db(owner_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404

        role = (user_row.get("role") or "").lower()
        if role != "canteen_owner":
            return jsonify({"message": "Access denied. Only canteen owners can view canteen info."}), 403

        # fetch canteen owned by this user
        canteen = get_canteen_by_owner_db(owner_id)
        if canteen is None:
            # could be DB error (models returns None on error). Distinguish if desired.
            return jsonify({"message": "Canteen not found"}), 404

        return jsonify({"message": "Canteen info fetched successfully", "canteen_info": canteen}), 200

    except Exception as e:
        logging.exception(f"Error in fetch_canteen_info_handler for user_id {owner_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    

def add_food_item_handler(user_id, name, price, description=None, status=None):
    """
    Business logic to validate form data, verify ownership, and insert food item.
    """
    try:
        # Validate input
        if not name:
            return jsonify({"message": "name is required"}), 400
        if price is None or str(price).strip() == "":
            return jsonify({"message": "price is required"}), 400

        # normalize and validate price
        try:
            price_val = float(price)
            if price_val < 0:
                return jsonify({"message": "price must be non-negative"}), 400
        except ValueError:
            return jsonify({"message": "price must be a numeric value"}), 400

        # Normalize status -> store as 'available'/'unavailable' or 1/0 depending on your DB.
        # We'll normalize to string 'available' or 'unavailable' here; models can convert if needed.
        status_norm = None
        if status is not None:
            s = str(status).strip().lower()
            if s in ("0", "false", "unavailable", "no"):
                status_norm = "unavailable"
            elif s in ("1", "true", "available", "yes"):
                status_norm = "available"
            else:
                # accept custom statuses, but prefer canonical values
                status_norm = s

        # 1) get canteen_id for this owner
        canteen_id = get_canteen_id_by_owner(user_id)
        if canteen_id is None:
            # Could be that user has no canteen (or DB error). Distinguish if models returns special sentinel.
            return jsonify({"message": "Canteen not found for this owner"}), 404

        # 2) get menu_id for this canteen
        menu_id = get_menu_id_by_canteen(canteen_id)
        if menu_id is None:
            return jsonify({"message": "Menu not found for this canteen"}), 404

        # 3) insert food item
        result = insert_food_item_for_menu(menu_id, name, description, price_val, status_norm)
        # result is dict with 'food_id' or None on DB error
        if result is None:
            logging.error(f"DB error while inserting food item for menu {menu_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        return jsonify({
            "message": "Food item added successfully",
            "food_id": result.get("food_id")
        }), 201

    except Exception as e:
        logging.exception(f"Unhandled error in add_food_item_handler for user_id {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    

def report_issue_by_canteen_owner_api(user_id, description: str):
    
    try:
        if not description or not str(description).strip():
            return jsonify({"message": "description is required"}), 400

        # Verify user and role
        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404

        role = (user_row.get("role") or "").lower()
        if role != "canteen_owner":
            return jsonify({"message": "Access denied. Only canteen owners can report this issue."}), 403

        # Get canteen_id for this owner
        canteen_id = get_canteen_id_by_owner(user_id)
        if canteen_id is None:
            return jsonify({"message": "Canteen not found for this owner"}), 404

        # Default status
        status_to_use = "open"

        # Insert issue
        result = insert_issue_for_canteen_owner(user_id, role, canteen_id, description.strip(), status_to_use)
        if result is None:
            logging.error(f"DB error while inserting issue for owner {user_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        return jsonify({"message": "Issue reported successfully", "issue_id": result.get("issue_id")}), 201

    except Exception as e:
        logging.exception(f"Error in report_issue_by_canteen_owner for user_id {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def fetch_canteen_reviews_owner_handler(user_id):
    """
    Business logic:
      - ensure user exists and role == 'canteen_owner'
      - fetch canteen owned by this user
      - fetch all reviews for that canteen
      - return canteen_info and reviews
    """
    try:
        # 1) verify user and role
        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404

        role = (user_row.get("role") or "").lower()
        if role != "canteen_owner":
            return jsonify({"message": "Access denied. Only canteen owners can access this endpoint."}), 403

        # 2) fetch canteen owned by this user
        canteen = get_canteen_by_owner_db(user_id)
        if not canteen:
            return jsonify({"message": "Canteen not found for this owner"}), 404

        canteen_id = canteen.get("canteen_id") if isinstance(canteen, dict) else (canteen[0] if isinstance(canteen, (list,tuple)) else None)
        if not canteen_id:
            logging.error(f"Unable to determine canteen_id for owner {user_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        result = get_reviews_for_canteen(canteen_id)

        # handle DB error
        if result is None:
            logging.error(f"DB error while fetching reviews for canteen {canteen_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        # handle canteen not found (models returns {"canteen": None, "reviews": []})
        if result.get("canteen") is None:
            return jsonify({"message": "Canteen not found"}), 404

        # success
        canteen_info = result.get("canteen")
        reviews = result.get("reviews", [])

        return jsonify({
            "message": "Canteen reviews fetched successfully",
            "canteen_info": canteen_info,
            "reviews": reviews
        }), 200

    except Exception as e:
        logging.exception(f"Error in fetch_canteen_reviews_handler for user_id {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def _validate_rating(value, name, required=False):
    """Convert and validate rating field (0–5)."""
    if value is None or value == "":
        if required:
            raise ValueError(f"{name} is required")
        return None
    try:
        v = float(value)
    except Exception:
        raise ValueError(f"{name} must be numeric")
    if v < 0 or v > 5:
        raise ValueError(f"{name} must be between 0 and 5")
    return v


def submit_canteen_review_handler(
    user_id,
    canteen_id,
    overall_rating,
    food_rating,
    hygiene_rating,
    staff_rating,
    facilities_rating,
    review_text
):
    """
    Handles logic for canteen review submission with optional images.
    """
    try:
        # --- Validate required fields ---
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400

        # Check if canteen exists
        canteen = get_canteen_by_id(canteen_id)
        if not canteen:
            return jsonify({"message": "Canteen not found"}), 404

        try:
            overall_rating = _validate_rating(overall_rating, "overall_rating", required=True)
            food_rating = _validate_rating(food_rating, "food_rating")
            hygiene_rating = _validate_rating(hygiene_rating, "hygiene_rating")
            staff_rating = _validate_rating(staff_rating, "staff_rating")
            facilities_rating = _validate_rating(facilities_rating, "facilities_rating")
        except ValueError as ve:
            return jsonify({"message": str(ve)}), 400

        # --- Handle image uploads

        # --- Insert review ---
        insert_result = insert_review_for_canteen(
            canteen_id=canteen_id,
            user_id=user_id,
            overall_rating=overall_rating,
            food_rating=food_rating,
            hygiene_rating=hygiene_rating,
            staff_rating=staff_rating,
            facilities_rating=facilities_rating,
            review_text=review_text
        )

        if insert_result is None:
            logging.error(f"Database error while inserting review for canteen {canteen_id}")
            return jsonify({"message": "Failed to add review"}), 500

        review_id = insert_result.get("review_id")

        # --- Recalculate canteen averages ---
        agg_result = recalc_canteen_aggregates(canteen_id)
        if agg_result is None:
            logging.error(f"Failed to update canteen aggregates for canteen {canteen_id}")
            return jsonify({
                "message": "Review added but failed to update canteen averages",
                "review_id": review_id
            }), 201

        # --- Success response ---
        return jsonify({
            "message": "Review and rating submitted successfully",
            "review_id": review_id,
            "updated_aggregates": agg_result
        }), 201

    except Exception as e:
        logging.exception(f"Unexpected error in submit_canteen_review_handler: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def admin_get_open_issues_handler(user_id):
    
    try:
        # 1) verify role
       
        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404
        role = (user_row.get("role") or "").lower()
        if role != "admin":
            return jsonify({"message": "Access denied. Admins only."}), 403

        # 2) fetch open issues
        issues = get_open_app_issues()
        if issues is None:
            logging.error("DB error while fetching open app issues")
            return jsonify({"message": "Internal Server Error"}), 500

        return jsonify({"message": "Open issues fetched successfully", "issues": issues}), 200

    except Exception as e:
        logging.exception(f"Error in admin_get_open_issues_handler for user {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def admin_get_app_feedbacks_handler(user_id, role_in_token=None):
    
    try:
        # 1) role check (token or DB)
        
        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404
        if (user_row.get("role") or "").lower() != "admin":
            return jsonify({"message": "Access denied. Admins only."}), 403

        # 2) fetch feedback rows
        rows = fetch_all_app_feedback_rows()
        if rows is None:
            logging.error("DB error while fetching app feedback rows")
            return jsonify({"message": "Internal Server Error"}), 500

        # 3) transform: each feedback_text_1 / feedback_text_2 becomes its own entry
        feedbacks = []
        for r in rows:
            fid = r.get("feedback_id") if isinstance(r, dict) else r[0]
            uid = r.get("user_id") if isinstance(r, dict) else r[1]
            f1 = r.get("feedback_text_1") if isinstance(r, dict) else r[2]
            f2 = r.get("feedback_text_2") if isinstance(r, dict) else r[3]
            created = r.get("created_at") if isinstance(r, dict) else r[4]

            if f1 and str(f1).strip():
                feedbacks.append({
                    "feedback_id": fid,
                    "user_id": uid,
                    "feedback_text": f1.strip(),
                    "slot": "feedback_text_1",
                    "created_at": created
                })
            if f2 and str(f2).strip():
                feedbacks.append({
                    "feedback_id": fid,
                    "user_id": uid,
                    "feedback_text": f2.strip(),
                    "slot": "feedback_text_2",
                    "created_at": created
                })

        return jsonify({"message": "App feedbacks fetched successfully", "feedbacks": feedbacks}), 200

    except Exception as e:
        logging.exception(f"Error in admin_get_app_feedbacks_handler for user {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def update_user_info_handler(user_id, name, phone_number, email, password_hash):
    try:
       
        user = get_user_by_id_db(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Build dictionary of fields to update
        update_fields = {}
        if name:
            update_fields["name"] = name
        if phone_number:
            update_fields["phone_number"] = phone_number
        if email:
            update_fields["email"] = email
        if password_hash:
            update_fields["password_hash"] = password_hash

        if not update_fields:
            return jsonify({"message": "No fields to update"}), 400

        success = update_user_info_db(user_id, update_fields)
        if not success:
            return jsonify({"message": "Failed to update user info"}), 500

        return jsonify({"message": "User info updated successfully"}), 200

    except Exception as e:
        logging.exception(f"Error in update_user_info_handler: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def update_canteen_profile_handler(user_id, update_payload: dict):
    
    try:
        
        user_row = get_user_role_by_id_db(user_id)
        if user_row is None:
            return jsonify({"message": "User not found"}), 404

        if (user_row.get("role") or "").lower() != "canteen_owner":
            return jsonify({"message": "Access denied. Only canteen owners can update profile."}), 403

        # Fetch canteen owned by this user
        canteen = get_canteen_by_owner_db(user_id)
        if canteen is None:
            return jsonify({"message": "Canteen not found for this owner"}), 404

        canteen_id = canteen.get("canteen_id") if isinstance(canteen, dict) else (canteen[0] if isinstance(canteen, (list,tuple)) else None)
        if not canteen_id:
            logging.error(f"Unable to determine canteen_id for owner {user_id}")
            return jsonify({"message": "Internal Server Error"}), 500

        if not update_payload:
            return jsonify({"message": "No fields to update"}), 400

        # Only allow whitelisted columns (safety)
        allowed = {"name","location","description","contact_no","days_open","opening_time","closing_time","peak_hr_start_time","peak_hr_end_time"}
        fields_to_update = {k:v for k,v in update_payload.items() if k in allowed}

        if not fields_to_update:
            return jsonify({"message": "No updatable fields provided"}), 400

        success = update_canteen_profile_db(canteen_id=canteen_id, update_fields=fields_to_update)
        if not success:
            return jsonify({"message": "Failed to update canteen profile"}), 500

        return jsonify({"message": "Canteen profile updated successfully"}), 200

    except Exception as e:
        logging.exception(f"Error in update_canteen_profile_handler for user {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500