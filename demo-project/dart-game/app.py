import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=os.path.abspath('static'))

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dart_game.db')


def get_db():
    """Get database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database schema."""
    conn = get_db()
    cursor = conn.cursor()

    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            misses INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Serve the static index.html file."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/players', methods=['GET'])
def list_players():
    """List all players."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM players ORDER BY name')
    players = [{'id': row['id'], 'name': row['name']} for row in cursor.fetchall()]
    conn.close()
    return jsonify(players)


@app.route('/api/players', methods=['POST'])
def create_player():
    """Create a new player."""
    data = request.get_json()
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO players (name) VALUES (?)', (name,))
        conn.commit()
        player_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': player_id, 'name': name}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Player name already taken'}), 409


@app.route('/api/players/<name>')
def get_player(name):
    """Find a player by name."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM players WHERE name = ?', (name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({'id': row['id'], 'name': row['name']})
    return jsonify({'error': 'Player not found'}), 404


@app.route('/api/scores', methods=['POST'])
def save_score():
    """Save a score record."""
    data = request.get_json()
    player_id = data.get('player_id')
    score = data.get('score')
    misses = data.get('misses')
    duration = data.get('duration')

    if not all([player_id, score is not None, misses is not None, duration is not None]):
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scores (player_id, score, misses, duration) VALUES (?, ?, ?, ?)
    ''', (player_id, score, misses, duration))
    conn.commit()
    conn.close()

    return jsonify({'success': True}), 201


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 20 players by best score."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.name, MAX(s.score) as best_score, COUNT(s.id) as games_played
        FROM players p
        JOIN scores s ON p.id = s.player_id
        GROUP BY p.name
        ORDER BY best_score DESC
        LIMIT 20
    ''')
    leaderboard = [{
        'name': row['name'],
        'best_score': row['best_score'],
        'games_played': row['games_played']
    } for row in cursor.fetchall()]
    conn.close()
    return jsonify(leaderboard)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
