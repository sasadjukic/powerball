

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
              'all-time': [3193, 3231, 6510],
              'six-months': [207, 187, 400],
              'recent-trends': [75, 53, 130]
            }

    sets = {
            'all-time' : [828, 906, 972, 973, 894, 928, 1009, 6510],
            'six-months' : [54, 61, 61, 53, 47, 58, 66, 400],
            'recent-trends' : [19, 20, 26, 17, 9, 26, 13, 130]
    }

    winning_hands = {
                     'singles': [216, 15, 5], 'pairs': [675, 46, 17], 
                     'two_pairs': [243, 12, 4], 'three_of_set': [138, 5, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [79, 3, 2], 10: [86, 5, 2], 20: [116, 6, 1], 30: [106, 5, 3], 
                  40: [81, 8, 0], 50: [98, 10, 6], 60: [108, 8, 3]
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
              'all-time': [640, 662, 1302],
              'six-months': [34, 46, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [460, 471, 371, 1302],
            'six-months' : [28, 29, 23, 80],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 9, 6, 7, 5, 7, 9, 3, 5, 
                       7, 3, 4, 6, 8, 8, 3, 10, 7, 3, 
                       3, 5, 5, 6, 4, 6, 8, 14, 7, 3, 
                       7, 9, 5, 7, 6, 4, 4, 3, 5, 7, 
                       3, 3, 7, 6, 4, 3, 5, 3, 6, 5, 
                       8, 5, 12, 4, 3, 3, 6, 5, 7, 6, 
                       7, 9, 4, 9, 6, 8, 6, 5, 6
                    ]

    white_numbers_trends = [
                        2, 1, 1, 3, 7, 1, 1, 3, 0, 1, 
                        3, 0, 1, 2, 2, 2, 0, 5, 4, 2, 
                        3, 1, 1, 3, 2, 3, 3, 7, 1, 1, 
                        2, 2, 2, 3, 2, 1, 1, 1, 2, 1, 
                        1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 
                        3, 3, 4, 1, 2, 3, 3, 2, 5, 1, 
                        1, 2, 3, 2, 0, 1, 0, 1, 2
                    ]

    red_numbers_6 = [
                     6, 6, 3, 4, 4, 0, 2, 1, 2, 2, 
                     1, 3, 0, 7, 3, 2, 4, 2, 5, 3, 
                     3, 4, 8, 0, 2, 3
                    ]

    red_numbers_trends = [
                          3, 2, 1, 1, 1, 0, 2, 0, 0, 0, 
                          0, 1, 0, 3, 0, 1, 2, 0, 1, 1, 
                          1, 1, 3, 0, 0, 2
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
                     6.94, 6.93, 7.56, 6.94, 6.42, 7.38, 6.78, 6.89, 6.91, 6.40, 
                     7.23, 7.81, 5.88, 6.44, 7.43, 7.57, 7.07, 7.35, 7.32, 7.50, 
                     8.53, 6.89, 8.50, 6.90, 6.14, 5.54, 8.66, 8.75, 6.54, 7.07, 
                     6.81, 8.41, 8.44, 5.97, 6.52, 8.42, 7.70, 7.02, 8.15, 7.34, 
                     6.62, 7.07, 7.18, 7.97, 7.61, 6.35, 7.73, 6.31, 6.07, 7.13, 
                     6.61, 7.63, 8.04, 6.76, 6.67, 6.98, 6.61, 7.29, 7.78, 6.53, 
                     9.31, 7.84, 8.73, 7.83, 6.41, 7.24, 7.77, 6.74, 8.14
                     ]
    red_numbers = [
                   4.34, 3.77, 3.58, 4.82, 4.04, 3.17, 3.30, 3.06, 4.83, 3.54, 
                   3.64, 3.59, 3.72, 4.92, 2.91, 2.95, 3.07, 4.44, 3.66, 4.57, 
                   4.31, 3.45, 3.70, 4.50, 3.98, 4.14
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
                     [11, 18, 58, 66, 68],
                     [10, 31, 33, 41, 51],
                     [14, 25, 35, 45, 53],
                     [7, 20, 30, 49, 57],
                     [15, 39, 42, 47, 61]
                     ]
    red_numbers = [4, 7, 18, 21, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )