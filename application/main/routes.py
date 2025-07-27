

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
              'all-time': [2992, 3047, 6120],
              'six-months': [197, 196, 400],
              'recent-trends': [66, 59, 130]
            }

    sets = {
            'all-time' : [776, 847, 912, 922, 847, 871, 945, 6120],
            'six-months' : [54, 52, 66, 49, 65, 61, 53, 400],
            'recent-trends' : [21, 12, 23, 19, 17, 20, 18, 130]
    }

    winning_hands = {
                     'singles': [201, 16, 8], 'pairs': [631, 41, 9], 
                     'two_pairs': [231, 14, 6], 'three_of_set': [133, 7, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 1], 10: [81, 7, 0], 20: [110, 8, 1], 30: [101, 4, 0], 
                  40: [73, 8, 2], 50: [88, 4, 2], 60: [101, 6, 2]
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
              'all-time': [606, 618, 1224],
              'six-months': [37, 43, 80], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [432, 442, 350, 1224],
            'six-months' : [26, 25, 29, 80],
            'recent-trends' : [5, 6, 15, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 7, 4, 9, 7, 5, 7, 7, 3, 3, 
                       6, 8, 5, 3, 4, 7, 6, 7, 3, 6, 
                       8, 2, 14, 4, 6, 1, 4, 12, 9, 5, 
                       4, 4, 7, 5, 7, 5, 7, 2, 3, 8, 
                       3, 5, 8, 9, 7, 4, 6, 7, 8, 7, 
                       5, 11, 7, 5, 5, 4, 6, 4, 7, 8, 
                       6, 8, 6, 4, 5, 4, 4, 2, 6
                    ]

    white_numbers_trends = [
                        3, 2, 1, 3, 3, 1, 2, 4, 2, 0, 
                        1, 2, 2, 0, 0, 2, 2, 1, 2, 0, 
                        3, 0, 5, 1, 4, 0, 2, 5, 3, 1, 
                        2, 2, 4, 1, 5, 1, 3, 0, 0, 1, 
                        0, 2, 4, 3, 2, 1, 0, 3, 1, 2, 
                        2, 5, 1, 2, 1, 1, 2, 2, 2, 0, 
                        4, 3, 2, 1, 2, 0, 2, 1, 3
                    ]

    red_numbers_6 = [
                     4, 5, 2, 2, 4, 3, 0, 2, 4, 1, 
                     3, 4, 3, 3, 3, 0, 1, 3, 4, 9, 
                     3, 2, 1, 5, 9, 0
                    ]

    red_numbers_trends = [
                          0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 
                          2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 
                          2, 2, 1, 3, 5, 0
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
                     7.25, 7.24, 7.64, 7.25, 6.49, 7.68, 7.00, 6.92, 7.36, 6.47, 
                     7.46, 7.76, 5.61, 7.00, 7.18, 7.31, 6.87, 6.74, 6.95, 7.15, 
                     9.40, 7.14, 9.40, 7.26, 6.38, 5.97, 8.64, 8.17, 6.22, 7.39, 
                     6.99, 8.76, 8.08, 6.29, 6.76, 8.29, 8.17, 6.47, 7.65, 6.82, 
                     6.61, 6.47, 6.77, 8.21, 7.43, 5.87, 8.06, 6.16, 5.67, 6.69, 
                     5.95, 7.75, 7.57, 6.96, 6.75, 7.17, 7.15, 6.82, 7.83, 6.37, 
                     9.27, 8.02, 8.35, 7.92, 5.97, 7.26, 7.73, 6.98, 8.66
                     ]
    red_numbers = [
                   3.65, 3.85, 4.11, 4.74, 4.51, 3.76, 3.51, 3.33, 4.32, 3.51, 
                   3.59, 3.15, 3.84, 4.11, 3.23, 3.17, 3.11, 4.63, 3.53, 4.25, 
                   4.71, 3.37, 3.13, 4.74, 4.49, 3.66
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
                     [16, 22, 40, 45, 46],
                     [2, 20, 55, 58, 60],
                     [4, 9, 28, 32, 53],
                     [15, 18, 47, 48, 57],
                     [17, 19, 25, 64, 66]
                     ]
    red_numbers = [3, 7, 10, 13, 15]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )