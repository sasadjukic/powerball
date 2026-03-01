

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
              'all-time': [3227, 3270, 6585],
              'six-months': [205, 191, 400],
              'recent-trends': [64, 63, 130]
            }

    sets = {
            'all-time' : [837, 912, 986, 983, 905, 941, 1021, 6585],
            'six-months' : [53, 53, 70, 48, 48, 65, 63, 400],
            'recent-trends' : [17, 14, 27, 15, 15, 25, 17, 130]
    }

    winning_hands = {
                     'singles': [217, 14, 3], 'pairs': [684, 48, 16], 
                     'two_pairs': [246, 12, 5], 'three_of_set': [138, 2, 0], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [86, 4, 0], 20: [118, 7, 3], 30: [106, 4, 1], 
                  40: [83, 8, 2], 50: [99, 11, 4], 60: [111, 10, 4]
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
              'all-time': [648, 669, 1317],
              'six-months': [34, 46, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [466, 475, 376, 1317],
            'six-months' : [26, 31, 23, 80],
            'recent-trends' : [9, 9, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 10, 4, 8, 6, 5, 9, 3, 5, 
                       6, 3, 4, 5, 5, 7, 3, 9, 6, 5, 
                       5, 6, 5, 5, 4, 6, 9, 16, 9, 4, 
                       6, 9, 6, 4, 4, 4, 4, 2, 5, 7, 
                       3, 4, 6, 5, 3, 3, 5, 6, 6, 4, 
                       9, 7, 11, 6, 3, 5, 5, 9, 6, 8, 
                       6, 6, 5, 9, 5, 9, 5, 5, 5
                    ]

    white_numbers_trends = [
                        0, 2, 1, 1, 5, 4, 0, 3, 1, 0, 
                        3, 0, 0, 1, 1, 2, 0, 4, 3, 2, 
                        5, 1, 2, 3, 1, 1, 5, 5, 2, 1, 
                        2, 0, 2, 1, 3, 2, 2, 1, 1, 4, 
                        0, 1, 2, 0, 1, 1, 1, 3, 2, 1, 
                        4, 2, 2, 2, 2, 4, 2, 5, 1, 4, 
                        1, 0, 4, 4, 2, 1, 0, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 4, 3, 2, 0, 1, 3, 
                     2, 3, 0, 6, 4, 2, 4, 2, 5, 3, 
                     3, 3, 8, 2, 1, 3
                    ]

    red_numbers_trends = [
                          1, 1, 0, 2, 2, 3, 0, 0, 0, 1, 
                          1, 1, 0, 3, 1, 0, 1, 1, 0, 0, 
                          1, 0, 4, 2, 0, 1
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
                     7.02, 7.36, 7.81, 7.10, 6.71, 7.48, 6.54, 7.12, 7.06, 6.52, 
                     7.33, 7.51, 5.15, 6.43, 7.38, 7.70, 6.86, 7.13, 7.71, 7.25, 
                     9.09, 6.76, 8.54, 7.34, 6.72, 5.55, 8.53, 8.42, 6.60, 7.10, 
                     7.06, 8.84, 8.76, 5.73, 6.85, 8.45, 7.73, 6.66, 7.39, 7.50, 
                     6.28, 6.79, 7.32, 7.85, 7.70, 6.09, 7.56, 6.57, 5.93, 7.02, 
                     6.70, 7.13, 8.16, 6.95, 6.32, 6.94, 6.64, 6.52, 7.27, 6.81, 
                     8.84, 8.28, 8.34, 8.40, 6.19, 7.54, 7.68, 6.88, 8.51
                     ]
    red_numbers = [
                   4.05, 3.96, 3.64, 4.92, 4.55, 3.79, 3.13, 3.41, 4.15, 3.79, 
                   3.58, 3.39, 3.66, 4.38, 3.02, 3.03, 3.23, 4.31, 3.62, 4.13, 
                   4.62, 3.43, 3.63, 4.61, 4.35, 3.62
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
                     [23, 24, 54, 55, 61],
                     [3, 4, 50, 63, 67],
                     [19, 20, 21, 35, 69],
                     [11, 42, 44, 53, 68],
                     [7, 8, 36, 41, 60]
                     ]
    red_numbers = [10, 11, 14, 17, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )