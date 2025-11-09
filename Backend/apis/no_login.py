from flask import Blueprint, request, jsonify, redirect, url_for
from app.models import add_user, check_user_exists, add_canteen_profile, get_user_by_phone, get_all_canteens_from_db, get_canteen_info_from_db, get_canteen_reviews_and_ratings_from_db, get_canteen_menu_from_db
from app.models import get_canteens_by_name, get_food_items_by_name, get_menu_by_canteen_id, update_menu_day_columns, get_user_role_by_id_db, get_food_items_by_ids, get_canteen_by_owner_db
import bcrypt
import logging
import jwt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import json

def all_canteens_api():
    try:
        canteens = get_all_canteens_from_db()

        if not canteens:
            return jsonify({"message": "No canteens found"}), 404

        return jsonify({
            "message": "Canteens fetched successfully",
            "canteens": canteens
        }), 200

    except Exception as e:
        logging.error(f"Error in canteen API: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def fetch_canteen_info(canteen_id):
    try:
        canteen_info = get_canteen_info_from_db(canteen_id)
        if not canteen_info:
            return jsonify({"message": "Canteen not found"}), 404
        return jsonify({
            "message": "Canteen info fetched successfully",
            "canteen_info": canteen_info
        }), 200 
    except Exception as e:
        logging.error(f"Error fetching canteen info: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def get_canteen_review_ratings_api(canteen_id):
    try:
        data = get_canteen_reviews_and_ratings_from_db(canteen_id)

        if not data:
            return jsonify({"message": "Canteen not found or no reviews available"}), 404

        return jsonify({
            "message": "Canteen reviews and ratings fetched successfully",
            "data": data
        }), 200

    except Exception as e:
        logging.error(f"Error in canteen details API: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    

def get_canteen_menu_details_api(canteen_id):
    try:    
        menu_data = get_canteen_menu_from_db(canteen_id)
        if not menu_data:
                return jsonify({"message": "Menu not found"}), 404

        return jsonify({
                "message": "Canteen menu fetched successfully",
                "data": menu_data
            }), 200

    except Exception as e:
        logging.error(f"Error fetching canteen menu details: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def search_canteens_handler(query: str):
   
    try:
        results = get_canteens_by_name(query)
        if results is None:
            return jsonify({"message": "Internal Server Error", "results": []}), 500

        if len(results) == 0:
            return jsonify({"message": "No matching canteens found", "results": []}), 404

        return jsonify({
            "message": "Canteens fetched successfully",
            "results": results
        }), 200

    except Exception as e:
        logging.exception(f"Error in search_canteens_handler for query={query}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500


def search_food_items_handler(q: str, available_only: bool = False):
    """
    Handles search for food items by name.
    Returns only canteen_name, food_name, and price.
    """
    try:
        rows = get_food_items_by_name(q, available_only=available_only)
        if rows is None:
            return jsonify({"message": "Internal Server Error", "results": []}), 500

        return jsonify({
            "message": "Food items fetched",
            "results": rows
        }), 200

    except Exception as e:
        logging.exception(f"Error in search_food_items_handler for q={q}: {e}")
        return jsonify({"message": "Internal Server Error", "results": []}), 500
    
DAYS = [
    ("Monday", "monday_price"),
    ("Tuesday", "tuesday_price"),
    ("Wednesday", "wednesday_price"),
    ("Thursday", "thursday_price"),
    ("Friday", "friday_price"),
    ("Saturday", "saturday_price"),
    ("Sunday", "sunday_price"),
]

def _parse_possible_json_or_csv(value):
    """
    Try to parse a JSON array string first; if fails, try comma-separated fallback.
    Returns list (possibly empty) and a boolean indicating whether fallback was used.
    """
    if value is None:
        return [], False
    if isinstance(value, (list, tuple)):
        return list(value), False
    s = str(value).strip()
    if not s:
        return [], False
    # try JSON
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return parsed, False
        # if parsed is a single value, wrap in list
        return [parsed], False
    except Exception:
        # fallback: split by comma
        parts = [p.strip() for p in s.split(",") if p.strip() != ""]
        return parts, True

def fetch_daywise_menu_handler(canteen_id):
    """
    Business logic: fetch the menu row and produce day-wise list of {item_name, price}.
    """
    try:
        menu_row = get_menu_by_canteen_id(canteen_id)
        if menu_row is None:
            return jsonify({"message": "Menu not found for given canteen_id", "menu": {}}), 404

        menu_result = {}
        warnings = []

        for day_col, price_col in DAYS:
            raw_items = menu_row.get(day_col) if isinstance(menu_row, dict) else None
            raw_prices = menu_row.get(price_col) if isinstance(menu_row, dict) else None

            items_list, items_fallback = _parse_possible_json_or_csv(raw_items)
            prices_list, prices_fallback = _parse_possible_json_or_csv(raw_prices)

            if items_fallback or prices_fallback:
                warnings.append(f"Parsing fallback used for {day_col}")

            # attempt to convert price strings to floats where possible
            parsed_prices = []
            for p in prices_list:
                if p is None or (isinstance(p, str) and p.strip() == ""):
                    parsed_prices.append(None)
                    continue
                try:
                    parsed_prices.append(float(p))
                except Exception:
                    # try remove currency symbol then parse
                    try:
                        cleaned = ''.join(ch for ch in str(p) if (ch.isdigit() or ch == '.' or ch == '-'))
                        parsed_prices.append(float(cleaned) if cleaned else None)
                    except Exception:
                        parsed_prices.append(None)

            # pair up to min length
            pair_count = min(len(items_list), len(parsed_prices)) if parsed_prices else len(items_list)
            day_entries = []
            if pair_count == 0 and (items_list or parsed_prices):
                # If items exist but no prices, still include items with null price
                for i, itm in enumerate(items_list):
                    price_val = parsed_prices[i] if i < len(parsed_prices) else None
                    day_entries.append({"item_name": itm, "price": price_val})
            else:
                for i in range(pair_count):
                    day_entries.append({"item_name": items_list[i], "price": parsed_prices[i] if i < len(parsed_prices) else None})

                # if there are extra items with no corresponding price, append them with price null
                if len(items_list) > pair_count:
                    for i in range(pair_count, len(items_list)):
                        day_entries.append({"item_name": items_list[i], "price": None})
                # if there are extra prices with no items, ignore them but warn
                if len(parsed_prices) > pair_count:
                    warnings.append(f"{day_col}: extra prices ignored")

            menu_result[day_col] = day_entries

        response = {"message": "Menu fetched successfully", "menu": menu_result}
        if warnings:
            response["warnings"] = warnings
        return jsonify(response), 200

    except Exception as e:
        logging.exception(f"Error in fetch_daywise_menu_handler for canteen_id {canteen_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

VALID_DAYS = {
    "monday": ("Monday", "monday_price"),
    "tuesday": ("Tuesday", "tuesday_price"),
    "wednesday": ("Wednesday", "wednesday_price"),
    "thursday": ("Thursday", "thursday_price"),
    "friday": ("Friday", "friday_price"),
    "saturday": ("Saturday", "saturday_price"),
    "sunday": ("Sunday", "sunday_price")
}

def _normalize_food_ids(food_ids):
    """Ensure list of ints (or strings) returned, filter out empties."""
    if not food_ids:
        return []
    return [fid for fid in [str(x).strip() for x in food_ids] if fid]


def update_daywise_menu_handler(user_id, canteen_id, day, food_ids):
    """
    user_id: id from JWT
    canteen_id: target canteen
    day: one of Monday..Sunday (case-insensitive)
    food_ids: list of food_id strings/ints
    """
    try:
        # Validate inputs
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        if not day:
            return jsonify({"message": "day is required"}), 400

        day_key = day.strip().lower()
        if day_key not in VALID_DAYS:
            return jsonify({"message": "Invalid day. Must be one of Monday..Sunday"}), 400

        day_col, price_col = VALID_DAYS[day_key]

        # Verify user is canteen owner of this canteen
        user_row = get_user_role_by_id_db(user_id)
        if not user_row:
            return jsonify({"message": "User not found"}), 404

        role = (user_row.get("role") or "").lower()
        if role != "canteen_owner":
            return jsonify({"message": "Access denied. Only canteen owners can update menu."}), 403

        # Confirm ownership - fetch canteen by owner and compare canteen_id
        canteen_row = get_canteen_by_owner_db(user_id)
        if not canteen_row:
            return jsonify({"message": "Canteen not found for owner"}), 404

        owner_canteen_id = str(canteen_row.get("canteen_id"))
        if str(canteen_id) != owner_canteen_id:
            return jsonify({"message": "Access denied. You do not own this canteen."}), 403

        # Get menu row
        menu_row = get_menu_by_canteen_id(canteen_id)
        if not menu_row:
            return jsonify({"message": "Menu not found for this canteen (create menu first)"}), 404

        menu_id = menu_row.get("menu_id")

        # Normalize incoming food ids
        food_ids = _normalize_food_ids(food_ids)
        if not food_ids:
            return jsonify({"message": "No food_ids provided"}), 400

        # Fetch food items details for these ids but ensure they belong to this menu_id
        foods = get_food_items_by_ids(menu_id, food_ids)
        if foods is None:
            return jsonify({"message": "Internal Server Error"}), 500

        if len(foods) == 0:
            return jsonify({"message": "No valid food items found for this menu/canteen"}), 400

        # foods: list of dicts {food_id, name, price}
        # Prepare lists to append
        append_names = []
        append_prices = []
        invalid_ids = []
        for fid in food_ids:
            found = next((f for f in foods if str(f.get("food_id")) == str(fid)), None)
            if found:
                append_names.append(found.get("name"))
                # ensure numeric price if possible
                try:
                    price_val = float(found.get("price")) if found.get("price") is not None else None
                except Exception:
                    price_val = None
                append_prices.append(price_val)
            else:
                invalid_ids.append(fid)

        # Fetch existing lists from menu_row, parse JSON or fallbacks (model returns raw column values)
        # The model function update_menu_day_columns handles parsing/updating atomically, but we prepare new lists to pass in.
        result = update_menu_day_columns(menu_id=menu_id, day_col=day_col, price_col=price_col,
                                         append_item_names=append_names, append_item_prices=append_prices)
        if result is None:
            return jsonify({"message": "Failed to update menu"}), 500

        response = {
            "message": "Menu updated successfully",
            "menu_id": menu_id,
            "day": day_col,
            "updated_items": result.get("updated_items"),
            "updated_prices": result.get("updated_prices"),
        }
        if invalid_ids:
            response["warnings"] = [f"These food_ids were invalid or not part of this menu: {invalid_ids}"]
        return jsonify(response), 200

    except Exception as e:
        logging.exception(f"Error in update_daywise_menu_handler: {e}")
        return jsonify({"message": "Internal Server Error"}), 500