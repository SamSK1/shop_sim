from flask import Flask,jsonify,request,render_template
import sqlite3

app=Flask(__name__)

def connect_db():
    db=sqlite3.connect('flask_store_project.db')
    db.execute('CREATE TABLE IF NOT EXISTS Items (item_id INTEGER PRIMARY KEY, item_name TEXT, item_price REAL, item_description TEXT, item_count INTEGER, item_img TEXT, item_category TEXT)')
    db.close()

connect_db()

@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET'])
def home_page():
    return render_template('base.html')

@app.route('/another_page',methods=['GET'])
def another_page():
    return render_template('another_page.html')

@app.route('/items_page',methods=['GET'])
def item_page():
    all_items=[]
    try:
        with sqlite3.connect('flask_store_project.db') as db:
            db.row_factory=sqlite3.Row
            cursor=db.cursor()
            cursor.execute('SELECT * FROM Items ')
            all_items=cursor.fetchall()
    except Exception as e:
        db.rollback()
        return jsonify('Error: '+str(e))
    
    finally:
        db.close()


    return render_template('items_page.html',all_items=all_items)

@app.route('/add_item',methods=['POST'])
def add_item():
    message = None
    
    try:
        data = request.get_json()
        item_name = data['item_name']
        item_price = data['item_price']
        item_description = data['item_description']
        item_count = data['item_count']
        item_img = data['item_img']
        item_category = data['item_category']

        with sqlite3.connect('flask_store_project.db') as db:
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO Items (item_name, item_price, item_description, item_count, item_img, item_category) VALUES (?, ?, ?, ?, ?, ?)',
                (item_name, item_price, item_description, item_count, item_img, item_category)
            )
            db.commit()
            message = f'Item {item_name} has been successfully added to the database!'
    
    except Exception as e:
        message = 'Error: ' + str(e)
    
    return jsonify(message=message)
    

@app.route('/update_item/<int:item_id>',methods=['PUT'])
def update_item(item_id):
    message=None
    try:
        data=request.get_json()
        item_name = data.get('item_name')
        item_price = data.get('item_price')
        item_description = data.get('item_description')
        item_count = data.get('item_count')
        item_img = data.get('item_img')
        item_category = data.get('item_category')

        with sqlite3.connect('flask_store_project.db') as db:
            cursor=db.cursor()
            cursor.execute('''UPDATE Items SET item_name=?,item_price=?,item_description=?,item_count=?,item_img=?,item_category=? WHERE item_id=? ''',(item_name,item_price,item_description,item_count,item_img,item_category,item_id))
            

            if cursor.rowcount == 0:
                return jsonify('Error: Item was not found'),404
            else:
                db.commit()
                return jsonify(message=f'Item {item_name} has been successfully updated')
            
    except Exception as e:
        db.rollback()
        message="Error: "+str(e)
    return jsonify(message=message)


if __name__=='__main__':
    app.run(debug=True)

