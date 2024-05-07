from flask import Flask, render_template, request, redirect, flash, url_for, session
#from flask_cors import CORS, cross_origin
from pendulum import *
import threading
import turtle


app = Flask(__name__)
app.secret_key = "Jxtym_ctrhtnysq_rk.x_cghznfyysq_jn_dim-akim"
#CORS(app, support_credentials=True)


@app.route("/")
def pend():
    return render_template("Simulation.html")


@app.route("/get_data")
def ret():
    return main.to_draw


@app.route('/fetch_visuals', methods=["POST"])
#@cross_origin(supports_credentials=True)
def login():
    print(request)
    return "succ"


class Main:
    def __init__(self, tickrate=50):
        #self.turtle = turtle.Turtle()
        #self.turtle.shape("circle")
        self.animator = Animator()
        self.vectors = []
        self.tickrate = tickrate
        self.to_draw = ""
        self.model = None

    def set_timeout(self):
        self.timer = threading.Timer(1 / self.tickrate, self.tick_move, args=None, kwargs=None)
        self.timer.start()

    def tick_move(self):
        for i in self.vectors:
            i.tick_move()
            #i.draw(self.turtle)
        self.set_timeout()
        self.to_draw = self.model.draw(self.animator)

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function

    def add_model(self, model):
        self.vectors.extend(model.get_working_vectors())
        self.model = model


class Animator:
    def __init__(self):
        """circle = 0"""
        """line = 1"""
        pass

    def circle(self, x, y, radius):
        return f"0 {x} {y} {radius};"

    def line(self, x1, y1, x2, y2):
        return f"1 {x1} {y1} {x2} {y2};"


if __name__ == "__main__":
    PENDULUM = Pendulum()
    main = Main()
    main.add_model(PENDULUM)
    main.set_timeout()
    app.run(host='0.0.0.0', debug=True)
