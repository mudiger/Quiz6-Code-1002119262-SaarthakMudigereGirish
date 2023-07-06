from flask import Flask, render_template, request

app = Flask(__name__)

rooms = {}


class Game:
    def __init__(self):
        self.piles = []
        self.players = []
        self.current_player = None
        self.min_stones = None
        self.max_stones = None
        self.cumulative_scores = {}  # Dictionary to store cumulative scores

    def add_player(self, player_name):
        self.players.append(player_name)
        self.cumulative_scores[player_name] = 0  # Initialize cumulative score for the player

    def judge_values(self, min_stones, max_stones, x, y, z):
        self.min_stones = min_stones
        self.max_stones = max_stones
        self.piles = [x, y, z]

    def start_game(self):
        self.current_player = self.players[0]

    def pick_stones(self, pile_index, num_stones):
        if self.is_game_over():
            return "Game over. Please start a new game."

        pile_size = self.piles[pile_index - 1]
        if num_stones < self.min_stones or num_stones > self.max_stones:
            return "Invalid number of stones. Please pick between {} and {} stones.".format(
                self.min_stones, self.max_stones)
        if num_stones > pile_size:
            return "Not enough stones in the pile. Please pick a smaller number."

        self.piles[pile_index - 1] -= num_stones
        self.cumulative_scores[self.current_player] += num_stones  # Add picked stones to the cumulative score
        self.current_player = self.get_next_player()

        return None

    def is_game_over(self):
        return all(pile == 0 for pile in self.piles)

    def get_next_player(self):
        current_player_index = self.players.index(self.current_player)
        next_player_index = (current_player_index + 1) % len(self.players)
        return self.players[next_player_index]

    def get_scores(self):
        return self.cumulative_scores

    def single_scores(self):
        return max(self.cumulative_scores.values())


game = Game()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route('/pick_stones', methods=['POST'])
def pick_stones():
    pile_index = int(request.form['pile_index'])
    num_stones = int(request.form['num_stones'])

    error_message = game.pick_stones(pile_index, num_stones)

    return render_template('player1.html', game=game, error_message=error_message)


@app.route("/judge", methods=["POST", "GET"])
def judge():
    if request.method == "POST":
        min_stones = int(request.form['min'])
        max_stones = int(request.form['max'])
        x = int(request.form['x'])
        y = int(request.form['y'])
        z = int(request.form['z'])
        game.judge_values(min_stones, max_stones, x, y, z)
    return render_template("judge.html", game=game)


@app.route("/player1", methods=["POST", "GET"])
def player1():
    player1 = ""
    if request.method == "POST":
        player1 = request.form['player1']
        game.add_player(player1)
        game.start_game()
    return render_template("player1.html", game=game, player1=player1)


@app.route("/player2", methods=["POST", "GET"])
def player2():
    if request.method == "POST":
        player2 = request.form['player2']
        game.add_player(player2)
        game.start_game()
    return render_template("player2.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)
