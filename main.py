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
def ret1():
    return main.to_draw


@app.route("/get_sliders")
def ret2():
    return main.model.sliders


@app.route("/get_kinetic")
def ret3():
    return str(main.model.get_kinetic_energy())


@app.route("/get_potential")
def ret4():
    return str(main.model.full_energy)


@app.route("/speed_graph")
def ret5():
    a = ""
    sh = main.model.log["speed"]
    for i in range(main.model.time):
        a += str((sh["x"][i]**2 + sh["y"][i]**2)**0.5 * sh["x"][i] / abs(sh["x"][i])) + " "
    return a


@app.route('/event', methods=["POST"])
#@cross_origin(supports_credentials=True)
def pst():
    main.handle_event(request.data.decode('ascii'))
    return "succ"


class Main:
    def __init__(self, tickrate=150):
        #self.turtle = turtle.Turtle()
        #self.turtle.shape("circle")
        self.animator = Animator()
        self.vectors = []
        self.tickrate = tickrate
        self.paused = True
        self.to_draw = ""
        self.model = None

    def handle_event(self, event):
        if event == "pause":
            self.paused = not self.paused
        elif event == "only_pause":
            self.paused = True
        elif event.startswith("slider"):
            parsed = event.split(" ")
            print(parsed)
            bar = getattr(self.model, parsed[1])
            bar(float(parsed[2]))

    def set_timeout(self):
        self.timer = threading.Timer(1 / self.tickrate, self.tick_move, args=None, kwargs=None)
        self.timer.start()

    def tick_move(self):
        if not self.paused:
            for i in self.vectors:
                i.tick_move()
                #i.draw(self.turtle)
        self.to_draw = self.model.draw(self.animator)
        self.set_timeout()

    # def run(self):
    #     while not self.stopped.wait(0.5):
    #         print("my thread")
    #         # call a function

    def add_model(self, model):
        self.vectors.extend(model.get_working_vectors())
        self.model = model


class Animator:
    def __init__(self):
        """circle = 0"""
        """line = 1"""
        pass

    def circle(self, x, y, radius, width, color):
        return f"0 {x} {y} {radius} {width} {color};"

    def line(self, x1, y1, x2, y2, width, color):
        return f"1 {x1} {y1} {x2} {y2} {width} {color};"


if __name__ == "__main__":
    PENDULUM = Pendulum()
    main = Main()
    main.add_model(PENDULUM)
    main.set_timeout()
    print(PENDULUM.get_potential_energy())
    print(PENDULUM.get_kinetic_energy())
    print(PENDULUM.full_energy)
    app.run(host='0.0.0.0', debug=True)
