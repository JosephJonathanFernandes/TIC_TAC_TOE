# API Documentation

## Overview

This document describes the RESTful API endpoints available in the Tic Tac Toe application.

## Base URL

```
http://127.0.0.1:5000
```

## Endpoints

### 1. Get Game Page

**Endpoint:** `GET /`

**Description:** Renders the main game page with initialized game state.

**Response:** HTML page

**Session Data Initialized:**
- `board`: Empty 9-cell array
- `current_player`: 'X'
- `game_over`: false
- `game_mode`: 'vs_computer'
- `difficulty`: 'hard'
- `stats`: Statistics object

---

### 2. Set Game Options

**Endpoint:** `POST /set_options`

**Description:** Configure game mode and difficulty settings.

**Request Body:**
```json
{
    "game_mode": "vs_computer",  // or "two_player"
    "difficulty": "hard"         // "easy", "medium", or "hard"
}
```

**Response:**
```json
{
    "success": true,
    "game_mode": "vs_computer",
    "difficulty": "hard"
}
```

**Status Codes:**
- `200 OK`: Options set successfully
- `400 Bad Request`: Invalid game mode or difficulty

---

### 3. Make Move

**Endpoint:** `POST /make_move`

**Description:** Submit a player move and get game state update.

**Request Body:**
```json
{
    "position": 4  // Cell index (0-8)
}
```

**Response (Game in Progress):**
```json
{
    "board": ["X", "", "", "", "O", "", "", "", ""],
    "winner": null,
    "game_over": false,
    "winning_line": null,
    "computer_position": 4,
    "current_player": "X"
}
```

**Response (Game Over):**
```json
{
    "board": ["X", "X", "X", "O", "O", "", "", "", ""],
    "winner": "X",
    "game_over": true,
    "winning_line": [0, 1, 2],
    "computer_position": null,
    "stats": {
        "player_wins": 1,
        "computer_wins": 0,
        "ties": 0,
        "total_games": 1
    }
}
```

**Status Codes:**
- `200 OK`: Move processed successfully
- `400 Bad Request`: Invalid position or position already taken

**Error Response:**
```json
{
    "error": "Position already taken"
}
```

---

### 4. Reset Game

**Endpoint:** `POST /reset_game`

**Description:** Reset the current game board while preserving statistics.

**Response:**
```json
{
    "success": true,
    "board": ["", "", "", "", "", "", "", "", ""]
}
```

**Status Codes:**
- `200 OK`: Game reset successfully

---

### 5. Reset Statistics

**Endpoint:** `POST /reset_stats`

**Description:** Clear all game statistics.

**Response:**
```json
{
    "success": true,
    "stats": {
        "player_wins": 0,
        "computer_wins": 0,
        "ties": 0,
        "total_games": 0
    }
}
```

**Status Codes:**
- `200 OK`: Statistics reset successfully

---

### 6. Get Statistics

**Endpoint:** `GET /get_stats`

**Description:** Retrieve current game statistics.

**Response:**
```json
{
    "stats": {
        "player_wins": 5,
        "computer_wins": 3,
        "ties": 2,
        "total_games": 10
    }
}
```

**Status Codes:**
- `200 OK`: Statistics retrieved successfully

---

## Data Models

### Board Array

The game board is represented as a 9-element array (indices 0-8):

```
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
```

Each element can be:
- `""` (empty)
- `"X"` (player X)
- `"O"` (player O)

### Winner Values

- `"X"`: Player X wins
- `"O"`: Player O wins
- `"tie"`: Draw/tie game
- `null`: Game in progress

### Winning Line

Array of 3 cell indices representing the winning combination:
- Rows: `[0,1,2]`, `[3,4,5]`, `[6,7,8]`
- Columns: `[0,3,6]`, `[1,4,7]`, `[2,5,8]`
- Diagonals: `[0,4,8]`, `[2,4,6]`

---

## Session Management

The application uses Flask sessions to maintain game state:

- **Storage**: Server-side session storage
- **Lifetime**: 24 hours
- **Security**: Encrypted with SECRET_KEY

Session data includes:
- Current board state
- Player turn
- Game over status
- Game mode and difficulty
- Statistics

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error

Error responses include a descriptive message:

```json
{
    "error": "Description of what went wrong"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing:
- Request rate limiting per IP
- Session-based throttling
- CSRF protection

---

## CORS

By default, CORS is not enabled. To enable cross-origin requests, add Flask-CORS:

```python
from flask_cors import CORS
CORS(app)
```

---

## Examples

### cURL Examples

**Make a move:**
```bash
curl -X POST http://127.0.0.1:5000/make_move \
  -H "Content-Type: application/json" \
  -d '{"position": 4}'
```

**Reset game:**
```bash
curl -X POST http://127.0.0.1:5000/reset_game
```

**Get statistics:**
```bash
curl http://127.0.0.1:5000/get_stats
```

### JavaScript Examples

**Make a move:**
```javascript
fetch('/make_move', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({position: 4})
})
.then(response => response.json())
.then(data => console.log(data));
```

**Set options:**
```javascript
fetch('/set_options', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        game_mode: 'vs_computer',
        difficulty: 'hard'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Testing

Use the provided test suite or tools like Postman to test API endpoints.

For automated testing:
```bash
pytest tests/test_api.py
```
