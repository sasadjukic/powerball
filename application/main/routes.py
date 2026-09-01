

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
              'all-time': [3405, 3484, 6980],
              'six-months': [180, 216, 400],
              'recent-trends': [58, 71, 130]
            }

    sets = {
            'all-time' : [888, 973, 1029, 1035, 966, 1009, 1080, 6980],
            'six-months' : [52, 61, 44, 53, 61, 69, 60, 400],
            'recent-trends' : [22, 17, 14, 15, 18, 23, 21, 130]
    }

    winning_hands = {
                     'singles': [234, 18, 5], 'pairs': [725, 41, 14], 
                     'two_pairs': [259, 13, 4], 'three_of_set': [146, 8, 3], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 3], 10: [94, 8, 2], 20: [120, 2, 0], 30: [108, 2, 1], 
                  40: [92, 9, 2], 50: [108, 9, 4], 60: [117, 6, 2]
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
              'all-time': [693, 703, 1396],
              'six-months': [46, 34, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [496, 504, 396, 1396],
            'six-months' : [30, 30, 20, 80],
            'recent-trends' : [13, 8, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 10, 7, 5, 8, 6, 5, 5, 6, 
                       4, 5, 6, 9, 2, 8, 10, 8, 3, 4, 
                       7, 3, 1, 6, 6, 4, 5, 4, 4, 9, 
                       6, 4, 2, 2, 4, 9, 7, 8, 2, 3, 
                       7, 9, 5, 7, 4, 5, 8, 7, 6, 9, 
                       3, 8, 5, 6, 7, 8, 8, 6, 9, 6, 
                       6, 4, 8, 10, 10, 4, 5, 4, 3
                    ]

    white_numbers_trends = [
                        0, 2, 2, 3, 4, 3, 1, 4, 3, 2, 
                        1, 2, 1, 3, 1, 1, 4, 2, 0, 1, 
                        1, 1, 0, 1, 3, 2, 2, 0, 3, 2, 
                        1, 1, 1, 0, 1, 3, 3, 3, 0, 2, 
                        1, 1, 1, 3, 2, 2, 1, 3, 2, 5, 
                        0, 0, 1, 4, 2, 2, 2, 4, 3, 1, 
                        2, 1, 3, 2, 4, 2, 3, 1, 2
                    ]

    red_numbers_6 = [
                     5, 6, 6, 2, 4, 3, 2, 1, 1, 4, 
                     2, 5, 5, 4, 4, 1, 2, 3, 0, 5, 
                     1, 2, 2, 2, 4, 4
                    ]

    red_numbers_trends = [
                          1, 3, 2, 2, 2, 0, 1, 1, 1, 2, 
                          0, 0, 1, 0, 0, 1, 2, 2, 0, 1, 
                          0, 1, 1, 0, 2, 0
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
                     6.82, 7.31, 7.85, 6.57, 7.25, 7.97, 6.26, 6.77, 6.46, 6.74, 
                     7.04, 7.20, 5.67, 6.51, 7.06, 7.66, 7.09, 7.51, 7.58, 7.05, 
                     8.99, 6.16, 8.57, 7.26, 6.22, 5.80, 8.14, 8.87, 6.49, 7.18, 
                     7.46, 8.29, 8.69, 6.16, 5.98, 8.01, 7.89, 6.76, 7.79, 7.33, 
                     6.72, 6.94, 6.81, 8.01, 6.90, 5.61, 8.12, 6.62, 6.12, 7.31, 
                     5.80, 8.40, 8.51, 6.98, 6.24, 6.92, 6.71, 7.28, 7.86, 6.91, 
                     9.31, 7.90, 8.12, 8.64, 6.44, 7.49, 7.30, 7.61, 8.01
                     ]
    red_numbers = [
                   4.40, 3.92, 3.78, 5.08, 4.38, 3.60, 3.21, 2.89, 4.20, 3.64, 
                   2.99, 3.20, 3.92, 4.65, 3.54, 2.96, 3.46, 4.21, 3.49, 4.09, 
                   4.23, 3.48, 3.71, 4.60, 4.38, 3.99
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
                     [11, 15, 29, 32, 64],
                     [14, 17, 52, 56, 63],
                     [3, 16, 23, 24, 57],
                     [10, 32, 56, 59, 66],
                     [10, 46, 61, 62, 66]
                     ]
    red_numbers = [4, 11, 20, 23, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )