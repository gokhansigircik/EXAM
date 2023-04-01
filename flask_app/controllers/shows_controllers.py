from flask_app.models.show_model import Show
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_model

# ***** this doesnt let me go the dashboard- checks the cond first ******
@app.route("/shows")
def dashboard():
    if not 'uid' in session:
        flash("access denied")
        return redirect("/")
    results = user_model.User.all_shows_with_users()
    print(results)
    print(session['uid'])
    return render_template('dashboard.html', results=results)

@app.route("/show/all")
def all_shows():
    return render_template('create_shows.html', all_shows=Show.get_all())

@app.route('/shows/destroy/<int:id>')
def distroy_shows(id):
    data = {
        "id": id
    }
    shows = Show.destroy(data)
    return redirect("/shows")

@app.route('/shows/display/<int:id>')
def display_shows(id):
    data = {
        "id": id
    }
    shows = Show.get_one(data)
    return render_template('show_shows.html', shows = shows)

@app.route('/shows/edit/<int:id>')
def edit_shows(id):

    data = {
        "id": id
    }
    result = Show.get_show_by_id(data)
    return render_template('edit_shows.html', result = result)


@app.route("/create_show", methods=["POST"])
def new_show():

    if not Show.validates_show_creation_updates(request.form):
        return redirect("/show/all")

    data={
        **request.form,
        "user_id": session['uid']
    }
    Show.save(data)
    return redirect("/shows")

@app.route("/edit_shows/<int:id>", methods=["POST"])
def updated_show(id):

    if not Show.validates_show_creation_updates(request.form):
        return redirect("/shows/edit/"+str(id))

    data={
        **request.form,
        "id": id
    }
    Show.update(data)
    return redirect("/shows")