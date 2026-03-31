

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
              'all-time': [3259, 3303, 6650],
              'six-months': [205, 191, 400],
              'recent-trends': [63, 66, 130]
            }

    sets = {
            'all-time' : [845, 926, 993, 989, 914, 955, 1028, 6650],
            'six-months' : [54, 59, 64, 49, 45, 70, 59, 400],
            'recent-trends' : [17, 20, 19, 14, 18, 26, 16, 130]
    }

    winning_hands = {
                     'singles': [220, 15, 4], 'pairs': [691, 46, 14], 
                     'two_pairs': [247, 12, 4], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 1], 10: [89, 7, 3], 20: [118, 4, 2], 30: [106, 4, 0], 
                  40: [85, 8, 3], 50: [101, 11, 3], 60: [111, 8, 2]
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
              'all-time': [654, 676, 1330],
              'six-months': [35, 45, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [470, 477, 383, 1330],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [10, 4, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 8, 4, 8, 7, 8, 8, 3, 6, 
                       7, 4, 4, 6, 2, 6, 5, 12, 7, 6, 
                       7, 5, 4, 4, 3, 5, 8, 16, 6, 5, 
                       6, 8, 5, 4, 4, 6, 3, 3, 5, 6, 
                       3, 4, 7, 4, 1, 2, 8, 6, 4, 4, 
                       9, 9, 6, 6, 5, 8, 6, 10, 7, 8, 
                       4, 5, 7, 7, 5, 8, 4, 6, 5
                    ]

    white_numbers_trends = [
                        0, 2, 2, 0, 1, 4, 4, 2, 2, 1, 
                        3, 2, 0, 3, 0, 1, 2, 5, 3, 3, 
                        2, 2, 3, 0, 1, 0, 2, 4, 2, 3, 
                        2, 0, 2, 0, 1, 4, 1, 1, 0, 2, 
                        2, 4, 2, 0, 0, 0, 4, 3, 1, 3, 
                        1, 4, 0, 3, 2, 5, 1, 5, 2, 2, 
                        1, 1, 3, 4, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     7, 5, 2, 3, 2, 4, 2, 0, 0, 3, 
                     2, 4, 1, 6, 3, 2, 2, 2, 3, 5, 
                     4, 2, 8, 3, 1, 4
                    ]

    red_numbers_trends = [
                          3, 1, 0, 1, 1, 4, 0, 0, 0, 1, 
                          0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 
                          2, 0, 2, 3, 1, 1
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
                     6.80, 7.11, 7.79, 7.07, 6.57, 7.75, 7.11, 6.92, 7.08, 6.56, 
                     7.29, 8.10, 5.41, 6.48, 6.98, 7.46, 7.11, 7.25, 7.30, 7.59, 
                     8.96, 6.58, 8.76, 6.91, 6.01, 5.23, 8.69, 8.75, 6.60, 7.02, 
                     7.26, 8.15, 8.26, 6.22, 6.78, 8.06, 7.63, 6.72, 7.78, 7.57, 
                     6.66, 7.05, 7.13, 8.23, 7.28, 5.77, 8.09, 6.10, 5.96, 6.94, 
                     6.00, 7.84, 7.79, 7.07, 6.49, 6.78, 6.49, 7.09, 8.30, 6.78, 
                     8.95, 8.89, 8.36, 8.20, 6.10, 7.41, 7.15, 7.23, 8.20
                     ]
    red_numbers = [
                   4.35, 4.05, 3.90, 4.53, 4.35, 3.92, 3.17, 3.27, 4.21, 3.30, 
                   3.42, 3.44, 3.49, 4.64, 2.81, 3.22, 3.20, 4.50, 3.70, 4.39, 
                   4.70, 3.24, 3.62, 4.35, 4.43, 3.80
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
                     [8, 17, 57, 60, 69],
                     [13, 23, 42, 53, 62],
                     [2, 14, 24, 26, 63],
                     [25, 28, 33, 47, 48],
                     [1, 17, 47, 59, 61]
                     ]
    red_numbers = [2, 7, 12, 14, 16]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )