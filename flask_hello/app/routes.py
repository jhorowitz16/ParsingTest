from flask import render_template
from app import app
import csv
from random import random

totals = [0, 0]
score = [0, 0]


@app.route('/')
@app.route('/index')
def index():
    data = select_random()
    return render_template(
        'index.html', title='Guess the Message', data=data, score=get_score())


@app.route('/w')
@app.route('/W')
def index_w():
    rand_message = select_random(W_rows)
    return render_template(
        'index.html', title='W Only', msg=rand_message, score=get_score())


@app.route('/J')
@app.route('/j')
def index_j():
    rand_message = select_random(J_rows)
    return render_template(
        'index.html', title='J Only', msg=rand_message, score=get_score())


@app.route('/greeting/<name>')
def give_greeting(name):
    return 'Hello, {0}!'.format(name)





def read_csv(person):
    filename = 'app/static/' + person + '_unique_words.csv'
    rows = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            rows.append(row)
    return rows


def select_random(rows=None):
    """
    select a random message from the set
    draw a random row, then a random message in that row
    might not be completely uniform if the last row doesn't have 10
    """
    print(totals)
    if not rows:
        if (int)(2 * random()):
            rows, answer = J_rows, "J"
            totals[0] += 1
        else:
            rows, answer = W_rows, "W"
            totals[1] += 1

    idx = (int) (len(rows) * random())
    row = rows[idx]
    row_idx = (int) (random() * 10)
    message = row[row_idx]
    print(message + ' ||| ' + str(idx) + ' ' + str(row_idx) + ' ' + answer)
    return {
        'message': message,
        'answer': answer
    }


def get_score():
    """
    return the string version of the score
    0 out of 0 is the default
    correct ouf of total questions
    """
    if sum(score) == 0:
        return "N/A"
    else:
        return str(score[0]) + " correct out of " + str(score[1])


J_rows = read_csv('J')
W_rows = read_csv('W')
