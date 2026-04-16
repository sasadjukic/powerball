

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
              'all-time': [3274, 3323, 6685],
              'six-months': [198, 198, 400],
              'recent-trends': [60, 69, 130]
            }

    sets = {
            'all-time' : [851, 932, 996, 991, 922, 960, 1033, 6685],
            'six-months' : [54, 58, 60, 49, 50, 73, 56, 400],
            'recent-trends' : [17, 24, 15, 11, 20, 27, 16, 130]
    }

    winning_hands = {
                     'singles': [221, 16, 5], 'pairs': [696, 49, 14], 
                     'two_pairs': [248, 9, 3], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 2, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 9, 5], 20: [118, 3, 1], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 11, 2], 60: [112, 9, 2]
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
              'all-time': [658, 679, 1337],
              'six-months': [35, 45, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [474, 478, 385, 1337],
            'six-months' : [26, 25, 29, 80],
            'recent-trends' : [11, 4, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 9, 8, 6, 3, 5, 
                       8, 4, 5, 6, 2, 5, 5, 11, 7, 5, 
                       8, 4, 4, 5, 3, 5, 7, 14, 5, 5, 
                       6, 6, 5, 4, 4, 6, 4, 4, 5, 6, 
                       4, 6, 9, 3, 2, 2, 8, 5, 5, 4, 
                       9, 11, 7, 5, 4, 8, 7, 10, 8, 8, 
                       3, 5, 8, 9, 5, 6, 2, 5, 5
                    ]

    white_numbers_trends = [
                        0, 1, 3, 1, 1, 4, 5, 0, 2, 2, 
                        4, 2, 2, 2, 0, 2, 3, 5, 2, 2, 
                        3, 1, 2, 1, 0, 0, 2, 3, 1, 2, 
                        1, 0, 1, 0, 1, 3, 1, 2, 0, 0, 
                        3, 5, 3, 0, 1, 0, 5, 1, 2, 3, 
                        0, 6, 1, 3, 2, 5, 2, 2, 3, 1, 
                        1, 1, 3, 5, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     8, 4, 2, 2, 3, 5, 2, 0, 0, 2, 
                     2, 4, 1, 4, 4, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 5
                    ]

    red_numbers_trends = [
                          4, 1, 1, 0, 1, 4, 0, 0, 0, 1, 
                          0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 
                          2, 0, 1, 2, 1, 2
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
                     6.58, 6.80, 7.61, 6.58, 7.07, 7.91, 6.96, 7.01, 7.48, 6.60, 
                     7.53, 7.37, 5.70, 7.09, 6.71, 7.35, 6.95, 7.60, 7.44, 7.51, 
                     9.07, 6.65, 8.30, 7.03, 6.11, 5.69, 8.76, 8.55, 6.43, 6.94, 
                     7.40, 8.18, 8.50, 6.14, 6.25, 8.41, 7.67, 6.41, 8.16, 7.29, 
                     6.56, 6.49, 7.39, 7.79, 7.30, 6.09, 7.90, 6.13, 6.23, 7.22, 
                     6.69, 8.11, 8.33, 6.81, 6.75, 7.17, 6.95, 6.69, 7.95, 6.58, 
                     8.52, 8.76, 8.25, 8.71, 6.24, 6.94, 6.87, 6.67, 8.12
                     ]
    red_numbers = [
                   4.39, 3.86, 3.84, 4.63, 4.37, 3.47, 3.35, 3.66, 4.24, 3.52, 
                   3.20, 3.48, 3.32, 4.70, 3.49, 2.87, 2.99, 4.56, 3.67, 4.23, 
                   4.96, 3.04, 3.68, 5.02, 4.01, 3.43
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
                     [5, 27, 35, 38, 61],
                     [25, 32, 48, 56, 66],
                     [11, 17, 49, 51, 63],
                     [12, 17, 38, 47, 54],
                     [2, 23, 28, 30, 59]
                     ]
    red_numbers = [1, 2, 4, 12, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )