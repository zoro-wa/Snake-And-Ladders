# SNAKE AND LADDERS GAME (Python + Pygame)


    Basic modern version of The classic *Snake And Ladders" board game which is built
    using **Python** And **Pygame". It includes **Player vs Player** and **Player vs Computer**
    modes with decent sound effects, smooth dice-rooling and good visuals.

##  VIDEO URL : https://youtu.be/kZac17eNnHw


## 📑 Table of Contents
-  [Features](#features)
-  [Installation](#installation)
-  [How to play](#how_to_play)
-  [Project Structure](#project_structure)
-  [Testing](#testing)
-  [Future Improvements](#future_improvements)
-  [Testing](#testing)


## ✨ Features
- 🎮 Player vs Player And Player vs Computer modes.
- 🎲 Simple dice roll animation with sound effects.
- 🪜 basic ladder climb and and snake fall movements.
- 🏆 Winner Screen with options to play_again and back to main menu options.
- 🔊 Start_menu bg music and dice roll sound effects.
- 🧩 Flexible and testbale code using pytest.


## ⚙️ Installation

1. Clone this repoistory:
   ```bash
      git clone https://github.com/zoro-wa/Snake-And-Ladders.git
      cd Snake-And-Ladders
      
      a. python -m venv venv
         source venv/bin/activate   # On Linux/Mac
         venv\Scripts\activate      # On Windows
      
      b. pip install required liabraries(pygame,os)

      c. python project.py


## 🕹️ How to Play
    
-  Choose **Player vs Player** or **Player vs Computer** in the start menu.
-  Press **Space** to roll the dice.
-  **Player** moves after **Space** is pressed where as Computer rolls automatically.
-  Ladders take you up 🪜 and snakes bring you down 🐍.
-  The first to reach the **100th tile** wins.


## 🧱 Project Structure

    Snake-And-Ladders/
    │
    ├── assets/
    │   ├── images/
    │   ├── sounds/
    │   └── music/
    │
    ├── Game/
    │   ├── __init__.py
    │   ├── board.py
    │   ├── dice.py
    │   └── player.py
    │
    ├── project.py
    ├── test_project.py
    └── README.md

## 🧪 Testing
The project includes unit tests written using **pytest**.
    Run all tests:
       pytest

## 🌱 Future Improvements
- Playable on mobile devices.
- Another board game can be added as an option such as Ludo.
- More player can be added.
- Improved Animations And Dice-Rolling.

## ❤️ Credits
- Developed by **Bidhan Raj Shakya**
- Built with **Python3** and **Pygame**
- A very Special thanks to **CS50**, **Manoj Kumar Mohotara** for this opportunity, support and motivation.