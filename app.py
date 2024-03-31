from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host
app.config['MYSQL_USER'] = 'root'   # MySQL username
app.config['MYSQL_PASSWORD'] = 'krish2092003'  # MySQL password
app.config['MYSQL_DB'] = 'outlet_management'  # MySQL database name

mysql = MySQL(app)

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
        alert("Login Successfully");
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

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/outlet_management", methods=['GET', 'POST'])
def outlet_management():
    cur = mysql.connection.cursor()
    
    # Check if it's a POST request to handle the search, otherwise display all records
    if request.method == 'POST':
        search_term = request.form['searchInput']
        query = f"SELECT Outlet_ID, Outlet_name, Location_name, Contact_No, timings, Ratings FROM Outlet WHERE Outlet_name LIKE '%{search_term}%'"
    else:
        query = "SELECT Outlet_ID, Outlet_name, Location_name, Contact_No, timings, Ratings FROM Outlet"
    cur.execute(query)
    outlets = cur.fetchall()  # Fetch all rows
    cur.close()
    return render_template("outlet_management.html", outlets=outlets)


@app.route("/stakeholder_details", methods=['GET', 'POST'])
def  stakeholder_details():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        search_term = request.form['searchInput']
        query  = f"SELECT * from stakeholder WHERE name LIKE '%{search_term}%'"
    else:
        query = "SELECT * FROM stakeholder"
    cur.execute(query)  # Adjust 'stakeholders' to your table name
    data = cur.fetchall()
    cur.close()
    return render_template("stakeholder_details.html", data=data)


@app.route("/inventory_details", methods=['GET', 'POST'])
def inventory_details():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        search_term = request.form['searchInput'].lower()  # Convert search term to lowercase
        query = """
        SELECT o.Outlet_name, i.Item_name, i.Price
        FROM Inventory i
        JOIN Outlet o ON i.Outlet_ID = o.Outlet_ID
        WHERE LOWER(i.Item_name) = %s  # Convert column data to lowercase for comparison
        """
        cur.execute(query, [search_term])
    else:
        query = """
        SELECT o.Outlet_name, i.Item_name, i.Price
        FROM Inventory i
        JOIN Outlet o ON i.Outlet_ID = o.Outlet_ID
        """
        cur.execute(query)

    items = cur.fetchall()
    cur.close()
    return render_template("Inventory.html", items=items)



@app.route("/employee_details", methods=['GET', 'POST'])
def employee_details():
    cur = mysql.connection.cursor()

    # Check if it's a POST request to handle the search, otherwise display all records
    if request.method == 'POST':
        search_term = request.form['searchInput']
        column_name = request.form['searchColumn']

        # Adjust the query to search for the specified column
        query = f"""
        SELECT o.Outlet_name, e.Employee_name, e.Role, e.Mobile_number, e.Shift_time
        FROM Employees e
        JOIN Outlet o ON e.Outlet_ID = o.Outlet_ID
        WHERE {column_name} LIKE %s
        """
        cur.execute(query, ['%' + search_term + '%'])
    else:
        query = """
        SELECT o.Outlet_name, e.Employee_name, e.Role, e.Mobile_number, e.Shift_time
        FROM Employees e
        JOIN Outlet o ON e.Outlet_ID = o.Outlet_ID
        """
        cur.execute(query)

    employees = cur.fetchall()
    cur.close()
    return render_template("employees_details.html", employees=employees)


@app.route("/Customer_feedback", methods=['GET', 'POST'])
def Customer_feedback():
    cur = mysql.connection.cursor()
    
    # Check if it's a POST request to handle the search, otherwise display all records
    if request.method == 'POST':
        search_term = request.form['searchInput'].lower()  # Convert search term to lowercase
        query = """
        SELECT o.Outlet_name, cf.Customer_email, cf.Customer_rating
        FROM Customer_feedback cf
        JOIN Outlet o ON cf.Outlet_ID = o.Outlet_ID
        WHERE LOWER(o.Outlet_name) = %s
        """
        cur.execute(query, [search_term])
    else:
        query = """
        SELECT o.Outlet_name, cf.Customer_email, cf.Customer_rating
        FROM Customer_feedback cf
        JOIN Outlet o ON cf.Outlet_ID = o.Outlet_ID
        """
        cur.execute(query)

    feedback_data = cur.fetchall()  # Fetch all rows of joined tables
    cur.close()
    return render_template("Customer_feedback.html", feedback_data=feedback_data)


@app.route("/Rent_details", methods=['GET', 'POST'])
def Rent_details():
    cur = mysql.connection.cursor()
    
    # Adjust the query based on whether it's a POST request (search operation) or not
    if request.method == 'POST':
        search_term = request.form['searchInput']
        query = """
        SELECT Rent_payment.Outlet_ID, Outlet.Outlet_name, Rent_payment.Mode_of_payment, 
               Rent_payment.Paid_amount, Rent_payment.Rent_from_date, Rent_payment.Rent_to_date, 
               Rent_payment.Due_amount
        FROM Rent_payment
        INNER JOIN Outlet ON Rent_payment.Outlet_ID = Outlet.Outlet_ID
        WHERE Outlet.Outlet_name LIKE %s
        """
        cur.execute(query, ['%' + search_term + '%'])
    else:
        query = """
        SELECT Rent_payment.Outlet_ID, Outlet.Outlet_name, Rent_payment.Mode_of_payment, 
               Rent_payment.Paid_amount, Rent_payment.Rent_from_date, Rent_payment.Rent_to_date, 
               Rent_payment.Due_amount
        FROM Rent_payment
        INNER JOIN Outlet ON Rent_payment.Outlet_ID = Outlet.Outlet_ID
        """
        cur.execute(query)
    
    rent_payments = cur.fetchall()
    cur.close()
    return render_template("Rent_payment.html", rent_payments=rent_payments)


@app.route("/Survey_details", methods=['GET', 'POST'])
def Survey_details():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        outlet_name = request.form.get('outletName', '')  #To avoid Key error exception hence used get too.
        warning_issued = request.form.get('warningIssued', '')  
        
        # Base query
        query = """
        SELECT s.Survey_ID, o.Outlet_name, s.Date_of_survey, st.name, s.Description, s.Warning_issued, s.Penalty_amount
        FROM Survey s
        JOIN Outlet o ON s.Outlet_ID = o.Outlet_ID
        JOIN Stakeholder st ON s.Stakeholder_ID = st.Stakeholder_ID
        WHERE 1=1
        """
        
        # Filtering conditions to avoid SQL injection hence DYnamic Query
        parameters = []
        if outlet_name:
            query += " AND o.Outlet_name LIKE %s"
            parameters.append('%' + outlet_name + '%')
        if warning_issued in ['Yes', 'No']:
            query += " AND s.Warning_issued = %s"
            parameters.append(warning_issued)
        
        cur.execute(query, parameters)
    else:
        # Initial page load without any filters
        query = """
        SELECT s.Survey_ID, o.Outlet_name, s.Date_of_survey, st.name, s.Description, s.Warning_issued, s.Penalty_amount
        FROM Survey s
        JOIN Outlet o ON s.Outlet_ID = o.Outlet_ID
        JOIN Stakeholder st ON s.Stakeholder_ID = st.Stakeholder_ID
        """
        cur.execute(query)

    surveys = cur.fetchall()
    cur.close()
    return  render_template("survey.html",surveys=surveys)

if __name__ == "__main__":
    app.run(debug=True)