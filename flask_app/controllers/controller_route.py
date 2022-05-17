from flask import render_template, redirect, request, session, flash
from flask_app import app 

from flask_app.models.model_user import User

# Display Route
@app.route('/')
def index():

    return render_template ('index.html')

# Display Route
@app.route('/wall')
def wall():
    if not "user_id" in session:
        return redirect("/")
    data = {"id": session['user_id'],
            **request.form}
    user = User.get_one(data)
# Understand why its not working
    return render_template ('dashboard.html', user=user)






# Clears Session
@app.route("/destroy_session")
def clear_session():
    session.clear()
    return redirect("/")

#RESTfull
#table_name/id(if possible)/action
#user/new             -> Display Route
#user/create          -> Action Route
#user/<int:id>        -> Display Route
#user/<int:id>/edit   -> Diplay Route
#user/<int:id>/update -> Action Route
#user/<int:id>/delete -> Action Route  -> this is not a post request route its a get 