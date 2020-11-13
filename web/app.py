from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

# Static Data
headings = ("System IP","DATE", "CVE NO", "SEVERITY", "AFFECTED PACKAGES", "PACKAGE NUMBER")

data = (
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),

	)

SOFAlarms = [300,50,100,200]
Totalseverity = [600,50,100,200]

# Main route
@app.route('/')
def main():
    return dashboard()

# dashboards endpoint
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", headings=headings, data=data, SOFAlarms=SOFAlarms, Totalseverity=Totalseverity)

# alerts endpoint
@app.route('/alerts')
def alerts():
    return render_template("alerts.html", headings=headings, data=data)

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