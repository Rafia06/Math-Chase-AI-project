# Math-Chase-AI-project

## Overview
The Math Chase Game is an AI-driven strategic math-based game developed using Python and Tkinter. It incorporates various AI techniques, such as Minimax with Alpha-Beta Pruning, Fuzzy Logic, and Genetic Algorithms, to deliver a challenging and interactive experience for players. The project is designed to test players' mathematical skills while providing a practical demonstration of AI concepts in gameplay.

## Key Features
- **Strategic AI:** Implements advanced algorithms, including Minimax with Alpha-Beta Pruning, Fuzzy Logic, and Genetic Algorithms, to adaptively respond to player actions.
- **Turn-Based Gameplay:** Supports single-player mode against an AI opponent and multiplayer modes with alternating turns.
- **Difficulty Levels:** Offers three difficulty levels (Easy, Medium, and Hard) tailored to players' preferences.
- **Dynamic Game Elements:** Features a score-based system with selectable actions like score addition and subtraction.
- **Interactive Interface:** Intuitive graphical interface powered by Tkinter for smooth player interactions.
- **Audio Feedback:** Includes sound effects for actions and events to enhance the user experience.

---

## Game Rules

1. **Turn-Based Gameplay:** Players take turns choosing score or subtraction values to affect their and the AI's scores.
2. **Goal:** Achieve the highest score to win the game.
3. **Actions:**
   - Select scores from an array to add to your total.
   - Choose subtraction values to deduct from opponents' totals.
4. **Winning Conditions:**
   - The player or AI with the highest score at the end of the game wins.

---

## AI Strategies and Implementation

### **Minimax Algorithm with Alpha-Beta Pruning**
- **Approach:**
  - Depth-limited search algorithm optimizing decision-making.
  - Evaluates the best moves for the AI by simulating player responses.

### **Genetic Algorithm**
- **Approach:**
  - Used in "Hard" mode to evolve optimal strategies.
  - Generates and refines move populations through selection, crossover, and mutation.

### **Fuzzy Logic System**
- **Approach:**
  - Determines the best move in "Easy" mode using simple fuzzy rules.
  - Weighs factors such as maximizing AI scores while minimizing player gains.
---

## Class Diagram

The association and encapsulation of each class are represented in the following class diagram:

![Class Diagram](https://github.com/Rafia06/image/blob/main/math_chase_class_diagram.png)

---

## Figures
### Opening
- ![Class Diagram](https://github.com/Rafia06/image/blob/main/Screenshot%202024-09-03%20124029.png)
### Choose Difficulty
- ![Class Diagram](https://github.com/Rafia06/image/blob/main/Screenshot%202024-09-03%20124303.png)
### Score board
- ![Class Diagram](https://github.com/Rafia06/image/blob/main/Screenshot%202024-09-03%20124518.png)
### Numbers
- ![Class Diagram](https://github.com/Rafia06/image/blob/main/Screenshot%202024-09-03%20124754.png)
### Win 
- ![Class Diagram](https://github.com/Rafia06/image/blob/main/Screenshot%202024-09-03%20125614.png)


---
## Installation
- Requirements:
  - Python 3.x
  - Tkinter for GUI
  - Pygame for sound effects
- Setup:
  - Install dependencies.
  - Run the main.py file to start the game.
  
## Conclusion
The project successfully developed an AI-powered Math game, integrating Minimax, Genetic Algorithms, and Fuzzy Logic for intelligent decision-making. These advanced techniques created a responsive and challenging AI opponent, significantly enhancing the overall gaming experience.
