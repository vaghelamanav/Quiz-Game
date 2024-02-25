import pygame
import sys
import pandas as pd

pygame.init()

# Set up display
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
mylogo = pygame.image.load('mylogo.png')
pygame.display.set_caption("Quiz Game")
pygame.display.set_icon(mylogo)

# Load background image
background_image = pygame.image.load("download.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load questions from Excel file
def load_questions(file_path):
    df = pd.read_excel(file_path)
    questions_list = []
    for index, row in df.iterrows():
        question = {
            "question": row["Question"],
            "choices": [row["Choice1"], row["Choice2"], row["Choice3"], row["Choice4"]],
            "correct_choice": row["CorrectChoice"],
        }
        questions_list.append(question)
    return questions_list

# Load questions from Excel file
questions = load_questions("Book1.xlsx")

# Game variables
current_question = 0
score = 0
quiz_over = False  # Flag to track if the quiz is over

# Home screen loop
home_screen = True
while home_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            home_screen = False

    # Display the home screen
    screen.blit(background_image, (0, 0))
    start_text = pygame.font.SysFont("poppins", 50).render("Click anywhere to start the quiz!", True, BLACK)
    screen.blit(start_text, (width // 3 - 200, height // 2 - 25))
    pygame.display.flip()
    pygame.time.Clock().tick(30)

question_font = pygame.font.SysFont("poppins", 58)
button_font = pygame.font.SysFont("poppins", 42)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not quiz_over:
                # Check if mouse click is within the choice area
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 50 < mouse_x < 750 and 150 < mouse_y < 450:
                    selected_choice = (mouse_y - 150) // 50
                    if 0 <= selected_choice < len(questions[current_question]["choices"]):  # Check if selected choice index is valid
                        if (
                            questions[current_question]["choices"][selected_choice]
                            == questions[current_question]["correct_choice"]
                        ):
                            score += 1

                        # Move to the next question
                        current_question += 1

                        # Check if all questions have been answered
                        if current_question == len(questions):
                            quiz_over = True

    # Check if current_question is within the valid range
    if 0 <= current_question < len(questions):
        # Display the current question in a box
        screen.blit(background_image, (0, 0))
        question_text = question_font.render(
            questions[current_question]["question"], True, BLACK
        )
        screen.blit(question_text, (70, 70))

        # Display choices
        choice_y = 150
        for i, choice in enumerate(questions[current_question]["choices"]):
            choice_color = GREEN if i == questions[current_question]["correct_choice"] else BLACK
            choice_text = button_font.render(choice, True, choice_color)
            screen.blit(choice_text, (70, choice_y + i * 50))

        # Update the display
        pygame.display.flip()

        # Control the game speed
        pygame.time.Clock().tick(30)

    # Check if all questions have been answered
    if quiz_over:
        # Display the final score and "Game Over" message
        game_over_text = question_font.render("Game Over", True, RED)

        text_width, text_height = question_font.size("Game Over")
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        screen.blit(game_over_text, (text_x, text_y))

        # Wait for a few seconds before showing the score
        pygame.time.delay(1000)

        print(f"Your final score: {score}/{len(questions)}")

        # Print additional message and score
        if score == len(questions):
            print("Congratulations! You answered all questions correctly!")
        elif score >= len(questions) * 0.6:
            print("Well done! You passed the quiz!")
        else:
            print("Better luck next time.")

        # Ask if the user wants to see the correct answers
        answer_prompt_text = "Do you want to see the correct answers? (yes/no): "
        answer = input(answer_prompt_text).lower()
        if answer == "yes":
            print("Correct answers:")
            for i, question in enumerate(questions):
                print(f"{i + 1}. {question['correct_choice']}")

        # Quit the game
        pygame.quit()
        sys.exit()
