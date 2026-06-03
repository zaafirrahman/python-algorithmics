from flask import Flask, request, jsonify
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC   = os.path.join(BASE_DIR, 'static')
DB       = os.path.join(BASE_DIR, 'dart_game.db')

app = Flask(__name__, static_folder=STATIC, static_url_path='')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS players (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scores (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER REFERENCES players(id),
                score     INTEGER NOT NULL,
                misses    INTEGER NOT NULL,
                duration  INTEGER NOT NULL,
                played_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

# ── Serve frontend ──────────────────────────────────────────────
@app.route('/')
def index():
    return app.send_static_file('index.html')

# ── Players ─────────────────────────────────────────────────────
@app.route('/api/players', methods=['GET'])
def list_players():
    with get_db() as conn:
        rows = conn.execute('SELECT id, name FROM players ORDER BY name').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/players', methods=['POST'])
def create_player():
    name = (request.json or {}).get('name', '').strip()
    if not name:
        return jsonify({'error': 'Nama tidak boleh kosong'}), 400
    try:
        with get_db() as conn:
            cur = conn.execute('INSERT INTO players (name) VALUES (?)', (name,))
            player_id = cur.lastrowid
        return jsonify({'id': player_id, 'name': name}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Nama sudah dipakai'}), 409

@app.route('/api/players/<name>', methods=['GET'])
def find_player(name):
    with get_db() as conn:
        row = conn.execute('SELECT id, name FROM players WHERE name = ?', (name,)).fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Tidak ditemukan'}), 404

# ── Scores ──────────────────────────────────────────────────────
@app.route('/api/scores', methods=['POST'])
def save_score():
    d = request.json or {}
    with get_db() as conn:
        conn.execute(
            'INSERT INTO scores (player_id, score, misses, duration) VALUES (?,?,?,?)',
            (d['player_id'], d['score'], d['misses'], d['duration'])
        )
    return jsonify({'ok': True}), 201

# ── Leaderboard ─────────────────────────────────────────────────
@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    with get_db() as conn:
        rows = conn.execute('''
            SELECT p.name,
                   MAX(s.score)  AS best_score,
                   COUNT(s.id)   AS games_played,
                   MIN(s.misses) AS best_misses
            FROM players p
            JOIN scores s ON p.id = s.player_id
            GROUP BY p.name
            ORDER BY best_score DESC
            LIMIT 20
        ''').fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    init_db()
    print('\n🎯  Dart Game berjalan di  http://localhost:5000\n')
    app.run(debug=True, port=5000)