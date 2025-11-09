

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
              'all-time': [3102, 3159, 6345],
              'six-months': [200, 192, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [804, 883, 942, 950, 880, 894, 992, 6345],
            'six-months' : [53, 58, 59, 53, 59, 49, 69, 400],
            'recent-trends' : [16, 20, 17, 14, 19, 16, 28, 130]
    }

    winning_hands = {
                     'singles': [208, 15, 4], 'pairs': [654, 40, 13], 
                     'two_pairs': [239, 15, 5], 'three_of_set': [138, 8, 2], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 6, 2], 20: [115, 8, 1], 30: [102, 2, 0], 
                  40: [80, 10, 5], 50: [91, 5, 3], 60: [105, 7, 2]
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
              'all-time': [628, 641, 1269],
              'six-months': [36, 44, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [449, 461, 359, 1269],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [7, 15, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 7, 4, 3, 7, 8, 6, 4, 
                       5, 5, 7, 6, 8, 8, 5, 6, 4, 2, 
                       3, 4, 9, 5, 5, 2, 7, 12, 10, 3, 
                       6, 8, 6, 7, 8, 3, 7, 2, 3, 9, 
                       3, 7, 10, 7, 5, 3, 4, 6, 5, 7, 
                       4, 9, 9, 5, 2, 1, 3, 4, 5, 7, 
                       10, 10, 3, 9, 6, 6, 8, 4, 6
                    ]

    white_numbers_trends = [
                        1, 3, 6, 1, 0, 0, 2, 2, 1, 3, 
                        1, 1, 3, 2, 3, 2, 3, 2, 0, 1, 
                        0, 2, 0, 2, 0, 1, 3, 4, 4, 1, 
                        1, 6, 0, 1, 0, 0, 2, 1, 2, 2, 
                        0, 3, 3, 2, 2, 1, 2, 1, 3, 2, 
                        1, 2, 4, 3, 1, 0, 1, 1, 1, 4, 
                        2, 3, 0, 3, 2, 6, 5, 2, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 4, 5, 1, 0, 2, 2, 2, 
                     4, 3, 2, 3, 4, 1, 2, 3, 4, 5, 
                     4, 5, 2, 3, 7, 1
                    ]

    red_numbers_trends = [
                          2, 1, 1, 2, 1, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 3, 1, 0, 1, 3, 2, 
                          0, 1, 0, 0, 0, 1
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
                     7.03, 7.24, 7.89, 6.93, 6.31, 7.66, 6.40, 6.69, 6.93, 7.08, 
                     7.40, 7.82, 5.27, 6.52, 6.81, 7.81, 6.62, 6.54, 7.22, 6.46, 
                     9.03, 7.05, 8.67, 7.33, 6.66, 5.54, 7.99, 8.32, 6.81, 7.32, 
                     7.51, 8.57, 8.52, 5.99, 7.16, 8.44, 8.13, 6.61, 7.45, 7.15, 
                     6.40, 6.70, 6.99, 8.08, 8.03, 5.81, 7.66, 6.49, 5.81, 7.24, 
                     6.34, 7.50, 8.40, 6.51, 6.87, 6.41, 6.81, 6.51, 7.63, 7.07, 
                     9.43, 8.09, 8.37, 8.73, 6.58, 7.47, 7.90, 7.10, 8.19
                     ]
    red_numbers = [
                   4.09, 3.42, 3.73, 5.08, 4.11, 3.40, 3.41, 3.67, 4.40, 3.62, 
                   3.57, 3.11, 3.52, 4.35, 3.17, 3.04, 3.18, 4.52, 4.02, 4.38, 
                   4.64, 3.55, 3.02, 4.73, 4.57, 3.70
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
                     [1, 5, 14, 43, 55],
                     [3, 7, 15, 32, 65],
                     [2, 16, 44, 47, 50],
                     [23, 31, 36, 51, 57],
                     [13, 34, 41, 42, 53]
                     ]
    red_numbers = [6, 7, 10, 11, 12]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )