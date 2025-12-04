

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
              'all-time': [3133, 3183, 6400],
              'six-months': [202, 191, 400],
              'recent-trends': [67, 63, 130]
            }

    sets = {
            'all-time' : [813, 891, 950, 958, 887, 905, 996, 6400],
            'six-months' : [57, 56, 58, 52, 57, 52, 68, 400],
            'recent-trends' : [17, 21, 18, 17, 17, 19, 21, 130]
    }

    winning_hands = {
                     'singles': [213, 19, 8], 'pairs': [659, 37, 13], 
                     'two_pairs': [240, 14, 2], 'three_of_set': [138, 8, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 2, 1], 10: [84, 3, 2], 20: [115, 6, 0], 30: [104, 3, 2], 
                  40: [81, 10, 4], 50: [92, 6, 2], 60: [105, 6, 2]
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
              'all-time': [632, 648, 1280],
              'six-months': [33, 47, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [453, 463, 364, 1280],
            'six-months' : [26, 25, 29, 80],
            'recent-trends' : [6, 12, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 6, 4, 5, 9, 10, 5, 4, 
                       5, 5, 5, 5, 7, 8, 5, 6, 6, 2, 
                       3, 5, 8, 4, 5, 4, 6, 13, 8, 4, 
                       6, 9, 7, 5, 7, 4, 5, 2, 3, 7, 
                       2, 5, 10, 8, 5, 4, 5, 5, 6, 7, 
                       8, 7, 9, 5, 2, 0, 4, 5, 5, 5, 
                       10, 10, 3, 8, 7, 7, 7, 4, 7
                    ]

    white_numbers_trends = [
                        1, 2, 3, 1, 1, 2, 3, 3, 1, 3, 
                        1, 2, 3, 2, 1, 2, 2, 3, 2, 2, 
                        0, 2, 0, 1, 0, 3, 2, 5, 3, 2, 
                        1, 6, 1, 1, 0, 1, 1, 1, 3, 2, 
                        0, 0, 4, 3, 0, 1, 3, 2, 2, 1, 
                        5, 2, 2, 2, 0, 0, 2, 3, 2, 3, 
                        1, 2, 0, 1, 2, 5, 3, 2, 2
                    ]

    red_numbers_6 = [
                     5, 5, 4, 3, 4, 1, 0, 2, 2, 2, 
                     2, 3, 0, 4, 3, 1, 2, 3, 5, 4, 
                     4, 5, 5, 3, 6, 2
                    ]

    red_numbers_trends = [
                          3, 1, 2, 0, 0, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 2, 0, 0, 1, 2, 1, 
                          1, 1, 3, 0, 0, 2
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
                     6.99, 7.52, 7.56, 6.53, 6.26, 7.75, 7.56, 6.67, 6.96, 6.40, 
                     6.89, 7.33, 5.13, 6.46, 7.16, 7.42, 6.91, 6.67, 7.28, 7.59, 
                     8.68, 6.84, 8.42, 6.75, 6.32, 5.74, 8.78, 8.67, 6.36, 7.25, 
                     7.11, 8.76, 8.32, 6.49, 6.67, 8.03, 7.79, 6.62, 8.31, 7.74, 
                     6.48, 6.84, 7.15, 7.88, 7.72, 6.11, 7.33, 6.36, 5.68, 7.31, 
                     6.40, 7.78, 7.93, 7.11, 6.66, 7.07, 6.97, 6.45, 7.49, 6.68, 
                     8.96, 8.53, 8.07, 7.80, 6.54, 7.54, 8.01, 7.77, 8.69
                     ]
    red_numbers = [
                   4.29, 3.63, 4.34, 4.63, 4.38, 3.49, 3.75, 3.51, 4.10, 3.42, 
                   3.48, 3.19, 3.46, 4.60, 3.13, 2.84, 3.14, 4.37, 3.81, 4.33, 
                   4.73, 3.18, 3.44, 4.38, 4.34, 4.04
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
                     [11, 50, 62, 66, 68],
                     [2, 23, 55, 60, 67],
                     [1, 3, 10, 13, 69],
                     [8, 9, 25, 35, 38],
                     [12, 26, 31, 51, 53]
                     ]
    red_numbers = [4, 5, 7, 16, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )