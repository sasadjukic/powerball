

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
              'all-time': [3394, 3470, 6955],
              'six-months': [180, 216, 400],
              'recent-trends': [63, 66, 130]
            }

    sets = {
            'all-time' : [887, 967, 1028, 1030, 964, 1004, 1075, 6955],
            'six-months' : [53, 59, 47, 50, 62, 71, 58, 400],
            'recent-trends' : [24, 19, 17, 13, 19, 21, 17, 130]
    }

    winning_hands = {
                     'singles': [234, 18, 6], 'pairs': [721, 39, 11], 
                     'two_pairs': [259, 14, 6], 'three_of_set': [145, 7, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 4], 10: [93, 7, 1], 20: [120, 3, 0], 30: [107, 1, 0], 
                  40: [92, 9, 2], 50: [106, 7, 2], 60: [117, 7, 2]
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
              'all-time': [690, 701, 1391],
              'six-months': [46, 34, 80], 
              'recent-trends': [17, 9, 26]
            }

    sets = {
            'all-time' : [494, 502, 395, 1391],
            'six-months' : [31, 28, 21, 80],
            'recent-trends' : [13, 9, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 7, 6, 8, 6, 5, 6, 6, 
                       4, 4, 5, 9, 2, 8, 9, 8, 4, 4, 
                       7, 3, 2, 6, 5, 4, 6, 5, 5, 9, 
                       5, 3, 2, 2, 4, 10, 6, 7, 2, 3, 
                       7, 9, 5, 7, 3, 5, 9, 8, 6, 9, 
                       3, 10, 5, 6, 7, 9, 7, 6, 9, 6, 
                       6, 3, 8, 12, 8, 5, 4, 3, 3
                    ]

    white_numbers_trends = [
                        0, 3, 2, 3, 4, 4, 1, 4, 3, 3, 
                        0, 1, 1, 5, 1, 2, 4, 1, 1, 1, 
                        3, 1, 0, 1, 2, 3, 2, 1, 3, 3, 
                        0, 0, 0, 0, 1, 3, 2, 3, 1, 2, 
                        2, 1, 1, 3, 2, 2, 1, 4, 1, 4, 
                        0, 0, 2, 3, 2, 1, 1, 3, 5, 1, 
                        2, 0, 3, 2, 2, 2, 2, 1, 2
                    ]

    red_numbers_6 = [
                     6, 4, 6, 2, 4, 5, 2, 1, 1, 3, 
                     2, 5, 5, 4, 4, 1, 2, 2, 0, 5, 
                     2, 2, 2, 2, 4, 4
                    ]

    red_numbers_trends = [
                          1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 
                          1, 0, 2, 1, 0, 1, 2, 1, 0, 1, 
                          0, 1, 0, 0, 2, 0
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
                     7.09, 7.36, 7.89, 7.08, 6.30, 8.05, 6.51, 6.73, 6.60, 6.51, 
                     7.22, 7.39, 5.39, 6.56, 6.67, 7.68, 6.79, 7.51, 7.45, 7.95, 
                     8.78, 6.38, 8.15, 7.59, 7.25, 6.11, 8.53, 8.68, 6.59, 7.42, 
                     7.11, 8.30, 8.28, 6.01, 6.83, 8.53, 7.90, 6.76, 7.91, 7.10, 
                     6.24, 6.89, 7.04, 7.45, 7.07, 6.10, 8.10, 6.84, 5.83, 7.13, 
                     6.29, 7.74, 7.62, 6.38, 6.28, 6.91, 7.22, 7.33, 7.67, 6.84, 
                     8.90, 8.14, 8.21, 9.42, 5.79, 7.11, 7.47, 6.99, 8.06
                     ]
    red_numbers = [
                   4.01, 3.89, 4.16, 4.32, 4.57, 3.82, 3.19, 3.64, 4.09, 3.48, 
                   3.34, 3.63, 3.78, 4.87, 3.26, 2.75, 3.17, 4.17, 3.28, 4.16, 
                   4.77, 3.41, 3.53, 4.41, 4.41, 3.89
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
                     [3, 23, 44, 61, 69],
                     [19, 45, 51, 66, 67],
                     [4, 8, 14, 27, 41],
                     [13, 20, 24, 56, 63],
                     [4, 20, 63, 64, 66]
                     ]
    red_numbers = [3, 8, 19, 20, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )