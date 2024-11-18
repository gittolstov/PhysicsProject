from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_cors import CORS, cross_origin
from pendulum import *
from cosmic_velocity import Cosmic_velocity
from electromagnetic_oscillations import Oscillations
from optic import Optic
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
    return str(main.model.time) + ";" + main.model.sliders


@app.route("/get_kinetic")
def ret3():
    return str(main.model.get_kinetic_energy())


@app.route("/get_potential")
def ret4():
    return str(main.model.full_energy)


@app.route("/graph/<number>")
def ret5(number):
    data = []
    for i in number:
        data.append(" ".join(main.model.get_graph(i)))
    return ";".join(data)


@app.route("/request_sliders")
def ret6():
    text = ""
    for i in range(len(main.model.setters_and_getters["setters"])):
        text += main.model.setters_and_getters["setters"][i] + "/"
        text += main.model.setters_and_getters["getters"][i] + "/"
        text += main.model.setters_and_getters["names"][i] + "/"
        text += main.model.setters_and_getters["modifiers"][i] + "/"
        text += main.model.setters_and_getters["shifts"][i] + ";"
    return text[:-1]


@app.route("/playback_names")
def ret7():
    return "\n".join(parser.readfile()[0])


@app.route("/energy")
def ret8():
    return str(main.model.get_kinetic()) + str(main.model.get_potential())


@app.route("/click/<point>")
def ret9(point):
    data = point.split("_")
    main.model.react_click(float(data[0]), float(data[1]))
    return ";".join(data)


@app.route('/event', methods=["POST"])
#@cross_origin(supports_credentials=True)
def pst():
    main.handle_event(request.data.decode('ascii'))
    return "succ"


class Main:
    def __init__(self, tickrate=100):
        print("MAIN PROCESS IS RUNNING")
        self.model_list = {
            "Pendulum": PENDULUM,
            "Cosmic_velocity": COSMIC,
            "Oscillations": ELECTRO,
            "Optic": OPTIC
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
        self.animatimer = 0
        self.model = None

    def handle_event(self, event):
        if event == "pause":
            self.pause()
        elif event == "only_pause":
            self.paused = True
        elif event == "model_pendulum":
            self.end_playback()
            self.reset_model(PENDULUM)
        elif event == "model_cosmic":
            self.end_playback()
            self.reset_model(COSMIC)
        elif event == "model_electro":
            self.end_playback()
            self.reset_model(ELECTRO)
        elif event == "model_optic":
            self.end_playback()
            self.reset_model(OPTIC)
        elif event == "reset":
            self.end_playback()
            self.model.reset()
            self.vectors = self.model.get_working_vectors()
        elif event == "playforth":
            self.end_playback()
        elif event.startswith("slider"):
            parsed = event.split(" ")
            bar = getattr(self.model, parsed[1])
            bar(float(parsed[2]))
        elif event.startswith("recording"):
            parsed = event.split(" ")
            self.load_playback(parsed[1])
        elif event.startswith("rewind"):
            parsed = event.split(" ")
            self.rewind(int(parsed[1]))
        elif event.startswith("save_record"):
            parsed = event.split(" ")
            parser.save(parsed[1], self.model.log)
            self.end_playback()
            self.model.reset()
            self.vectors = self.model.get_working_vectors()

    def pause(self):
            self.paused = not self.paused

    def set_timeout(self):
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
        self.to_draw = self.model.draw(self.animator) + self.animator.pause(int(self.paused))
        self.to_draw += self.animator.playing_back(30, 30, 5, "10", "red", 1 * self.animatimer % 80 >= 40, self.playingback)
        self.animatimer += 1
        self.set_timeout()

    # def run(self):
    #     while not self.stopped.wait(0.5):
    #         print("my thread")
    #         # call a function

    def rewind(self, frame):
        ln = 0
        for i in self.model.log["self"]:
            ln = len(self.model.log["self"][i])
            break
        if self.playingback:
            length = 0
            for i in self.recording["object"]["self"]:
                length = len(self.recording["object"]["self"][i])
            if frame < length:
                self.model.apply_log(self.recording["object"], frame)
                self.recording['frame'] = frame
        elif frame < ln:
            self.model.time = frame
            self.model.apply_log(self.model.log, frame)

    def reset_model(self, model):
        model.reset()
        self.add_model(model)

    def add_model(self, model):
        self.vectors = model.get_working_vectors()
        self.model = model
        self.model.main = self

    def add_model_byname(self, model_name):
        a = self.model_list[model_name]
        self.vectors = a.get_working_vectors()
        self.model = a
        self.model.main = self

    def start_playback(self, dct):
        self.playingback = True
        self.add_model_byname(dct["simulation_type"])
        self.recording["object"] = dct
        self.recording["frame"] = 0
        add_to_log(self.model.log, dct)

    def end_playback(self):
        self.playingback = False

    def playback_frame(self):
        self.recording["frame"] += 1
        #print(self.recording["frame"])
        self.model.apply_log(self.recording["object"], self.recording["frame"])

    def load_playback(self, name):
        self.start_playback(parser.fetch(name))


class Animator:
    def __init__(self):
        """circle = 0"""
        """line = 1"""
        """vector = 2"""
        """scheme = 3"""
        """pause = 4"""
        """playback = 5"""
        """planet = 6"""
        """ship = 7"""
        """pendulum = 8"""
        """explosion = 9"""
        """semicircle = 10"""
        """laserpointer = 11"""
        """angle = 12"""
        pass

    def circle(self, x, y, radius, width, color):
        return f"0 {x} {y} {radius} {width} {color};"

    def line(self, x1, y1, x2, y2, width, color):
        return f"1 {x1} {y1} {x2} {y2} {width} {color};"

    def vector(self, x1, y1, x2, y2, width, color):
        return f"2 {x1} {y1} {x2} {y2} {width} {color};"

    def scheme(self):
        return "3;"

    def pause(self, paused):
        return f"4 {paused};"

    def playing_back(self, x, y, radius, width, color, on, playback):
        return f"0 {x} {y} {radius} {width} {color};" * (on and playback) + f"5 " + "1" * playback + "0" * (not playback) + ";"

    def planet(self, x, y, radius):
        return f"6 {x} {y} {radius};"

    def ship(self, x, y, x2, y2):
        return f"7 {x} {y} {x2} {y2};"

    def pendulum(self, x, y, rad):
        return f"8 {x} {y} {rad};"

    def ship_boom(self, x, y, x2, y2, frame):
        return f"9 {x} {y} {x2} {y2} {frame};"

    def semicircle(self, x, y, radius, beginning, contrast):
        return f"10 {x} {y} {radius} {beginning} {contrast};"

    def laserpointer(self, x, y, angle, size):
        return f"11 {x} {y} {angle} {size};"

    def angle(self, x, y, size):
        return f"12 {x} {y} {size};"


if __name__ == "__main__":
    PENDULUM = Pendulum()
    COSMIC = Cosmic_velocity()
    ELECTRO = Oscillations()
    OPTIC = Optic()
    main = Main()
    parser = Log_parser()
    main.add_model(ELECTRO)
    main.set_timeout()
    app.run(host='0.0.0.0', debug=False)
