from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session,jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def start():
    """Render start page, ask what size board player wants"""
    return render_template('start.html')

@app.route('/home')
def home_page():
    """take board size from start page and create board"""
    """check that board is an appropriate size"""
    """store curernt board in session"""
    size = int(request.args["board-size"])
    if size < 3 or size >15:
        flash('Please pick a number between 3 and 15', 'error')
        return redirect('/')

    board = boggle_game.make_board(size)
    session['board'] = board 
    highscore = session.get("highscore", 0)
    return render_template('base.html', board=board)

@app.route('/check-word')
def check_word():
    """take baord and word and pass to boggle_game method to check word"""
    """return json for our ajax request made in our js file"""
    word = request.args["words"]
    board = session['board']
    resp = boggle_game.check_valid_word(board, word)
    return jsonify({'server' : resp})


@app.route('/score', methods=["POST"])
def score():
    """take incoming score data from our js file, return score, highscore and games played as json"""
    score = request.json["scores"]
    highscore = session.get("highscore", 0)
    gamesplayed = session.get("games", 0)
    if score > highscore:
        highscore = score
        session['highscore'] = highscore
    session["games"] = gamesplayed + 1
    return jsonify({"score" : score, "highscore" : highscore, "games": gamesplayed})
    