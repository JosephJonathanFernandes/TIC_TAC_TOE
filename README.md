# 🎮 Tic Tac Toe - Professional Edition

A modern, professional web-based Tic Tac Toe game built with Flask, featuring multiple difficulty levels, two-player mode, and comprehensive statistics tracking.

## ✨ Features

### 🎯 Game Modes
- **vs Computer**: Play against AI opponents with varying difficulty levels
  - **Easy**: Perfect for beginners, makes occasional mistakes
  - **Medium**: Balanced gameplay with strategic moves
  - **Hard**: Unbeatable AI using minimax algorithm with alpha-beta pruning
- **Two Player**: Local multiplayer mode for playing with friends

### 📊 Statistics & Tracking
- Real-time game statistics
- Win/loss/tie tracking
- Total games played counter
- Persistent session data
- Reset statistics option

### 🎨 Modern UI/UX
- Beautiful gradient design
- Smooth animations and transitions
- Responsive layout for all devices
- Visual feedback for moves
- Winning line highlighting
- Interactive hover effects

### 🔊 Audio Feedback
- Sound effects for moves
- Different sounds for wins, losses, and ties
- Optional sound toggle

### 🛠️ Technical Features
- Clean, modular code architecture
- Configuration management system
- Error handling and validation
- Session-based game state
- RESTful API design
- Type hints and documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

1. **Navigate to the project directory**
   ```bash
   cd TIC_TAC_TOE/tic_tac_toe
   ```

2. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies** (if not already installed)
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## 💻 Technologies Used

- **Backend**: Flask 3.0.0 (Python web framework)
- **Frontend**: 
  - Bootstrap 5 (via bootstrap-flask)
  - JavaScript ES6+ (game logic)
  - CSS3 (modern styling with animations)
- **AI Engine**: Minimax algorithm with alpha-beta pruning
- **Session Management**: Flask-Session
- **Configuration**: python-dotenv

## 📁 Project Structure

```
tic_tac_toe/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── game_engine.py        # Game logic and AI engine
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css    # Modern styles and animations
│   └── js/
│       └── game.js      # Frontend game logic with classes
└── templates/
    ├── base.html        # Base template
    └── index.html       # Main game page
```


## 🎮 How to Play

1. **Choose your game mode**:
   - Select "vs Computer" to play against AI
   - Select "Two Player" for local multiplayer

2. **Set difficulty** (vs Computer mode only):
   - Easy: Beginner-friendly AI
   - Medium: Moderate challenge
   - Hard: Expert-level AI

3. **Make your move**:
   - Click on any empty cell to place your mark (X)
   - In vs Computer mode, the AI will respond automatically
   - In Two Player mode, players alternate turns

4. **Win the game**:
   - Get three marks in a row (horizontal, vertical, or diagonal)
   - Winning cells will be highlighted
   - Statistics will update automatically

5. **Play again**:
   - Click "New Game" to start fresh
   - Click "Reset Stats" to clear all statistics

## 🧠 AI Algorithm

The game uses a **Minimax algorithm with Alpha-Beta pruning** for the Hard difficulty:

- **Minimax**: Explores all possible game states to find optimal moves
- **Alpha-Beta Pruning**: Optimizes performance by eliminating unnecessary branches
- **Depth-based Scoring**: Prefers faster wins and slower losses
- **First Move Randomization**: Adds variety to gameplay

Difficulty levels:
- **Easy**: Random moves with 30% chance of blocking
- **Medium**: 70% strategic play, 30% random
- **Hard**: Perfect play using minimax algorithm

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key-here

# Game Settings
ENABLE_SOUND=true
DEFAULT_DIFFICULTY=hard
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `FLASK_DEBUG` | Debug mode | `true` |
| `SECRET_KEY` | Session encryption key | Auto-generated |
| `ENABLE_SOUND` | Enable sound effects | `true` |
| `DEFAULT_DIFFICULTY` | Default AI difficulty | `hard` |

## 🎨 Customization

### Changing Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #48bb78;
    --danger-color: #f56565;
}
```

### Adjusting AI Difficulty

Edit `game_engine.py` and modify the difficulty methods to customize AI behavior.

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🐛 Troubleshooting

### Game not loading
- Check that Flask server is running
- Verify the correct port (default: 5000)
- Check browser console for errors

### Sound not working
- Verify browser supports Web Audio API
- Check if sounds are enabled in config
- Try refreshing the page

### Statistics not persisting
- Ensure cookies are enabled in browser
- Verify SECRET_KEY is set properly

## 🚀 Future Enhancements

- [ ] Online multiplayer support
- [ ] User accounts and global leaderboards
- [ ] Tournament mode
- [ ] Custom board sizes (4x4, 5x5)
- [ ] AI training visualization
- [ ] Mobile app version
- [ ] Accessibility improvements

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Flask framework by Pallets Projects
- Bootstrap for responsive design
- Flask-Bootstrap for easy integration
- Minimax algorithm concept

---

**Made with ❤️ and Python**

Enjoy playing Tic Tac Toe! 🎮


## 💡 Code Highlights

### Session Management
```python
@app.route('/')
def index():
    session['board'] = [""] * 9
    session['current_player'] = 'X'
    session['game_over'] = False
    return render_template('index.html', board=session['board'])
```

### Win Detection
```python
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
```

### AJAX Game Updates
```javascript
fetch('/make_move', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ position: parseInt(position) })
})
```

## 🎨 Styling Example
```css
.game-board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    max-width: 300px;
    margin: 0 auto;
}
```

## ✨ Why Windsurf IDE?

I'm thrilled to have created this project in mere minutes! Windsurf IDE's automation and smart templates saved me hours of tedious work. The fact that I can create a full-stack web app so quickly is a testament to the incredible technology we have today.

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Add difficulty levels for computer player
- Implement multiplayer support
- Add sound effects and animations
- Create a game history feature
