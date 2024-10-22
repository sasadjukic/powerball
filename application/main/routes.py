

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
    white_numbers_6 = [7, 7, 4, 7, 9, 4, 6, 5, 11, 3, 
                       8, 5, 2, 5, 4, 5, 2, 4, 8, 4, 
                       7, 4, 6, 5, 4, 5, 6, 2, 5, 8, 
                       10, 5, 12, 5, 5, 7, 7, 7, 8, 4, 
                       2, 5, 6, 6, 10, 5, 7, 5, 3, 3, 
                       4, 6, 6, 5, 7, 6, 7, 4, 6, 5, 
                       4, 5, 3, 10, 2, 5, 7, 7, 12
                    ]
    white_numbers_trends = [4, 3, 1, 2, 2, 0, 2, 2, 2, 2, 
                            4, 2, 1, 3, 1, 2, 1, 2, 2, 1, 
                            5, 1, 0, 1, 3, 1, 1, 0, 1, 3, 
                            2, 1, 3, 3, 1, 0, 4, 2, 2, 0, 
                            1, 1, 3, 1, 4, 3, 2, 2, 0, 1, 
                            0, 3, 2, 0, 2, 1, 3, 0, 1, 2, 
                            0, 1, 2, 4, 2, 1, 2, 1, 2
                    ]
    red_numbers_6 = [3, 1, 3, 3, 3, 2, 4, 2, 6, 2, 
                     1, 2, 2, 4, 4, 3, 3, 0, 3, 6, 
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
                     6.61, 7.18, 7.64, 6.40, 6.72, 7.43, 6.62, 5.98, 7.16, 7.35, 7.76, 
                     7.10, 5.34, 6.66, 6.71, 8.08, 6.91, 6.77, 8.19, 7.23, 9.21, 7.07, 
                     8.07, 7.33, 7.05, 5.85, 9.09, 7.32, 5.69, 7.27, 6.57, 8.56, 8.92, 
                     6.01, 6.52, 8.66, 8.73, 6.82, 8.53, 7.34, 6.69, 6.65, 6.50, 7.23, 
                     6.81, 6.02, 8.08, 6.46, 5.45, 6.78, 6.82, 6.88, 7.52, 7.23, 7.15, 
                     6.97, 7.39, 6.81, 8.07, 6.42, 9.20, 8.00, 8.39, 8.32, 6.23, 7.03, 
                     7.54, 7.80, 9.11
                     ]
    red_numbers = [
                   3.78, 3.22, 4.06, 4.81, 4.17, 4.14, 3.41, 3.35, 4.31, 4.04, 
                   3.54, 2.86, 3.65, 4.72, 3.18, 3.24, 3.26, 4.31, 3.93, 3.53, 
                   4.73, 3.45, 3.52, 4.35, 4.13, 4.31
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
                     [14, 22, 29, 36, 58], 
                     [3, 20, 49, 53, 64], 
                     [18, 30, 43, 62, 69], 
                     [7, 16, 31, 54, 57], 
                     [5, 21, 25, 40, 42]
                     ]
    red_numbers = [1, 10, 14, 4, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )