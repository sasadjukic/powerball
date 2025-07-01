

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
              'all-time': [2962, 3024, 6065],
              'six-months': [193, 200, 400],
              'recent-trends': [65, 61, 130]
            }

    sets = {
            'all-time' : [766, 841, 903, 915, 840, 864, 936, 6065],
            'six-months' : [53, 53, 60, 57, 63, 63, 51, 400],
            'recent-trends' : [15, 18, 22, 20, 21, 19, 15, 130]
    }

    winning_hands = {
                     'singles': [198, 14, 5], 'pairs': [626, 41, 14], 
                     'two_pairs': [229, 14, 5], 'three_of_set': [132, 9, 2], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 3], 20: [110, 8, 4], 30: [101, 5, 1], 
                  40: [72, 7, 3], 50: [87, 4, 1], 60: [99, 5, 1]
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
              'all-time': [603, 610, 1213],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [429, 441, 343, 1213],
            'six-months' : [28, 26, 26, 80],
            'recent-trends' : [5, 9, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 6, 5, 9, 6, 9, 6, 4, 3, 3, 
                       5, 8, 5, 4, 5, 8, 7, 6, 2, 7, 
                       6, 2, 14, 3, 4, 2, 4, 9, 9, 5, 
                       5, 7, 5, 5, 7, 6, 8, 4, 5, 8, 
                       4, 4, 9, 9, 6, 4, 7, 5, 7, 6, 
                       5, 12, 8, 6, 6, 5, 5, 3, 7, 8, 
                       4, 8, 4, 5, 5, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        2, 1, 1, 3, 3, 1, 2, 0, 2, 2, 
                        0, 2, 4, 2, 2, 3, 2, 1, 0, 1, 
                        2, 0, 6, 1, 2, 0, 2, 3, 5, 2, 
                        2, 2, 1, 3, 4, 1, 4, 0, 1, 4, 
                        1, 3, 4, 3, 2, 0, 1, 3, 0, 2, 
                        1, 7, 2, 0, 1, 1, 1, 1, 3, 2, 
                        2, 3, 0, 2, 2, 1, 2, 1, 0
                    ]

    red_numbers_6 = [
                     5, 4, 2, 3, 3, 4, 1, 1, 5, 1, 
                     3, 5, 3, 4, 3, 0, 1, 2, 4, 8, 
                     2, 1, 1, 6, 7, 1
                    ]

    red_numbers_trends = [
                          0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 
                          3, 1, 2, 0, 1, 0, 0, 0, 2, 2, 
                          2, 1, 0, 3, 4, 0
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
                     7.38, 7.22, 6.97, 6.62, 6.91, 7.52, 6.89, 6.52, 7.23, 6.69, 
                     7.14, 8.22, 5.16, 6.31, 7.11, 7.32, 7.46, 6.75, 7.64, 7.39, 
                     8.96, 6.46, 9.14, 7.21, 6.17, 6.20, 8.93, 8.21, 6.61, 6.93, 
                     6.58, 8.63, 7.65, 5.84, 6.15, 8.17, 7.79, 7.21, 8.15, 7.29, 
                     6.80, 6.83, 7.31, 7.82, 7.57, 6.08, 7.59, 6.19, 5.77, 6.81, 
                     6.45, 7.24, 7.20, 7.03, 6.53, 7.07, 7.37, 7.29, 7.92, 6.68, 
                     9.05, 8.73, 8.45, 8.25, 6.19, 7.31, 7.73, 7.62, 8.39
                     ]
    red_numbers = [
                   4.18, 3.52, 3.59, 4.76, 4.03, 4.23, 3.31, 3.62, 4.08, 3.66, 
                   3.82, 3.24, 4.02, 4.64, 3.35, 3.28, 3.21, 4.51, 3.46, 4.21, 
                   4.68, 3.10, 2.85, 4.59, 4.47, 3.59
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
                     [1, 26, 38, 46, 65],
                     [2, 8, 18, 30, 66],
                     [5, 6, 13, 37, 53],
                     [24, 25, 28, 58, 60],
                     [27, 29, 34, 36, 68]
                     ]
    red_numbers = [2, 11, 12, 22, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )