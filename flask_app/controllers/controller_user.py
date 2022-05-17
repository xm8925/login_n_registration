from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt 

from flask_app.models.model_user import User

# Creating a User
# Action Route (never render on an action route)
@app.route('/user/create', methods=['post'])
def create_user():
    if not User.validate(request.form):
        return redirect('/')
    # This ^ validates the form
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    
    data = {
        **request.form,
        "password" : pw_hash
    }
    
    session['user_id'] = User.create(data)
    
    return redirect('/wall')


# Login
# Action Route (never render on an action route)
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "error_user_valid_email")
        return redirect("/")
    print(user_in_db.password)
    print(request.form['password'])
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "error_user_valid_password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/wall")

#RESTfull
#table_name/id(if possible)/action
#user/new             -> Display Route
#user/create          -> Action Route
#user/<int:id>        -> Display Route
#user/<int:id>/edit   -> Diplay Route
#user/<int:id>/update -> Action Route
#user/<int:id>/delete -> Action Route  -> this is not a post request route its a get 