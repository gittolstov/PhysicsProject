from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_cors import CORS, cross_origin
from pendulum import *
import threading
import turtle


app = Flask(__name__)
app.secret_key = "Jxtym_ctrhtnysq_rk.x_cghznfyysq_jn_dim-akim"
CORS(app, support_credentials=True)


@app.route("/")
def pend():
    return render_template("Simulation.html")


@app.route("/get_data")
def ret():
    return {"funni_json": "very coplex and intriguing string which is contained inside a sent json object"}


@app.route('/fetch_visuals', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    print(request)
    return "succ"


class Main:
    def __init__(self, tickrate=50):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.vectors = []
        self.tickrate = tickrate

    def set_timeout(self):
        self.timer = threading.Timer(1 / self.tickrate, self.tick_move, args=None, kwargs=None)
        self.timer.start()

    def tick_move(self):
        for i in self.vectors:
            i.tick_move()
            i.draw(self.turtle)
        self.set_timeout()

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function


if __name__ == "__main__":
    PENDULUM = Pendulum()
    main = Main()
    main.vectors.extend(PENDULUM.get_working_vectors())
    main.set_timeout()
    # app.run(host='0.0.0.0', debug=True)
