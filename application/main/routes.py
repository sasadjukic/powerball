

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
    white_numbers_6 = [7, 8, 4, 7, 9, 4, 6, 5, 11, 3, 
                       8, 4, 2, 5, 5, 4, 2, 4, 8, 4, 
                       7, 4, 6, 5, 4, 5, 7, 2, 6, 8, 
                       10, 5, 11, 5, 5, 7, 7, 7, 8, 4, 
                       2, 5, 6, 6, 10, 5, 7, 5, 3, 3, 
                       4, 5, 6, 5, 7, 6, 7, 4, 6, 5, 
                       4, 5, 3, 10, 2, 5, 7, 7, 12
                    ]
    white_numbers_trends = [4, 4, 1, 2, 1, 0, 2, 2, 2, 2, 
                            4, 2, 1, 3, 2, 2, 1, 2, 2, 1, 
                            5, 1, 0, 1, 3, 1, 2, 0, 2, 3, 
                            2, 1, 2, 3, 1, 0, 4, 2, 3, 0, 
                            1, 1, 3, 1, 4, 3, 1, 2, 0, 0, 
                            0, 3, 2, 0, 2, 1, 3, 0, 1, 2, 
                            0, 1, 2, 3, 2, 1, 2, 1, 2
                    ]
    red_numbers_6 = [2, 1, 3, 3, 3, 2, 4, 2, 6, 2, 
                     1, 2, 2, 4, 4, 3, 3, 0, 3, 7, 
                     9, 5, 2, 1, 3, 2
                    ]

    red_numbers_trends = [0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 
                          1, 0, 0, 2, 1, 1, 1, 0, 2, 4, 
                          2, 3, 0, 0, 1, 0
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
                     6.77, 7.91, 7.42, 6.54, 6.27, 7.05, 6.27, 6.92, 7.00, 7.04, 
                     7.71, 7.70, 5.22, 6.67, 7.22, 7.25, 6.40, 6.94, 7.86, 7.83, 
                     8.81, 7.23, 8.21, 6.86, 6.33, 6.02, 9.18, 7.42, 6.62, 6.95, 
                     6.99, 8.31, 8.43, 6.16, 6.40, 8.80, 8.23, 6.89, 8.42, 7.32, 
                     6.28, 7.07, 6.41, 7.79, 7.42, 6.14, 8.24, 6.57, 5.79, 6.62, 
                     6.67, 6.60, 7.62, 7.20, 6.81, 7.40, 7.14, 6.58, 8.01, 6.18, 
                     9.28, 8.18, 8.61, 7.99, 6.14, 7.54, 7.83, 7.5, 8.82
                     ]
    red_numbers = [
                   3.42, 3.24, 3.90, 5.12, 4.31, 3.82, 3.51, 3.76, 4.04, 3.58, 
                   3.75, 2.83, 3.78, 4.43, 3.08, 3.09, 3.61, 4.86, 3.52, 3.71, 
                   4.74, 3.33, 3.75, 4.63, 4.02, 4.17
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
                     [12, 27, 37, 42, 54], 
                     [8, 23, 43, 48, 57], 
                     [1, 36, 53, 63, 64], 
                     [14, 18, 30, 60, 69], 
                     [2, 25, 29, 47, 58]
                     ]
    red_numbers = [3, 10, 15, 5, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )