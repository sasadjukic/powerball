

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
              'all-time': [3354, 3426, 6870],
              'six-months': [182, 213, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [867, 961, 1016, 1022, 952, 989, 1063, 6870],
            'six-months' : [46, 59, 53, 53, 61, 70, 58, 400],
            'recent-trends' : [13, 24, 13, 17, 22, 22, 19, 130]
    }

    winning_hands = {
                     'singles': [231, 16, 7], 'pairs': [712, 43, 12], 
                     'two_pairs': [255, 13, 5], 'three_of_set': [144, 6, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [82, 4, 1], 10: [93, 7, 2], 20: [120, 5, 0], 30: [107, 2, 0], 
                  40: [90, 9, 4], 50: [104, 8, 3], 60: [115, 8, 2]
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
              'all-time': [679, 695, 1374],
              'six-months': [43, 37, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [485, 497, 392, 1374],
            'six-months' : [28, 30, 22, 80],
            'recent-trends' : [6, 15, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 4, 6, 8, 5, 5, 3, 5, 
                       5, 4, 5, 8, 2, 9, 8, 7, 6, 4, 
                       9, 3, 3, 6, 4, 3, 8, 9, 4, 8, 
                       7, 3, 3, 3, 5, 8, 7, 6, 3, 4, 
                       6, 9, 7, 5, 4, 5, 8, 7, 6, 6, 
                       6, 10, 5, 3, 8, 9, 8, 7, 8, 8, 
                       5, 3, 10, 12, 7, 4, 3, 4, 2
                    ]

    white_numbers_trends = [
                        1, 2, 4, 2, 1, 1, 0, 2, 0, 3, 
                        0, 2, 3, 5, 0, 6, 4, 0, 1, 1, 
                        3, 1, 0, 1, 1, 2, 1, 2, 1, 2, 
                        3, 2, 0, 2, 1, 0, 2, 4, 1, 1, 
                        2, 1, 2, 5, 2, 2, 1, 4, 2, 3, 
                        1, 2, 3, 0, 4, 1, 3, 1, 4, 3, 
                        2, 1, 1, 3, 2, 3, 2, 1, 1
                    ]

    red_numbers_6 = [
                     5, 4, 4, 3, 5, 6, 1, 0, 0, 2, 
                     3, 6, 4, 6, 5, 0, 1, 3, 0, 5, 
                     2, 1, 4, 4, 2, 4
                    ]

    red_numbers_trends = [
                          0, 1, 2, 1, 1, 1, 0, 0, 0, 1, 
                          1, 4, 2, 3, 2, 0, 0, 2, 0, 2, 
                          0, 0, 1, 0, 1, 1
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
                     6.25, 7.34, 7.82, 6.91, 6.66, 7.44, 6.55, 6.62, 6.55, 6.53, 
                     7.68, 7.45, 5.79, 7.09, 6.72, 7.68, 7.19, 7.47, 7.57, 7.49, 
                     9.54, 6.81, 8.30, 7.06, 5.88, 5.51, 8.67, 8.72, 6.46, 7.44, 
                     6.98, 8.10, 8.30, 5.94, 6.49, 8.62, 7.76, 6.25, 8.01, 7.53, 
                     6.41, 6.58, 7.35, 7.70, 7.76, 6.12, 7.84, 5.97, 5.67, 6.93, 
                     6.87, 8.13, 7.90, 6.59, 6.93, 6.77, 6.47, 6.77, 7.89, 7.28, 
                     9.25, 7.89, 8.04, 9.25, 6.42, 7.36, 7.12, 7.10, 8.47
                     ]
    red_numbers = [
                   4.08, 3.80, 3.94, 4.96, 4.46, 3.77, 3.30, 3.51, 3.86, 3.17, 
                   3.58, 3.42, 3.65, 4.63, 3.35, 2.90, 3.12, 4.29, 3.70, 3.93, 
                   4.51, 3.65, 3.76, 4.75, 4.18, 3.73
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
                     [11, 28, 35, 51, 69],
                     [6, 19, 49, 65, 67],
                     [2, 19, 21, 33, 58],
                     [10, 11, 27, 28, 50],
                     [1, 3, 13, 14, 56]
                     ]
    red_numbers = [2, 9, 11, 16, 20]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )