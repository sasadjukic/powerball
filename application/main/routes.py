

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
              'all-time': [3422, 3502, 7015],
              'six-months': [180, 217, 400],
              'recent-trends': [60, 69, 130]
            }

    sets = {
            'all-time' : [891, 980, 1036, 1036, 970, 1016, 1086, 7015],
            'six-months' : [49, 63, 47, 49, 62, 68, 62, 400],
            'recent-trends' : [20, 17, 18, 12, 15, 25, 23, 130]
    }

    winning_hands = {
                     'singles': [235, 18, 4], 'pairs': [729, 41, 14], 
                     'two_pairs': [260, 13, 5], 'three_of_set': [147, 8, 3], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 2], 10: [96, 8, 3], 20: [120, 2, 0], 30: [108, 2, 1], 
                  40: [93, 9, 2], 50: [108, 8, 3], 60: [118, 7, 3]
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
              'all-time': [697, 706, 1403],
              'six-months': [46, 34, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [500, 505, 398, 1403],
            'six-months' : [33, 28, 19, 80],
            'recent-trends' : [13, 7, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 10, 7, 5, 6, 5, 5, 5, 7, 
                       4, 5, 6, 9, 4, 9, 8, 6, 5, 4, 
                       8, 2, 1, 7, 7, 4, 5, 4, 5, 7, 
                       6, 4, 2, 2, 3, 8, 7, 7, 3, 5, 
                       7, 8, 5, 7, 4, 5, 8, 7, 6, 7, 
                       3, 7, 6, 4, 7, 8, 9, 7, 10, 6, 
                       7, 3, 7, 12, 10, 4, 6, 3, 4
                    ]

    white_numbers_trends = [
                        0, 2, 3, 3, 3, 3, 0, 3, 3, 2, 
                        1, 1, 1, 2, 3, 2, 2, 1, 2, 2, 
                        2, 1, 1, 2, 3, 2, 2, 1, 2, 2, 
                        1, 1, 1, 0, 1, 2, 2, 1, 1, 3, 
                        1, 2, 0, 1, 1, 1, 2, 2, 2, 3, 
                        0, 0, 2, 4, 2, 2, 3, 6, 3, 1, 
                        3, 1, 2, 4, 5, 1, 3, 1, 2
                    ]

    red_numbers_6 = [
                     5, 6, 8, 2, 4, 2, 3, 1, 2, 3, 
                     2, 4, 4, 5, 4, 1, 2, 3, 0, 4, 
                     0, 3, 3, 1, 4, 4
                    ]

    red_numbers_trends = [
                          1, 3, 2, 1, 1, 0, 2, 1, 2, 2, 
                          0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 
                          0, 2, 2, 0, 2, 0
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
                     6.68, 7.40, 8.13, 6.83, 6.75, 7.21, 6.32, 6.23, 6.66, 6.95, 
                     6.82, 7.12, 5.62, 6.91, 6.44, 7.58, 7.32, 7.87, 6.74, 7.11, 
                     9.43, 6.15, 7.90, 6.98, 6.34, 5.51, 8.98, 8.25, 6.72, 7.17, 
                     7.12, 8.48, 8.19, 5.81, 7.11, 8.28, 8.04, 6.85, 7.52, 7.70, 
                     6.75, 6.22, 6.99, 8.01, 7.50, 5.97, 7.75, 6.68, 6.02, 6.70, 
                     6.59, 7.99, 7.91, 7.47, 7.16, 7.30, 7.21, 6.93, 8.75, 6.31, 
                     8.83, 7.77, 8.47, 8.97, 6.41, 6.89, 7.45, 7.14, 8.64
                ]
    red_numbers = [
                   4.18, 3.71, 3.89, 4.62, 4.46, 3.77, 3.55, 3.19, 4.08, 3.39, 
                   3.51, 3.05, 3.59, 5.04, 3.42, 3.08, 3.26, 4.51, 3.89, 4.42, 
                   4.27, 3.08, 3.69, 4.34, 4.39, 3.62
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
                     [6, 18, 27, 39, 53],
                     [8, 19, 25, 55, 66],
                     [29, 32, 39, 40, 69],
                     [6, 25, 55, 68, 69],
                     [13, 20, 23, 58, 69]
                     ]
    red_numbers = [5, 11, 15, 18, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )