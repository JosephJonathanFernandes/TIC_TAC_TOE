"""
Tic Tac Toe - A professional web-based game with multiple difficulty levels.
"""
import os
from flask import Flask, render_template, request, jsonify, session
from flask_bootstrap import Bootstrap5
from game_engine import TicTacToeEngine
from config import config

app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

bootstrap = Bootstrap5(app)


def initialize_game_session():
    """Initialize a new game session."""
    session['board'] = [""] * 9
    session['current_player'] = 'X'
    session['game_over'] = False
    session['game_mode'] = session.get('game_mode', 'vs_computer')
    session['difficulty'] = session.get('difficulty', app.config['DEFAULT_DIFFICULTY'])
    session['stats'] = session.get('stats', {
        'player_wins': 0,
        'computer_wins': 0,
        'ties': 0,
        'total_games': 0
    })

@app.route('/')
def index():
    """Main game page."""
    initialize_game_session()
    return render_template('index.html', 
                         board=session['board'],
                         game_mode=session.get('game_mode', 'vs_computer'),
                         difficulty=session.get('difficulty', 'hard'),
                         stats=session.get('stats', {}))

@app.route('/set_options', methods=['POST'])
def set_options():
    """Set game options (mode and difficulty)."""
    data = request.json
    game_mode = data.get('game_mode', 'vs_computer')
    difficulty = data.get('difficulty', 'hard')
    
    if game_mode not in ['vs_computer', 'two_player']:
        return jsonify({'error': 'Invalid game mode'}), 400
    
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Invalid difficulty'}), 400
    
    session['game_mode'] = game_mode
    session['difficulty'] = difficulty
    initialize_game_session()
    
    return jsonify({
        'success': True,
        'game_mode': game_mode,
        'difficulty': difficulty
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    """Handle player move and computer response."""
    if session.get('game_over', False):
        return jsonify({'error': 'Game is over'}), 400
        
    position = request.json.get('position')
    if not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({'error': 'Invalid position'}), 400
        
    board = session.get('board', [""] * 9)
    if board[position] != "":
        return jsonify({'error': 'Position already taken'}), 400
    
    game_mode = session.get('game_mode', 'vs_computer')
    current_player = session.get('current_player', 'X')
    
    # Initialize game engine
    engine = TicTacToeEngine(session.get('difficulty', 'hard'))
    
    # Player's move
    try:
        board, winner = engine.make_move(board, position, current_player)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    winning_line = None
    computer_position = None
    
    # Check for winner after player's move
    if winner is None and game_mode == 'vs_computer' and current_player == 'X':
        # Computer's move
        computer_position = engine.get_computer_move(board)
        if computer_position is not None:
            board, winner = engine.make_move(board, computer_position, 'O')
    elif game_mode == 'two_player':
        # Switch player in two-player mode
        current_player = 'O' if current_player == 'X' else 'X'
        session['current_player'] = current_player
    
    session['board'] = board
    
    if winner:
        session['game_over'] = True
        winning_line = engine.get_winning_line(board)
        
        # Update statistics
        stats = session.get('stats', {
            'player_wins': 0,
            'computer_wins': 0,
            'ties': 0,
            'total_games': 0
        })
        
        stats['total_games'] += 1
        if winner == 'X':
            stats['player_wins'] += 1
        elif winner == 'O':
            stats['computer_wins'] += 1
        elif winner == 'tie':
            stats['ties'] += 1
        
        session['stats'] = stats
        
        return jsonify({
            'board': board,
            'winner': winner,
            'game_over': True,
            'winning_line': winning_line,
            'computer_position': computer_position,
            'stats': stats
        })
    
    return jsonify({
        'board': board,
        'winner': None,
        'game_over': False,
        'winning_line': None,
        'computer_position': computer_position,
        'current_player': current_player
    })

@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the current game."""
    initialize_game_session()
    return jsonify({
        'success': True,
        'board': session['board']
    })

@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    """Reset game statistics."""
    session['stats'] = {
        'player_wins': 0,
        'computer_wins': 0,
        'ties': 0,
        'total_games': 0
    }
    return jsonify({
        'success': True,
        'stats': session['stats']
    })

@app.route('/get_stats', methods=['GET'])
def get_stats():
    """Get current game statistics."""
    return jsonify({
        'stats': session.get('stats', {
            'player_wins': 0,
            'computer_wins': 0,
            'ties': 0,
            'total_games': 0
        })
    })


if __name__ == '__main__':
    app.run(debug=True)
