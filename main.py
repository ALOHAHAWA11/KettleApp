import datetime
import os
from flask import Flask, render_template, request, flash

import config
from config import SECRET_KEY
from db_handler import DatabaseHandler
from entities.kettle import Kettle
from loguru import logger

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'db.db')))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Route for index page. On this page you can boil a water"""
    logger.info("Index page on a screen.")
    db = DatabaseHandler(app)
    if request.method == 'POST':
        logger.debug("Accepted POST request on /index.")
        data = request.form
        global kettle
        kettle = Kettle(
            name=data['name'],
            volume=float(data['volume']),
            power=int(data['power'])
        )
        logger.debug("Kettle object has been created.")
        if bool(data['is_active']):
            if data['filled_water'] > data['volume']:
                flash('Нельзя залить в чайник объем воды больший, чем объем чайника')
                logger.error("Validation error on index page.")
            kettle.fill_water(float(data['filled_water']))
            logger.info("Water in a kettle")
            kettle.turn_on()
            logger.info("Kettle is turned on.")
            for temp in kettle.boil_water(float(data['start_temp'])):
                db.insert_record(datetime.datetime.now(), temp)
            flash('Вода закипела! Чайник отключен.')
            logger.info("End of a boil process.")
    return render_template('index.html')


@app.route('/cancel', methods=['POST'])
def cancel():
    """Page of a canceling of the boil process"""
    logger.info("Cancel page on the screen.")
    if request.method == 'POST':
        logger.debug("Accepted POST request on /cancel")
        kettle.turn_off()
        logger.info("Kettle is turned off.")
        current_temp = str(kettle.current_temp)
    return render_template('cancel.html', current_temp=current_temp)


if __name__ == '__main__':
    if config.DEBUG:
        logger.add('logs.log', format="{time} {level} {message}", level="DEBUG")
    else:
        logger.add('logs.log', format="{time} {level} {message}", level="INFO")
    logger.info("Start of application.")
    app.run(debug=True)
