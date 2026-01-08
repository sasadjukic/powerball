

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
              'all-time': [3174, 3216, 6475],
              'six-months': [206, 188, 400],
              'recent-trends': [72, 57, 130]
            }

    sets = {
            'all-time' : [821, 903, 964, 969, 891, 921, 1006, 6475],
            'six-months' : [53, 61, 59, 53, 51, 54, 69, 400],
            'recent-trends' : [17, 20, 22, 19, 11, 27, 14, 130]
    }

    winning_hands = {
                     'singles': [215, 16, 7], 'pairs': [670, 43, 16], 
                     'two_pairs': [242, 13, 3], 'three_of_set': [138, 6, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [78, 2, 2], 10: [86, 5, 2], 20: [115, 5, 0], 30: [105, 4, 3], 
                  40: [81, 9, 1], 50: [97, 9, 6], 60: [107, 8, 2]
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
              'all-time': [636, 659, 1295],
              'six-months': [32, 48, 80], 
              'recent-trends': [8, 18, 26]
            }

    sets = {
            'all-time' : [457, 467, 371, 1295],
            'six-months' : [27, 26, 27, 80],
            'recent-trends' : [8, 6, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 9, 7, 4, 4, 7, 11, 4, 5, 
                       7, 4, 4, 6, 8, 8, 3, 10, 6, 3, 
                       3, 5, 5, 6, 5, 5, 5, 15, 7, 3, 
                       7, 9, 8, 6, 6, 4, 3, 3, 4, 7, 
                       3, 4, 7, 6, 4, 4, 5, 5, 6, 5, 
                       8, 5, 11, 5, 1, 2, 5, 6, 6, 6, 
                       8, 9, 4, 8, 6, 8, 6, 5, 9
                    ]

    white_numbers_trends = [
                        2, 0, 1, 3, 3, 2, 3, 3, 0, 2, 
                        2, 1, 1, 2, 2, 2, 0, 5, 3, 2, 
                        2, 1, 1, 2, 2, 3, 0, 7, 2, 2, 
                        3, 3, 3, 2, 1, 2, 0, 1, 2, 1, 
                        1, 0, 1, 2, 0, 1, 2, 2, 1, 1, 
                        5, 3, 4, 1, 0, 2, 3, 4, 4, 1, 
                        0, 2, 2, 1, 1, 2, 0, 2, 3
                    ]

    red_numbers_6 = [
                     6, 6, 3, 3, 4, 0, 2, 1, 2, 2, 
                     1, 2, 0, 5, 3, 2, 3, 3, 5, 4, 
                     3, 5, 8, 1, 3, 3
                    ]

    red_numbers_trends = [
                          3, 2, 1, 0, 0, 0, 2, 0, 0, 0, 
                          0, 0, 0, 2, 0, 1, 1, 0, 2, 1, 
                          2, 1, 6, 0, 0, 2
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
                     7.22, 7.22, 7.66, 6.42, 6.58, 7.04, 6.56, 7.24, 6.58, 7.13, 
                     6.78, 8.01, 5.44, 6.39, 7.04, 7.26, 7.28, 6.87, 7.76, 7.05, 
                     8.61, 6.85, 8.33, 7.31, 6.36, 5.91, 8.08, 8.75, 6.64, 6.76, 
                     6.89, 9.10, 8.08, 5.91, 6.92, 8.58, 8.20, 6.89, 8.07, 7.53, 
                     6.51, 6.60, 6.85, 7.92, 7.58, 5.93, 7.94, 6.54, 5.85, 7.00, 
                     6.42, 6.91, 8.85, 7.14, 6.44, 7.04, 7.18, 6.62, 7.86, 6.53, 
                     9.23, 8.31, 7.94, 8.26, 5.99, 8.01, 7.57, 7.26, 8.42
                     ]
    red_numbers = [
                   4.21, 3.77, 3.73, 4.64, 4.05, 3.70, 3.61, 3.64, 4.14, 3.29, 
                   3.39, 3.65, 3.65, 4.78, 3.14, 3.16, 3.07, 4.36, 3.66, 3.76, 
                   4.58, 3.63, 3.68, 4.62, 3.94, 4.15
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
                     [7, 17, 19, 28, 40],
                     [6, 27, 29, 38, 63],
                     [21, 31, 37, 45, 54],
                     [24, 32, 55, 58, 59],
                     [4, 8, 22, 23, 30]
                     ]
    red_numbers = [5, 15, 16, 19, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )