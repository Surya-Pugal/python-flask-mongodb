'''
Created on 2023-03-18

@author: Surya Pugal

source:
https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/
https://faun.pub/integrating-mongodb-with-flask-8f6568863c2a

    
'''

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

#initialize the Flask app
app = Flask(__name__)

#connect and create a db named as mydb (So we have created the 
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
    
      

@app.route('/data', methods=['POST', 'GET'])
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



    

# @app.route()
        
        

if __name__ == '__main__':
    app.run(debug=True)