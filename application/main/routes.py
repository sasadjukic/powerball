

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
              'all-time': [3066, 3120, 6270],
              'six-months': [198, 193, 400],
              'recent-trends': [64, 66, 130]
            }

    sets = {
            'all-time' : [796, 870, 932, 941, 870, 886, 975, 6270],
            'six-months' : [55, 53, 61, 52, 63, 50, 66, 400],
            'recent-trends' : [15, 20, 20, 11, 22, 14, 28, 130]
    }

    winning_hands = {
                     'singles': [205, 15, 3], 'pairs': [646, 40, 14], 
                     'two_pairs': [238, 14, 6], 'three_of_set': [137, 9, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [82, 4, 1], 20: [115, 10, 5], 30: [102, 3, 0], 
                  40: [77, 10, 4], 50: [90, 5, 2], 60: [103, 6, 2]
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
              'all-time': [621, 633, 1254],
              'six-months': [37, 43, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [447, 451, 356, 1254],
            'six-months' : [30, 22, 28, 80],
            'recent-trends' : [12, 9, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 9, 5, 3, 8, 7, 5, 3, 
                       4, 5, 4, 6, 9, 9, 4, 5, 4, 4, 
                       4, 4, 12, 5, 6, 2, 5, 10, 9, 5, 
                       6, 4, 7, 7, 9, 3, 8, 1, 2, 8, 
                       4, 8, 9, 7, 8, 5, 3, 6, 5, 7, 
                       5, 8, 9, 3, 3, 2, 3, 3, 7, 5, 
                       9, 10, 5, 9, 6, 5, 6, 3, 8
                    ]

    white_numbers_trends = [
                        1, 1, 5, 1, 0, 1, 3, 2, 1, 1, 
                        3, 1, 0, 3, 5, 4, 1, 1, 1, 0, 
                        0, 3, 4, 2, 1, 1, 3, 3, 3, 1, 
                        2, 2, 2, 2, 0, 0, 2, 0, 0, 4, 
                        2, 3, 1, 2, 3, 2, 2, 0, 3, 3, 
                        1, 0, 6, 1, 1, 0, 0, 0, 2, 2, 
                        5, 4, 1, 5, 3, 2, 2, 2, 2
                    ]

    red_numbers_6 = [
                     5, 7, 2, 5, 5, 1, 0, 2, 3, 1, 
                     3, 1, 2, 2, 2, 1, 2, 2, 6, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          2, 2, 0, 3, 3, 0, 0, 0, 2, 0, 
                          0, 0, 0, 2, 1, 1, 2, 1, 2, 1, 
                          0, 2, 1, 0, 1, 0
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
                     6.48, 7.23, 8.16, 6.65, 6.33, 7.20, 7.04, 6.50, 7.10, 6.78, 
                     7.21, 8.05, 4.98, 6.38, 7.17, 7.76, 6.80, 7.20, 7.31, 7.20, 
                     8.38, 6.89, 9.18, 7.45, 6.53, 5.73, 8.88, 8.56, 6.43, 7.18, 
                     6.85, 7.99, 8.64, 6.31, 6.69, 8.10, 8.33, 6.72, 7.74, 7.11, 
                     6.77, 7.05, 7.43, 7.22, 8.19, 5.94, 7.75, 6.31, 5.61, 6.92, 
                     6.21, 7.79, 7.94, 7.29, 6.66, 6.97, 6.54, 6.41, 8.10, 6.31, 
                     9.68, 8.70, 8.07, 8.28, 6.33, 7.23, 7.62, 7.18, 8.28
                     ]
    red_numbers = [
                   3.98, 3.73, 3.70, 4.77, 4.23, 3.45, 3.29, 3.44, 4.09, 3.29, 
                   3.67, 3.46, 3.74, 4.60, 3.18, 2.90, 3.25, 4.58, 3.65, 4.43, 
                   4.64, 3.65, 3.01, 4.77, 4.61, 3.89
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
                     [10, 12, 18, 24, 28],
                     [2, 22, 63, 66, 68],
                     [23, 41, 50, 52, 64],
                     [49, 51, 55, 62, 66],
                     [8, 19, 21, 44, 69]
                     ]
    red_numbers = [3, 7, 14, 21, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )