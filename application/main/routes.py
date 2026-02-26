

from flask import render_template, Blueprint, request
from application.data.main_data import latest, earliest, next_draw
from application.data.user_search import (generate_percentage, white_balls, red_balls,
                                          get_streak, get_drought,
                                          get_red_drought, get_red_streak,
                                          monthly_number, monthly_number_red,
                                          yearly_number, yearly_number_red)
from application.data.matrix_data import m_data
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
        # Get user input for a powerball number they want to search
        number = int(request.form['number_input'])

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
    splits = {
              'all-time': [3225, 3268, 6580],
              'six-months': [206, 191, 400],
              'recent-trends': [65, 63, 130]
            }

    sets = {
            'all-time' : [836, 912, 985, 982, 905, 940, 1020, 6580],
            'six-months' : [52, 55, 69, 49, 48, 64, 63, 400],
            'recent-trends' : [16, 16, 26, 15, 16, 25, 16, 130]
    }

    winning_hands = {
                     'singles': [216, 13, 2], 'pairs': [684, 48, 17], 
                     'two_pairs': [246, 13, 5], 'three_of_set': [138, 2, 0], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [86, 4, 1], 20: [118, 7, 3], 30: [106, 4, 1], 
                  40: [83, 8, 2], 50: [99, 11, 4], 60: [111, 10, 4]
                }
    total_pairs = sum(values[0] for values in pair_count.values())
    total_pairs_6 = sum(values[1] for values in pair_count.values())
    total_pairs_recent = sum(values[2] for values in pair_count.values())

    return render_template('winning_hands.html',
                           splits=splits,
                           sets=sets,
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
    splits = {
              'all-time': [647, 669, 1316],
              'six-months': [33, 47, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [466, 474, 376, 1316],
            'six-months' : [26, 30, 24, 80],
            'recent-trends' : [9, 8, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 10, 4, 8, 5, 5, 9, 3, 5, 
                       6, 3, 4, 5, 5, 8, 3, 9, 7, 4, 
                       5, 6, 5, 5, 4, 6, 9, 16, 9, 4, 
                       6, 9, 6, 5, 3, 4, 5, 2, 5, 7, 
                       3, 4, 6, 5, 3, 3, 5, 6, 6, 4, 
                       9, 7, 11, 5, 3, 5, 5, 9, 6, 8, 
                       6, 6, 5, 10, 4, 9, 5, 5, 5
                    ]

    white_numbers_trends = [
                        0, 2, 1, 1, 5, 3, 0, 3, 1, 0, 
                        4, 0, 0, 1, 1, 2, 0, 4, 4, 1, 
                        5, 1, 2, 3, 1, 1, 5, 5, 2, 1, 
                        2, 0, 2, 2, 2, 2, 2, 1, 1, 4, 
                        0, 1, 2, 0, 1, 1, 1, 4, 2, 1, 
                        4, 2, 3, 1, 2, 4, 2, 5, 1, 4, 
                        1, 0, 4, 4, 1, 1, 0, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 4, 3, 2, 0, 1, 2, 
                     2, 3, 0, 6, 4, 2, 4, 2, 5, 3, 
                     3, 4, 8, 2, 1, 3
                    ]

    red_numbers_trends = [
                          1, 1, 0, 2, 2, 3, 0, 0, 0, 0, 
                          1, 1, 0, 3, 1, 0, 1, 1, 0, 0, 
                          2, 0, 4, 2, 0, 1
                         ]
                         
    return render_template('trends.html',
                            white_numbers_6 = white_numbers_6,
                            white_numbers_trends = white_numbers_trends,
                            red_numbers_6 = red_numbers_6,
                            red_numbers_trends = red_numbers_trends
                          )

@powerball.route('/powerball_matrix', methods=['POST', 'GET'])
def powerball_matrix():
    number = None
    if request.method == 'POST':
        # Get user input for a powerball number they want to search
        number = int(request.form['matrix-input'])

    return render_template('powerball_matrix.html', 
                            number=number, 
                            m_data=m_data
                            )

@powerball.route('/fun_facts', methods=['POST', 'GET'])
def fun_facts():
    return render_template('fun_facts.html')

@powerball.route('/probabilities', methods=['POST', 'GET'])
def probabilities():
    draw = next_draw().strftime('%m-%d-%Y')
    white_numbers = [
                     7.25, 7.24, 8.15, 6.48, 6.38, 7.37, 6.78, 6.80, 7.19, 6.84, 
                     7.30, 7.66, 5.12, 6.64, 7.32, 7.40, 7.00, 6.89, 7.73, 7.46, 
                     8.65, 6.70, 8.85, 7.68, 6.59, 5.49, 8.59, 8.78, 6.97, 6.59, 
                     7.52, 8.06, 8.57, 6.14, 7.04, 8.13, 8.24, 6.36, 7.84, 7.74, 
                     6.29, 6.34, 6.81, 8.06, 7.32, 6.25, 7.49, 6.44, 5.55, 7.07, 
                     6.68, 7.63, 8.24, 7.06, 6.45, 7.01, 7.11, 6.88, 7.51, 6.87, 
                     9.02, 8.34, 8.60, 7.56, 6.02, 6.86, 7.44, 6.91, 8.66
                     ]
    red_numbers = [
                   4.56, 3.75, 4.17, 5.02, 4.02, 3.83, 3.35, 3.26, 3.82, 3.41, 
                   3.50, 3.44, 3.19, 4.71, 3.25, 2.81, 3.13, 4.29, 3.84, 4.17, 
                   4.64, 3.65, 3.67, 4.74, 4.16, 3.62
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
                     [23, 35, 50, 57, 67],
                     [24, 37, 44, 52, 60],
                     [11, 21, 29, 40, 49],
                     [27, 47, 48, 61, 65],
                     [25, 28, 46, 59, 69]
                     ]
    red_numbers = [1, 13, 19, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )