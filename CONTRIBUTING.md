# Contributing to Tic Tac Toe

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Detailed steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:
- A clear, descriptive title
- Detailed explanation of the proposed functionality
- Why this enhancement would be useful
- Any relevant examples or mockups

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, documented code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed

3. **Test your changes**
   - Ensure all existing functionality still works
   - Test your new feature thoroughly
   - Check for any console errors

4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
   
   Use clear commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for changes to existing features
   - `Refactor:` for code refactoring
   - `Docs:` for documentation changes

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots/GIFs of UI changes (if applicable)

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TIC_TAC_TOE.git
   cd TIC_TAC_TOE
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r tic_tac_toe/requirements.txt
   ```

4. Run the application:
   ```bash
   cd tic_tac_toe
   python app.py
   ```

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Python Example
```python
def calculate_winner(board: list[str]) -> tuple[str | None, list[int] | None]:
    """
    Determine the winner of the game.
    
    Args:
        board: List of 9 strings representing the game board
        
    Returns:
        Tuple of (winner, winning_line) or (None, None) if no winner
    """
    # Implementation here
    pass
```

### JavaScript Example
```javascript
/**
 * Handle a cell click event
 * @param {number} index - The index of the clicked cell
 */
function handleCellClick(index) {
    // Implementation here
}
```

## Project Structure

```
TIC_TAC_TOE/
├── tic_tac_toe/
│   ├── app.py              # Flask application
│   ├── game_engine.py      # Game logic
│   ├── config.py           # Configuration
│   ├── static/
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript files
│   └── templates/          # HTML templates
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt
```

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing! 🎮
