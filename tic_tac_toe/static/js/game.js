// ===== Game Configuration =====
const GameConfig = {
    PLAYER_X: 'X',
    PLAYER_O: 'O',
    SOUNDS_ENABLED: true
};

// ===== Toast Notification System =====
class ToastManager {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <span class="toast-message">${message}</span>
            <button class="toast-close" aria-label="Close">×</button>
        `;

        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => this.remove(toast));

        this.container.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(() => this.remove(toast), 3000);
    }

    remove(toast) {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }
}

// ===== Sound Effects =====
class SoundManager {
    constructor() {
        this.sounds = {
            move: this.createSound(440, 0.1, 'sine'),
            win: this.createSound(523, 0.3, 'square'),
            lose: this.createSound(220, 0.3, 'sawtooth'),
            tie: this.createSound(330, 0.2, 'sine')
        };
    }

    createSound(frequency, duration, type = 'sine') {
        return () => {
            if (!GameConfig.SOUNDS_ENABLED) return;

            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = frequency;
                oscillator.type = type;
                gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + duration);
            } catch (e) {
                console.log('Audio not supported');
            }
        };
    }

    play(soundName) {
        if (this.sounds[soundName]) {
            this.sounds[soundName]();
        }
    }
}

// ===== Game Manager =====
class GameManager {
    constructor() {
        this.cells = document.querySelectorAll('.cell');
        this.status = document.getElementById('status');
        this.resetButton = document.getElementById('reset-game');
        this.resetStatsButton = document.getElementById('reset-stats');
        this.gameModeSelect = document.getElementById('game-mode');
        this.difficultySelect = document.getElementById('difficulty');
        this.difficultyControl = document.getElementById('difficulty-control');

        this.soundManager = new SoundManager();
        this.toastManager = new ToastManager();
        this.isProcessing = false;

        this.init();
    }

    init() {
        this.attachEventListeners();
        this.updateDifficultyVisibility();
    }

    attachEventListeners() {
        this.cells.forEach(cell => {
            cell.addEventListener('click', (e) => this.handleMove(e));
            // Add keyboard accessibility
            cell.setAttribute('tabindex', '0');
            cell.setAttribute('role', 'button');
            cell.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleMove(e);
                }
            });
        });

        this.resetButton.addEventListener('click', () => this.resetGame());
        this.resetStatsButton.addEventListener('click', () => this.resetStats());

        this.gameModeSelect.addEventListener('change', () => this.handleOptionsChange());
        this.difficultySelect.addEventListener('change', () => this.handleOptionsChange());
    }

    updateDifficultyVisibility() {
        const gameMode = this.gameModeSelect.value;
        this.difficultyControl.style.display = gameMode === 'vs_computer' ? 'flex' : 'none';
    }

    async handleOptionsChange() {
        this.updateDifficultyVisibility();

        const gameMode = this.gameModeSelect.value;
        const difficulty = this.difficultySelect.value;

        try {
            const response = await fetch('/set_options', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game_mode: gameMode, difficulty: difficulty })
            });

            const data = await response.json();
            if (data.success) {
                this.resetGame(false);
                this.toastManager.show('Game settings updated!', 'success');
            }
        } catch (error) {
            console.error('Error setting options:', error);
            this.toastManager.show('Failed to update settings', 'error');
        }
    }

    async handleMove(event) {
        console.log('handleMove called', event.target);
        
        if (this.isProcessing) {
            console.log('Already processing, ignoring click');
            return;
        }

        const cell = event.target;
        const position = parseInt(cell.dataset.index);
        
        console.log('Cell clicked:', position, 'Content:', cell.textContent);

        if (cell.textContent !== '' || cell.classList.contains('disabled')) {
            console.log('Cell is occupied or disabled');
            return;
        }

        this.isProcessing = true;
        this.soundManager.play('move');

        try {
            console.log('Sending move to server:', position);
            const response = await fetch('/make_move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ position: position })
            });

            const data = await response.json();
            console.log('Server response:', data);

            if (data.error) {
                this.toastManager.show(data.error, 'error');
                this.isProcessing = false;
                return;
            }

            // Animate player move
            this.updateBoard(data.board, position);

            // Animate computer move if present
            if (data.computer_position !== null && data.computer_position !== undefined) {
                setTimeout(() => {
                    this.updateCell(data.computer_position, data.board[data.computer_position]);
                    this.soundManager.play('move');
                }, 300);
            }

            if (data.winner) {
                setTimeout(() => {
                    this.handleGameOver(data.winner, data.winning_line);
                    this.updateStats(data.stats);
                }, 400);
            } else {
                const gameMode = this.gameModeSelect.value;
                if (gameMode === 'two_player') {
                    const nextPlayer = data.current_player || 'X';
                    this.status.textContent = `Player ${nextPlayer}'s turn`;
                    this.status.className = `status-${nextPlayer.toLowerCase()}`;
                } else {
                    this.status.textContent = "Your turn (X)";
                    this.status.className = "status-x";
                }
            }

            if (data.game_over) {
                this.disableBoard();
            }
        } catch (error) {
            console.error('Error:', error);
            this.toastManager.show('An error occurred. Please try again.', 'error');
        } finally {
            this.isProcessing = false;
        }
    }

    updateBoard(board, animateIndex = null) {
        this.cells.forEach((cell, index) => {
            if (animateIndex !== null && index === animateIndex) {
                this.updateCell(index, board[index]);
            } else if (cell.textContent !== board[index]) {
                this.updateCell(index, board[index]);
            }
        });
    }

    updateCell(index, value) {
        const cell = this.cells[index];
        cell.textContent = value;
        cell.setAttribute('aria-label', value ? `${value} placed` : 'Empty cell');
        
        if (value === 'X') {
            cell.classList.add('x');
        } else if (value === 'O') {
            cell.classList.add('o');
        }
    }

    handleGameOver(winner, winningLine) {
        if (winner === 'tie') {
            this.status.textContent = "🤝 It's a tie!";
            this.status.className = 'status-tie';
            this.soundManager.play('tie');
        } else {
            const gameMode = this.gameModeSelect.value;
            if (gameMode === 'two_player') {
                this.status.textContent = `🎉 Player ${winner} wins!`;
            } else {
                if (winner === 'X') {
                    this.status.textContent = `🎉 You win!`;
                    this.soundManager.play('win');
                } else {
                    this.status.textContent = `💔 Computer wins!`;
                    this.soundManager.play('lose');
                }
            }
            this.status.className = `status-${winner.toLowerCase()}`;

            // Highlight winning line
            if (winningLine) {
                winningLine.forEach(index => {
                    setTimeout(() => {
                        this.cells[index].classList.add('winning');
                    }, 100);
                });
            }
        }
    }

    disableBoard() {
        this.cells.forEach(cell => {
            cell.classList.add('disabled');
        });
    }

    async resetGame(fullReload = true) {
        if (fullReload) {
            try {
                const response = await fetch('/reset_game', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                const data = await response.json();
                if (data.success) {
                    this.clearBoard();
                }
            } catch (error) {
                console.error('Error resetting game:', error);
                window.location.reload();
            }
        } else {
            this.clearBoard();
        }
    }

    clearBoard() {
        this.cells.forEach(cell => {
            cell.textContent = '';
            cell.className = 'cell';
        });

        this.status.textContent = "Your turn (X)";
        this.status.className = 'status-x';
        this.isProcessing = false;
    }

    async resetStats() {
        if (!confirm('Are you sure you want to reset all statistics?')) {
            return;
        }

        try {
            const response = await fetch('/reset_stats', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (data.success) {
                this.updateStats(data.stats);
                this.toastManager.show('Statistics reset successfully!', 'success');
            }
        } catch (error) {
            console.error('Error resetting stats:', error);
            this.toastManager.show('Failed to reset statistics', 'error');
        }
    }

    updateStats(stats) {
        document.getElementById('stat-wins').textContent = stats.player_wins || 0;
        document.getElementById('stat-losses').textContent = stats.computer_wins || 0;
        document.getElementById('stat-ties').textContent = stats.ties || 0;
        document.getElementById('stat-total').textContent = stats.total_games || 0;

        // Add pulse animation to stats
        [document.getElementById('stat-wins'),
         document.getElementById('stat-losses'),
         document.getElementById('stat-ties'),
         document.getElementById('stat-total')].forEach(el => {
            el.parentElement.style.animation = 'none';
            setTimeout(() => {
                el.parentElement.style.animation = 'popIn 0.3s ease';
            }, 10);
        });
    }
}

// ===== Initialize Game =====
document.addEventListener('DOMContentLoaded', () => {
    new GameManager();
});
