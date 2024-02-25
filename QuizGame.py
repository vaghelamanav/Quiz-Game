import subprocess
import time

def main():
    print("Welcome to the Quiz Launcher!")

    while True:
        play_quiz = input("Do you want to play the quiz? (yes/no): ").lower()

        if play_quiz == "yes":
            print("Get ready! The quiz will start in 3 seconds.")
            
            # Add a 3-second timer
            time.sleep(3)

            quiz_file = "game18.py"
            subprocess.run(["python", quiz_file])

            break

        elif play_quiz == "no":
            print("Okay, maybe next time.")
            break

        else:
            print("Please just say 'yes' or 'no'.")

if __name__ == "__main__":
    main()
