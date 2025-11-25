import mysql.connector
from app.logging_config import setup_logging
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
import uuid
from flask import jsonify
from flask_bcrypt import Bcrypt
import os
import re
import logging
import base64
import random
import json
from app.cloudinary_setup import cloudinary


import cloudinary.uploader
bcrypt = Bcrypt()



            
def _upload_to_cloudinary(file_obj):
    try:
        print("This cloudinary block runs")
        
        # Upload the file without providing a public_id
        result = cloudinary.uploader.upload(
            file_obj,
            folder="du_canteen/menu",  # optional folder
            overwrite=False,
            resource_type="image"
        )
        
        # The URL of the uploaded file
        url = result.get('secure_url')
        print("Uploaded file URL:", url)
        return url
    
    except Exception as e:
        logging.exception("Cloudinary upload failed: %s", e)
        return None


def get_db_connection():
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'du_canteen_hub')
        db_port = os.getenv('DB_PORT', 3306)
        db_ssl_mode = os.getenv('DB_SSL_MODE', 'DISABLED')

        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=int(db_port),
            ssl_disabled=(db_ssl_mode.upper() == 'DISABLED')
        )

        logging.info("Database connection established.")
        return connection
    except mysql.connector.Error as err :
        print(f"Error: {err}")
        logging.error("Error connecting to the database: %s", err)
        return None
    
