from flask import Flask, render_template, request

app = Flask(__name__)

rooms = {}
question = ""
answer = ""

class Game:
    def __init__(self):
        self.players = []
        self.cumulative_scores = {}  # Dictionary to store cumulative scores
        self.question = None
        self.answer = None
        self.answer1 = None
        self.answer2 = None

    def add_player(self, player_name):
        self.players.append(player_name)
        self.cumulative_scores[player_name] = 0  # Initialize cumulative score for the player

    def judge_values(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer1(self, answer1):
        self.answer1 = answer1
        if self.answer == self.answer1:
            print("OK")
            self.cumulative_scores[self.players[0]] += 1
        else:
            print("NO")
            self.cumulative_scores[self.players[0]] -= 2

    def check_answer2(self, answer2):
        self.answer2 = answer2
        if self.answer == self.answer2:
            print("OK")
            self.cumulative_scores[self.players[1]] += 1
        else:
            print("NO")
            self.cumulative_scores[self.players[1]] -= 2

    # def is_game_over(self):
    #     return all(pile == 0 for pile in self.piles)

    def get_scores(self):
        return self.cumulative_scores


game = Game()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route('/check_answer1', methods=['POST'])
def check_answer1():
    answer1 = request.form['answer1']
    game.check_answer1(answer1)
    return render_template('player1.html', game=game)


@app.route('/check_answer2', methods=['POST'])
def check_answer2():
    answer2 = request.form['answer2']
    game.check_answer2(answer2)
    return render_template('player2.html', game=game)


@app.route("/judge", methods=["POST", "GET"])
def judge():
    global question
    if request.method == "POST":
        question = request.form['question']
        answer = request.form['answer']
        game.judge_values(question, answer)
    return render_template("judge.html", game=game)


@app.route("/player1", methods=["POST", "GET"])
def player1():
    player1 = ""
    if request.method == "POST":
        player1 = request.form['player1']
        game.add_player(player1)
        #game.start_game()
    return render_template("player1.html", game=game, player1=player1, question = question)


@app.route("/player2", methods=["POST", "GET"])
def player2():
    player2 = ""
    if request.method == "POST":
        player2 = request.form['player2']
        game.add_player(player2)
        #game.start_game()
    return render_template("player2.html", game=game, player2=player2, question = question)


if __name__ == "__main__":
    app.run(debug=True)


# A History Bee (HB) is a two player game with an additional person as the judge. We will call those P1, P2, and J.
#   The J gives ("sends") each player a question, such as "When was the war of 1812?" P1 and P2 try to respond as quickly as possible,
#   The J sees their responses (if any) and responds to each in time order (first one submitted, if correct, gets points, if not correct,
#   looks at the other player's submission, continue on for a maximum of 4 attempts, or as soon as one is correct.) The J gives feedback
#   to each responce (OK, NO), Each player gives their name at the start, and each player sees both names and the scores.
#   Each player starts with N points (set by J), and a correct answer score +1 point, an incorrect answer -2 points)
#   To ensure that the game is fair, all questions and responses are logged in a text window that only the J sees,
#   each line (entry) in the format:
#   [time, originator] message text
#   for example:
#   [0, Joe] Where is the Alamo?
#   [12, Pat] In Dallas
#   [14, Judge] NO
#   [50, Penny] San Antonio
#   [51, Judge] OK
#   The time may either be in seconds since the game began, or the actual system time if you prefer. On the J screen show current time
#   in either format.
#   The J at anytime may restart the game.
