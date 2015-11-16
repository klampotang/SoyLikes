from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from HtmlClarifai2DArray import *
# index view function suppressed for brevity

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def input():
    form = LoginForm()
    if form.validate_on_submit():
          flash('Login requested for OpenID="%s", remember_me=%s' %
                (form.openid.data, str(form.remember_me.data)))
          return redirect('/clarifai')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/clarifai', methods=['GET', 'POST'])
def images():
	keywords = HtmlClarifai2DArray("kellylpt")
	print keywords
