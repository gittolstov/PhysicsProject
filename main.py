from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_cors import CORS, cross_origin
from pendulum import *
from log_parser import *
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
    def __init__(self, tickrate=100):
        self.model_list = {
            "Pendulum": Pendulum
        }
        self.animator = Animator()
        self.vectors = []
        self.tickrate = tickrate
        self.paused = True
        self.playingback = False
        self.recording = {
            "object": {},
            "frame": 0
        }
        self.to_draw = ""
        self.model = None

    def handle_event(self, event):
        if event == "pause":
            self.paused = not self.paused
        elif event == "only_pause":
            self.paused = True
        elif event == "log_animation":
            parser.save("testlog2", self.model.log)
        elif event == "play_animation":
            print("started")
            self.load_playback("testlog2")
        elif event.startswith("slider"):
            parsed = event.split(" ")
            print(parsed)
            bar = getattr(self.model, parsed[1])
            bar(float(parsed[2]))

    def set_timeout(self):#should be in every model
        self.timer = threading.Timer(1 / self.tickrate, self.tick_move, args=None, kwargs=None)
        self.timer.start()

    def tick_move(self):
        if not self.paused:
            if self.playingback:
                self.playback_frame()
            else:
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

    def add_model_byname(self, model_name):
        a = self.model_list[model_name]()
        self.vectors.extend(a.get_working_vectors())
        self.model = a

    def start_playback(self, dct):
        self.playingback = True
        self.recording["object"] = dct
        self.recording["frame"] = 0

    def playback_frame(self):
        self.recording["frame"] += 1
        print(self.recording["frame"])
        self.model.apply_log(self.recording["object"], self.recording["frame"])

    def load_playback(self, name):
        self.start_playback(parser.fetch(name))


class Animator:
    def __init__(self):
        """circle = 0"""
        """line = 1"""
        """vector = 2"""
        pass

    def circle(self, x, y, radius, width, color):
        return f"0 {x} {y} {radius} {width} {color};"

    def line(self, x1, y1, x2, y2, width, color):
        return f"1 {x1} {y1} {x2} {y2} {width} {color};"

    def vector(self, x1, y1, x2, y2, width, color):
        return f"2 {x1} {y1} {x2} {y2} {width} {color};"


if __name__ == "__main__":
    PENDULUM = Pendulum()
    main = Main()
    parser = Log_parser()
    main.add_model(PENDULUM)
    main.set_timeout()
    print(PENDULUM.get_potential_energy())
    print(PENDULUM.get_kinetic_energy())
    print(PENDULUM.full_energy)
    app.run(host='0.0.0.0', debug=True)
