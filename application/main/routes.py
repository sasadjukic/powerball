
import datetime
from flask import render_template, Blueprint, request
from application.data.main_data import latest, start_date
from application.data.user_search import (generate_percentage, white_balls, 
                                          red_balls, date_search,
                                          get_streak, get_draught,
                                          get_red_draught, get_red_streak)
from application.data.recent_winners_white import recent_white_winners
from application.data.recent_winners_red import recent_red_winners
from application.data.all_time_winners_white import all_time_white_winners
from application.data.all_time_winners_red import all_time_red_winners

powerball = Blueprint('powerball', __name__)
last_updated = latest
@powerball.route('/')
def home():
    return render_template('index.html', last_updated=last_updated)

@powerball.route('/rules', methods=['POST', 'GET'])
def rules():
    return render_template('rules.html')

@powerball.route('/all_time_winners', methods=['POST', 'GET'])
def all_time_winners():
    # Generate bar charts for all time winners
    white_all_time = all_time_white_winners()
    red_all_time = all_time_red_winners()
    return render_template('winners.html', 
                            white_all_time=white_all_time, 
                            red_all_time=red_all_time
                            )

@powerball.route('/recent_winners', methods=['POST', 'GET'])
def recent_winners():
    # Generate bar charts for winners in last 6 months
    chart_white_numbers = recent_white_winners()
    chart_red_numbers = recent_red_winners()
    return render_template('recent_winners.html', 
                            chart_white_numbers=chart_white_numbers, 
                            chart_red_numbers=chart_red_numbers
                            )

@powerball.route('/search', methods=['POST', 'GET'])
def search():
    number = None
    if request.method == 'POST':
        # Get user input for a powerball number and date from which they want to start search
        number = int(request.form['number_input'])
        time_period = request.form['date_input']

        # call date_search function with time_period user input
        date_frame = date_search(time_period, start_date)

        # get total number of draws in user specified time frame
        number_of_pulls = date_frame.shape[0]

        # if user number is greater or equall to 70, then flash error
        if number >= 70:
            flash('Invalid Input')
            return redirect(url_for('search'))

        # if user number is less than 70, then fetch white balls
        if number < 70:
            # Get number of times searched number appears
            white_occurrences = white_balls(number, date_frame)
            # Generate percentage
            white_percentage = generate_percentage(white_occurrences, number_of_pulls)

            white_draughts = get_draught(number, date_frame)
            white_streaks = get_streak(number, date_frame)

            # if user number is less than 26, then fetch both white and red balls 
            if number <= 26:
                red_occurrences = red_balls(number, date_frame)
                red_percentage = generate_percentage(red_occurrences, number_of_pulls)
                red_draught = get_red_draught(number, date_frame)
                red_streak = get_red_streak(number, date_frame)

                return render_template('search.html', number=number, 
                                        red_occurrences=red_occurrences, 
                                        red_percentage=red_percentage, 
                                        red_draught=red_draught,
                                        red_streak=red_streak,
                                        white_occurrences=white_occurrences, 
                                        white_percentage=white_percentage, 
                                        white_draughts=white_draughts,
                                        white_streaks=white_streaks,
                                        time_period=time_period,
                                        last_updated=last_updated
                                        )

            return render_template('search.html', number=number, 
                                    white_occurrences=white_occurrences, 
                                    white_percentage=white_percentage, 
                                    time_period=time_period,
                                    last_updated=last_updated,
                                    white_draughts=white_draughts,
                                    white_streaks=white_streaks
                                    )
    
    return render_template('search.html', number=number)

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    return render_template('predictions.html')