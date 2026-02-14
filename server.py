"""HealthOS API — lightweight Flask server for GitHub deployment."""
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__,
    static_folder='.' if os.path.isdir('.') else '.',
    static_url_path=''
)

DATA_DIR = os.environ.get('DATA_DIR', './data')
DATA_FILE = os.path.join(DATA_DIR, 'healthos_data.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def read_data():
    """Read health data from disk."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def write_data(data):
    """Write health data to disk (atomically)."""
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, DATA_FILE)  # atomic on POSIX


# ─── API Routes ──────────────────────────────────────────────

@app.route('/api/data', methods=['GET'])
def get_data():
    """Return all health data."""
    data = read_data()
    return jsonify(data)


@app.route('/api/data', methods=['PUT'])
def put_data():
    """Replace all health data."""
    data = request.get_json(force=True)
    if not isinstance(data, list):
        return jsonify({'error': 'Expected JSON array'}), 400
    write_data(data)
    return jsonify({'ok': True, 'count': len(data), 'synced': datetime.utcnow().isoformat() + 'Z'})


@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok', 'entries': len(read_data())})


# ─── Seed data on first run ─────────────────────────────────

# Use example data for public repository, users can replace with their own data
EXAMPLE_SEED_FILE = os.path.join(os.path.dirname(__file__), 'example_data.json')
USER_SEED_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def seed_if_empty():
    """Copy seed data to data volume on first run."""
    if not os.path.exists(DATA_FILE):
        # Try user data first, then example data
        if os.path.exists(USER_SEED_FILE):
            import shutil
            shutil.copy2(USER_SEED_FILE, DATA_FILE)
            print(f'[HealthOS] Seeded data from user data.json')
        elif os.path.exists(EXAMPLE_SEED_FILE):
            import shutil
            shutil.copy2(EXAMPLE_SEED_FILE, DATA_FILE)
            print(f'[HealthOS] Seeded data from example_data.json (demo data)')
        else:
            print(f'[HealthOS] No seed data found, starting with empty dataset')


# ─── Static files (PWA) ─────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


# ─── Boot ────────────────────────────────────────────────────

if __name__ == '__main__':
    seed_if_empty()
    port = int(os.environ.get('PORT', 5000))
    print(f'[HealthOS] Server starting on port {port}')
    app.run(host='0.0.0.0', port=port, debug=False)
