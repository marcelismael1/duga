from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("dashboard.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/alerts')
def alerts():
    return render_template("alerts.html")

@app.route('/configurations')
def configurations():
    return render_template("configurations.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)