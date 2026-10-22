

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
              'all-time': [3466, 3532, 7090],
              'six-months': [190, 206, 400],
              'recent-trends': [70, 59, 130]
            }

    sets = {
            'all-time' : [903, 992, 1047, 1049, 983, 1027, 1089, 7090],
            'six-months' : [52, 60, 49, 57, 60, 67, 55, 400],
            'recent-trends' : [16, 24, 19, 18, 19, 21, 13, 130]
    }

    winning_hands = {
                     'singles': [235, 14, 1], 'pairs': [736, 39, 14], 
                     'two_pairs': [265, 17, 6], 'three_of_set': [150, 10, 5], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [87, 6, 2], 10: [96, 5, 3], 20: [122, 3, 2], 30: [109, 3, 2], 
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
              'all-time': [704, 714, 1418],
              'six-months': [45, 35, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [504, 512, 402, 1418],
            'six-months' : [29, 34, 17, 80],
            'recent-trends' : [10, 10, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 6, 9, 9, 6, 5, 2, 6, 6, 5, 
                       2, 4, 6, 10, 5, 9, 9, 5, 5, 3, 
                       8, 3, 3, 6, 6, 5, 4, 4, 7, 9, 
                       6, 7, 4, 3, 4, 8, 7, 7, 2, 6, 
                       5, 9, 2, 10, 4, 5, 5, 8, 6, 8, 
                       5, 5, 5, 5, 8, 6, 9, 8, 8, 5, 
                       5, 3, 5, 9, 10, 4, 6, 4, 4
                    ]

    white_numbers_trends = [
                        2, 2, 3, 3, 1, 1, 1, 1, 2, 1, 
                        2, 2, 2, 3, 3, 3, 3, 2, 3, 1, 
                        4, 1, 3, 2, 2, 1, 0, 2, 3, 2, 
                        1, 4, 3, 1, 1, 1, 2, 2, 1, 3, 
                        1, 5, 0, 3, 2, 1, 1, 1, 2, 2, 
                        2, 1, 1, 1, 3, 2, 3, 4, 2, 0, 
                        1, 1, 0, 2, 3, 0, 2, 2, 2
                    ]

    red_numbers_6 = [
                     1, 5, 7, 2, 4, 1, 4, 1, 4, 4, 
                     3, 4, 5, 7, 4, 1, 2, 3, 1, 4, 
                     0, 3, 4, 1, 3, 2
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 1, 0, 2, 0, 3, 2, 
                          1, 0, 1, 3, 1, 0, 0, 1, 1, 2, 
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
                     6.33, 7.19, 7.91, 7.20, 6.25, 7.73, 7.13, 6.54, 6.60, 6.89, 
                     6.99, 7.53, 5.14, 6.95, 6.78, 7.84, 6.86, 7.14, 7.41, 7.02, 
                     9.09, 6.55, 8.75, 7.26, 6.21, 5.33, 8.24, 8.62, 6.87, 7.54, 
                     7.35, 8.32, 8.59, 6.24, 6.68, 8.79, 8.17, 6.32, 7.58, 7.41, 
                     6.30, 6.91, 6.31, 8.33, 7.82, 5.36, 7.92, 6.35, 5.85, 6.99, 
                     6.18, 7.71, 8.63, 7.17, 6.52, 6.55, 7.27, 6.94, 7.65, 6.52, 
                     8.90, 8.15, 8.46, 8.81, 6.75, 7.28, 7.77, 7.02, 8.24
                ]
    red_numbers = [
                   4.13, 4.26, 4.32, 4.57, 4.32, 3.74, 3.06, 3.44, 4.06, 3.57, 
                   3.16, 3.50, 4.27, 4.46, 3.24, 2.86, 3.35, 4.13, 3.34, 4.08, 
                   4.44, 3.35, 3.61, 4.50, 4.35, 3.89
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
                     [39, 45, 61, 63, 69],
                     [1, 12, 33, 42, 66],
                     [3, 11, 20, 31, 40],
                     [7, 10, 36, 38, 62],
                     [24, 29, 44, 52, 64]
                     ]
    red_numbers = [8, 14, 17, 24, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )