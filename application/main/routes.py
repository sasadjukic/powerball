

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
              'all-time': [3112, 3174, 6370],
              'six-months': [196, 196, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [808, 885, 944, 953, 885, 900, 995, 6370],
            'six-months' : [54, 55, 57, 53, 58, 52, 71, 400],
            'recent-trends' : [18, 19, 16, 14, 20, 17, 26, 130]
    }

    winning_hands = {
                     'singles': [210, 17, 5], 'pairs': [657, 39, 14], 
                     'two_pairs': [239, 14, 4], 'three_of_set': [138, 8, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 2, 1], 10: [84, 5, 2], 20: [115, 6, 1], 30: [102, 2, 0], 
                  40: [81, 10, 6], 50: [92, 6, 2], 60: [105, 7, 2]
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
              'all-time': [628, 646, 1274],
              'six-months': [34, 46, 80], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [449, 462, 363, 1274],
            'six-months' : [24, 27, 29, 80],
            'recent-trends' : [4, 15, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 6, 3, 5, 8, 8, 6, 4, 
                       5, 6, 7, 5, 6, 7, 5, 6, 4, 1, 
                       3, 4, 9, 4, 5, 2, 7, 12, 10, 2, 
                       7, 8, 7, 6, 8, 3, 7, 2, 3, 7, 
                       2, 5, 11, 8, 5, 3, 5, 6, 6, 8, 
                       6, 8, 9, 5, 2, 1, 4, 5, 4, 6, 
                       10, 10, 3, 9, 7, 7, 8, 5, 6
                    ]

    white_numbers_trends = [
                        1, 2, 6, 1, 0, 2, 3, 2, 1, 4, 
                        1, 2, 3, 1, 1, 2, 3, 2, 0, 1, 
                        0, 2, 0, 1, 0, 1, 3, 4, 4, 0, 
                        2, 5, 1, 1, 0, 0, 1, 1, 3, 2, 
                        0, 1, 4, 3, 1, 1, 3, 2, 3, 1, 
                        3, 2, 3, 2, 1, 0, 2, 2, 1, 4, 
                        2, 2, 0, 1, 3, 6, 4, 3, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 3, 5, 1, 0, 2, 2, 2, 
                     4, 3, 1, 3, 3, 1, 2, 3, 5, 4, 
                     4, 5, 5, 3, 7, 1
                    ]

    red_numbers_trends = [
                          1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 3, 1, 0, 1, 3, 1, 
                          1, 1, 3, 0, 0, 1
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
                     7.24, 7.13, 7.61, 7.03, 6.28, 7.45, 7.36, 6.63, 6.74, 6.45, 
                     6.96, 7.59, 5.73, 6.13, 6.54, 7.46, 7.13, 6.90, 7.41, 7.06, 
                     9.07, 6.27, 8.67, 6.52, 6.44, 5.86, 7.90, 8.14, 6.51, 7.38, 
                     7.22, 8.62, 9.04, 6.28, 6.71, 8.08, 8.72, 6.78, 8.26, 7.46, 
                     6.46, 7.11, 7.00, 8.11, 7.58, 6.21, 7.72, 6.47, 5.87, 7.08, 
                     6.53, 7.57, 7.91, 6.97, 6.52, 6.39, 6.97, 6.70, 7.87, 6.95, 
                     8.83, 8.63, 8.56, 8.24, 6.15, 7.47, 7.69, 7.46, 8.22
                     ]
    red_numbers = [
                   4.10, 3.79, 3.65, 4.95, 4.25, 3.59, 3.40, 3.36, 4.59, 3.45, 
                   3.69, 3.24, 3.82, 4.49, 3.23, 3.02, 3.14, 4.49, 3.87, 4.06, 
                   4.22, 3.40, 3.33, 4.34, 4.64, 3.89
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
                     [3, 10, 20, 22, 66],
                     [11, 13, 23, 29, 33],
                     [17, 25, 36, 55, 65],
                     [34, 35, 38, 63, 67],
                     [1, 7, 16, 27, 64]
                     ]
    red_numbers = [3, 5, 15, 18, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )