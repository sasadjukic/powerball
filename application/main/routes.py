

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
              'all-time': [3344, 3411, 6845],
              'six-months': [187, 208, 400],
              'recent-trends': [56, 73, 130]
            }

    sets = {
            'all-time' : [864, 956, 1014, 1019, 948, 986, 1058, 6845],
            'six-months' : [45, 60, 56, 54, 59, 71, 55, 400],
            'recent-trends' : [10, 21, 14, 19, 23, 23, 20, 130]
    }

    winning_hands = {
                     'singles': [229, 15, 6], 'pairs': [710, 44, 12], 
                     'two_pairs': [255, 14, 6], 'three_of_set': [143, 5, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 3, 0], 10: [92, 7, 1], 20: [120, 5, 0], 30: [107, 3, 1], 
                  40: [90, 9, 4], 50: [104, 9, 3], 60: [115, 8, 3]
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
              'all-time': [676, 693, 1369],
              'six-months': [41, 39, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [482, 496, 391, 1369],
            'six-months' : [26, 30, 24, 80],
            'recent-trends' : [5, 16, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 4, 9, 5, 7, 7, 5, 4, 3, 4, 
                       7, 3, 5, 7, 2, 9, 6, 10, 7, 5, 
                       11, 3, 3, 8, 4, 2, 8, 9, 3, 8, 
                       7, 3, 3, 5, 5, 8, 6, 6, 3, 5, 
                       6, 9, 6, 4, 3, 4, 8, 8, 6, 5, 
                       7, 10, 7, 3, 7, 10, 8, 7, 7, 9, 
                       5, 4, 9, 12, 7, 3, 2, 3, 1
                    ]

    white_numbers_trends = [
                        1, 1, 4, 2, 1, 0, 0, 1, 0, 2, 
                        0, 1, 3, 4, 1, 6, 2, 1, 1, 1, 
                        3, 1, 0, 2, 2, 1, 2, 2, 0, 4, 
                        3, 2, 0, 2, 1, 1, 3, 3, 0, 1, 
                        3, 3, 1, 4, 1, 2, 2, 4, 2, 2, 
                        2, 3, 3, 0, 3, 3, 3, 1, 3, 4, 
                        2, 1, 1, 4, 4, 2, 1, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 4, 2, 4, 5, 1, 0, 0, 2, 
                     3, 6, 4, 7, 5, 0, 1, 2, 0, 4, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          0, 1, 2, 0, 1, 0, 1, 0, 0, 1, 
                          1, 4, 3, 4, 2, 0, 0, 1, 0, 1, 
                          0, 1, 1, 0, 1, 1
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
                     7.19, 7.33, 8.23, 6.77, 6.74, 7.79, 6.72, 6.47, 6.96, 6.53, 
                     6.67, 7.17, 5.40, 6.17, 6.49, 8.18, 7.12, 7.71, 6.95, 7.33, 
                     9.28, 6.78, 7.75, 6.99, 5.66, 5.37, 7.98, 8.79, 6.37, 7.57, 
                     6.97, 9.45, 8.34, 5.75, 6.62, 8.86, 7.19, 6.72, 7.35, 7.54, 
                     6.43, 7.29, 6.92, 8.05, 7.77, 6.02, 8.23, 6.45, 6.09, 7.27, 
                     6.37, 7.73, 8.77, 6.93, 6.61, 6.86, 6.82, 6.35, 8.41, 6.98, 
                     9.08, 8.68, 8.27, 8.35, 6.43, 7.21, 7.38, 6.86, 8.14
                     ]
    red_numbers = [
                   3.94, 3.77, 3.80, 4.73, 4.66, 4.11, 3.03, 3.36, 4.09, 2.98, 
                   3.65, 3.70, 3.87, 4.48, 3.11, 2.67, 3.11, 4.35, 3.55, 4.52, 
                   4.50, 3.35, 3.87, 4.35, 4.19, 4.26
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
                     [5, 19, 44, 48, 65],
                     [13, 23, 28, 47, 52],
                     [18, 35, 52, 64, 65],
                     [8, 10, 29, 35, 37],
                     [3, 36, 43, 50, 60]
                     ]
    red_numbers = [3, 7, 17, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )