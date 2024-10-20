

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
    white_numbers_6 = [6, 7, 4, 8, 9, 4, 6, 5, 11, 3, 
                       8, 5, 2, 5, 4, 5, 2, 4, 8, 4, 
                       7, 4, 6, 5, 3, 5, 6, 2, 5, 8, 
                       10, 5, 12, 5, 6, 7, 7, 7, 8, 4, 
                       3, 5, 6, 7, 10, 5, 7, 5, 3, 3, 
                       4, 6, 6, 5, 7, 6, 6, 5, 6, 5, 
                       4, 4, 3, 9, 2, 5, 7, 7, 12
                    ]
    white_numbers_trends = [3, 4, 1, 3, 2, 0, 2, 2, 2, 2, 
                            4, 2, 1, 3, 1, 2, 1, 2, 2, 1, 
                            5, 1, 1, 1, 2, 1, 1, 0, 1, 3, 
                            2, 1, 3, 3, 1, 0, 4, 2, 2, 0, 
                            1, 1, 3, 1, 4, 3, 2, 2, 0, 1, 
                            0, 3, 2, 0, 2, 1, 2, 0, 1, 2, 
                            0, 0, 2, 3, 2, 1, 2, 2, 3
                    ]
    red_numbers_6 = [3, 1, 3, 3, 3, 2, 4, 2, 6, 2, 
                     1, 2, 2, 4, 3, 3, 3, 0, 3, 6, 
                     9, 5, 2, 1, 4, 2
                    ]

    red_numbers_trends = [0, 0, 2, 0, 1, 1, 1, 0, 0, 
                          1, 1, 0, 0, 2, 1, 1, 1, 0, 
                          2, 4, 2, 3, 0, 0, 1, 0
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
                     6.95, 7.14, 7.97, 6.77, 7.13, 6.85, 7.02, 6.71, 7.34, 7.41, 7.09, 
                     7.43, 5.46, 6.43, 6.87, 7.22, 6.75, 7.42, 7.47, 7.49, 8.97, 6.55, 
                     8.28, 7.25, 6.44, 6.06, 8.67, 7.49, 5.98, 6.85, 7.24, 8.42, 8.04, 
                     6.13, 6.42, 8.42, 8.25, 7.10, 8.32, 7.36, 6.51, 7.22, 6.46, 7.70, 
                     7.44, 6.16, 7.45, 6.06, 5.31, 7.18, 6.34, 6.73, 8.23, 6.99, 7.06, 
                     7.32, 7.18, 6.37, 7.76, 5.96, 9.73, 8.36, 8.23, 8.45, 6.59, 7.30, 
                     7.78, 7.66, 9.31
                     ]
    red_numbers = [
                   3.50, 3.42, 4.14, 4.87, 4.37, 3.69, 3.43, 3.55, 4.10, 3.75, 3.83, 
                   3.33, 3.74, 4.84, 3.24, 2.70, 3.33, 4.88, 3.95, 3.57, 4.73, 3.26, 
                   3.44, 4.52, 3.89, 3.93
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
                     [12, 27, 43, 53, 60], 
                     [8, 37, 54, 57, 61], 
                     [22, 33, 49, 65, 67], 
                     [3, 17, 50, 55, 58], 
                     [1, 11, 15, 30, 39]
                     ]
    red_numbers = [5, 10, 7, 18, 9]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )