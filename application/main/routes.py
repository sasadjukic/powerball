

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
              'all-time': [3079, 3127, 6290],
              'six-months': [202, 189, 400],
              'recent-trends': [66, 64, 130]
            }

    sets = {
            'all-time' : [797, 876, 936, 943, 872, 888, 978, 6290],
            'six-months' : [53, 58, 61, 52, 62, 50, 64, 400],
            'recent-trends' : [13, 22, 21, 12, 19, 14, 29, 130]
    }

    winning_hands = {
                     'singles': [205, 13, 2], 'pairs': [648, 40, 13], 
                     'two_pairs': [239, 15, 7], 'three_of_set': [137, 9, 3], 
                     'full_house': [19, 3, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [83, 5, 2], 20: [115, 9, 4], 30: [102, 3, 0], 
                  40: [78, 11, 3], 50: [90, 5, 2], 60: [103, 5, 2]
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
              'all-time': [624, 634, 1258],
              'six-months': [36, 44, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [448, 454, 356, 1258],
            'six-months' : [28, 24, 28, 80],
            'recent-trends' : [10, 11, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 7, 4, 3, 8, 8, 5, 4, 
                       4, 5, 6, 7, 9, 10, 3, 6, 4, 4, 
                       4, 4, 10, 5, 6, 2, 6, 11, 9, 4, 
                       6, 6, 7, 7, 9, 3, 7, 1, 2, 8, 
                       3, 8, 9, 8, 8, 4, 3, 6, 5, 7, 
                       5, 9, 9, 4, 2, 2, 3, 3, 6, 5, 
                       9, 9, 5, 9, 6, 5, 6, 3, 7
                    ]

    white_numbers_trends = [
                        1, 1, 5, 0, 0, 0, 2, 3, 1, 2, 
                        2, 1, 2, 3, 4, 4, 1, 2, 1, 1, 
                        0, 3, 3, 1, 1, 1, 3, 4, 4, 1, 
                        2, 4, 1, 2, 0, 0, 2, 0, 0, 2, 
                        2, 3, 0, 2, 2, 2, 2, 1, 3, 2, 
                        1, 1, 5, 2, 1, 0, 0, 0, 2, 1, 
                        5, 3, 1, 6, 3, 3, 3, 2, 2
                    ]

    red_numbers_6 = [
                     4, 6, 3, 4, 5, 1, 0, 2, 3, 1, 
                     3, 2, 2, 3, 2, 1, 2, 2, 6, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          2, 1, 1, 2, 3, 0, 0, 0, 1, 1, 
                          0, 1, 0, 2, 1, 1, 2, 1, 2, 1, 
                          0, 2, 1, 0, 1, 0
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
                     6.92, 6.84, 8.08, 7.07, 6.37, 7.74, 7.11, 6.76, 7.24, 6.66, 
                     6.90, 7.55, 5.42, 6.11, 7.11, 7.74, 7.17, 6.68, 7.51, 6.91, 
                     8.82, 6.49, 8.80, 7.52, 6.75, 6.06, 8.16, 8.27, 6.72, 6.39, 
                     7.15, 8.94, 8.36, 6.28, 6.63, 9.08, 7.74, 6.16, 7.84, 7.20, 
                     6.55, 6.70, 7.18, 8.32, 7.35, 6.17, 7.48, 5.91, 6.35, 7.24, 
                     5.56, 7.95, 8.15, 7.53, 7.19, 6.63, 6.53, 6.55, 7.78, 6.27, 
                     9.22, 8.10, 7.87, 8.47, 6.22, 7.12, 8.06, 7.45, 8.85
                     ]
    red_numbers = [
                   3.78, 3.83, 3.93, 5.19, 4.30, 3.56, 3.32, 3.52, 4.13, 3.60, 
                   3.39, 3.22, 3.86, 4.61, 2.84, 3.11, 3.39, 4.27, 3.72, 4.13, 
                   4.69, 3.41, 3.37, 4.73, 4.42, 3.68
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
                     [3, 21, 37, 43, 45],
                     [2, 20, 28, 34, 64],
                     [6, 19, 22, 57, 60],
                     [26, 35, 36, 52, 54],
                     [33, 50, 58, 61, 69]
                     ]
    red_numbers = [7, 8, 9, 18, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )