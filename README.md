🧟 Zombie Survival Game
A 2D top-down shooter game built using Python and Pygame, where you fight off endless waves of zombies, collect powerups, earn coins, and upgrade your abilities in between waves through an in-game shop.

🎮 Features
🧟 Multiple zombie types: Normal, Fast, Tank, and Boss

💥 Two weapons: Pistol and Shotgun (switch with Q)

🛍️ Upgrade shop between waves (opens every 30 seconds)

💰 Coins system to buy:

Health refills

Speed boost

Faster fire rate

Unlock shotgun

🎯 Bullet collision detection and splatter effects

🔄 Day/Night cycle

❤️ Powerups: Health and Speed Boost

🎵 Custom sound effects and background music

🖼️ Screenshots


🔧 Requirements
Python 3.7+

pygame

Install pygame via pip if needed:

bash
Copy code
pip install pygame
▶️ How to Run
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/zombie-survival-game.git
cd zombie-survival-game
Run the game:

bash
Copy code
python main.py
Controls:

Arrow keys / WASD: Move

SPACE: Shoot

Q: Switch weapon

ESC: Close shop / exit game

R: Restart after game over

📁 Folder Structure
css
Copy code
zombie-survival-game/
│
├── assets/
│   ├── player.png
│   ├── zombie.png
│   ├── zombie_fast.png
│   ├── zombie_tank.png
│   ├── zombie_boss.png
│   ├── bullet.png
│   ├── heart.png
│   ├── speed.png
│   └── sounds/
│       ├── shoot.mp3
│       ├── zombie_hit.wav
│       ├── player_hit.wav
│       ├── game_over.wav
│       └── background.mp3
│
├── main.py
└── README.md
🚀 Future Improvements
Add new weapons and enemy types

Save/load system for upgrades and high scores

Boss fights with unique mechanics

Controller support

Multiplayer mode (LAN)