def check_user_exists(phone_number, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE phone_number=%s AND role=%s"
    cursor.execute(query, (phone_number, role))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def add_user(user_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO users (name, phone_number, password_hash, role, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        user_data['name'],
        user_data['phone_number'],
        user_data['password'],
        user_data['role'],
        user_data['email']
    ))
    conn.commit()

    # Fetch the auto-generated user_id
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return user_id


def add_canteen_profile(profile_data):
    """
    Returns (canteen_id, menu_id, {"message": ...})
    On failure returns (None, None, {"message": ...})
    """
    if not isinstance(profile_data, dict):
        logging.error("add_canteen_profile called with non-dict profile_data: %r", profile_data)
        return None, None, {"message": "Invalid profile_data provided"}

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if canteen already exists for this owner
        check_query = "SELECT canteen_id FROM canteens WHERE owner_id = %s"
        cursor.execute(check_query, (profile_data["owner_id"],))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            conn.close()
            return None, None, {"message": "Canteen profile already exists for this owner"}

        # 1) Insert canteen
        canteen_query = """
            INSERT INTO canteens (
                owner_id, name, location, description, contact_no,
                days_open, opening_time, closing_time, peak_hr_start_time, peak_hr_end_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(canteen_query, (
            profile_data["owner_id"],
            profile_data["canteen_name"],
            profile_data["location"],
            profile_data["description"],
            str(profile_data["contact_number"]).strip(),
            profile_data["days_open"],
            profile_data["opening_time"],
            profile_data["closing_time"],
            profile_data["peak_hr_start_time"],
            profile_data["peak_hr_end_time"]
        ))
        conn.commit()
        canteen_id = cursor.lastrowid
        now = datetime.utcnow()
        # 2) Insert initial menu row
        menu_insert_query = """
            INSERT INTO menu (
                canteen_id,
                day_wise,
                Monday, monday_price,
                Tuesday, tuesday_price,
                Wednesday, wednesday_price,
                Thursday, thursday_price,
                Friday, friday_price,
                Saturday, saturday_price,
                Sunday, sunday_price,
                menu_file_1,
                menu_file_2,
                created_at,
                updated_at
            )
            VALUES (
                %s, %s,   -- canteen_id, day_wise
                %s, %s,   -- Monday, monday_price
                %s, %s,   -- Tuesday, tuesday_price
                %s, %s,   -- Wednesday, wednesday_price
                %s, %s,   -- Thursday, thursday_price
                %s, %s,   -- Friday, friday_price
                %s, %s,   -- Saturday, saturday_price
                %s, %s,   -- Sunday, sunday_price
                %s, %s,   -- menu_file1, menu_file2
                %s, %s    -- created_at, updated_at
            )
        """

        menu_values = (
            canteen_id,                          # canteen_id
            "yes",                                # day_wise
            None, None,                           # Monday, monday_price
            None, None,                           # Tuesday, tuesday_price
            None, None,                           # Wednesday, wednesday_price
            None, None,                           # Thursday, thursday_price
            None, None,                           # Friday, friday_price
            None, None,                           # Saturday, saturday_price
            None, None,                           # Sunday, sunday_price
            profile_data.get("menu_file_1"),      # menu_file1 (URL or None)
            profile_data.get("menu_file_2"),      # menu_file2 (URL or None)
            now,                                  # created_at
            now                                   # updated_at
        )

        # Debug (optional): ensure placeholders match values
        # Uncomment the next two lines to print debug info to console/log
        # logging.debug("placeholders count: %d", menu_insert_query.count("%s"))
        # logging.debug("menu_values length: %d", len(menu_values))
        logging.debug("placeholders count: %d", menu_insert_query.count("%s"))
        logging.debug("menu_values length: %d", len(menu_values))
        logging.debug("menu_values preview: %r", menu_values[:6])

        if menu_insert_query.count("%s") != len(menu_values):
            logging.error("Placeholder/value mismatch in add_canteen_profile: %s placeholders vs %s values",
                          menu_insert_query.count("%s"), len(menu_values))
            # don't attempt execution if mismatch
            return None, None, {"message": "Internal server error (menu insert mismatch)"}

        cursor.execute(menu_insert_query, menu_values)
        conn.commit()
        menu_id = cursor.lastrowid

        return canteen_id, menu_id, {"message": "Canteen profile created successfully"}

    except Exception as e:
        logging.exception(f"Error adding canteen profile: {str(e)}")
        try:
            if conn:
                conn.rollback()
        except Exception:
            pass
        return None, None, {"message": "Failed to create canteen profile"}

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass
    
def get_user_by_phone(phone_number):
    """
    Returns dict with user fields or None.
    Uses a buffered dictionary cursor and always closes cursor+connection.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("DB connection is None in get_user_by_phone")
            return None

        # buffered=True prevents "Unread result found"
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """
            SELECT user_id, name, phone_number, password_hash AS password,
                   role, email
            FROM users
            WHERE phone_number = %s
            LIMIT 1
        """
        cursor.execute(query, (phone_number,))

        user = cursor.fetchone()   # returns a dict because dictionary=True

        if not user:
            return None

        # Normalize keys to match existing code expectations
        return {
            "user_id": user.get("user_id"),
            "name": user.get("name"),
            "phone_number": user.get("phone_number"),
            "password": user.get("password"),   # password_hash aliased to password
            "role": user.get("role"),
            "email": user.get("email")
        }

    except Exception as e:
        logging.error(f"Error fetching user: {str(e)}", exc_info=True)
        return None

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def get_open_app_issues():
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        
        query = """
            SELECT issue_id, user_id, role, issue_text, created_at
            FROM app_issue
            WHERE status = %s
            ORDER BY created_at DESC
        """
        cursor.execute(query, ("open",))
        rows = cursor.fetchall() or []
        return rows
    

    except Exception as e:
        logging.exception(f"DB error in get_open_app_issues: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass

def fetch_all_app_feedback_rows():
   
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT feedback_id, user_id, feedback_text_1, feedback_text_2, created_at
            FROM app_feedback
            ORDER BY created_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall() or []
        return rows
    except Exception as e:
        logging.exception(f"DB error in fetch_all_app_feedback_rows: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass

def _like_pattern(q: str) -> str:
    return f"%{q}%"

def get_food_items_by_name(q: str, available_only: bool = False, limit: int = 50):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                c.name AS canteen_name,
                fi.name AS food_name,
                fi.price
            FROM food_items fi
            JOIN menu m ON fi.menu_id = m.menu_id
            JOIN canteens c ON m.canteen_id = c.canteen_id
            WHERE LOWER(fi.name) LIKE LOWER(%s)
             OR LOWER(c.name) LIKE LOWER(%s)  -- Also search canteen name
        """
        params = [_like_pattern(q), _like_pattern(q)]  # for fi.name and c.name

        if available_only:
            query += " AND (fi.status IS NULL OR LOWER(fi.status) IN ('available', '1', 'true', 'yes'))"

        query += " ORDER BY c.name ASC, fi.name ASC LIMIT %s"
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall() or []
        return rows

    except Exception as e:
        logging.exception(f"DB error in get_food_items_by_name for q={q}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_canteens_by_name(query: str, limit: int = 50):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query_sql = """
            SELECT
                canteen_id,
                name AS canteen_name,
                location,
                CONCAT(opening_time, ' - ', closing_time) AS timings,
                overall_rating
            FROM canteens
            WHERE LOWER(name) LIKE LOWER(%s)
            ORDER BY overall_rating DESC
            LIMIT %s
        """

        cursor.execute(query_sql, (_like_pattern(query), limit))
        rows = cursor.fetchall() or []
        return rows

    except Exception as e:
        logging.exception(f"DB error in get_canteens_by_name for query={query}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_review_for_canteen(canteen_id, user_id,
                              overall_rating, food_rating=None, hygiene_rating=None,
                              staff_rating=None, facilities_rating=None,
                              review_text=None):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        now = datetime.utcnow()
        
        insert_q = """
            INSERT INTO canteen_reviews
                (canteen_id, user_id, overall_rating, food_rating, hygiene_rating,
                 staff_rating, facilities_rating, review_text, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_q, (
            canteen_id, user_id, overall_rating, food_rating, hygiene_rating,
            staff_rating, facilities_rating, review_text, now
        ))

        conn.commit()
        
        review_id = cursor.lastrowid

        return {"review_id": review_id}

    except Exception as e:
        logging.exception(f"DB error in insert_review_for_canteen for canteen {canteen_id}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def recalc_canteen_aggregates(canteen_id):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Try Postgres-style (ROUND(..., 2)) update first; fallback to MySQL style if it errors.
        try:
            update_query_pg = """
                UPDATE canteens
                SET
                    overall_rating = (
                        SELECT ROUND(AVG(overall_rating)::numeric, 2) FROM canteen_reviews WHERE canteen_id = %s
                    ),
                    overall_food = (
                        SELECT ROUND(AVG(food_rating)::numeric, 2) FROM canteen_reviews WHERE canteen_id = %s AND food_rating IS NOT NULL
                    ),
                    overall_hygiene = (
                        SELECT ROUND(AVG(hygiene_rating)::numeric, 2) FROM canteen_reviews WHERE canteen_id = %s AND hygiene_rating IS NOT NULL
                    ),
                    overall_staff = (
                        SELECT ROUND(AVG(staff_rating)::numeric, 2) FROM canteen_reviews WHERE canteen_id = %s AND staff_rating IS NOT NULL
                    ),
                    overall_facilities = (
                        SELECT ROUND(AVG(facilities_rating)::numeric, 2) FROM canteen_reviews WHERE canteen_id = %s AND facilities_rating IS NOT NULL
                    )
                WHERE canteen_id = %s
            """
            cursor.execute(update_query_pg, (canteen_id, canteen_id, canteen_id, canteen_id, canteen_id, canteen_id))
            conn.commit()
        except Exception:
            # fallback (MySQL): no ::numeric cast
            try:
                conn.rollback()
            except Exception:
                pass
            update_query_mysql = """
                UPDATE canteens
                SET
                    overall_rating = (SELECT ROUND(AVG(overall_rating), 2) FROM canteen_reviews WHERE canteen_id = %s),
                    overall_food = (SELECT ROUND(AVG(food_rating), 2) FROM canteen_reviews WHERE canteen_id = %s AND food_rating IS NOT NULL),
                    overall_hygiene = (SELECT ROUND(AVG(hygiene_rating), 2) FROM canteen_reviews WHERE canteen_id = %s AND hygiene_rating IS NOT NULL),
                    overall_staff = (SELECT ROUND(AVG(staff_rating), 2) FROM canteen_reviews WHERE canteen_id = %s AND staff_rating IS NOT NULL),
                    overall_facilities = (SELECT ROUND(AVG(facilities_rating), 2) FROM canteen_reviews WHERE canteen_id = %s AND facilities_rating IS NOT NULL)
                WHERE canteen_id = %s
            """
            cursor.execute(update_query_mysql, (canteen_id, canteen_id, canteen_id, canteen_id, canteen_id, canteen_id))
            conn.commit()

        # fetch updated aggregates
        fetch_q = """
            SELECT overall_rating, overall_food, overall_hygiene, overall_staff, overall_facilities
            FROM canteens
            WHERE canteen_id = %s
            LIMIT 1
        """
        # Use a new cursor to ensure compatibility with some drivers
        cursor2 = conn.cursor()
        cursor2.execute(fetch_q, (canteen_id,))
        row = cursor2.fetchone()
        try:
            cursor2.close()
        except Exception:
            pass

        if not row:
            return None

        # Row may be tuple or dict depending on cursor type
        if isinstance(row, (list, tuple)):
            overall_rating, overall_food, overall_hygiene, overall_staff, overall_facilities = row
        elif isinstance(row, dict):
            overall_rating = row.get("overall_rating")
            overall_food = row.get("overall_food")
            overall_hygiene = row.get("overall_hygiene")
            overall_staff = row.get("overall_staff")
            overall_facilities = row.get("overall_facilities")
        else:
            overall_rating = overall_food = overall_hygiene = overall_staff = overall_facilities = None

        return {
            "overall_rating": float(overall_rating) if overall_rating is not None else None,
            "overall_food": float(overall_food) if overall_food is not None else None,
            "overall_hygiene": float(overall_hygiene) if overall_hygiene is not None else None,
            "overall_staff": float(overall_staff) if overall_staff is not None else None,
            "overall_facilities": float(overall_facilities) if overall_facilities is not None else None
        }

    except Exception as e:
        logging.exception(f"DB error in recalc_canteen_aggregates for {canteen_id}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass



def get_all_canteens_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  

        query = """
            SELECT 
                canteen_id,
                name,
                location,
                days_open,
                opening_time,
                closing_time,
                overall_rating
            FROM canteens
        """
        cursor.execute(query)
        canteens = cursor.fetchall()

        cursor.close()
        conn.close()

        return canteens

    except Exception as e:
        logging.error(f"Error fetching canteens from DB: {str(e)}")
        return None
    

    
def get_canteen_menu_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query_menu = "SELECT * FROM menu WHERE canteen_id = %s"
        cursor.execute(query_menu, (canteen_id,))
        menu = cursor.fetchone()

        if not menu:
            cursor.close()
            conn.close()
            return None

        # Collect menu files
        menu_files = []
        if menu.get("menu_file_1"):
            menu_files.append(menu["menu_file_1"])
        if menu.get("menu_file_2"):
            menu_files.append(menu["menu_file_2"])

        # Collect day wise menu
        day_wise_menu = []
        if menu.get("day_wise", "").lower() == "yes":
            day_columns = [
                ("Monday", "monday_price"),
                ("Tuesday", "tuesday_price"),
                ("Wednesday", "wednesday_price"),
                ("Thursday", "thursday_price"),
                ("Friday", "friday_price"),
                ("Saturday", "saturday_price"),
                ("Sunday", "sunday_price")
            ]

            for day, price_col in day_columns:
                food_ids_text = menu.get(day)
                prices_text = menu.get(price_col)

                if not food_ids_text:
                    continue

                day_wise_menu.append({
                    "day": day,
                    "items": food_ids_text,
                    "price": prices_text,
                })

        cursor.close()
        conn.close()

        # Decide final return type
        menu_type = (
            "both" if menu_files and day_wise_menu else
            "image_only" if menu_files else
            "day_wise" if day_wise_menu else
            None
        )

        return {
            "canteen_id": canteen_id,
            "menu": day_wise_menu if day_wise_menu else None,   
            "menu_files": menu_files,
            "menu_type": menu_type
        }

    except Exception as e:
        logging.error(f"Error fetching canteen menu for canteen_id {canteen_id}: {str(e)}")
        return None



def get_canteen_info_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  

        query = """
            SELECT 
                canteen_id,
                name,
                location,
                description,
                contact_no,
                days_open,
                opening_time,
                closing_time,
                peak_hr_start_time,
                peak_hr_end_time,
                overall_rating,
                canteen_image_1,
                canteen_image_2
            FROM canteens
            WHERE canteen_id = %s
        """
        cursor.execute(query, (canteen_id,))
        canteen_info = cursor.fetchone()

        canteen_info["images"] = []
        if canteen_info.get("canteen_image_1"):
            canteen_info["images"].append(canteen_info["canteen_image_1"])
        if canteen_info.get("canteen_image_2"):
            canteen_info["images"].append(canteen_info["canteen_image_2"])

        print("Canteen images array:", canteen_info)

        cursor.close()
        conn.close()

        return canteen_info

    except Exception as e:
        logging.error(f"Error fetching canteen info from DB: {str(e)}")
        return None
    
def get_canteen_reviews_and_ratings_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

    
        query_canteen = """
            SELECT 
                canteen_id,
                name,
                overall_rating,
                overall_food,
                overall_hygiene,
                overall_staff,
                overall_facilities
            FROM canteens
            WHERE canteen_id = %s
        """
        cursor.execute(query_canteen, (canteen_id,))
        canteen = cursor.fetchone()

        if not canteen:
            cursor.close()
            conn.close()
            return None  

        query_reviews = """
            SELECT 
                review_id,
                overall_rating,
                review_text,
                image_1,
                image_2,
                image_3,
                created_at
            FROM canteen_reviews
            WHERE canteen_id = %s
            ORDER BY created_at DESC
            LIMIT 5
        """
        cursor.execute(query_reviews, (canteen_id,))
        reviews = cursor.fetchall()

        cursor.close()
        conn.close()


        
        import base64
        for review in reviews:
            if review["image_1"]:
                review["image_1"] = base64.b64encode(review["image_1"]).decode("utf-8")
            if review["image_2"]:
                review["image_2"] = base64.b64encode(review["image_2"]).decode("utf-8")
            if review["image_3"]:
                review["image_3"] = base64.b64encode(review["image_3"]).decode("utf-8")

        return {
            "canteen_id": canteen["canteen_id"],
            "canteen_name": canteen["name"],
            "overall_rating": canteen["overall_rating"],
            "overall_food": canteen["overall_food"],
            "overall_hygiene": canteen["overall_hygiene"],
            "overall_staff": canteen["overall_staff"],
            "overall_facilities": canteen["overall_facilities"],
            "top_reviews": reviews
        }

    except Exception as e:
        logging.error(f"Error fetching reviews and ratings for canteen_id {canteen_id}: {str(e)}")
        return None
    
def get_menu_by_canteen_id(canteen_id):
    """
    Fetch the menu row for a given canteen_id.
    Returns a dict with all menu columns (Monday, monday_price, ...), or None if not found/error.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                menu_id,
                canteen_id,
                day_wise,
                Monday, monday_price,
                Tuesday, tuesday_price,
                Wednesday, wednesday_price,
                Thursday, thursday_price,
                Friday, friday_price,
                Saturday, saturday_price,
                Sunday, sunday_price,
                menu_fil_1,
                menu_file_2,
                created_at,
                updated_at
            FROM menu
            WHERE canteen_id = %s
            LIMIT 1
        """
        cursor.execute(query, (canteen_id,))
        row = cursor.fetchone()
        return row if row else None
    except Exception as e:
        logging.exception(f"DB error in get_menu_by_canteen_id for canteen_id {canteen_id}: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass

def get_user_by_id_db(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id, name, phone_number, role, email FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return {
                "user_id": user[0],
                "name": user[1],
                "phone_number": user[2],
                
                "role": user[3],
                "email": user[4]
            }
        return None

    except Exception as e:
        logging.error(f"Error fetching user: {str(e)}")
        return None
    
def get_all_canteens_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  

        query = """
            SELECT 
                canteen_id,
                name,
                location,
                days_open,
                opening_time,
                closing_time,
                overall_rating
            FROM canteens
        """
        cursor.execute(query)
        canteens = cursor.fetchall()

        cursor.close()
        conn.close()

        return canteens

    except Exception as e:
        logging.error(f"Error fetching canteens from DB: {str(e)}")
        return None



    
def get_reviews_by_id_db(user_id):

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                c.name AS canteen_name,
                r.overall_rating,
                r.review_text
            FROM reviews r
            JOIN canteens c ON r.canteen_id = c.canteen_id
            WHERE r.user_id = %s
            ORDER BY r.overall_rating DESC, r.created_at DESC
            LIMIT %s
        """
        cursor.execute(query, (user_id, limit))
        rows = cursor.fetchall()
        return rows or []

    except Exception as e:
        logging.exception(f"DB error in get_top_reviews_by_user for user_id {user_id}: {e}")
        return None

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def submit_user_feedback_db(user_id, feedback_text):
    try:

        if not feedback_text:
            return jsonify({"message": "feedback_text is required"}), 400
        
        row = get_feedback_by_user(user_id)

        # row is expected as a dict or tuple depending on your models implementation.
        # We'll assume models returns a dict or None.
        if row is None:
            # insert new row with feedback_text_1
            created = insert_feedback_for_user(user_id, feedback_text)
            if created:
                return jsonify({"message": "Feedback submitted successfully", "slot": "feedback_text_1"}), 201
            else:
                logging.error(f"Failed to insert feedback for user_id {user_id}")
                return jsonify({"message": "Internal Server Error"}), 500

        # if row exists, check which slots are empty
        # Expected row keys: feedback_text_1, feedback_text_2
        f1 = (row.get("feedback_text_1") or "").strip()
        f2 = (row.get("feedback_text_2") or "").strip()

        if f1 and f2:
            # both filled -> limit exhausted
            return jsonify({"message": "Max feedback limits exhausted for this account"}), 400

        # choose which slot to fill (prefer feedback_text_1 if empty)
        slot_to_update = "feedback_text_1" if not f1 else "feedback_text_2"

        updated = update_feedback_slot_for_user(user_id, slot_to_update, feedback_text)
        if updated:
            return jsonify({"message": "Feedback submitted successfully", "slot": slot_to_update}), 200
        else:
            logging.error(f"Failed to update feedback for user_id {user_id} slot {slot_to_update}")
            return jsonify({"message": "Internal Server Error"}), 500

    except Exception as e:
        logging.exception(f"Error in submit_user_feedback for user_id {user_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

def get_feedback_by_user(user_id):
    """
    Return a dict with keys: feedback_id, user_id, feedback_text_1, feedback_text_2, created_at
    Returns None if no row exists or on error.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT feedback_id, user_id, feedback_text_1, feedback_text_2, created_at
            FROM app_feedback
            WHERE user_id = %s
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None

        # adapt to tuple row structure
        # assuming order: feedback_id, user_id, feedback_text_1, feedback_text_2, created_at
        return {
            "feedback_id": row[0],
            "user_id": row[1],
            "feedback_text_1": row[2],
            "feedback_text_2": row[3],
            "created_at": row[4]
        }
    except Exception as e:
        logging.exception(f"DB error in get_feedback_by_user for user_id {user_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def insert_feedback_for_user(user_id, feedback_text):
    """
    Insert a new row for the user with feedback_text in feedback_text_1 and created_at now.
    Returns True on success, False on failure.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO app_feedback (user_id, feedback_text_1, feedback_text_2)
            VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (user_id, feedback_text, None))
        conn.commit()
        return True
    except Exception as e:
        logging.exception(f"DB error in insert_feedback_for_user for user_id {user_id}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return False
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def update_feedback_slot_for_user(user_id, slot_name: str, feedback_text: str):
    """
    Update either feedback_text_1 or feedback_text_2 for the given user and set created_at to now.
    slot_name must be either 'feedback_text_1' or 'feedback_text_2'.
    Returns True on success, False on failure.
    """
    if slot_name not in ("feedback_text_1", "feedback_text_2"):
        logging.error(f"Invalid slot_name passed to update_feedback_slot_for_user: {slot_name}")
        return False

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Build query dynamically but safe param binding for values
        
        query = f"""
            UPDATE app_feedback
            SET {slot_name} = %s
            WHERE user_id = %s
        """
        cursor.execute(query, (feedback_text, user_id))
        if cursor.rowcount == 0:
            # No row updated (maybe row deleted concurrently)
            return False
        conn.commit()
        return True
    except Exception as e:
        logging.exception(f"DB error in update_feedback_slot_for_user for user_id {user_id}, slot {slot_name}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return False
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def get_user_role_by_id_db(user_id):
    """
    Returns a dict { "user_id": ..., "role": ... } for the given user_id.
    Returns None if user not found or on error.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id, role FROM users WHERE user_id = %s LIMIT 1"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        # row format depends on DB driver; adapt if needed
        return {"user_id": row[0], "role": row[1]}
    except Exception as e:
        logging.exception(f"DB error in get_user_role_by_id for user_id {user_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def insert_issue_for_user_db(user_id, role, issue_text):
    """
    Insert a new issue into app_issue (created_at default to NOW()).
    Returns {"issue_id": <id>} on success, None on failure.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Corrected SQL: three columns -> three placeholders
        query_mysql = """
            INSERT INTO app_issue (user_id, role, issue_text)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_mysql, (user_id, role, issue_text))

        try:
            issue_id = cursor.lastrowid
        except Exception:
            issue_id = None

        conn.commit()
        return {"issue_id": issue_id}

    except Exception as e:
        logging.exception(f"DB error in insert_issue_for_user for user_id {user_id}: {e}")
        if conn:
            try: conn.rollback()
            except Exception: pass
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception: pass
        try:
            if conn: conn.close()
        except Exception: pass
def get_canteen_by_id(canteen_id):
    """
    Return one canteen row dict (minimal check) or None if not found/error.
    Uses dictionary cursor if supported by driver.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        # dictionary=True style cursor (adjust if your driver uses different arg)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT canteen_id FROM canteens WHERE canteen_id = %s LIMIT 1"
        cursor.execute(query, (canteen_id,))
        row = cursor.fetchone()
        return row if row else None
    except Exception as e:
        logging.exception(f"DB error in get_canteen_by_id for {canteen_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def get_canteen_by_owner_db(user_id):
    """
    Fetch the canteen row owned by the given user_id.
    Returns a dict with canteen details or None if not found / on error.

    Expected canteens table to have owner_user_id column referencing users.user_id.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                canteen_id,
                name,
                location,
                description,
                contact_no,
                days_open,
                opening_time,
                closing_time,
                peak_hr_start_time,
                peak_hr_end_time,
                overall_rating
            FROM canteens
            WHERE owner_id = %s
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        canteen = cursor.fetchone()
        # If no row, return None (handled by caller as not found)
        return canteen
    except Exception as e:
        logging.exception(f"DB error in get_canteen_by_owner for user_id {user_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def get_canteen_id_by_owner(user_id):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT canteen_id FROM canteens WHERE owner_id = %s LIMIT 1"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        # If your driver returns tuple, take first element; if dict, adapt accordingly
        return row[0] if isinstance(row, (list, tuple)) else row.get("canteen_id")
    except Exception as e:
        logging.exception(f"DB error in get_canteen_id_by_owner for user {user_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def get_menu_id_by_canteen(canteen_id):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT menu_id FROM menu WHERE canteen_id = %s LIMIT 1"
        cursor.execute(query, (canteen_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return row[0] if isinstance(row, (list, tuple)) else row.get("menu_id")
    except Exception as e:
        logging.exception(f"DB error in get_menu_id_by_canteen for canteen {canteen_id}: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def insert_food_item_for_menu(menu_id, name, description, price, status=None):
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        now = datetime.utcnow()

        # Try PostgreSQL-style RETURNING first (some drivers support it), else fallback to lastrowid
        try:
            insert_query_pg = """
                INSERT INTO food_items (menu_id, name, price, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING food_id
            """
            cursor.execute(insert_query_pg, (menu_id, name, price, status, now, now))
            row = cursor.fetchone()
            if row:
                food_id = row[0]
            else:
                food_id = None
        except Exception:
            # fallback path (MySQL, sqlite)
            try:
                conn.rollback()
            except Exception:
                pass
            insert_query = """
                INSERT INTO food_items (menu_id, name, price, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (menu_id, name, price, status, now, now))
            try:
                food_id = cursor.lastrowid
            except Exception:
                food_id = None

        conn.commit()
        return {"food_id": food_id}

    except Exception as e:
        logging.exception(f"DB error in insert_food_item_for_menu for menu {menu_id}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def insert_issue_for_canteen_owner(raised_by, role, canteen_id, description, status="open"):
    
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        now = datetime.utcnow()

        # Try PostgreSQL RETURNING first, fallback to lastrowid
        try:
            insert_query_pg = """
                INSERT INTO issues (raised_by, role, canteen_id, description, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING issue_id
            """
            cursor.execute(insert_query_pg, (raised_by, role, canteen_id, description, status, now))
            row = cursor.fetchone()
            if row:
                issue_id = row[0]
            else:
                issue_id = None
        except Exception:
            # fallback (MySQL, sqlite)
            try:
                conn.rollback()
            except Exception:
                pass
            insert_query = """
                INSERT INTO issues (raised_by, role, canteen_id, description, status, created_at, resolved_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (raised_by, role, canteen_id, description, status, now, None))
            try:
                issue_id = cursor.lastrowid
            except Exception:
                issue_id = None

        conn.commit()
        return {"issue_id": issue_id}

    except Exception as e:
        logging.exception(f"DB error in insert_issue_for_canteen_owner for canteen {canteen_id}: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def get_reviews_for_canteen(canteen_id):
    
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Fetch canteen summary (select only the fields you need)
        canteen_query = """
            SELECT
                
                overall_rating,
                overall_food,
                overall_hygiene,
                overall_staff,
                overall_facilities
            FROM canteens
            WHERE canteen_id = %s
            LIMIT 1
        """
        cursor.execute(canteen_query, (canteen_id,))
        canteen_row = cursor.fetchone()
        if not canteen_row:
            # Canteen not found — return clear structure (caller can treat as 404)
            return {"canteen": None, "reviews": []}

        # 2) Fetch reviews for this canteen
        reviews_query = """
            SELECT
                review_id,
                canteen_id,
                user_id,
                overall_rating,
                review_text,
                created_at
            FROM canteen_reviews
            WHERE canteen_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(reviews_query, (canteen_id,))
        reviews = cursor.fetchall() or []

        # 3) Return combined structure
        return {
            "canteen": canteen_row,
            "reviews": reviews
        }

    except Exception as e:
        logging.exception(f"DB error in get_reviews_for_canteen for canteen {canteen_id}: {e}")
        return None

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def _parse_list_column(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    s = str(value).strip()
    if not s:
        return []
    # try parse JSON
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return parsed
        return [parsed]
    except Exception:
        # fallback split by comma
        parts = [p.strip() for p in s.split(",") if p.strip() != ""]
        return parts

def get_menu_by_canteen_id(canteen_id):
    """
    Return dict for one menu row (dictionary cursor).
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT menu_id, canteen_id, day_wise,
                   Monday, monday_price, Tuesday, tuesday_price,
                   Wednesday, wednesday_price, Thursday, thursday_price,
                   Friday, friday_price, Saturday, saturday_price,
                   Sunday, sunday_price, menu_file_1, menu_file_2, created_at, updated_at
            FROM menu
            WHERE canteen_id = %s
            LIMIT 1
        """
        cursor.execute(query, (canteen_id,))
        row = cursor.fetchone()
        return row if row else None
    except Exception as e:
        logging.exception(f"DB error in get_menu_by_canteen_id for canteen {canteen_id}: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass


def get_all_food_items_by_menu_id(menu_id):
    """
    Fetch ALL food items for a given menu_id.
    Returns list of dicts: {food_id, name, price}
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT food_id, name, price
            FROM food_items
            WHERE menu_id = %s
            ORDER BY food_id
        """
        cursor.execute(query, (menu_id,))
        rows = cursor.fetchall() or []
        return rows
    except Exception as e:
        logging.exception(f"DB error in get_all_food_items_by_menu_id for menu {menu_id}: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass


def get_food_items_by_ids(menu_id, food_id_list):
    """
    Fetch food items matching menu_id and given food_ids.
    Returns list of dicts: {food_id, name, price}
    """
    if not food_id_list:
        return []
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Build parameter placeholders safely
        placeholders = ",".join(["%s"] * len(food_id_list))
        query = f"""
            SELECT food_id, name, price
            FROM food_items
            WHERE menu_id = %s AND food_id IN ({placeholders})
        """
        params = [menu_id] + food_id_list
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall() or []
        return rows
    except Exception as e:
        logging.exception(f"DB error in get_food_items_by_ids for menu {menu_id}: {e}")
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass


def update_menu_day_columns(menu_id, day_col, price_col, append_item_names, append_item_prices):
    """
    Atomically fetch current day lists, append provided items/prices, and update the row.
    - day_col: e.g. "Monday"
    - price_col: e.g. "monday_price"
    - append_item_names: list[str]
    - append_item_prices: list[float|None]
    Returns:
      {"updated_items": [...], "updated_prices": [...]} on success
      None on error
    """
    conn = None
    cursor = None
    try:
        if not append_item_names:
            return {"updated_items": [], "updated_prices": []}

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch current values FOR UPDATE to avoid race condition (driver+DB must support it)
        # We'll try a SELECT ... FOR UPDATE; if fails, fall back to simple SELECT
        try:
            sel_q = f"SELECT {day_col}, {price_col} FROM menu WHERE menu_id = %s FOR UPDATE"
            cursor.execute(sel_q, (menu_id,))
            row = cursor.fetchone()
            # row may be tuple or dict depending on cursor type
            if row is None:
                return None
            if isinstance(row, dict):
                cur_items_raw = row.get(day_col)
                cur_prices_raw = row.get(price_col)
            else:
                # when cursor returns tuple, order is as selected
                cur_items_raw = row[0]
                cur_prices_raw = row[1]
        except Exception:
            # fallback select
            cursor.execute(f"SELECT {day_col}, {price_col} FROM menu WHERE menu_id = %s", (menu_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            if isinstance(row, dict):
                cur_items_raw = row.get(day_col)
                cur_prices_raw = row.get(price_col)
            else:
                cur_items_raw = row[0]
                cur_prices_raw = row[1]

        # Parse current lists
        cur_items = _parse_list_column(cur_items_raw)
        cur_prices = _parse_list_column(cur_prices_raw)

        # Convert existing price strings to floats where possible
        def _to_float_list(lst):
            new = []
            for x in lst:
                if x is None or x == "":
                    new.append(None)
                    continue
                try:
                    new.append(float(x))
                except Exception:
                    # strip non-numeric
                    s = ''.join(ch for ch in str(x) if (ch.isdigit() or ch in ".-"))
                    try:
                        new.append(float(s) if s else None)
                    except Exception:
                        new.append(None)
            return new

        cur_prices = _to_float_list(cur_prices)

        # Append new ones (keeping indices aligned)
        for nm, pr in zip(append_item_names, append_item_prices):
            cur_items.append(nm)
            cur_prices.append(pr)

        # Serialize to JSON string for storage
        items_to_store = json.dumps(cur_items, ensure_ascii=False)
        prices_to_store = json.dumps(cur_prices)

        # Update row
        update_q = f"""
            UPDATE menu
            SET {day_col} = %s,
                {price_col} = %s,
                updated_at = %s
            WHERE menu_id = %s
        """
        now = datetime.utcnow()
        cursor.execute(update_q, (items_to_store, prices_to_store, now, menu_id))
        conn.commit()

        return {"updated_items": cur_items, "updated_prices": cur_prices}

    except Exception as e:
        logging.exception(f"DB error in update_menu_day_columns for menu {menu_id}: {e}")
        try:
            if conn:
                conn.rollback()
        except Exception:
            pass
        return None
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass


def update_user_info_db(user_id, update_fields):
   
    if not update_fields:
        return False

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        set_clauses = []
        values = []
        for col, val in update_fields.items():
            set_clauses.append(f"{col} = %s")
            values.append(val)

        set_clause = ", ".join(set_clauses)
        values.append(datetime.utcnow())
        values.append(user_id)

        query = f"""
            UPDATE users
            SET {set_clause}, updated_at = %s
            WHERE user_id = %s
        """
        cursor.execute(query, tuple(values))
        conn.commit()
        return True
    except Exception as e:
        logging.exception(f"DB error in update_user_info_db: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_canteen_profile_db(canteen_id, update_fields: dict):
   
    if not update_fields:
        return False

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        set_clauses = []
        params = []
        for col, val in update_fields.items():
            # ensure columns are safe (caller already whitelisted, but double-check)
            set_clauses.append(f"{col} = %s")
            params.append(val)

        # add updated_at
        set_clause = ", ".join(set_clauses)
        #params.append(datetime.utcnow())
        params.append(canteen_id)

        query = f"""
            UPDATE canteens
            SET {set_clause}
            WHERE canteen_id = %s
        """
        # removed  updated_at = %s from queryy


        # Log what we're updating 
        logging.info(f"Updating canteen {canteen_id} with fields: {list(update_fields.keys())}")

        cursor.execute(query, tuple(params))
        conn.commit()
        return True
    except Exception as e:
        logging.exception(f"DB error in update_canteen_profile_db for canteen_id {canteen_id}: {e}")
        try:
            if conn:
                conn.rollback()
        except Exception:
            pass
        return False
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass

def get_menu_row(canteen_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu WHERE canteen_id = %s LIMIT 1", (canteen_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_menu_images(canteen_id, urls):
    """
    urls: list of urls (strings) in the order received from client (can be length 1 or 2).
    Behavior:
      - If a menu row for canteen_id doesn't exist, create one and set menu_file_1/menu_file_2 accordingly.
      - If exists, fill null slot(s) first (menu_file_1 then menu_file_2),
        for remaining urls, overwrite starting from menu_file_1 (or in same order).
    Returns dict of updated columns: {"menu_file_1": url_or_none, "menu_file_2": url_or_none}
    """
    if not urls:
        return {"menu_file_1": None, "menu_file_2": None}

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT menu_id, menu_file_1, menu_file_2 FROM menu WHERE canteen_id = %s LIMIT 1", (canteen_id,))
        row = cursor.fetchone()

        now = datetime.utcnow()

        if not row:
            # Insert new menu row with provided urls put into slots in order
            menu_file_1 = urls[0] if len(urls) >= 1 else None
            menu_file_2 = urls[1] if len(urls) >= 2 else None

            insert_query = """
                INSERT INTO menu (
                    canteen_id, day_wise, Monday, monday_price, Tuesday, tuesday_price,
                    Wednesday, wednesday_price, Thursday, thursday_price,
                    Friday, friday_price, Saturday, saturday_price, Sunday, sunday_price,
                    menu_file_1, menu_file_2, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            # minimal default values (NULLs for day entries); day_wise default to "No"
            values = (
                canteen_id, "No",
                None, None, None, None,
                None, None, None, None,
                None, None, None, None,
                None, None,
                menu_file_1, menu_file_2,
                now, now
            )
            cursor.execute(insert_query, values)
            conn.commit()
            return {"menu_file_1": menu_file_1, "menu_file_2": menu_file_2}

        # Row exists: apply fill-null-then-overwrite logic
        current_1 = row.get("menu_file_1")
        current_2 = row.get("menu_file_2")

        # Build list representing slots in order: first fill nulls (left-to-right)
        slots = [current_1, current_2]
        updated_slots = list(slots)  # copy

        urls_iter = iter(urls)
        # First pass: fill null or empty slots
        for i in range(len(slots)):
            if (updated_slots[i] is None or updated_slots[i] == ""):
                try:
                    val = next(urls_iter)
                    updated_slots[i] = val
                except StopIteration:
                    break

        # Second pass: if still urls left, overwrite from slot 0 onwards
        for i in range(len(slots)):
            try:
                val = next(urls_iter)
                updated_slots[i] = val
            except StopIteration:
                break

        # If nothing changed, still we may want to overwrite? but logic above handles it.
        # Build update query for whichever slots changed/unconditionally update both for simplicity.
        update_query = "UPDATE menu SET menu_file_1 = %s, menu_file_2 = %s, updated_at = %s WHERE canteen_id = %s"
        params = (updated_slots[0], updated_slots[1], now, canteen_id)
        cursor.execute(update_query, params)
        conn.commit()

        return {"menu_file_1": updated_slots[0], "menu_file_2": updated_slots[1]}

    except Exception as e:
        logging.exception("Error updating menu images: %s", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------- CANTEEN IMAGE UPDATES ----------
def get_canteen_row(canteen_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT canteen_id, canteen_image_1, canteen_image_2 FROM canteens WHERE canteen_id = %s LIMIT 1", (canteen_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_canteen_images(canteen_id, urls):
    """
    urls: list of urls (strings).
    Fill null slot(s) first, else overwrite.
    Returns dict {"canteen_image_1": val1, "canteen_image_2": val2}
    """
    if not urls:
        return {"canteen_image_1": None, "canteen_image_2": None}

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT canteen_image_1, canteen_image_2 FROM canteens WHERE canteen_id = %s LIMIT 1", (canteen_id,))
        row = cursor.fetchone()

        if not row:
            raise ValueError(f"Canteen with id {canteen_id} not found")

        current_1 = row.get("canteen_image_1")
        current_2 = row.get("canteen_image_2")

        slots = [current_1, current_2]
        updated_slots = list(slots)

        urls_iter = iter(urls)
        # Fill nulls first
        for i in range(len(slots)):
            if (updated_slots[i] is None or updated_slots[i] == ""):
                try:
                    val = next(urls_iter)
                    updated_slots[i] = val
                except StopIteration:
                    break

        # Overwrite remaining slots if urls left
        for i in range(len(slots)):
            try:
                val = next(urls_iter)
                updated_slots[i] = val
            except StopIteration:
                break

        update_query = "UPDATE canteens SET canteen_image_1 = %s, canteen_image_2 = %s WHERE canteen_id = %s"
        cursor.execute(update_query, (updated_slots[0], updated_slots[1], canteen_id))
        conn.commit()

        return {"canteen_image_1": updated_slots[0], "canteen_image_2": updated_slots[1]}

    except Exception as e:
        logging.exception("Error updating canteen images: %s", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()