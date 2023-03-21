'''
Created on 2023-03-18

@author: Surya Pugal

source:
https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/
https://faun.pub/integrating-mongodb-with-flask-8f6568863c2a ##########
https://medium.com/codex/simple-registration-login-system-with-flask-mongodb-and-bootstrap-8872b16ef915
https://www.section.io/engineering-education/building-a-simple-python-note-app-with-flask-and-mongodb/
https://www.grepper.com/answers/44330/button+in+flask
https://medium.com/nerd-for-tech/developing-a-simple-create-read-update-and-delete-crud-application-using-flask-and-mariadb-f037a5798ee2
https://github.com/sofwanbl/flask_mariadb_crud
    
'''

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

#initialize the Flask app
app = Flask(__name__)

#connect and create a db named as flaskmongo (So we have created the 
# the database named as mydb but in mongodb the database is not 
# created until it contains some data so our db is still not created)
app.config['MONGO_URI'] = "mongodb://localhost:27017/flaskmongo"

#initializing the client for mongodb
mongo = PyMongo(app)

#creating the customer collection
customer_collection = mongo.db.customers


@app.route('/')
def index():
    return render_template('index.html')
    
      

# @app.route('/data', methods=['POST', 'GET'])
def show_data():
    print("im in data route")
    if request.method == 'POST':
        cus_name = request.form["name"]
        print(f"customer name: {cus_name}")
        cus_phone_no = request.form.get("phone")
        print(f"customer phone: {cus_phone_no}")
        cus_loc = request.form.get("location")
        print(f"customer location: {cus_loc}")
        
        if cus_name != "" and cus_phone_no != "" and cus_loc != "":
            customer_collection.insert_one({"name" : cus_name, "phone" : cus_phone_no, "location" : cus_loc})
            return ("data added to the database successfully")
        else:
            return("Kindly fill all the fields")
    return render_template('index.html')


@app.route('/read')
def read_data():
    data = (customer_collection.find())
    print(f"read all data: {data}")
    return render_template('customer.html', customer=data)

# @app.route('/update', methods=['POST', 'GET'])
def update_data():
    # if request.method == 'POST':
    cus_name = request.form["name"]
    # cus_phone_no = request.form.get("phone")
    cus_loc = request.form.get("location")
    customer_collection.update_one({"name" : cus_name}, {"$set" : {"location" : cus_loc}})
    return redirect("/button")

@app.route('/button', methods=['POST'])
def button():
    print(request.form['submit_button'])
    print(request.method)
    if request.method == 'POST':
        if request.form['submit_button'] == 'Add':
            show_data()
            return render_template('index.html') 
        elif request.form['submit_button'] == 'Update':
            update_data()
            return render_template('index.html')
        else:
            return render_template('index.html')
            

@app.route('/delete/<name>')
def delete_data(name):
    customer_collection.delete_one({"name" : name})
    # for delete all data use remove() method
    # customer_collection.remocve({})
    return redirect("/")
    

        
        

if __name__ == '__main__':
    app.run(debug=True)