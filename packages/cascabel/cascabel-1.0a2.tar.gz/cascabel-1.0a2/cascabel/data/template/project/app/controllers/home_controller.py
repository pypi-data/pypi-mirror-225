from flask import render_template, redirect, url_for, flash

from resources.vars.vars import db
from app.requests.user_request import LoginForm, RegisterForm
from app.models.main.user_model import UserModel


class HomeController:

    def index(self):  
        return render_template("home/index.html")
    
    
    def get_login(self):
        login_form = LoginForm()
        return render_template("home/login.html", login_form = login_form)
    
    
    def post_login(self):
        
        login_form = LoginForm()
        
        if not login_form.validate_on_submit():
            return render_template("home/login.html", login_form = login_form)
        
        user = UserModel.query.filter_by(email=login_form.email.data, password=login_form.password.data).first()
        
        if user == None:
            flash("Email and/or password are incorrect.")
            return render_template("home/login.html", login_form = login_form)
        
        flash("Successful login.")
        return redirect(url_for('home_index'))


    def get_register(self):
        register_form = RegisterForm()
        return render_template("home/register.html", register_form = register_form)
    
    
    def post_register(self):
        
        register_form = RegisterForm()
        
        if not register_form.validate_on_submit():
            return render_template("home/register.html", register_form = register_form)
        
        user = UserModel.query.filter_by(email=register_form.email.data).first()
        if user != None:
            flash("The email is already in use.")
            return render_template("home/register.html", register_form = register_form)
        
        new_user = UserModel(email = register_form.email.data,
                             name = register_form.name.data,
                             password = register_form.password.data,
                             birth_date = register_form.birth_date.data
                            )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('home_index'))
