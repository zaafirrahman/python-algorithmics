Build a dart shooter web game with a Python Flask backend and SQLite database.

## Project Structure
dart-game/
├── app.py
├── requirements.txt
└── static/
    └── index.html

---

## Backend — app.py

Flask server with SQLite. Use absolute paths for DB and static folder so it works regardless of working directory.

### API Endpoints
- GET  /                     → serve static/index.html
- GET  /api/players          → list all players [{id, name}]
- POST /api/players          → create player {name}, returns {id, name}; 409 if name taken
- GET  /api/players/<name>   → find player by name
- POST /api/scores           → save {player_id, score, misses, duration}
- GET  /api/leaderboard      → top 20: [{name, best_score, games_played}] ordered by best_score DESC

### Database Schema
players: id (PK autoincrement), name (TEXT UNIQUE)
scores:  id (PK autoincrement), player_id (FK), score (INT), misses (INT), duration (INT), played_at (DATETIME DEFAULT CURRENT_TIMESTAMP)

Leaderboard is a query (not a view) that joins players + scores, groups by name, returns MAX(score) as best_score and COUNT as games_played.

---

## Frontend — static/index.html

Single HTML file. No external JS frameworks. Uses HTML5 Canvas for the game. Google Fonts allowed (Bebas Neue, Share Tech Mono, Rajdhani).

### Screens (show/hide with display flex/none + animation fadeIn)
1. Login Screen  — select existing player OR type new name, call API to login/register
2. Game Screen   — HUD + canvas
3. Leaderboard Screen — result banner + table + play again / change player buttons

### Game Logic

#### State variables
- score, misses, timeLeft = 180, gameActive, elapsed = 0
- elapsed tracks seconds since game start (increments in tick, resets on startGame)
- elapsed is separate from timeLeft — do NOT derive elapsed from MAX_TIME - timeLeft

#### Timer
- MAX_TIME = 180 (3 minutes), countdown via setInterval every 1000ms
- Each tick: timeLeft--, elapsed++
- Timer hits 0 → endGame('win')

#### Target movement
- Circle bouncing off canvas walls
- Speed formula: spd = 1.2 + elapsed * 0.025
  - Second 0   → speed 1.2 (slow)
  - Second 60  → speed 2.7
  - Second 120 → speed 4.2
  - Second 180 → speed 5.7 (fast)
- Apply speed every frame in update(): normalize (dx,dy) vector then multiply by spd
- Initial dx/dy on startGame: random angle, speed 1.2

#### Scoring on click
- Account for canvas scaling: cx = (e.clientX - rect.left) * (canvas.width / rect.width)
- TARGET_RADIUS = 52, ratio = distance / TARGET_RADIUS
  - ratio <= 0.06  → 50 pts (bullseye)
  - ratio <= 0.14  → 40 pts
  - ratio <= 0.26  → 30 pts
  - ratio <= 0.42  → 20 pts
  - ratio <= 0.60  → 15 pts
  - ratio <= 0.78  → 10 pts
  - ratio <= 1.00  → 5 pts
  - ratio >  1.00  → MISS
- MAX_MISSES = 5 → endGame('lose')
- On hit: respawn target at random position, random angle, speed = 1.2 + elapsed * 0.025

#### End game
- Stop game loop (cancelAnimationFrame) and timer (clearInterval)
- POST score to /api/scores
- Fetch /api/leaderboard
- Show leaderboard screen

### HUD (above canvas)
- Timer (MM:SS) — turns red when <= 30s
- Current player name
- Score
- Miss counter (e.g. 2/5)

### Floating text on click
- Hit: "+{pts}" in gold/green floating upward, fades out
- Miss: "MISS!" in red

### Dart target drawing (drawTarget function)
Rings from outside to inside with these colors:
#1a1a2e → #e63946 → #f1faee → #1d3557 → #f1faee → #e63946 → #ffd60a (bullseye)
Add subtle crosshair lines and a glow shadow effect.

### Canvas background
Dark (#070710) with a subtle grid (lines every 40px, rgba(30,30,60,0.6)).

### Leaderboard screen
- Show "TIME UP!" (gold) or "GAME OVER" (red) banner
- Show player name + score + misses for this round
- Highlight current player's row in the table
- Medal emojis for top 3 (🥇🥈🥉)

### Visual style
Dark arcade aesthetic. CSS variables for colors:
--red: #e63946, --gold: #ffd60a, --green: #57cc99, --dim: #8d99ae
--bg: #0a0a0f, --card: #12121a, --border: #1e1e2e, --text: #edf2f4

Cards have a 2px gradient top border (red → gold). Buttons use Bebas Neue font.
Add a scanline overlay on body::before for retro feel.

---

## requirements.txt
flask>=3.0

---

## How to run
python app.py → starts on http://localhost:5000
DB file (dart_game.db) is auto-created on first run in the same directory as app.py.

---

## Important implementation notes
- Canvas click handler must account for canvas scaling: multiply by (canvas.width / rect.width)
- Use requestAnimationFrame for game loop, clearInterval for timer on game end
- All API calls use fetch() with Content-Type: application/json
- Flask static_folder must use os.path.abspath so it works from any working directory
- No external JS libraries, no build tools needed