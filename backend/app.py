"""
Moi AIMER Toi - Python Backend Server
A Flask-based REST API for storing photos, memories, and couple data
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from functools import wraps
import jwt
import time

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'moi_aimer_toi.db')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Simple API key (for local/dev use). Prefer setting BACKEND_API_KEY in environment.
API_KEY = os.environ.get('BACKEND_API_KEY', 'dev-key')

# JWT config (simple local auth)
JWT_SECRET = os.environ.get('BACKEND_JWT_SECRET', 'dev-jwt-secret')
JWT_ALGO = 'HS256'
JWT_EXP_SECONDS = int(os.environ.get('BACKEND_JWT_EXP', 60 * 60 * 12))

def require_auth(func):
    """Allow access if request has valid Bearer JWT or valid API key (backwards compatible)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check Bearer token
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1].strip()
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
                # attach user info if needed
                request.user = payload.get('sub')
                return func(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Invalid token', 'details': str(e)}), 401

        # Fallback to API key in header or query
        key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if key == API_KEY:
            return func(*args, **kwargs)

        return jsonify({'error': 'Unauthorized'}), 401
    return wrapper

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS couple_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_date TEXT NOT NULL,
        home_message TEXT,
        intro_text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        photo_filename TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS perspectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perspective_number INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(perspective_number)
    )''')

    c.execute('SELECT COUNT(*) FROM couple_data')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO couple_data (start_date, home_message, intro_text) VALUES (?, ?, ?)',
                  ('2023-11-10', 'Default home message', 'Default intro text'))

    conn.commit()
    conn.close()

# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'Backend is running!',
        'timestamp': datetime.now().isoformat(),
        'database': 'SQLite'
    })

# ==================== UPLOADS ====================
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_DIR, filename)

# ==================== COUPLE DATA ENDPOINTS ====================
@app.route('/api/couple-data', methods=['GET'])
def get_couple_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM couple_data LIMIT 1')
    row = c.fetchone()
    conn.close()
    return jsonify(dict(row)) if row else jsonify({})

@app.route('/api/couple-data/start-date', methods=['PUT'])
@require_auth
def update_start_date():
    data = request.json
    start_date = data.get('start_date')
    if not start_date:
        return jsonify({'error': 'start_date is required'}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE couple_data SET start_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', (start_date,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Start date updated'})

@app.route('/api/couple-data/home-message', methods=['PUT'])
@require_auth
def update_home_message():
    data = request.json
    home_message = data.get('home_message')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE couple_data SET home_message = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', (home_message,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Home message updated'})

@app.route('/api/couple-data/intro', methods=['PUT'])
@require_auth
def update_intro():
    data = request.json
    intro_text = data.get('intro_text')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE couple_data SET intro_text = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', (intro_text,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Intro text updated'})

# ==================== MEMORIES ENDPOINTS ====================
def memory_row_to_dict(row):
    d = dict(row)
    filename = d.get('photo_filename')
    d['photo_url'] = f"/uploads/{filename}" if filename else None
    return d

@app.route('/api/memories', methods=['GET'])
def get_memories():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM memories ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return jsonify([memory_row_to_dict(r) for r in rows])

@app.route('/api/memories/<int:memory_id>', methods=['GET'])
def get_memory(memory_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(memory_row_to_dict(row))
    return jsonify({'error': 'Memory not found'}), 404

@app.route('/api/memories', methods=['POST'])
@require_auth
def create_memory():
    # Support both JSON and multipart/form-data (for file upload)
    title = None
    description = None
    photo_filename = None

    if request.content_type and 'multipart/form-data' in request.content_type:
        title = request.form.get('title')
        description = request.form.get('description')
        photo = request.files.get('photo')
        if photo:
            photo_filename = f"{int(datetime.now().timestamp())}-{photo.filename}"
            photo.save(os.path.join(UPLOADS_DIR, photo_filename))
    else:
        data = request.json or {}
        title = data.get('title')
        description = data.get('description')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO memories (title, description, photo_filename) VALUES (?, ?, ?)',
              (title, description, photo_filename))
    conn.commit()
    memory_id = c.lastrowid
    conn.close()

    return jsonify({'id': memory_id, 'title': title, 'description': description, 'photo_url': f"/uploads/{photo_filename}" if photo_filename else None, 'created_at': datetime.now().isoformat()}), 201

@app.route('/api/memories/<int:memory_id>', methods=['PUT'])
@require_auth
def update_memory(memory_id):
    # Support multipart (photo upload) or JSON update
    photo_filename = None
    if request.content_type and 'multipart/form-data' in request.content_type:
        title = request.form.get('title')
        description = request.form.get('description')
        photo = request.files.get('photo')
        if photo:
            photo_filename = f"{int(datetime.now().timestamp())}-{photo.filename}"
            photo.save(os.path.join(UPLOADS_DIR, photo_filename))
    else:
        data = request.json or {}
        title = data.get('title')
        description = data.get('description')

    conn = get_db_connection()
    c = conn.cursor()
    if photo_filename:
        c.execute('UPDATE memories SET title = ?, description = ?, photo_filename = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                  (title, description, photo_filename, memory_id))
    else:
        c.execute('UPDATE memories SET title = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                  (title, description, memory_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Memory updated'})

@app.route('/api/memories/<int:memory_id>', methods=['DELETE'])
@require_auth
def delete_memory(memory_id):
    conn = get_db_connection()
    c = conn.cursor()
    # find filename to remove
    c.execute('SELECT photo_filename FROM memories WHERE id = ?', (memory_id,))
    row = c.fetchone()
    if row:
        filename = row['photo_filename']
        if filename:
            filepath = os.path.join(UPLOADS_DIR, filename)
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                # log but continue
                print('Warning: could not remove file', filepath, e)
    # delete DB row
    c.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Memory deleted'})

# ==================== PERSPECTIVES ENDPOINTS ====================
@app.route('/api/perspectives', methods=['GET'])
def get_perspectives():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM perspectives ORDER BY perspective_number')
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ==================== AUTH (simple) ====================
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    ADMIN_USER = os.environ.get('BACKEND_ADMIN_USER', 'admin')
    ADMIN_PASS = os.environ.get('BACKEND_ADMIN_PASS', 'password')
    if username == ADMIN_USER and password == ADMIN_PASS:
        now = int(time.time())
        payload = {'sub': username, 'iat': now, 'exp': now + JWT_EXP_SECONDS}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/perspectives/<int:number>', methods=['GET'])
def get_perspective(number):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM perspectives WHERE perspective_number = ?', (number,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'perspective_number': number, 'content': ''})

@app.route('/api/perspectives', methods=['POST'])
@require_auth
def create_or_update_perspective():
    data = request.json
    perspective_number = data.get('perspective_number')
    content = data.get('content')
    if not perspective_number or not content:
        return jsonify({'error': 'perspective_number and content are required'}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM perspectives WHERE perspective_number = ?', (perspective_number,))
    exists = c.fetchone()
    if exists:
        c.execute('UPDATE perspectives SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE perspective_number = ?', (content, perspective_number))
    else:
        c.execute('INSERT INTO perspectives (perspective_number, content) VALUES (?, ?)', (perspective_number, content))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Perspective saved'})

@app.route('/api/perspectives/<int:number>', methods=['PUT'])
@require_auth
def update_perspective(number):
    data = request.json
    content = data.get('content')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE perspectives SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE perspective_number = ?', (content, number))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Perspective updated'})

if __name__ == '__main__':
    print("🚀 Initializing database...")
    init_db()
    print("✅ Database initialized")
    print("\n🚀 Starting Moi AIMER Toi Backend Server...")
    print("📡 Server running on http://localhost:3001")
    print("\n📋 API Endpoints:")
    print("   GET  /api/health - Check server status")
    print("   GET  /api/couple-data - Get couple data")
    print("   GET  /api/memories - Get all memories")
    print("   POST /api/memories - Create new memory (X-API-KEY required)")
    print("   GET  /api/perspectives - Get all perspectives")
    print("\n")
    app.run(debug=False, port=3001, host='localhost')
