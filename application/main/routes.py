
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
                     6.87, 7.32, 7.95, 6.72, 7.04, 7.53, 6.91, 6.43, 7.33, 7.8, 6.73, 
                     7.52, 4.89, 6.66, 6.96, 6.85, 6.78, 6.96, 7.64, 7.48, 8.86, 6.84, 
                     8.39, 7.33, 6.56, 5.9, 8.46, 7.38, 5.87, 7.16, 7.03, 9.08, 8.13, 
                     5.77, 6.56, 9.07, 8.15, 7.55, 8.49, 7.23, 6.56, 7.07, 6.36, 8.35, 
                     7.27, 5.75, 8.1, 5.97, 5.16, 7.02, 6.69, 6.74, 8.05, 7.06, 6.67, 
                     7.27, 7.1, 6.08, 7.99, 6.58, 8.41, 7.84, 8.94, 8.52, 6.28, 7.31, 
                     7.57, 7.97, 9.14
                     ]
    red_numbers = [
                   3.69, 3.32, 3.89, 5.12, 3.93, 3.88, 3.68, 3.42, 4.52, 3.88, 
                   3.97, 3.18, 4.03, 4.54, 3.02, 3.18, 3.12, 4.85, 3.36, 3.51, 
                   4.68, 3.12, 3.79, 4.87, 3.78, 3.67
                   ]
    return render_template('odds.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    white_numbers = [[10, 18, 32, 53, 59], 
                     [6, 36, 44, 47, 63], 
                     [7, 12, 21, 27, 61], 
                     [19, 39, 45, 66, 68], 
                     [3, 23, 33, 37, 64]
                     ]
    red_numbers = [4, 24, 6, 23, 11]
    return render_template('predictions.html', 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )