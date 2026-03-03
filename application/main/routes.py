

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
              'all-time': [3230, 3272, 6590],
              'six-months': [205, 191, 400],
              'recent-trends': [63, 64, 130]
            }

    sets = {
            'all-time' : [838, 914, 986, 984, 905, 941, 1022, 6590],
            'six-months' : [53, 54, 69, 49, 47, 65, 63, 400],
            'recent-trends' : [18, 14, 25, 15, 15, 25, 18, 130]
    }

    winning_hands = {
                     'singles': [217, 13, 3], 'pairs': [685, 49, 17], 
                     'two_pairs': [246, 12, 4], 'three_of_set': [138, 2, 0], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [87, 5, 1], 20: [118, 7, 3], 30: [106, 4, 1], 
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
              'all-time': [648, 670, 1318],
              'six-months': [34, 46, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [466, 475, 377, 1318],
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
                       3, 6, 10, 4, 8, 6, 5, 9, 2, 5, 
                       6, 2, 4, 5, 5, 7, 4, 10, 6, 5, 
                       5, 5, 5, 5, 4, 6, 9, 16, 9, 4, 
                       6, 9, 6, 4, 4, 4, 4, 3, 5, 7, 
                       2, 4, 6, 5, 3, 3, 5, 6, 6, 4, 
                       9, 7, 11, 6, 3, 5, 5, 9, 6, 8, 
                       5, 7, 5, 9, 5, 9, 5, 5, 5
                    ]

    white_numbers_trends = [
                        0, 3, 1, 1, 5, 4, 0, 3, 1, 0, 
                        2, 0, 0, 1, 1, 2, 1, 4, 3, 2, 
                        4, 1, 2, 2, 1, 1, 5, 5, 2, 1, 
                        2, 0, 2, 1, 3, 2, 2, 1, 1, 4, 
                        0, 1, 2, 0, 1, 1, 1, 3, 2, 1, 
                        4, 2, 2, 2, 2, 4, 2, 5, 1, 4, 
                        1, 1, 4, 4, 2, 1, 0, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 4, 3, 2, 0, 1, 3, 
                     2, 3, 0, 6, 4, 2, 4, 2, 5, 4, 
                     3, 3, 8, 2, 0, 3
                    ]

    red_numbers_trends = [
                          1, 1, 0, 2, 2, 3, 0, 0, 0, 1, 
                          1, 1, 0, 3, 1, 0, 1, 1, 0, 1, 
                          1, 0, 4, 2, 0, 0
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
                     6.67, 7.44, 7.76, 6.70, 6.84, 7.11, 6.49, 6.68, 6.85, 6.37, 
                     7.43, 7.54, 5.63, 6.59, 6.61, 7.29, 6.84, 7.42, 7.53, 7.42, 
                     9.17, 6.75, 8.76, 7.15, 6.34, 5.50, 8.46, 8.59, 7.04, 6.87, 
                     7.06, 8.69, 8.52, 6.03, 5.97, 8.28, 8.11, 7.22, 7.65, 7.91, 
                     6.16, 6.98, 7.24, 7.63, 7.07, 5.86, 8.17, 6.23, 5.94, 7.06, 
                     7.07, 7.94, 8.24, 7.09, 6.82, 6.60, 6.75, 7.03, 7.85, 6.47, 
                     9.09, 8.00, 7.96, 8.79, 6.33, 7.84, 6.92, 6.79, 8.80, 8.51
                     ]
    red_numbers = [
                   3.89, 3.78, 3.77, 4.62, 4.29, 3.96, 3.45, 3.43, 4.03, 3.25, 
                   3.39, 3.28, 3.30, 4.69, 3.28, 3.22, 3.29, 4.60, 3.93, 4.44, 
                   4.57, 3.36, 3.71, 4.59, 4.15, 3.73
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
                     [14, 15, 34, 36, 64],
                     [38, 42, 53, 60, 67],
                     [10, 17, 21, 50, 58],
                     [12, 28, 39, 51, 59],
                     [4, 6, 22, 41, 44]
                     ]
    red_numbers = [2, 6, 18, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )