

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
              'all-time': [3101, 3155, 6340],
              'six-months': [201, 191, 400],
              'recent-trends': [63, 67, 130]
            }

    sets = {
            'all-time' : [803, 883, 942, 950, 880, 893, 989, 6340],
            'six-months' : [52, 59, 59, 54, 61, 48, 67, 400],
            'recent-trends' : [15, 20, 19, 14, 20, 16, 26, 130]
    }

    winning_hands = {
                     'singles': [208, 15, 4], 'pairs': [654, 41, 14], 
                     'two_pairs': [239, 15, 5], 'three_of_set': [137, 7, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 6, 2], 20: [115, 8, 2], 30: [102, 2, 0], 
                  40: [80, 11, 5], 50: [91, 5, 3], 60: [105, 7, 2]
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
              'all-time': [627, 641, 1268],
              'six-months': [35, 45, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [449, 460, 359, 1268],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [8, 14, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 8, 7, 4, 3, 7, 8, 6, 4, 
                       5, 5, 7, 6, 8, 9, 5, 6, 4, 2, 
                       3, 4, 9, 5, 5, 2, 7, 12, 10, 3, 
                       6, 8, 6, 8, 8, 3, 7, 2, 3, 10, 
                       3, 7, 10, 7, 6, 3, 4, 6, 5, 7, 
                       4, 9, 8, 5, 2, 1, 3, 4, 5, 6, 
                       10, 9, 3, 9, 6, 7, 8, 3, 6
                    ]

    white_numbers_trends = [
                        1, 3, 5, 1, 0, 0, 2, 2, 1, 3, 
                        1, 1, 3, 2, 3, 2, 3, 2, 0, 1, 
                        0, 2, 0, 2, 0, 2, 3, 5, 4, 1, 
                        1, 6, 0, 1, 0, 0, 2, 1, 2, 2, 
                        1, 3, 3, 2, 2, 1, 2, 1, 3, 2, 
                        1, 2, 4, 3, 1, 0, 1, 1, 1, 3, 
                        2, 2, 0, 4, 2, 6, 5, 1, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 4, 5, 1, 0, 2, 2, 2, 
                     3, 3, 2, 3, 4, 1, 2, 3, 5, 5, 
                     4, 5, 2, 3, 7, 1
                    ]

    red_numbers_trends = [
                          2, 1, 1, 2, 1, 0, 0, 0, 1, 2, 
                          0, 2, 0, 2, 3, 1, 0, 1, 3, 2, 
                          0, 1, 0, 0, 0, 1
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
                     7.18, 7.64, 8.08, 6.60, 6.16, 6.68, 7.05, 6.22, 7.09, 6.74, 
                     7.20, 7.83, 5.27, 6.25, 7.50, 7.50, 7.15, 6.99, 6.94, 7.75, 
                     9.01, 6.59, 8.91, 6.94, 6.21, 5.77, 8.81, 7.79, 6.45, 6.99, 
                     6.98, 8.57, 8.62, 6.41, 6.47, 8.21, 8.51, 6.67, 8.12, 7.76, 
                     6.28, 6.83, 6.83, 8.04, 7.68, 5.89, 7.85, 6.45, 5.69, 6.50, 
                     6.15, 7.66, 7.82, 6.92, 6.33, 7.20, 7.18, 6.47, 7.64, 6.64, 
                     9.13, 8.67, 8.51, 8.34, 6.14, 7.22, 8.06, 7.55, 8.72
                     ]
    red_numbers = [
                   4.38, 3.50, 3.83, 5.10, 3.99, 3.88, 3.39, 3.26, 4.22, 3.33, 
                   3.32, 3.05, 4.07, 4.39, 3.25, 2.86, 3.18, 4.56, 3.60, 3.84, 
                   4.84, 3.57, 3.28, 4.88, 4.43, 4.00
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
                     [9, 16, 17, 21, 67],
                     [1, 6, 50, 57, 58],
                     [5, 20, 27, 32, 51],
                     [3, 31, 38, 47, 56],
                     [7, 25, 33, 52, 62]
                     ]
    red_numbers = [4, 16, 19, 24, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )