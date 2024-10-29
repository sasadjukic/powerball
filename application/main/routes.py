

from flask import render_template, Blueprint, request
from application.data.main_data import latest, earliest, next_draw
from application.data.user_search import (generate_percentage, white_balls, red_balls,
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
from application.data.recent_winners_white import recent_white_winners
from application.data.recent_winners_red import recent_red_winners

powerball = Blueprint('powerball', __name__)

@powerball.route('/')
def home():
    return render_template('index.html', latest=latest)

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

@powerball.route('/top_6_months', methods=['POST', 'GET'])
def top_6_months():
    # Generate bar charts for top 6 months
    white_top_6 = recent_white_winners()
    red_top_6 = recent_red_winners()
    return render_template('winners_6m.html', 
                            white_top_6=white_top_6, 
                            red_top_6=red_top_6
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

        # if user number is greater or equall to 70, then flash error
        if number >= 70:
            flash('Invalid Input')
            return redirect(url_for('search'))

        # if user number is less than 70, then fetch white balls
        if number < 70:
            # Get number of times searched number appears
            white_occurrences = white_balls(number)
            # Generate percentage
            white_percentage = generate_percentage(white_occurrences)

            white_droughts = get_drought(number)
            white_streaks = get_streak(number)

            monthly_winners = monthly_number(number)
            months = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
            pm = per_month(monthly_winners, months)
            chart_white_monthly = white_monthly_winners(number, pm)

            yearly_winners = yearly_number(number)
            py = per_year(yearly_winners)
            chart_white_yearly = white_yearly_winners(number, py)

            # if user number is less than 26, then fetch both white and red balls 
            if number <= 26:
                red_occurrences = red_balls(number)
                red_percentage = generate_percentage(red_occurrences)
                red_drought = get_red_drought(number)
                red_streak = get_red_streak(number)

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
                                        earliest=earliest,
                                        latest=latest,
                                        chart_white_monthly = chart_white_monthly,
                                        chart_red_monthly = chart_red_monthly,
                                        chart_white_yearly = chart_white_yearly,
                                        chart_red_yearly = chart_red_yearly
                                        )

            return render_template('search.html', number=number, 
                                    white_occurrences=white_occurrences, 
                                    white_percentage=white_percentage, 
                                    earliest=earliest,
                                    latest=latest,
                                    white_droughts=white_droughts,
                                    white_streaks=white_streaks,
                                    chart_white_monthly = chart_white_monthly,
                                    chart_white_yearly = chart_white_yearly
                                    )
    
    return render_template('search.html', number=number)


@powerball.route('/winning_hands_white', methods=['POST', 'GET'])
def winning_hands_white():
    return render_template('winning_hands.html')

@powerball.route('/winning_hands_red', methods=['POST', 'GET'])
def winning_hands_red():
    return render_template('winning_hands_red.html')

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [7, 7, 4, 7, 9, 4, 6, 6, 10, 3, 
                       8, 5, 2, 5, 5, 4, 2, 4, 8, 3, 
                       8, 3, 6, 5, 4, 4, 8, 2, 6, 7, 
                       10, 6, 11, 5, 5, 7, 7, 7, 8, 5, 
                       2, 5, 6, 6, 11, 5, 6, 6, 3, 3, 
                       5, 5, 5, 5, 6, 6, 7, 4, 6, 5, 
                       4, 4, 3, 10, 2, 5, 8, 7, 12
                    ]
    white_numbers_trends = [4, 4, 1, 1, 1, 0, 2, 2, 2, 2, 
                            4, 3, 1, 3, 2, 2, 1, 2, 2, 1, 
                            6, 1, 0, 1, 3, 1, 3, 0, 2, 3, 
                            2, 2, 2, 2, 0, 0, 4, 1, 3, 1, 
                            1, 0, 3, 1, 5, 2, 1, 2, 0, 0, 
                            1, 3, 1, 0, 2, 1, 3, 0, 1, 2, 
                            0, 1, 2, 3, 2, 1, 3, 1, 1
                    ]
    red_numbers_6 = [2, 1, 3, 3, 3, 2, 4, 2, 6, 2, 
                     1, 2, 2, 4, 5, 3, 4, 0, 3, 7, 
                     8, 5, 1, 1, 3, 2
                    ]

    red_numbers_trends = [0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 
                          1, 0, 0, 2, 2, 1, 2, 0, 1, 4, 
                          2, 2, 0, 0, 1, 0
                         ]
    return render_template('trends.html',
                            white_numbers_6 = white_numbers_6,
                            white_numbers_trends = white_numbers_trends,
                            red_numbers_6 = red_numbers_6,
                            red_numbers_trends = red_numbers_trends
                          )

@powerball.route('/probabilities', methods=['POST', 'GET'])
def probabilities():
    draw = next_draw()
    white_numbers = [
                     7.22, 7.68, 7.90, 6.94, 6.67, 7.99, 7.01, 6.03, 6.87, 7.00, 
                     7.36, 7.92, 4.94, 6.45, 6.95, 7.22, 7.01, 7.23, 8.05, 7.17, 
                     9.49, 6.83, 8.55, 7.21, 6.60, 5.90, 8.47, 7.31, 5.78, 7.43, 
                     6.72, 9.08, 8.78, 6.14, 6.05, 8.62, 7.82, 7.42, 8.26, 6.95, 
                     6.40, 6.85, 6.74, 7.67, 7.36, 6.27, 7.91, 6.08, 5.44, 6.34, 
                     6.35, 7.15, 8.11, 7.53, 6.77, 7.34, 6.99, 6.85, 8.33, 6.23, 
                     8.53, 8.05, 8.70, 8.20, 6.02, 7.13, 7.17, 7.33, 9.14
                     ]
    red_numbers = [
                   3.35, 3.68, 3.93, 4.74, 4.18, 4.16, 3.71, 3.52, 4.14, 3.81, 
                   3.62, 2.78, 3.76, 4.66, 3.35, 3.13, 3.47, 4.42, 3.96, 3.71, 
                   4.64, 3.31, 3.30, 4.32, 4.13, 4.22
                   ]
    return render_template('probabilities.html', 
                            draw=draw,
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    draw = next_draw()
    white_numbers = [
                     [12, 21, 36, 53, 61], 
                     [8, 30, 37, 49, 59], 
                     [10, 17, 28, 40, 43], 
                     [6, 27, 52, 54, 55], 
                     [3, 11, 45, 64, 67]
                     ]
    red_numbers = [4, 14, 22, 7, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )