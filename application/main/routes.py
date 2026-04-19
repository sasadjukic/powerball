

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
              'all-time': [3276, 3326, 6690],
              'six-months': [197, 199, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [851, 932, 998, 992, 923, 960, 1034, 6690],
            'six-months' : [54, 56, 62, 49, 51, 72, 56, 400],
            'recent-trends' : [17, 21, 17, 12, 21, 25, 17, 130]
    }

    winning_hands = {
                     'singles': [221, 16, 5], 'pairs': [697, 49, 15], 
                     'two_pairs': [248, 9, 3], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 2, 0], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 8, 5], 20: [119, 4, 2], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 11, 2], 60: [112, 9, 2]
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
              'all-time': [659, 679, 1338],
              'six-months': [35, 45, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [475, 478, 385, 1338],
            'six-months' : [27, 24, 29, 80],
            'recent-trends' : [11, 4, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 9, 8, 6, 3, 5, 
                       8, 4, 4, 5, 2, 5, 5, 11, 7, 5, 
                       8, 4, 4, 6, 4, 5, 7, 14, 5, 5, 
                       6, 5, 5, 4, 4, 6, 4, 4, 6, 6, 
                       4, 6, 9, 3, 2, 3, 8, 5, 5, 4, 
                       9, 10, 7, 5, 4, 8, 7, 10, 8, 8, 
                       4, 5, 8, 8, 5, 6, 2, 5, 5
                    ]

    white_numbers_trends = [
                        0, 1, 3, 1, 1, 4, 5, 0, 2, 2, 
                        4, 2, 2, 2, 0, 1, 3, 4, 1, 2, 
                        3, 1, 2, 2, 1, 0, 2, 3, 1, 2, 
                        1, 0, 1, 0, 1, 3, 1, 2, 1, 0, 
                        3, 5, 3, 0, 1, 1, 5, 1, 2, 3, 
                        0, 6, 1, 3, 2, 4, 2, 1, 3, 1, 
                        2, 1, 3, 5, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     9, 4, 2, 2, 3, 5, 2, 0, 0, 2, 
                     2, 3, 1, 4, 4, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 5
                    ]

    red_numbers_trends = [
                          5, 1, 1, 0, 1, 3, 0, 0, 0, 1, 
                          0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 
                          2, 0, 1, 2, 1, 2
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
                     6.81, 6.93, 8.00, 7.03, 6.67, 7.35, 6.99, 6.41, 6.58, 6.65, 
                     7.42, 7.72, 5.21, 6.74, 6.69, 7.75, 7.09, 7.22, 7.41, 7.28, 
                     8.90, 6.58, 8.46, 7.35, 6.24, 5.55, 8.35, 8.85, 6.25, 6.88, 
                     7.15, 8.18, 8.75, 6.24, 6.88, 8.57, 8.06, 6.40, 7.92, 7.15, 
                     6.89, 7.14, 7.33, 8.25, 7.17, 5.61, 8.06, 6.49, 5.70, 7.16, 
                     6.23, 8.43, 7.89, 6.84, 6.79, 6.37, 6.93, 7.12, 7.91, 6.94, 
                     8.89, 7.97, 7.64, 8.94, 6.32, 6.99, 7.62, 7.15, 8.57
                     ]
    red_numbers = [
                   4.38, 3.98, 4.07, 4.64, 4.36, 4.03, 3.08, 3.42, 4.11, 3.49, 
                   3.69, 3.32, 3.67, 4.09, 3.11, 3.21, 3.22, 4.21, 3.71, 4.07, 
                   4.32, 3.51, 3.71, 4.53, 3.98, 4.09
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
                     [25, 32, 45, 48, 58],
                     [1, 32, 46, 60, 62],
                     [19, 28, 50, 53, 67],
                     [5, 20, 48, 50, 64],
                     [6, 36, 49, 63, 65]
                     ]
    red_numbers = [5, 14, 15, 19, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )