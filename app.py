"""import random

jackpot = random.randint(1, 100)

guess = int(input("Guess kro :"))
count = 1

while(guess != jackpot):
    if (guess > jackpot):
        print(' Galat, guess kiya higher')
    else:
        print('Galat, guess kiya lower')

    guess = int(input("Guess kro :"))

    count += 1

else:
    print(f'correct guess attempts in {count}')"""

# Flask se required functions import kar rahe hain
from flask import Flask, render_template, request, session

# Random number generate karne ke liye random module
import random


# Flask application create kar rahe hain
app = Flask(__name__)


# Flask session ko secure/sign karne ke liye secret key
# Production project mein ise environment variable mein rakhna better hai
app.secret_key = "number-game-secret-key"


# NEW GAME FUNCTION


def start_new_game():

    # 1 se 100 ke beech random number generate
    # Ye hi user ko guess karna hai
    session["jackpot"] = random.randint(1, 100)

    # Starting attempts = 0
    session["attempts"] = 0

    # Starting score = 100
    session["score"] = 100

    # Starting message
    session["message"] = "Start guessing!"

    # Game abhi complete nahi hua
    session["game_over"] = False



# HOME ROUTE


# "/" ka matlab website ka home page
#
# methods=["GET", "POST"]
# GET  -> page open karne ke liye
# POST -> form submit karne ke liye

@app.route("/", methods=["GET", "POST"])
def home():

    # CHECK: Kya user ka game already bana hai?


    # Agar session mein jackpot nahi hai,
    # iska matlab ye new user/game hai
    if "jackpot" not in session:

        # New game start karo
        start_new_game()


   
   
    # FORM SUBMIT CHECK

    # Agar user ne form submit kiya hai
    if request.method == "POST":

        # Form se "action" ki value lekar aa rahe hain
        #
        # Guess button:
        # action = "guess"
        #
        # New Game button:
        # action = "restart"

        action = request.form.get("action")


        # NEW GAME

        if action == "restart":

            # Purana game reset karo
            start_new_game()


        
        # USER GUESS


        elif action == "guess" and not session["game_over"]:

            # HTML input se user ka guess le rahe hain
            #
            # request.form se value string mein milti hai
            # isliye int() se integer mein convert kar rahe hain

            guess = int(request.form["guess"])


            # Har valid guess par attempts +1
            session["attempts"] += 1


            # Session mein stored secret number
            jackpot = session["jackpot"]


            # GUESS TOO HIGH

            if guess > jackpot:

                # Wrong guess hone par 10 points minus
                session["score"] = max(
                    0,
                    session["score"] - 10
                )

                # User ko message
                session["message"] = (
                    " Too High! Try a lower number."
                )

            # GUESS TOO LOW
           

            elif guess < jackpot:

                # Wrong guess hone par 10 points minus
                session["score"] = max(
                    0,
                    session["score"] - 10
                )

                # User ko message
                session["message"] = (
                    " Too Low! Try a higher number."
                )


            # CORRECT GUESS
           
            else:

                # User ne correct number guess kar liya
                session["message"] = (
                    f"Correct! You guessed it in "
                    f"{session['attempts']} attempts!"
                )

                # Game finish
                session["game_over"] = True


    
    # HTML PAGE RENDER
   
    # index.html ko browser mein send kar rahe hain
    #
    # Python variables HTML mein available honge:
    #
    # attempts
    # score
    # message
    # game_over

    return render_template(
        "index.html",

        attempts=session["attempts"],

        score=session["score"],

        message=session["message"],

        game_over=session["game_over"]
    )



# RUN APPLICATION


# Ye code tabhi chalega jab app.py directly run hoga
if __name__ == "__main__":

    # Local computer par Flask server start
    app.run(debug=True)