

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
              'all-time': [3288, 3338, 6715],
              'six-months': [197, 198, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [854, 935, 1000, 1000, 925, 963, 1038, 6715],
            'six-months' : [55, 54, 61, 52, 51, 72, 55, 400],
            'recent-trends' : [17, 23, 14, 17, 20, 22, 17, 130]
    }

    winning_hands = {
                     'singles': [223, 16, 6], 'pairs': [698, 48, 14], 
                     'two_pairs': [249, 10, 3], 'three_of_set': [141, 4, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 5], 20: [120, 5, 2], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 10, 2], 60: [112, 9, 1]
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
              'all-time': [662, 681, 1343],
              'six-months': [36, 44, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [477, 480, 386, 1343],
            'six-months' : [29, 21, 30, 80],
            'recent-trends' : [11, 5, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 4, 8, 6, 8, 9, 8, 6, 4, 4, 
                       7, 3, 3, 5, 2, 5, 6, 11, 8, 5, 
                       8, 3, 4, 7, 4, 5, 6, 13, 6, 6, 
                       7, 5, 6, 3, 5, 9, 3, 3, 5, 5, 
                       4, 6, 9, 3, 2, 3, 8, 5, 6, 4, 
                       10, 10, 7, 4, 4, 8, 8, 9, 8, 7, 
                       4, 6, 9, 9, 5, 5, 1, 5, 4
                    ]

    white_numbers_trends = [
                        0, 1, 4, 2, 0, 3, 5, 0, 2, 2, 
                        3, 2, 2, 2, 0, 1, 4, 5, 2, 1, 
                        3, 1, 1, 3, 1, 0, 1, 2, 1, 3, 
                        2, 1, 1, 0, 1, 5, 1, 2, 1, 0, 
                        3, 5, 3, 0, 1, 1, 5, 0, 2, 2, 
                        1, 5, 1, 1, 2, 3, 3, 1, 3, 1, 
                        2, 2, 4, 4, 1, 0, 1, 1, 1
                    ]

    red_numbers_6 = [
                     9, 5, 3, 2, 3, 5, 2, 0, 0, 1, 
                     3, 2, 1, 4, 3, 1, 2, 2, 2, 5, 
                     4, 2, 8, 4, 1, 6
                    ]

    red_numbers_trends = [
                          4, 2, 2, 0, 1, 2, 0, 0, 0, 0, 
                          1, 1, 1, 0, 2, 0, 0, 0, 0, 3, 
                          1, 0, 0, 2, 1, 3
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
                     6.89, 6.81, 8.46, 6.53, 6.55, 7.59, 6.71, 6.63, 6.95, 6.49, 
                     7.67, 7.76, 5.49, 6.37, 6.48, 7.46, 7.42, 7.54, 7.59, 7.27, 
                     8.69, 6.79, 8.74, 6.82, 6.10, 5.68, 8.86, 9.18, 6.99, 7.14, 
                     6.98, 8.04, 8.30, 6.11, 6.52, 8.41, 7.93, 6.57, 8.36, 7.62, 
                     6.59, 6.53, 7.08, 7.51, 7.51, 6.06, 8.09, 6.29, 6.20, 6.92, 
                     6.75, 7.77, 7.99, 7.22, 6.83, 7.27, 6.52, 6.33, 8.20, 6.91, 
                     8.64, 8.18, 8.03, 8.33, 6.29, 7.10, 7.16, 6.84, 8.37
                     ]
    red_numbers = [
                   4.37, 3.92, 3.85, 5.11, 4.30, 3.82, 3.39, 3.44, 4.06, 3.37, 
                   3.66, 3.32, 3.61, 4.66, 3.23, 2.61, 3.31, 4.08, 3.52, 3.77, 
                   4.69, 3.25, 3.70, 4.48, 4.41, 4.07
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
                     [10, 20, 28, 47, 50],
                     [11, 24, 25, 33, 61],
                     [3, 53, 55, 59, 64],
                     [15, 19, 44, 53, 54],
                     [2, 13, 16, 33, 51]
                     ]
    red_numbers = [1, 4, 8, 13, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )