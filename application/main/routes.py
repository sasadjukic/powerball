
import datetime
from flask import render_template, Blueprint, request
from application.data.main_data import latest, start_date
from application.data.user_search import (generate_percentage, white_balls, 
                                          red_balls, date_search,
                                          get_streak, get_drought,
                                          get_red_drought, get_red_streak,
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

            white_droughts = get_drought(number, date_frame)
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
                red_drought = get_red_drought(number, date_frame)
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
                                        red_drought=red_drought,
                                        red_streak=red_streak,
                                        white_occurrences=white_occurrences, 
                                        white_percentage=white_percentage, 
                                        white_droughts=white_droughts,
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
                                    white_droughts=white_droughts,
                                    white_streaks=white_streaks,
                                    chart_white_monthly = chart_white_monthly,
                                    chart_white_yearly = chart_white_yearly
                                    )
    
    return render_template('search.html', number=number)

@powerball.route('/odds', methods=['POST', 'GET'])
def odds():
    white_numbers = [
                     6.89, 7.29, 7.93, 6.20, 7.05, 7.30, 7.03, 6.04, 7.21, 6.93, 6.91, 7.62, 
                     5.31, 6.32, 7.10, 7.48, 7.07, 6.72, 7.86, 7.06, 8.99, 7.12, 8.60, 7.77, 
                     6.03, 5.92, 8.70, 8.49, 5.24, 6.78, 6.74, 8.06, 8.96, 6.12, 6.40, 8.69, 
                     7.90, 7.47, 8.15, 6.90, 6.30, 7.24, 6.08, 7.95, 7.61, 5.95, 8.18, 6.03, 
                     5.55, 7.35, 6.58, 7.13, 7.76, 8.15, 7.10, 7.01, 6.72, 6.81, 8.15, 6.45, 
                     9.18, 8.05, 8.61, 8.26, 6.45, 7.56, 7.16, 7.55, 8.73
                     ]
    red_numbers = [
                   3.74, 3.56, 4.01, 4.94, 4.49, 3.63, 3.73, 3.91, 4.32, 3.29, 4.00, 2.87, 
                   4.07, 4.60, 3.24, 3.10, 3.00, 4.44, 3.78, 3.71, 4.70, 3.33, 3.26, 4.29, 
                   3.84, 4.15
                   ]
    return render_template('odds.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    white_numbers = [
                     [13, 17, 26, 52, 59], 
                     [7, 25, 28, 39, 62], 
                     [6, 19, 41, 45, 56], 
                     [3, 21, 33, 37, 50], 
                     [14, 18, 31, 61, 66]
                     ]
    red_numbers = [6, 14, 9, 15, 23]
    return render_template('predictions.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )