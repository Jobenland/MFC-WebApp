from flask import (Blueprint, render_template, request,
                   redirect, flash, url_for, g, current_app, session)
from flask_login import (login_user, logout_user, current_user, login_required)

from . import db
from .models import User
from .utils import validate_captcha

import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template

import json

main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
    g.user = current_user


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """The main page for the app"""

    with open("app/channeldata.json", "r") as jsonFile:
        data = json.load(jsonFile)

    channels = data['Channels']
    voltage = data['Voltage']

    with open("app/channeldata.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Channel Data", "Channels",
                            "Voltage", hover)

    script, div = components(plot)

    my_var="System awaiting query..."
    return render_template("vTwo.html", data=my_var,
                           the_div=div, the_script=script)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if current_app.config.get('SHOW_CAPTCHA'):
        captcha_response = request.form.get('g-recaptcha-response')
        if not validate_captcha(captcha_response):
            flash('Bad Captcha')
            return redirect(url_for('main.register'))

    email = request.form['email']
    password = request.form['password']
    password_confirm = request.form['password_confirm']

    if password != password_confirm:
        flash('Passwords must match!')
        return redirect(url_for('main.register'))

    user = User.create(email, password)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        flash('User already exists!')
        return redirect(url_for('main.register'))

    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['email']
    password = request.form['password']

    if current_app.config.get('SHOW_CAPTCHA'):
        captcha_response = request.form.get('g-recaptcha-response')
        if not validate_captcha(captcha_response):
            flash('Bad Captcha')
            return redirect(url_for('main.login'))

    registered_user = User.get_user(username, password)

    if registered_user is None:
        flash('Username or Password is invalid')
        return redirect(url_for('main.login'))
    else:
        login_user(registered_user)

    #flash('Logged in successfully')
    return redirect(url_for('main.index'))

@main.route('/options')
def options():
    return render_template('spo.html')
    
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/all', methods = ['POST'])
def all():
    #THIS IS FOR TESTING. REMOVE IN PRODUCTION
    y = 0.034
    vol = (255*((y-0.034)/(1.032)))/5.000
    vol = int(round(vol))
    x = (hex(vol))
    data = [int(x , 16), 0x00]
    channel = 47
    hchanu = hex(channel)
    hchanr= int(hchanu , 16)
    voltage = 5.0*((data[0] * 256 +data[1])/ 65536.0) 
    print ("Voltage :%.2f V" %voltage)
    print (x)
    print (vol)
    voltt = str(voltage)
    chan = str(channel)
    session['my_var'] = 'A Voltage of '+voltt+'v was successfully sent to channel '+ chan
    session['my_volty'] = voltt
    session['my_chan'] = chan
    data = 'test'
    return redirect(url_for('main.update'))    

    """
    import smbus2
    import time

    try:
        bus = smbus2.SMBus(1)
        y = float(request.form['voltage'])
        vol = (255*((y-0.034)/(1.032)))/5.000
        vol = int(round(vol))
        x = (hex(vol))
        data = [int(x , 16), 0x00]
        channel = int(request.form['channel'])
        hchanu = hex(channel)
        hchanr= int(hchanu , 16)
        bus.write_i2c_block_data(0x56, hchanr, data)
        time.sleep(0.5)
        voltage = 5.0*((data[0] * 256 +data[1])/ 65536.0) 
        print ("Voltage :%.2f V" %voltage)
        print (x)
        print (vol)
        voltt = str(voltage)
        chan = str(channel)
        session['my_var'] = 'A Voltage of '+voltt+'v was successfully sent to channel '+ chan
        data = 'test'
        return redirect(url_for('main.update'))
    except:
        session['my_var'] = '***FATAL SERVER ERROR! A error occured while sending voltage to system...***'
    """

   
@main.route('/changevol', methods = ['POST'])
def changevol():
    try:
        #THIS IS FOR TESTING. REMOVE IN PRODUCTION
        y = float(request.form['voltage'])
        vol = (255*((y-0.034)/(1.032)))/5.000
        vol = int(round(vol))
        x = (hex(vol))
        data = [int(x , 16), 0x00]
        channel = int(request.form['channel'])
        hchanu = hex(channel)
        hchanr= int(hchanu , 16)
        voltage = 5.0*((data[0] * 256 +data[1])/ 65536.0) 
        print ("Voltage :%.2f V" %voltage)
        print (x)
        print (vol)
        voltt = str(voltage)
        chan = str(channel)
        session['my_var'] = 'A Voltage of '+voltt+'v was successfully sent to channel '+ chan
        session['my_volty'] = voltt
        session['my_chan'] = chan
        data = 'test'
        return redirect(url_for('main.update'))
    except ValueError:
        flash("Either no number was given or a number out of range was submitted\n. Error Code: 69")
        return redirect(url_for('main.index'))

    """
    import smbus2
    import time

    try:
        bus = smbus2.SMBus(1)
        y = float(request.form['voltage'])
        vol = (255*((y-0.034)/(1.032)))/5.000
        vol = int(round(vol))
        x = (hex(vol))
        data = [int(x , 16), 0x00]
        channel = int(request.form['channel'])
        hchanu = hex(channel)
        hchanr= int(hchanu , 16)
        bus.write_i2c_block_data(0x56, hchanr, data)
        time.sleep(0.5)
        voltage = 5.0*((data[0] * 256 +data[1])/ 65536.0) 
        print ("Voltage :%.2f V" %voltage)
        print (x)
        print (vol)
        voltt = str(voltage)
        chan = str(channel)
        session['my_var'] = 'A Voltage of '+voltt+'v was successfully sent to channel '+ chan
        data = 'test'
        return redirect(url_for('main.update'))
    except:
        session['my_var'] = '***FATAL SERVER ERROR! A error occured while sending voltage to system...***'
    """

   
@main.route('/update')
def update():
    try:
        my_var = session.get('my_var', None)
        my_volty = session.get('my_volty', None)
        my_chan = session.get('my_chan', None)

        with open("app/channeldata.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if my_chan == "47":
            voltage = data['Voltage']
            print('all')
            for i in range(len(voltage)):
                voltage[i] = 0
        elif my_chan != "47":
            channels = data['Channels']
            voltage = data['Voltage']
        
            index = channels.index(my_chan)
            voltage[index] = my_volty
            print('none')
        
        with open("app/channeldata.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        '''
        for channel in channels:
            data["Channels"].append(channel)
        
        for volt in voltage:
            data["Voltage"].append(volt)
        '''

        hover = create_hover_tool()
        plot = create_bar_chart(data, "Channel Data", "Channels",
                                "Voltage", hover)

        script, div = components(plot)

        return render_template("vTwo.html", data=my_var,
                            the_div=div, the_script=script)
    except ValueError:
        flash("Voltage was sent but is not listed as a valid channel for this setup. Error Code: 420")
        return redirect(url_for('main.index'))


def create_hover_tool():
    # we'll code this function in a moment
    return None

def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1000, height=500):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Voltage"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Channel"
    plot.xaxis.major_label_orientation = 1
    return plot
