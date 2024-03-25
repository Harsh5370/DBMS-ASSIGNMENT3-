from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Sample User Data
user_data = {
    "shubham.kshirsagar@iitgn.ac.in": "password"
}

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("username")
    password = request.form.get("pswrd")

    if email in user_data and user_data[email] == password:
        return """
        <script>
        alert("Login Successful");
        window.location.href = "{}";
        </script>
        """.format(url_for("outlet_management"))
    else:
        return """
        <script>
        alert("Login Failed");
        window.location.href = "/";
        </script>
        """

@app.route("/outlet_management")
def outlet_management():
    return render_template("outlet_management.html")

if __name__ == "__main__":
    app.run(debug=True)