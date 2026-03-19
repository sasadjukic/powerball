

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
              'all-time': [3249, 3288, 6625],
              'six-months': [206, 190, 400],
              'recent-trends': [64, 63, 130]
            }

    sets = {
            'all-time' : [843, 921, 991, 987, 909, 949, 1025, 6625],
            'six-months' : [54, 58, 64, 50, 46, 68, 60, 400],
            'recent-trends' : [17, 17, 22, 17, 15, 24, 18, 130]
    }

    winning_hands = {
                     'singles': [218, 13, 2], 'pairs': [688, 46, 15], 
                     'two_pairs': [247, 13, 5], 'three_of_set': [140, 4, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 1], 10: [88, 6, 2], 20: [118, 4, 2], 30: [106, 4, 1], 
                  40: [84, 9, 3], 50: [100, 11, 2], 60: [111, 8, 4]
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
              'all-time': [652, 673, 1325],
              'six-months': [35, 45, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [468, 477, 380, 1325],
            'six-months' : [25, 30, 25, 80],
            'recent-trends' : [9, 8, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 9, 4, 8, 7, 7, 8, 3, 6, 
                       5, 2, 4, 7, 5, 6, 5, 11, 7, 6, 
                       6, 5, 4, 4, 3, 5, 8, 15, 8, 6, 
                       6, 9, 5, 4, 4, 5, 3, 3, 5, 6, 
                       1, 5, 6, 4, 2, 3, 7, 6, 6, 5, 
                       9, 9, 7, 7, 4, 6, 5, 10, 6, 8, 
                       3, 6, 6, 7, 5, 9, 5, 6, 5
                    ]

    white_numbers_trends = [
                        0, 3, 2, 0, 2, 4, 2, 2, 2, 1, 
                        2, 0, 0, 3, 0, 2, 2, 4, 3, 3, 
                        3, 2, 3, 0, 1, 1, 3, 4, 2, 3, 
                        2, 0, 2, 1, 3, 3, 2, 1, 0, 3, 
                        0, 3, 1, 0, 0, 1, 3, 3, 1, 3, 
                        2, 4, 1, 3, 3, 3, 0, 5, 0, 3, 
                        1, 1, 4, 3, 2, 1, 0, 2, 1
                    ]

    red_numbers_6 = [
                     7, 4, 2, 4, 2, 4, 2, 0, 0, 3, 
                     2, 4, 1, 6, 4, 2, 2, 2, 4, 5, 
                     4, 2, 8, 3, 0, 3
                    ]

    red_numbers_trends = [
                          2, 0, 0, 1, 2, 4, 0, 0, 0, 1, 
                          1, 2, 1, 0, 1, 0, 1, 1, 0, 2, 
                          2, 0, 2, 3, 0, 0
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
                     7.06, 7.10, 7.65, 6.75, 6.86, 7.43, 6.29, 7.15, 6.98, 6.65, 
                     6.46, 7.87, 4.82, 6.68, 7.02, 7.14, 6.80, 7.05, 7.30, 6.64, 
                     9.05, 6.10, 8.45, 7.07, 6.54, 6.12, 8.84, 8.62, 6.38, 7.11, 
                     7.05, 8.50, 8.51, 6.04, 7.37, 7.68, 7.80, 6.95, 8.00, 7.53, 
                     6.36, 6.92, 7.05, 7.86, 7.50, 5.97, 8.59, 6.68, 5.55, 6.89, 
                     6.50, 7.72, 8.60, 7.32, 6.72, 7.12, 7.06, 6.99, 7.73, 6.96, 
                     9.23, 8.15, 8.09, 8.36, 6.02, 7.14, 7.26, 7.63, 8.62
                     ]
    red_numbers = [
                   4.25, 3.64, 4.01, 4.75, 4.21, 3.99, 3.41, 3.09, 4.08, 3.37, 
                   3.53, 3.54, 3.73, 4.35, 3.11, 3.14, 3.07, 4.57, 4.07, 4.23, 
                   4.49, 3.37, 3.48, 4.57, 4.12, 3.83
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
                     [12, 29, 46, 62, 64],
                     [20, 22, 25, 36, 65],
                     [7, 15, 27, 67, 69],
                     [16, 23, 34, 45, 47],
                     [9, 13, 37, 40, 41]
                     ]
    red_numbers = [2, 3, 5, 16, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )