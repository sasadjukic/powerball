

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
              'all-time': [3322, 3388, 6800],
              'six-months': [189, 205, 400],
              'recent-trends': [52, 76, 130]
            }

    sets = {
            'all-time' : [861, 945, 1008, 1015, 941, 977, 1053, 6800],
            'six-months' : [48, 54, 58, 57, 54, 72, 57, 400],
            'recent-trends' : [11, 14, 14, 25, 24, 19, 23, 130]
    }

    winning_hands = {
                     'singles': [227, 14, 6], 'pairs': [708, 49, 14], 
                     'two_pairs': [251, 11, 4], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 8, 1], 20: [120, 5, 2], 30: [107, 3, 1], 
                  40: [89, 8, 4], 50: [103, 11, 2], 60: [115, 10, 4]
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
              'all-time': [671, 689, 1360],
              'six-months': [39, 41, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [480, 490, 390, 1360],
            'six-months' : [27, 27, 26, 80],
            'recent-trends' : [7, 13, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 4, 7, 7, 8, 7, 5, 5, 3, 4, 
                       7, 2, 4, 6, 2, 7, 5, 11, 6, 4, 
                       9, 3, 4, 8, 5, 2, 8, 11, 4, 7, 
                       8, 4, 5, 5, 6, 9, 6, 4, 3, 5, 
                       6, 9, 6, 3, 2, 4, 8, 6, 5, 3, 
                       7, 13, 5, 4, 6, 11, 8, 8, 7, 7, 
                       4, 4, 10, 13, 7, 3, 2, 4, 3
                    ]

    white_numbers_trends = [
                        1, 1, 2, 3, 1, 1, 0, 1, 1, 1, 
                        0, 0, 2, 2, 1, 3, 2, 2, 1, 0, 
                        2, 1, 0, 4, 2, 0, 3, 1, 1, 4, 
                        3, 3, 1, 2, 2, 4, 3, 2, 1, 1, 
                        2, 3, 3, 2, 1, 3, 4, 2, 3, 0, 
                        3, 4, 1, 0, 2, 3, 3, 1, 2, 3, 
                        2, 1, 3, 6, 4, 1, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 3, 2, 4, 5, 3, 0, 0, 2, 
                     2, 5, 3, 5, 4, 1, 2, 2, 1, 5, 
                     3, 2, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          1, 1, 2, 0, 1, 1, 1, 0, 0, 1, 
                          1, 3, 2, 2, 3, 0, 0, 1, 0, 1, 
                          0, 1, 0, 0, 1, 3
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
                     7.32, 7.05, 8.25, 6.83, 6.49, 7.34, 6.38, 7.12, 6.45, 6.75, 
                     7.17, 7.64, 5.24, 7.00, 6.83, 7.55, 7.46, 7.45, 7.75, 7.26, 
                     8.62, 6.12, 8.28, 7.31, 6.32, 5.78, 8.69, 8.04, 5.87, 7.02, 
                     6.69, 8.73, 8.57, 6.33, 7.17, 8.33, 8.15, 6.62, 8.31, 6.88, 
                     6.11, 6.57, 7.23, 7.97, 7.77, 6.48, 7.90, 6.92, 6.02, 6.79, 
                     6.20, 7.69, 8.06, 6.71, 6.96, 6.48, 6.72, 6.83, 7.87, 7.12, 
                     8.48, 7.76, 8.50, 8.96, 6.55, 7.36, 7.22, 7.24, 8.37
                     ]
    red_numbers = [
                   3.92, 3.61, 4.08, 4.61, 4.31, 3.92, 3.58, 3.16, 4.24, 3.36, 
                   3.40, 3.25, 3.61, 4.76, 3.39, 2.75, 3.47, 4.33, 3.83, 3.99, 
                   4.42, 3.26, 3.79, 4.75, 4.19, 4.02
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
                     [17, 42, 53, 64, 65],
                     [8, 13, 35, 47, 48],
                     [5, 8, 12, 14, 37],
                     [11, 16, 17, 57, 62],
                     [10, 24, 32, 48, 49]
                     ]
    red_numbers = [9, 10, 12, 16, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )