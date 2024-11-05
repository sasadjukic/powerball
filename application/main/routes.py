

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
    winning_hands = {
                     'singles': [183, 13, 6], 'pairs': [572, 45, 16], 
                     'two_pairs': [212, 15, 2], 'three_of_set': [119, 7, 0], 
                     'full_house': [15, 0, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 6, 0], 10: [68, 5, 1], 20: [99, 8, 3], 30: [95, 9, 2], 
                  40: [64, 5, 2], 50: [81, 6, 0], 60: [93, 6, 1]}
    total_pairs = sum(values[0] for values in pair_count.values())
    total_pairs_6 = sum(values[1] for values in pair_count.values())
    total_pairs_recent = sum(values[2] for values in pair_count.values())

    return render_template('winning_hands.html',
                           winning_hands=winning_hands,
                           total_winning_hands=total_winning_hands,
                           total_winning_hands_6=total_winning_hands_6,
                           total_winning_hands_recent=total_winning_hands_recent, 
                           pair_count=pair_count, 
                           total_pairs=total_pairs,
                           total_pairs_6=total_pairs_6,
                           total_pairs_recent=total_pairs_recent
                           )

@powerball.route('/winning_hands_red', methods=['POST', 'GET'])
def winning_hands_red():
    return render_template('winning_hands_red.html')

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [6, 7, 4, 7, 9, 5, 6, 6, 10, 4, 
                       6, 5, 3, 5, 5, 4, 2, 5, 7, 3, 
                       7, 4, 6, 5, 4, 4, 8, 2, 7, 7, 
                       10, 6, 12, 5, 5, 7, 7, 6, 8, 5, 
                       2, 5, 7, 6, 12, 5, 5, 8, 3, 3, 
                       5, 5, 6, 5, 6, 6, 7, 6, 6, 5, 
                       5, 4, 3, 10, 2, 5, 7, 6, 11
                    ]
    white_numbers_trends = [3, 4, 1, 1, 1, 1, 1, 2, 2, 2, 
                            4, 3, 2, 2, 2, 1, 1, 3, 2, 1, 
                            4, 2, 0, 1, 3, 1, 3, 0, 3, 3, 
                            2, 2, 2, 1, 0, 0, 3, 1, 3, 1, 
                            1, 0, 4, 1, 6, 2, 1, 4, 0, 0, 
                            1, 3, 2, 0, 1, 1, 2, 2, 0, 1, 
                            1, 1, 1, 3, 2, 1, 3, 1, 1
                    ]
    red_numbers_6 = [2, 2, 3, 3, 3, 2, 4, 2, 6, 2, 
                     1, 2, 2, 3, 4, 3, 4, 0, 3, 7, 
                     9, 6, 1, 1, 3, 2
                    ]

    red_numbers_trends = [0, 1, 2, 0, 0, 1, 1, 0, 0, 1, 
                          1, 0, 0, 2, 2, 1, 2, 0, 1, 2, 
                          3, 3, 0, 0, 1, 0
                         ]
    return render_template('trends.html',
                            white_numbers_6 = white_numbers_6,
                            white_numbers_trends = white_numbers_trends,
                            red_numbers_6 = red_numbers_6,
                            red_numbers_trends = red_numbers_trends
                          )

@powerball.route('/probabilities', methods=['POST', 'GET'])
def probabilities():
    draw = next_draw().strftime('%m-%d-%Y')
    white_numbers = [
                     6.99, 7.53, 7.64, 6.55, 6.62, 6.98, 6.66, 6.25, 7.07, 7.25, 
                     7.43, 7.53, 5.23, 6.57, 6.81, 7.52, 7.17, 7.14, 7.58, 6.92, 
                     8.95, 6.90, 8.15, 7.35, 6.59, 6.28, 8.43, 7.64, 6.26, 7.18, 
                     7.14, 8.42, 8.82, 6.03, 6.26, 8.83, 8.22, 7.21, 8.72, 6.68, 
                     6.57, 6.61, 6.57, 7.98, 7.50, 6.60, 8.41, 6.22, 5.78, 7.21, 
                     6.17, 6.61, 8.16, 7.25, 6.68, 6.99, 6.83, 6.15, 8.20, 6.12, 
                     9.51, 7.73, 8.09, 8.41, 6.43, 7.34, 7.79, 7.81, 8.78
                     ]
    red_numbers = [
                   3.64, 3.54, 4.02, 4.72, 4.03, 3.27, 3.51, 3.29, 4.42, 4.01, 
                   3.79, 2.85, 4.05, 4.72, 3.26, 3.19, 3.44, 4.99, 3.63, 3.79, 
                   4.80, 3.34, 3.35, 4.16, 4.06, 4.13
                   ]
    return render_template('probabilities.html', 
                            draw=draw,
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    draw = next_draw().strftime('%m-%d-%Y')
    white_numbers = [
                     [26, 33, 36, 53, 69], 
                     [7, 21, 28, 51, 57], 
                     [14, 37, 48, 50, 61], 
                     [6, 8, 17, 32, 63], 
                     [1, 26, 49, 66, 67]
                     ]
    red_numbers = [2, 14, 4, 18, 9]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )