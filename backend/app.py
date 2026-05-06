"""
FitLife Tracker Backend - Flask REST API
SQLite Database (no setup required!)
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

try:
    from .db import get_connection, execute_query, execute_single, init_database
except ImportError:
    from db import get_connection, execute_query, execute_single, init_database

print("APP.PY LOADED")
print("APP FILE IS RUNNING")

def generate_plan(goal, diet_type):
    if goal == "lose":
        diet = ["Oats", "Salad", "Grilled Chicken"]
        workout = ["Running", "Cycling", "HIIT"]
    elif goal == "gain":
        diet = ["Rice", "Eggs", "Milk"]
        workout = ["Weight Training", "Push-ups"]
    else:
        diet = ["Balanced Meal"]
        workout = ["Walking"]

    return diet, workout

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app, supports_credentials=True)

# Get the directory where this app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'fitlife.db')

# Initialize database on startup
init_database()

# ==================== FRONTEND ROUTES ====================

@app.route('/')
def serve_frontend():
    """Serve the main HTML frontend"""
    return render_template('fit.html')

# Flask automatically serves /static/ files

# ==================== USER PROFILE API ====================

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print("Received data:", data)

        if not data:
            return jsonify({'error': 'No data received'}), 400

        required_fields = ['name', 'age', 'height', 'weight', 'goal', 'diet_type', 'period']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        query = """
        INSERT INTO users (name, age, height, weight, goal, diet_type, health_conditions, allergies, period)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            data['name'],
            int(data['age']),
            int(data['height']),
            float(data['weight']),
            data['goal'],
            data['diet_type'],
            data.get('health_conditions', 'none'),
            data.get('allergies', 'none'),
            data['period']
        )

        diet, workout = generate_plan(data['goal'], data['diet_type'])

        try:
            result = execute_query(query, params)
            if result is None:
                return jsonify({'error': 'Database error creating user.'}), 500
            return jsonify({
                'isOk': True,
                'message': 'Profile created successfully!',
                'diet_plan': diet,
                'workout_plan': workout
            })
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
            if 'UNIQUE constraint failed: users.name' in str(e):
                return jsonify({'isOk': False, 'error': 'Profile with this name already exists. Please use a different name or update the existing profile.'}), 409
            raise

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/<name>', methods=['GET'])
def get_profile(name):
    """Get user profile by name"""
    query = "SELECT * FROM users WHERE name = ?"
    user = execute_single(query, (name,))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_dict = dict(user)
    return jsonify(user_dict)

@app.route('/api/profile/<name>', methods=['PUT'])
def update_profile(name):
    """Update user profile"""
    data = request.get_json()
    
    query = """
    UPDATE users SET 
        age = ?, height = ?, weight = ?, goal = ?, diet_type = ?,
        health_conditions = ?, allergies = ?, period = ?, badge_count = ?
    WHERE name = ?
    """
    params = (
        int(data.get('age', 0)),
        int(data.get('height', 0)),
        float(data.get('weight', 0)),
        data.get('goal', 'lose'),
        data.get('diet_type', 'both'),
        data.get('health_conditions', 'none'),
        data.get('allergies', 'none'),
        data.get('period', 'month'),
        int(data.get('badge_count', 0)),
        name
    )
    
    result = execute_query(query, params)
    if result is None:
        return jsonify({'error': 'Failed to update profile'}), 500
    
    return jsonify({'isOk': True, 'message': 'Profile updated successfully!'})

# ==================== WEIGHT LOGS API ====================

@app.route('/api/weight-log', methods=['POST'])
def create_weight_log():
    """Log a new weight entry"""
    data = request.get_json()
    
    if 'name' not in data or 'weight' not in data:
        return jsonify({'error': 'Missing required fields: name, weight'}), 400
    
    user = execute_single("SELECT id FROM users WHERE name = ?", (data['name'],))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    query = "INSERT INTO weight_logs (user_id, weight) VALUES (?, ?)"
    result = execute_query(query, (user['id'], float(data['weight'])))
    
    if result is None:
        return jsonify({'error': 'Failed to log weight'}), 500
    
    return jsonify({'isOk': True, 'message': 'Weight logged successfully!'})

@app.route('/api/weight-logs/<name>', methods=['GET'])
def get_weight_logs(name):
    """Get all weight logs for a user"""
    user = execute_single("SELECT id FROM users WHERE name = ?", (name,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    query = "SELECT * FROM weight_logs WHERE user_id = ? ORDER BY created_at ASC"
    logs = execute_query(query, (user['id'],), fetch=True)
    
    if logs is None:
        return jsonify([])
    
    logs_list = [dict(log) for log in logs]
    return jsonify(logs_list)

@app.route('/api/weight-log/<int:log_id>', methods=['DELETE'])
def delete_weight_log(log_id):
    """Delete a weight log"""
    query = "DELETE FROM weight_logs WHERE id = ?"
    result = execute_query(query, (log_id,))
    
    if result is None:
        return jsonify({'error': 'Failed to delete weight log'}), 500
    
    return jsonify({'isOk': True, 'message': 'Weight log deleted successfully!'})

# ==================== BADGES API ====================

@app.route('/api/badges/<name>', methods=['GET'])
def get_badges(name):
    """Get all badges for a user"""
    user = execute_single("SELECT id FROM users WHERE name = ?", (name,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    query = "SELECT * FROM badges WHERE user_id = ? ORDER BY earned_at DESC"
    badges = execute_query(query, (user['id'],), fetch=True)
    
    if badges is None:
        return jsonify([])
    
    badges_list = [dict(badge) for badge in badges]
    return jsonify(badges_list)

@app.route('/api/badge', methods=['POST'])
def add_badge():
    """Add a badge to user"""
    data = request.get_json()
    
    if 'name' not in data or 'badge_name' not in data:
        return jsonify({'error': 'Missing required fields: name, badge_name'}), 400
    
    user = execute_single("SELECT id FROM users WHERE name = ?", (data['name'],))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    query = "INSERT INTO badges (user_id, badge_name) VALUES (?, ?)"
    result = execute_query(query, (user['id'], data['badge_name']))
    
    if result is None:
        return jsonify({'error': 'Failed to add badge'}), 500
    
    execute_query("UPDATE users SET badge_count = badge_count + 1 WHERE id = ?", (user['id'],))
    
    return jsonify({'isOk': True, 'message': 'Badge earned!'})

# ==================== DATA API (Combined) ====================

@app.route('/api/data/<name>', methods=['GET'])
def get_all_data(name):
    """Get all data for a user (profile + weight logs)"""
    user = execute_single("SELECT * FROM users WHERE name = ?", (name,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    logs = execute_query(
        "SELECT * FROM weight_logs WHERE user_id = ? ORDER BY created_at ASC",
        (user['id'],), fetch=True
    )
    
    badges = execute_query(
        "SELECT * FROM badges WHERE user_id = ? ORDER BY earned_at DESC",
        (user['id'],), fetch=True
    )
    
    return jsonify({
        'profile': dict(user),
        'weight_logs': [dict(log) for log in (logs or [])],
        'badges': [dict(badge) for badge in (badges or [])]
    })

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn = get_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500

@app.route('/test')
def test():
    return "WORKING"

@app.route('/api/debug/tables')
def check_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return jsonify([t[0] for t in tables])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# --- Advanced Plan API ---
@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json
    conditions = data.get("conditions","").lower()
    allergies = data.get("allergies","").lower()

    diet = "Balanced diet"
    exercise = "Regular exercise"

    if "diabetes" in conditions:
        diet = "Low sugar, high fiber"
        exercise = "Walking + cardio"
    elif "bp" in conditions:
        diet = "Low sodium"
        exercise = "Yoga"

    if "nuts" in allergies:
        diet += " (no nuts)"

    return jsonify({"diet": diet, "exercise": exercise})
