

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
              'all-time': [3470, 3533, 7095],
              'six-months': [192, 204, 400],
              'recent-trends': [71, 58, 130]
            }

    sets = {
            'all-time' : [905, 994, 1047, 1049, 983, 1028, 1089, 7095],
            'six-months' : [53, 61, 49, 56, 59, 68, 54, 400],
            'recent-trends' : [17, 25, 19, 16, 19, 22, 12, 130]
    }

    winning_hands = {
                     'singles': [235, 13, 1], 'pairs': [736, 39, 13], 
                     'two_pairs': [266, 18, 7], 'three_of_set': [150, 10, 5], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [87, 6, 2], 10: [96, 5, 3], 20: [122, 3, 2], 30: [109, 3, 1], 
                  40: [94, 8, 2], 50: [109, 8, 2], 60: [118, 6, 1]
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
              'all-time': [704, 715, 1419],
              'six-months': [45, 35, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [504, 513, 402, 1419],
            'six-months' : [29, 35, 16, 80],
            'recent-trends' : [9, 11, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 6, 9, 10, 7, 5, 2, 6, 5, 5, 
                       2, 4, 6, 10, 6, 9, 8, 5, 6, 3, 
                       8, 3, 3, 6, 6, 5, 4, 4, 7, 9, 
                       6, 7, 4, 3, 4, 7, 7, 7, 2, 6, 
                       5, 9, 2, 10, 4, 5, 4, 8, 6, 8, 
                       5, 5, 5, 5, 9, 6, 9, 8, 8, 5, 
                       5, 3, 5, 8, 10, 4, 6, 4, 4
                    ]

    white_numbers_trends = [
                        2, 2, 2, 4, 2, 1, 1, 1, 2, 1, 
                        2, 2, 2, 3, 4, 2, 3, 2, 4, 1, 
                        4, 1, 3, 2, 2, 1, 0, 2, 3, 2, 
                        1, 4, 2, 1, 1, 1, 2, 1, 1, 3, 
                        1, 5, 0, 3, 2, 1, 1, 1, 2, 2, 
                        2, 1, 1, 1, 4, 2, 3, 4, 2, 0, 
                        1, 1, 0, 2, 3, 0, 2, 1, 2
                    ]

    red_numbers_6 = [
                     1, 5, 7, 2, 4, 1, 4, 1, 4, 4, 
                     3, 4, 5, 7, 4, 1, 2, 3, 2, 4, 
                     0, 3, 4, 1, 3, 1
                    ]

    red_numbers_trends = [
                          0, 1, 2, 0, 1, 0, 2, 0, 3, 2, 
                          1, 0, 1, 3, 1, 0, 0, 1, 2, 2, 
                          0, 1, 2, 1, 0, 0
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
                     7.28, 7.25, 8.34, 7.27, 6.72, 7.25, 6.47, 6.69, 6.67, 6.72, 
                     7.22, 7.53, 5.47, 6.67, 7.25, 7.62, 6.99, 7.19, 7.31, 7.51, 
                     9.19, 6.85, 8.60, 7.05, 6.05, 5.87, 8.30, 8.36, 6.74, 6.97, 
                     6.96, 8.79, 8.36, 6.19, 6.19, 8.43, 7.66, 7.10, 7.61, 7.42, 
                     6.39, 7.08, 6.90, 7.64, 7.00, 5.70, 8.06, 6.70, 6.39, 7.40, 
                     6.72, 7.67, 8.00, 7.04, 6.83, 7.00, 7.01, 6.61, 8.21, 6.07, 
                     8.51, 7.60, 8.11, 8.97, 6.59, 6.95, 7.46, 6.77, 8.51
                ]
    red_numbers = [
                   3.94, 4.15, 4.06, 4.55, 4.21, 4.11, 3.43, 3.29, 4.46, 3.54, 
                   3.45, 3.26, 3.82, 4.64, 3.44, 2.97, 3.05, 4.28, 3.52, 4.17, 
                   4.06, 3.44, 3.69, 4.55, 4.23, 3.69
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
                     [19, 24, 26, 51, 64],
                     [16, 38, 47, 48, 53],
                     [11, 26, 28, 32, 63],
                     [27, 46, 49, 63, 67],
                     [9, 15, 30, 46, 61]
                     ]
    red_numbers = [4, 13, 19, 20, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )