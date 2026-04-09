

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
              'all-time': [3270, 3312, 6670],
              'six-months': [204, 192, 400],
              'recent-trends': [64, 65, 130]
            }

    sets = {
            'all-time' : [850, 931, 994, 990, 917, 958, 1030, 6670],
            'six-months' : [54, 61, 62, 49, 47, 72, 55, 400],
            'recent-trends' : [18, 24, 17, 11, 19, 26, 15, 130]
    }

    winning_hands = {
                     'singles': [221, 16, 5], 'pairs': [694, 48, 15], 
                     'two_pairs': [247, 9, 2], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 9, 5], 20: [118, 3, 2], 30: [106, 4, 0], 
                  40: [85, 8, 3], 50: [101, 11, 2], 60: [111, 8, 2]
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
              'all-time': [657, 677, 1334],
              'six-months': [36, 44, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [473, 477, 384, 1334],
            'six-months' : [26, 26, 28, 80],
            'recent-trends' : [11, 3, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 8, 8, 7, 3, 6, 
                       8, 4, 5, 6, 2, 6, 5, 12, 7, 6, 
                       7, 4, 4, 5, 3, 5, 7, 15, 6, 5, 
                       6, 7, 5, 4, 4, 6, 4, 3, 5, 6, 
                       4, 6, 7, 4, 1, 2, 7, 6, 4, 4, 
                       9, 11, 6, 6, 4, 8, 7, 10, 7, 7, 
                       3, 5, 7, 8, 5, 7, 3, 5, 5
                    ]

    white_numbers_trends = [
                        0, 1, 3, 1, 1, 5, 5, 0, 2, 2, 
                        4, 2, 1, 2, 0, 2, 3, 5, 3, 3, 
                        2, 2, 3, 1, 0, 0, 1, 4, 1, 2, 
                        1, 0, 2, 0, 1, 3, 1, 1, 0, 1, 
                        3, 5, 2, 0, 0, 0, 4, 3, 1, 3, 
                        0, 6, 0, 3, 2, 5, 2, 3, 2, 1, 
                        1, 1, 2, 5, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     8, 4, 3, 2, 3, 4, 2, 0, 0, 3, 
                     2, 4, 1, 5, 3, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 4
                    ]

    red_numbers_trends = [
                          4, 1, 1, 0, 2, 3, 0, 0, 0, 1, 
                          0, 1, 1, 0, 0, 0, 0, 0, 0, 3, 
                          2, 0, 1, 4, 1, 1
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
                     7.08, 7.48, 8.22, 6.33, 6.43, 7.89, 7.00, 6.59, 6.90, 6.88, 
                     7.63, 7.34, 5.03, 6.26, 7.09, 7.36, 6.67, 7.76, 7.55, 7.05, 
                     8.82, 6.63, 8.48, 6.74, 6.39, 6.04, 8.24, 9.00, 6.71, 7.09, 
                     7.62, 8.50, 8.01, 6.21, 6.54, 8.06, 8.02, 6.72, 7.40, 7.67, 
                     6.28, 7.03, 6.88, 8.08, 7.34, 5.75, 7.95, 6.24, 5.43, 7.25, 
                     6.53, 8.04, 8.34, 6.99, 6.68, 6.65, 7.02, 6.93, 7.89, 6.72, 
                     8.36, 8.47, 8.74, 8.59, 6.14, 7.27, 7.20, 7.24, 8.54
                     ]
    red_numbers = [
                   4.06, 3.72, 4.17, 4.28, 4.52, 3.89, 3.22, 3.33, 4.08, 3.65, 
                   3.28, 3.42, 3.55, 4.74, 2.91, 2.93, 3.18, 4.32, 3.73, 4.42, 
                   4.86, 3.59, 3.55, 4.72, 4.14, 3.74
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
                     [22, 36, 39, 57, 64],
                     [28, 30, 44, 47, 53],
                     [21, 49, 62, 67, 69],
                     [38, 55, 61, 64, 68],
                     [7, 8, 39, 53, 59]
                     ]
    red_numbers = [2, 10, 14, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )