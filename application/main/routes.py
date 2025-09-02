

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
              'all-time': [3033, 3083, 6200],
              'six-months': [200, 190, 400],
              'recent-trends': [68, 57, 130]
            }

    sets = {
            'all-time' : [787, 861, 921, 936, 859, 877, 959, 6200],
            'six-months' : [55, 55, 64, 54, 62, 54, 56, 400],
            'recent-trends' : [20, 19, 17, 21, 19, 12, 22, 130]
    }

    winning_hands = {
                     'singles': [204, 16, 5], 'pairs': [638, 40, 12], 
                     'two_pairs': [234, 13, 5], 'three_of_set': [136, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [82, 5, 1], 20: [113, 9, 3], 30: [102, 5, 1], 
                  40: [75, 10, 3], 50: [88, 3, 1], 60: [101, 4, 2]
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
              'all-time': [615, 625, 1240],
              'six-months': [40, 40, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [441, 445, 354, 1240],
            'six-months' : [30, 20, 30, 80],
            'recent-trends' : [12, 4, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 5, 4, 10, 6, 5, 8, 7, 5, 2, 
                       7, 7, 5, 5, 6, 8, 4, 7, 4, 6, 
                       6, 3, 15, 5, 7, 1, 4, 10, 7, 4, 
                       5, 2, 8, 7, 10, 6, 7, 2, 3, 10, 
                       4, 5, 9, 8, 6, 5, 4, 6, 5, 7, 
                       6, 10, 7, 3, 3, 3, 4, 4, 7, 5, 
                       7, 8, 7, 7, 6, 3, 4, 2, 7
                    ]

    white_numbers_trends = [
                        1, 1, 1, 3, 1, 2, 2, 6, 3, 0, 
                        3, 2, 0, 2, 3, 3, 0, 3, 3, 0, 
                        1, 2, 3, 2, 3, 0, 2, 4, 0, 0, 
                        3, 0, 5, 4, 5, 2, 1, 1, 0, 4, 
                        1, 1, 3, 1, 2, 2, 1, 2, 2, 3, 
                        2, 0, 2, 1, 0, 0, 1, 2, 1, 1, 
                        4, 3, 2, 3, 3, 0, 1, 1, 4
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 5, 3, 0, 2, 3, 1, 
                     3, 3, 3, 1, 2, 0, 1, 2, 4, 6, 
                     4, 3, 2, 5, 10, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 3, 0, 0, 2, 1, 0, 
                          0, 0, 0, 1, 0, 0, 1, 2, 0, 1, 
                          1, 2, 2, 1, 3, 0
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
                     7.35, 7.09, 7.50, 6.26, 6.08, 7.59, 6.57, 6.89, 7.17, 6.50, 
                     7.43, 8.01, 5.28, 6.48, 6.93, 7.31, 7.44, 7.21, 7.55, 7.57, 
                     8.95, 6.56, 8.75, 7.29, 6.32, 6.16, 8.37, 7.83, 6.59, 7.28, 
                     7.01, 8.39, 8.63, 6.31, 6.55, 9.13, 7.97, 6.87, 8.01, 7.38, 
                     6.44, 6.39, 7.29, 8.19, 7.68, 6.31, 7.81, 6.42, 5.39, 6.94, 
                     6.08, 7.82, 7.89, 7.31, 6.62, 7.29, 6.30, 5.98, 8.15, 6.41, 
                     9.24, 8.35, 8.75, 8.42, 5.68, 6.70, 7.97, 7.06, 8.56
                     ]
    red_numbers = [
                   3.47, 3.60, 3.76, 4.89, 4.47, 3.73, 3.54, 3.74, 3.92, 3.73, 
                   3.52, 3.27, 3.91, 4.31, 3.42, 2.80, 2.86, 4.52, 3.77, 4.14, 
                   4.60, 3.22, 3.62, 4.76, 4.58, 3.85
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
                     [11, 18, 38, 57, 68],
                     [29, 33, 37, 63, 64],
                     [6, 20, 22, 55, 58],
                     [19, 23, 28, 66, 69],
                     [40, 51, 60, 61, 62]
                     ]
    red_numbers = [9, 11, 13, 14, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )