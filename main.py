import copy
import math
import random
import time
import tkinter as tk
from pygame import mixer

from tkinter import *

depth = None
difficulty = ""
current_player = ""


def checkWins():
    game_over_label = tk.Label(window, bg="#f8f9fa", fg="#495057",
                               font=("8514oem", 14, "bold"), padx=44, pady=25, bd=1,
                               relief="solid")

    if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
        game_over_label.config(text="AI WINS")
        gameOverSound()
    elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
        game_over_label.config(text="Player 1 Wins")
        gameWinSound()
    elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
        game_over_label.config(text="Player 2 Wins")
        gameWinSound()
    else:
        game_over_label.config(text="It's a tie")
        gameWinSound()

    game_over_label.place(relx=0.5, rely=0.5, anchor="center")

    return


def generate_moves(scores, selected):
    # Generates a list of available moves (indices of unselected scores)
    return [i for i, score in enumerate(scores) if not selected[i]]


############################# Heuristic ###################################
def evaluate(aiScore, human1Score, human2Score):
    return aiScore - (human1Score + human2Score)


############################# Heuristic ###################################

def game_over(selected):
    # Returns True if all scores have been selected
    return all(selected)

# Min-Max with alpha-beta prunning for "Medium"
def minimax(depth, alpha, beta, maximizing_player, scores, selected, aiScore, human1Score, human2Score):
    if depth <= 0 or game_over(selected):
        return evaluate(aiScore, human1Score, human2Score)

    if maximizing_player == 0:
        max_eval = float('-inf')
        for move in generate_moves(scores, selected):
            selected[move] = True
            aiScore += scores[move]
            eval_score = minimax(depth - 1, alpha, beta, (maximizing_player + 1) % 3, scores, selected, aiTotalScore+game_state[move],
                                 human1Score, human2Score)
            selected[move] = False
            aiScore -= scores[move]
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(scores, selected):
            selected[move] = True

            if maximizing_player == 1:
                human1Score += scores[move]
            else:
                human2Score += scores[move]
            eval_score = minimax(depth - 1, alpha, beta, (maximizing_player + 1) % 3, scores, selected, aiScore,
                                 human1Score, human2Score)
            selected[move] = False
            if maximizing_player == 1:
                human1Score -= scores[move]
            else:
                human2Score -= scores[move]
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

# Fuzzy Logic for "Easy"
def fuzzy_logic(scores, selected, aiScore, human1Score, human2Score):
    # Simple fuzzy logic implementation
    available_moves = generate_moves(scores, selected)
    move_evaluations = []

    for move in available_moves:
        ai_delta = scores[move]
        human1_delta = human1Score
        human2_delta = human2Score
        evaluation = fuzzy_evaluation(ai_delta, human1_delta, human2_delta)
        move_evaluations.append((move, evaluation))

    # Sort by evaluation score, descending
    move_evaluations.sort(key=lambda x: x[1], reverse=True)

    return move_evaluations[0][0]


def fuzzy_evaluation(ai_delta, human1_delta, human2_delta):
    # Basic fuzzy rules: higher AI score, lower human scores are better
    ai_weight = 0.6
    human1_weight = 0.2
    human2_weight = 0.2

    return ai_weight * ai_delta - human1_weight * human1_delta - human2_weight * human2_delta


# Genetic Algorithm for "Hard"
def genetic_algorithm(scores, selected, aiScore, human1Score, human2Score):
    population_size = 10
    generations = 100
    mutation_rate = 0.1
    available_moves = generate_moves(scores, selected)

    # Initial population: random valid moves
    population = [random.choice(available_moves) for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [evaluate_individual(individual, scores, aiScore, human1Score, human2Score) for individual in
                          population]
        population = evolve_population(population, fitness_scores, mutation_rate, available_moves)

    # Select the best individual
    best_individual = max(population,
                          key=lambda ind: evaluate_individual(ind, scores, aiScore, human1Score, human2Score))
    return best_individual


def evaluate_individual(move, scores, aiScore, human1Score, human2Score):
    # Evaluate how good the move is
    return aiScore + scores[move] - (human1Score + human2Score)


def evolve_population(population, fitness_scores, mutation_rate, available_moves):
    # Select top individuals to breed
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
    new_population = sorted_population[:len(population) // 2]

    # Breeding
    while len(new_population) < len(population):
        parent1, parent2 = random.sample(new_population, 2)
        child = crossover(parent1, parent2)
        new_population.append(mutate(child, mutation_rate, available_moves))

    return new_population


def crossover(parent1, parent2):
    # Simple crossover: choose one of the parents' moves
    return parent1 if random.random() > 0.5 else parent2


def mutate(individual, mutation_rate, available_moves):
    # Simple mutation: randomly change the move
    if random.random() < mutation_rate:
        return random.choice(available_moves)
    return individual


def update_scores():
    # Create separate labels for each player
    p1_score_label.config(
        text="Player 1: " + str(humanTotalScore1),
        bg="#f9ca24",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )
    p2_score_label.config(
        text="Player 2: " + str(humanTotalScore2),
        bg="#f0932b",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )
    ai_score_label.config(
        text="AI: " + str(aiTotalScore),
        bg="#badc58",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )


def game_over(selectedSub):
    return all(selectedSub)


def update_game_state():
    for button in score_buttons:
        button.config(state=tk.DISABLED if selected[button.index] else tk.NORMAL, disabledforeground="#535c68")

    for button in subtraction_buttons:
        button.config(state=tk.DISABLED if selectedSub[button.index] else tk.NORMAL, disabledforeground="#535c68")


def create_score_buttons():
    score_array_text.place(relx=0.019, rely=0.500, anchor="w")

    score_buttons_frame = tk.Frame(canvas, bg="")
    score_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

    for i, score in enumerate(game_state):
        button = Button(score_buttons_frame, text=str(score), command=lambda index=i: process_score_selection(index))
        button.config(
            bg="#2ed573",
            fg="black",
            font=("8514oem", 12), bd=1,
            relief="solid",
            padx=10,
            pady=5,
            width=4,
            height=1,

        )
        button.index = i
        button.pack(side="left", padx=5, pady=(10, 10))
        score_buttons.append(button)


def create_subtraction_buttons():
    subtract_array_text.place(relx=0.019, rely=0.699, anchor="w")

    subtraction_buttons_frame = tk.Frame(canvas, bg="")
    subtraction_buttons_frame.place(relx=0.5, rely=0.7, anchor="center")

    for i, sub in enumerate(subtraction_state):
        button = Button(subtraction_buttons_frame, text=str(sub),
                        command=lambda index=i: process_subtraction_selection(index))
        button.config(
            bg="#ff4757",
            fg="black",
            font=("8514oem", 12),
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            width=4,
            height=1
        )
        button.index = i
        button.pack(side="left", padx=5, pady=(10, 10))
        subtraction_buttons.append(button)

def ai_turn():
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore
    current_player = "AI"
    player_label.config(text="Current player: " + current_player)
    window.update()
    time.sleep(1)

    best_move_sub = 0
    best_move = 0
    if difficulty == "Medium":
        best_score = float('-inf')
        best_score_sub = float('-inf')
        for move in generate_moves(game_state, selected):
            selected[move] = True
            eval_score = minimax(depth, float('-inf'), float('inf'), 1, game_state, selected,
                                 aiTotalScore + game_state[move],
                                 humanTotalScore1, humanTotalScore2)
            selected[move] = False
            if eval_score > best_score:
                best_score = eval_score
                best_move = move
            print("AI explores:", move, "and best score:", eval_score)
        print("AI Best Score Found at:", best_move, "and best score:", best_score)
        for move in generate_moves(subtraction_state, selectedSub):
            selectedSub[move] = True
            eval_score_sub = minimax(depth, float('-inf'), float('inf'), 1, subtraction_state, selectedSub,
                                     aiTotalScore,
                                     humanTotalScore1, humanTotalScore2)
            selectedSub[move] = False
            if eval_score_sub > best_score_sub:
                best_score_sub = eval_score_sub
                best_move_sub = move
            print("AI explores:", move, "and best sub score:", eval_score_sub)
        print("AI Best Subtraction Score Found at:", best_move_sub, "and best score:", best_score_sub)



    elif difficulty == "Easy":
        best_move = fuzzy_logic(game_state, selected, aiTotalScore, humanTotalScore1, humanTotalScore2)
        best_move_sub=fuzzy_logic(subtraction_state, selectedSub, aiTotalScore, humanTotalScore1, humanTotalScore2)
    elif difficulty == "Hard":
        best_move = genetic_algorithm(game_state, selected, aiTotalScore, humanTotalScore1, humanTotalScore2)
        best_move_sub = genetic_algorithm(subtraction_state, selectedSub, aiTotalScore, humanTotalScore1, humanTotalScore2)

    selected[best_move] = True
    selectedSub[best_move_sub] = True

    aiTotalScore += game_state[best_move]
    humanTotalScore1 -= subtraction_array[best_move_sub]
    humanTotalScore2 -= subtraction_array[best_move_sub]

    update_scores()
    update_game_state()
    gameBounsSound()

    if game_over(selected):
        checkWins()
    else:
        player1_turn()



def player1_turn():
    global current_player
    current_player = "Player 1"
    player_label.config(text="Current player: " + current_player)


def player2_turn():
    global current_player
    current_player = "Player 2"
    player_label.config(text="Current player: " + current_player)


def process_score_selection(index):
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore, score_selected, hint_label

    if not selected[index]:
        chosen_index = index
        selected[chosen_index] = True
        score = game_state[chosen_index]
        if current_player == "Player 1":
            humanTotalScore1 += score

        elif current_player == "Player 2":
            humanTotalScore2 += score

        update_scores()
        update_game_state()
        score_selected = True


def process_subtraction_selection(index):
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore, score_selected

    if not selectedSub[index] and score_selected == True:
        score_selected = False
        chosen_sub_index = index
        selectedSub[chosen_sub_index] = True
        score_sub = subtraction_state[chosen_sub_index]
        if current_player == "Player 1":
            humanTotalScore2 -= score_sub
            aiTotalScore -= score_sub

        elif current_player == "Player 2":
            humanTotalScore1 -= score_sub
            aiTotalScore -= score_sub

        update_scores()
        update_game_state()
        gameBounsSound()

        if game_over(selectedSub):
            checkWins()
        else:
            if current_player == 'Player 1':
                player2_turn()
            else:
                current_player = "AI"
                ai_turn()


def toggle_sound():
    global sound_on, sound_button_image

    if sound_on:
        mixer.music.pause()
        sound_button.config(image=mute_icon)
        sound_on = False
    else:
        mixer.music.unpause()
        sound_button.config(image=sound_icon)
        sound_on = True


def gameBounsSound():
    button_sound = mixer.Sound("game-bonus.mp3")
    if sound_on:
        button_sound.play()


def gameOpenningSound():
    button_sound = mixer.Sound("game_openning.mp3")
    if sound_on:
        button_sound.play()


def gameOverSound():
    button_sound = mixer.Sound("game_over.wav")
    if sound_on:
        button_sound.play()


def gameWinSound():
    button_sound = mixer.Sound("game_win.wav")
    if sound_on:
        button_sound.play()


def save_difficulty(difficul):
    global depth
    global difficulty

    difficulty = difficul

    if difficulty == "Easy":
        depth = 0
    elif difficulty == "Medium":
        # medium level
        depth = math.log(len(score_array), 2) / 2
    else:
        depth = 0
    difficulty_label = tk.Label(window, text="Level: " + difficulty, bg="#f8f9fa", fg="#495057",
                                font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                relief="solid")
    difficulty_label.place(relx=0.019 + 0.22, rely=0.1, anchor="w")
    buttonEasy.destroy()
    buttonHard.destroy()
    buttonMedium.destroy()
    select_level.destroy()

    print("Difficulty level selected:", difficulty)


def save_current_player(cur_player):
    # also check if difficulty is selected
    global current_player, difficulty
    if difficulty != "":
        buttonFirstPlayer.destroy()
        buttonSecondPlayer.destroy()
        buttonAI.destroy()
        select_current_player.destroy()
        current_player = cur_player
        if current_player == "Player 1":
            player1_turn()
        elif current_player == "Player 2":
            player2_turn()
        else:
            window.after(1000, ai_turn)
        print("Current player:", current_player)
        create_score_buttons()
        create_subtraction_buttons()


def create_button(btn, color, paddingx):
    btn.config(
        bg=color,
        fg="white",
        font=("8514oem", 12),
        bd=1,
        relief="solid",
        padx=paddingx,
        pady=5,
        width=4,
        height=1
    )



####################################################################### Initialize Game ###################################################################################################

def start_game():
    front_window.destroy()
    main_window()


def front_window():
    global front_window
    front_window = tk.Tk()
    front_window.title("Math Chase")

    front_window.state('zoomed')
    front_window.size()
    front_window.configure(bg="#bb8fce")

    game_title = tk.Label(front_window, text="Math Chase", font=("8514oem", 100, "bold"), bg="#bb8fce", fg="#2d3436")
    game_title.pack(pady=150)

    start_button = tk.Button(front_window, text="Start Play", command=start_game,
                             font=("8514oem", 18, "bold"), bg="#e67e22", fg="white", padx=20, pady=10)
    start_button.pack()

    front_window.mainloop()

def main_window():
    global window, canvas, background_image, score_array_text, subtract_array_text, player_label
    global p1_score_label, p2_score_label, ai_score_label, game_over_label
    global select_current_player, buttonFirstPlayer, buttonSecondPlayer, buttonAI
    global select_level, buttonEasy, buttonMedium, buttonHard,selected,selectedSub
    global score_buttons, subtraction_buttons, score_selected, game_state, subtraction_state
    global sound_icon, mute_icon, sound_button_image, sound_button
    global humanTotalScore1, humanTotalScore2, aiTotalScore, sound_on

    # Create the main window
    window = tk.Tk()
    window.title("Math Chase")
    window.state('zoomed')
    window.size()
    window.configure(bg="#ffffff")
    background_image = tk.PhotoImage(file="game-background-4956017_960_720.png")

    # Create a Canvas
    canvas = Canvas(window, width=window.winfo_width(), height=window.winfo_height())
    canvas.pack(fill=BOTH, expand=True)

    # Add Image inside the Canvas
    canvas.create_image(0, 0, image=background_image, anchor='nw')

    # Create Labels
    score_array_text = tk.Label(window, text="Score Array", bg="#2ed573", fg="white",
                                font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                relief="solid")
    subtract_array_text = tk.Label(window, text="Subtraction Array", bg="#ff4757", fg="white",
                                   font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                   relief="solid")

    player_label = tk.Label(window, text="Current player: " + current_player, bg="#f8f9fa", fg="#495057",
                            font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                            relief="solid")
    player_label.place(relx=0.019, rely=0.1, anchor="w")

    p1_score_label = tk.Label(window, bg="#e056fd", fg="white", font=("8514oem", 14, "bold"),
                              padx=10, pady=15, bd=1, relief="solid")
    p1_score_label.place(relx=0.019, rely=0.25, anchor="w")

    p2_score_label = tk.Label(window, bg="#eccc68", fg="white", font=("8514oem", 14, "bold"),
                              padx=10, pady=25, bd=1, relief="solid")
    p2_score_label.place(relx=0.019 + .17, rely=0.25, anchor="w")

    ai_score_label = tk.Label(window, bg="#eccc68", fg="white", font=("8514oem", 14, "bold"),
                              padx=10, pady=15, bd=1, relief="solid")
    ai_score_label.place(relx=0.019 + .17 + .17, rely=0.25, anchor="w")

    game_over_label = tk.Label(window, bg="#f8f9fa", fg="#495057",
                               font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                               relief="solid")

    # Create buttons
    score_buttons = []
    subtraction_buttons = []
    score_selected = False



    # Current player selection
    select_current_player = tk.Label(window, text="Select first player", bg="white", fg="#2d3436",
                                     font=("8514oem", 14, "bold"), padx=15, pady=8, bd=1,
                                     relief="solid")
    select_current_player.place(relx=.5, rely=0.6, anchor="center")

    buttonFirstPlayer = Button(text="Player 1", command=lambda: save_current_player("Player 1"))
    create_button(buttonFirstPlayer, "#27ae60", 25)
    buttonFirstPlayer.place(relx=.5 - .078, rely=.7, anchor="center")

    buttonSecondPlayer = Button(text="Player 2", command=lambda: save_current_player("Player 2"))
    create_button(buttonSecondPlayer, "#f39c12", 25)
    buttonSecondPlayer.place(relx=.5, rely=.7, anchor="center")

    buttonAI = Button(text="AI", command=lambda: save_current_player("AI"))
    create_button(buttonAI, "#e74c3c", 25)
    buttonAI.place(relx=.5 + .078, rely=.7, anchor="center")

    # Level selection
    select_level = tk.Label(window, text="Select Level", bg="white", fg="#2d3436",
                            font=("8514oem", 14, "bold"), padx=15, pady=8, bd=1,
                            relief="solid")
    select_level.place(relx=.5, rely=0.40, anchor="center")

    buttonEasy = Button(text="Easy", command=lambda: save_difficulty("Easy"))
    create_button(buttonEasy, "#27ae60", 15)
    buttonEasy.place(relx=.5 - .078, rely=.5, anchor="center")

    buttonMedium = Button(text="Medium", command=lambda: save_difficulty("Medium"))
    create_button(buttonMedium, "#f39c12", 15)
    buttonMedium.place(relx=.5, rely=.5, anchor="center")

    buttonHard = Button(text="Hard", command=lambda: save_difficulty("Hard"))
    create_button(buttonHard, "#e74c3c", 15)
    buttonHard.place(relx=.5 + .078, rely=.5, anchor="center")

    # Initialize game state
    game_state = copy.deepcopy(score_array)
    subtraction_state = copy.deepcopy(subtraction_array)
    selected = [False] * len(score_array)
    selectedSub = [False] * len(subtraction_array)

    humanTotalScore1 = 0
    humanTotalScore2 = 0
    aiTotalScore = 0

    # Initialize mixer for sound playback
    mixer.init()

    # Load the sound icons and reduce their size by 20 pixels
    sound_icon = tk.PhotoImage(file="sound_on.png").subsample(18)
    mute_icon = tk.PhotoImage(file="sound_off.png").subsample(18)

    # Set initial sound state
    sound_on = True

    # Create the sound button
    sound_button_image = sound_icon  # Store a reference to the image object
    sound_button = tk.Button(window, image=sound_button_image, command=toggle_sound, bg="black")
    sound_button.place(relx=window.winfo_width() - .10, rely=0.05, anchor="ne")

    # Start the game with Player 1
    gameOpenningSound()
    update_scores()

    window.mainloop()

# Global variables
size = 9  # Adjust the size according to your needs
min_value = -50
max_value = 55

score_array = [random.randint(min_value, max_value) for _ in range(size)]
subtraction_array = [random.randint(min_value, max_value) for _ in range(size)]
front_window()  # Start the game with the front window
