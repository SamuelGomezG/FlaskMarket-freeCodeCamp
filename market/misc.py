from flask import request, flash
from market.models import Item, User
from flask_login import current_user, login_user
from market import db

def purchaseItem():
    purchased_item = request.form.get("purchased_item")
    p_item_obj = Item.query.filter_by(name=purchased_item).first()
    if p_item_obj:
        if current_user.can_purchase(p_item_obj):
            p_item_obj.buy(current_user)
            
            flash(f"Congratulations, you purchased {p_item_obj.name} for ${p_item_obj.price}", category="success")
        else:
            flash(f"Unfortunately, you don't have enough money to purchase {p_item_obj.name}", category="danger")

def sellItem():
    sold_item = request.form.get("sold_item")
    s_item_obj = Item.query.filter_by(name=sold_item).first()
    if s_item_obj:
        if current_user.can_sell(s_item_obj):
            s_item_obj.sell(current_user)
            
            flash(f"Congratulations, you sold {s_item_obj.name} back to market", category="success")
        else:
            flash(f"Something went wrong with selling {s_item_obj.name}", category="danger")

#Create and register a new user
def registerUser(form):
    user_to_create = User(
        username=form.username.data,
        email_address=form.email_address.data,
        password=form.password1.data
    )
    db.session.add(user_to_create)
    db.session.commit()
    
    login_user(user_to_create)
    flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")