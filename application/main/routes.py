
import datetime
from flask import render_template, Blueprint, request
from application.data.main_data import latest, start_date
from application.data.user_search import (generate_percentage, white_balls, 
                                          red_balls, date_search,
                                          get_streak, get_draught,
                                          get_red_draught, get_red_streak,
                                          monthly_number, monthly_number_red,
                                          yearly_number, yearly_number_red)
from application.data.user_search_monthly import per_month, white_monthly_winners
from application.data.user_search_monthly_red import red_monthly_winners
from application.data.user_search_yearly import per_year, white_yearly_winners
from application.data.user_search_yearly_red import red_yearly_winners
from application.data.recent_winners import get_recent
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
    # Get recent powerball winners with draw dates
    recent = get_recent()
    return render_template('recent_winners.html', 
                            recent = recent
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

            monthly_winners = monthly_number(number)
            months = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
            pm = per_month(monthly_winners, months)
            chart_white_monthly = white_monthly_winners(number, pm)

            yearly_winners = yearly_number(number)
            py = per_year(yearly_winners)
            chart_white_yearly = white_yearly_winners(number, py)

            # if user number is less than 26, then fetch both white and red balls 
            if number <= 26:
                red_occurrences = red_balls(number, date_frame)
                red_percentage = generate_percentage(red_occurrences, number_of_pulls)
                red_draught = get_red_draught(number, date_frame)
                red_streak = get_red_streak(number, date_frame)

                monthly_winner_red = monthly_number_red(number)
                months_red = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
                pm_red = per_month(monthly_winner_red, months_red)
                chart_red_monthly = red_monthly_winners(number, pm_red)

                yearly_winner_red = yearly_number_red(number)
                py_red = per_year(yearly_winner_red)
                chart_red_yearly = red_yearly_winners(number, py_red)
                
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
                                        last_updated=last_updated,
                                        chart_white_monthly = chart_white_monthly,
                                        chart_red_monthly = chart_red_monthly,
                                        chart_white_yearly = chart_white_yearly,
                                        chart_red_yearly = chart_red_yearly
                                        )

            return render_template('search.html', number=number, 
                                    white_occurrences=white_occurrences, 
                                    white_percentage=white_percentage, 
                                    time_period=time_period,
                                    last_updated=last_updated,
                                    white_draughts=white_draughts,
                                    white_streaks=white_streaks,
                                    chart_white_monthly = chart_white_monthly,
                                    chart_white_yearly = chart_white_yearly
                                    )
    
    return render_template('search.html', number=number)

@powerball.route('/odds', methods=['POST', 'GET'])
def odds():
    white_numbers = [
                     6.95, 7.47, 7.55, 6.55, 6.22, 7.8, 6.52, 6.69, 6.63, 6.85, 6.98, 
                     7.49, 5.09, 6.5, 6.64, 7.36, 6.59, 6.53, 7.96, 7.84, 8.57, 7.21, 
                     9.17, 7.23, 5.91, 5.85, 8.76, 7.92, 6.04, 6.62, 7.0, 8.29, 9.27, 
                     6.07, 6.14, 8.52, 7.73, 6.98, 9.06, 7.14, 7.3, 7.27, 6.49, 7.89, 
                     7.17, 6.14, 8.09, 6.42, 5.82, 7.11, 6.68, 7.23, 7.91, 7.11, 6.32, 
                     7.36, 6.71, 6.31, 8.26, 6.41, 9.14, 8.0, 8.87, 8.31, 6.35, 6.78, 
                     7.67, 8.07, 9.12
                     ]
    red_numbers = [
                   3.64, 3.34, 3.99, 5.15, 4.16, 3.55, 3.28, 3.81, 4.12, 3.94, 3.53, 
                   3.14, 4.15, 4.39, 3.18, 3.17, 3.39, 4.61, 3.86, 3.79, 4.55, 3.21, 
                   3.61, 4.65, 3.87, 3.92
                   ]
    return render_template('odds.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    white_numbers = [
                     [11, 19, 45, 47, 61], 
                     [3, 27, 39, 51, 55], 
                     [20, 32, 49, 52, 69], 
                     [6, 28, 50, 53, 57], 
                     [12, 16, 31, 44, 65]
                     ]
    red_numbers = [6, 18, 9, 11, 24]
    return render_template('predictions.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )