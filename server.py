from flask import Flask,request,jsonify,render_template
import sqlite3


app=Flask(__name__)


def start_db():
    connect_db=sqlite3.connect('grocery_store.db')
    connect_db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, item_name TEXT, item_price INTEGER, item_description TEXT) ')
    connect_db.close()


start_db()

@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET'])
def load_home_page():
    
    return render_template('base.html')

@app.route('/get_items',methods=['GET'])
def get_items():
    pass


if __name__=='__main__':
    app.run(debug=True)