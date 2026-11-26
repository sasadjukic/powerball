

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
              'all-time': [3498, 3574, 7165],
              'six-months': [192, 204, 400],
              'recent-trends': [64, 64, 130]
            }

    sets = {
            'all-time' : [914, 1003, 1053, 1057, 998, 1042, 1098, 7165],
            'six-months' : [57, 63, 48, 48, 63, 72, 49, 400],
            'recent-trends' : [19, 19, 15, 19, 25, 22, 11, 130]
    }

    winning_hands = {
                     'singles': [236, 11, 1], 'pairs': [744, 40, 13], 
                     'two_pairs': [269, 19, 9], 'three_of_set': [152, 10, 3], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [88, 7, 3], 10: [96, 5, 0], 20: [122, 2, 1], 30: [111, 4, 3], 
                  40: [95, 7, 1], 50: [112, 10, 4], 60: [119, 5, 1]
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
              'all-time': [709, 724, 1433],
              'six-months': [43, 37, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [506, 519, 408, 1433],
            'six-months' : [27, 34, 19, 80],
            'recent-trends' : [6, 12, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 7, 9, 8, 8, 5, 4, 6, 7, 4, 
                       3, 4, 7, 10, 6, 9, 9, 6, 5, 3, 
                       8, 2, 5, 4, 5, 6, 4, 3, 8, 5, 
                       5, 6, 4, 4, 4, 6, 5, 7, 2, 6, 
                       5, 8, 4, 10, 7, 3, 4, 9, 7, 10, 
                       6, 2, 6, 6, 9, 6, 9, 10, 8, 6, 
                       5, 3, 3, 8, 6, 4, 4, 5, 5
                    ]

    white_numbers_trends = [
                        2, 1, 2, 5, 2, 1, 2, 2, 2, 0, 
                        2, 1, 4, 1, 2, 2, 2, 3, 2, 0, 
                        3, 1, 4, 1, 0, 1, 1, 1, 3, 0, 
                        2, 3, 3, 3, 2, 3, 2, 1, 0, 1, 
                        2, 5, 2, 4, 3, 1, 1, 3, 3, 3, 
                        5, 0, 1, 2, 2, 3, 3, 2, 1, 2, 
                        1, 1, 0, 1, 1, 1, 0, 2, 2
                    ]

    red_numbers_6 = [
                     2, 4, 6, 3, 3, 1, 3, 1, 4, 4, 
                     2, 5, 5, 6, 2, 1, 4, 2, 3, 5, 
                     2, 3, 5, 1, 3, 0
                    ]

    red_numbers_trends = [
                          1, 0, 0, 1, 1, 0, 1, 0, 2, 0, 
                          1, 2, 2, 1, 1, 0, 2, 0, 3, 2, 
                          2, 1, 2, 0, 1, 0
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
                     6.52, 7.31, 8.09, 7.49, 6.55, 7.59, 7.48, 6.71, 6.90, 6.51, 
                     7.18, 7.65, 5.31, 6.15, 7.08, 7.89, 7.57, 7.66, 7.10, 6.92, 
                     8.62, 5.86, 8.29, 7.02, 6.16, 5.81, 8.16, 8.86, 6.95, 7.16, 
                     6.99, 8.73, 8.43, 5.53, 6.31, 7.95, 7.68, 7.01, 7.65, 7.55, 
                     7.03, 7.60, 7.21, 8.42, 6.87, 5.86, 7.51, 6.74, 5.78, 7.30, 
                     6.70, 7.41, 7.70, 7.17, 6.30, 7.79, 7.07, 7.15, 8.05, 6.21, 
                     8.82, 8.05, 8.56, 8.43, 6.61, 7.01, 6.74, 7.14, 8.39
                ]
    red_numbers = [
                   4.33, 3.80, 3.63, 4.48, 4.21, 3.63, 3.26, 3.04, 4.18, 3.69, 
                   3.54, 3.26, 3.78, 5.10, 3.72, 2.61, 3.48, 4.14, 3.86, 4.06, 
                   4.46, 3.66, 3.93, 4.35, 4.23, 3.57
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
                     [3, 10, 33, 45, 47],
                     [7, 22, 42, 56, 66],
                     [7, 22, 36, 42, 56],
                     [8, 16, 21, 32, 51],
                     [18, 33, 34, 53, 61]
                     ]
    red_numbers = [9, 10, 12, 18, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )