import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


# ------------------------ BEGIN FUNCTIONS ------------------------ #
# Function to retrieve DB connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conn

# Get all items from the "items" table of the db
def get_all_items():
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Closes db connection (You should do this after each query, otherwise your database may become locked.)
    return result
# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/")
def home():
    items = get_all_items() # Call defined function to get all items
    # Return the page to be rendered
    return render_template("index.html", items=items)

# EXAMPLE OF POST REQUEST
@app.route("/new-item", methods=["POST"])
def add_item():
    data = request.form
    item_name = data["name"]
    item_quantity = data["quantity"]

    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection
    # Prepare the query statemenet
    query = "INSERT INTO items (name, quantity) VALUES (%s, %s)"
    values = (item_name,item_quantity,)
    # Execute and commit changes to the db
    cursor.execute(query, values)
    conn.commit() # Commit saves the changes to the db. If you don't include this, then changes will not save.
    conn.close() # Closes db connection (You should do this after each query, otherwise your database may become locked.)
    
    # Send message to page
    flash("Item added successfully")
    # Redirect to home
    return redirect(url_for("home"))
# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
