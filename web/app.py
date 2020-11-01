from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

# Main route
@app.route('/')
def main():
    return render_template("dashboard.html")

# dashboards endpoint
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# alerts endpoint
@app.route('/alerts')
def alerts():
    return render_template("alerts.html")

# Config endpoint
@app.route('/configurations')
def configurations():
    return render_template("configurations.html")

# about endpoint
@app.route('/about')
def about():
    return render_template("about.html")

# default route
@app.route('/<name>')
def default_route(name):
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)