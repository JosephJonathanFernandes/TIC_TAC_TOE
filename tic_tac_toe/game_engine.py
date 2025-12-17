"""
Game engine for Tic Tac Toe with multiple difficulty levels.
"""
import random
from typing import List, Optional, Tuple

class TicTacToeEngine:
    """Tic Tac Toe game logic and AI."""
    
    WINNING_COMBINATIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    
    def __init__(self, difficulty: str = 'hard'):
        """
        Initialize the game engine.
        
        Args:
            difficulty: AI difficulty level ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty.lower()
        self.board = [""] * 9
        
    def check_winner(self, board: List[str]) -> Optional[str]:
        """
        Check if there's a winner on the board.
        
        Args:
            board: Current board state
            
        Returns:
            'X', 'O', 'tie', or None if game continues
        """
        for combo in self.WINNING_COMBINATIONS:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
                return board[combo[0]]
        
        if "" not in board:
            return "tie"
        return None
    
    def get_winning_line(self, board: List[str]) -> Optional[List[int]]:
        """
        Get the winning line indices if there's a winner.
        
        Args:
            board: Current board state
            
        Returns:
            List of winning cell indices or None
        """
        for combo in self.WINNING_COMBINATIONS:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
                return combo
        return None
    
    def get_empty_cells(self, board: List[str]) -> List[int]:
        """Get list of empty cell indices."""
        return [i for i, cell in enumerate(board) if cell == ""]
    
    def minimax(self, board: List[str], depth: int, is_maximizing: bool, 
                alpha: float, beta: float) -> int:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current board state
            depth: Current depth in game tree
            is_maximizing: Whether maximizing player's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Score of the position
        """
        result = self.check_winner(board)
        
        if result == 'O':
            return 10 - depth
        elif result == 'X':
            return depth - 10
        elif result == 'tie':
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for pos in self.get_empty_cells(board):
                board[pos] = 'O'
                score = self.minimax(board, depth + 1, False, alpha, beta)
                board[pos] = ''
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for pos in self.get_empty_cells(board):
                board[pos] = 'X'
                score = self.minimax(board, depth + 1, True, alpha, beta)
                board[pos] = ''
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def get_best_move_hard(self, board: List[str]) -> int:
        """Get best move using minimax algorithm."""
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # First move randomization for variety
        empty_cells = self.get_empty_cells(board)
        if len(empty_cells) >= 8:
            return random.choice(empty_cells)
        
        # Use minimax for subsequent moves
        for pos in empty_cells:
            board[pos] = 'O'
            score = self.minimax(board, 0, False, alpha, beta)
            board[pos] = ''
            if score > best_score:
                best_score = score
                best_move = pos
        
        return best_move
    
    def get_best_move_medium(self, board: List[str]) -> int:
        """Get medium difficulty move (mix of smart and random)."""
        empty_cells = self.get_empty_cells(board)
        
        # 70% chance to play optimally, 30% random
        if random.random() < 0.7:
            # Check for winning move
            for pos in empty_cells:
                board[pos] = 'O'
                if self.check_winner(board) == 'O':
                    board[pos] = ''
                    return pos
                board[pos] = ''
            
            # Block opponent's winning move
            for pos in empty_cells:
                board[pos] = 'X'
                if self.check_winner(board) == 'X':
                    board[pos] = ''
                    return pos
                board[pos] = ''
            
            # Take center if available
            if 4 in empty_cells:
                return 4
            
            # Take corners
            corners = [0, 2, 6, 8]
            available_corners = [c for c in corners if c in empty_cells]
            if available_corners:
                return random.choice(available_corners)
        
        # Random move
        return random.choice(empty_cells)
    
    def get_best_move_easy(self, board: List[str]) -> int:
        """Get easy difficulty move (mostly random, occasionally blocks)."""
        empty_cells = self.get_empty_cells(board)
        
        # 30% chance to block winning move
        if random.random() < 0.3:
            for pos in empty_cells:
                board[pos] = 'X'
                if self.check_winner(board) == 'X':
                    board[pos] = ''
                    return pos
                board[pos] = ''
        
        # Random move
        return random.choice(empty_cells)
    
    def get_computer_move(self, board: List[str]) -> int:
        """
        Get computer move based on difficulty level.
        
        Args:
            board: Current board state
            
        Returns:
            Index of cell to play
        """
        if self.difficulty == 'easy':
            return self.get_best_move_easy(board)
        elif self.difficulty == 'medium':
            return self.get_best_move_medium(board)
        else:  # hard
            return self.get_best_move_hard(board)
    
    def make_move(self, board: List[str], position: int, player: str) -> Tuple[List[str], Optional[str]]:
        """
        Make a move on the board.
        
        Args:
            board: Current board state
            position: Cell index to play
            player: Player symbol ('X' or 'O')
            
        Returns:
            Tuple of (updated board, winner if any)
        """
        if board[position] != "":
            raise ValueError("Position already taken")
        
        board[position] = player
        winner = self.check_winner(board)
        return board, winner
