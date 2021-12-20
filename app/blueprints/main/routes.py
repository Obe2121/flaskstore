from flask import render_template, request, redirect, url_for, flash
import requests
from app.models import User, Item, Cart
from flask_login import login_required, login_user, current_user, logout_user
from .import bp as main



@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/shop', methods=['GET', 'POST'])
@login_required
def shop():
    if request.method == 'POST':
        url = f'https://fakestoreapi.com/products?limit=5'
        response = requests.get(url)
        if response.ok:
            if not response.json()[0]:
                 error_string="We had an error loading your data likely the year or round is not in the database"
                 return render_template('shop.html.j2', error = error_string)
            data = response.json()[1] 
            new_item=[]
            
            item_dict={
                'item_id':data['id'],
                'item_name':data['title'],
                'item_price':data['price'],
                'item_des':data['description'],
                'item_category':data['category']
            }
            new_item.append(item_dict)
            new_items = Item(user_id = current_user.id, item_name=item_dict['item_name'], item_price = item_dict['item_price'], item_des=item_dict['item_des'],item_category=item_dict['item_category'])
        new_items.add_item()   
        print(new_items)
        return render_template('shop.html.j2', items=new_item)
    else:
        error_string = "Houston We had a problem"
        return render_template('shop.html.j2', error = error_string)

#@main.route('/cart', methods=['POST'])
#def cart():
 #new_task = Item(user_id = current_user.id, task_name=activity_dict['activity'], task_type = activity_dict['type'],task_key=activity_dict['key'])
            #new_task.add_task()
            #flash(f'You have added {activity_dict["activity"]}, congratulations', #'success')
        #print(new_activity)
        #return render_template('shop.html.j2', activities=new_activity)