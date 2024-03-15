from flask import Flask, render_template, request, redirect, flash, url_for, session


app = Flask(__name__)
app.secret_key = "Jxtym_ctrhtnysq_rk.x_cghznfyysq_jn_dim-akim"


@app.route("/")
def pend():
    return render_template("Simulation.html")


@app.route("/get_data")
def ret():
    return {"funni_json": "very coplex and intriguing string which is contained inside a sent json object"}


@app.route('/fetch_visuals', methods=["POST"])
def login():
    print(request)
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
