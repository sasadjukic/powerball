

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
              'all-time': [3036, 3085, 6205],
              'six-months': [201, 189, 400],
              'recent-trends': [68, 57, 130]
            }

    sets = {
            'all-time' : [788, 862, 922, 936, 859, 877, 961, 6205],
            'six-months' : [55, 56, 64, 53, 60, 54, 58, 400],
            'recent-trends' : [20, 20, 17, 20, 19, 10, 24, 130]
    }

    winning_hands = {
                     'singles': [204, 16, 5], 'pairs': [639, 40, 12], 
                     'two_pairs': [234, 13, 5], 'three_of_set': [136, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [82, 5, 1], 20: [113, 9, 3], 30: [102, 5, 1], 
                  40: [75, 9, 3], 50: [88, 3, 0], 60: [102, 5, 3]
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
              'all-time': [615, 626, 1245],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [441, 445, 355, 1240],
            'six-months' : [30, 20, 30, 80],
            'recent-trends' : [11, 4, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 4, 5, 10, 6, 5, 8, 7, 5, 2, 
                       7, 7, 5, 5, 6, 9, 4, 7, 4, 6, 
                       6, 3, 14, 5, 7, 1, 4, 10, 8, 4, 
                       5, 2, 8, 7, 10, 5, 7, 2, 3, 10, 
                       4, 5, 9, 7, 6, 5, 4, 6, 4, 7, 
                       6, 10, 7, 3, 3, 3, 4, 4, 7, 5, 
                       8, 8, 7, 7, 6, 3, 4, 2, 8
                    ]

    white_numbers_trends = [
                        0, 1, 2, 3, 1, 2, 2, 6, 3, 0, 
                        3, 2, 0, 2, 3, 4, 0, 3, 3, 0, 
                        1, 2, 3, 2, 3, 0, 2, 3, 1, 0, 
                        3, 0, 5, 3, 5, 2, 1, 1, 0, 4, 
                        1, 1, 3, 1, 2, 2, 1, 2, 2, 2, 
                        2, 0, 2, 1, 0, 0, 1, 1, 1, 1, 
                        5, 3, 2, 3, 3, 0, 1, 1, 5
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 5, 3, 0, 2, 3, 1, 
                     3, 3, 3, 1, 2, 0, 1, 2, 4, 6, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 3, 0, 0, 1, 1, 0, 
                          0, 0, 0, 1, 0, 0, 1, 2, 0, 1, 
                          1, 3, 2, 1, 3, 0
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
                     7.14, 7.28, 7.97, 7.05, 6.44, 6.86, 7.00, 7.58, 7.13, 6.53, 
                     7.07, 8.17, 5.42, 6.76, 7.25, 7.56, 6.78, 6.83, 7.30, 7.88, 
                     9.62, 6.37, 9.41, 7.20, 6.30, 5.53, 8.46, 8.53, 6.20, 6.90, 
                     6.55, 8.60, 8.97, 6.13, 7.10, 8.56, 7.95, 6.90, 8.00, 7.16, 
                     6.06, 7.38, 7.31, 7.66, 7.50, 5.42, 7.67, 6.07, 5.18, 7.28, 
                     6.34, 7.25, 8.18, 6.65, 6.54, 7.11, 6.54, 6.27, 7.95, 6.93, 
                     8.67, 8.32, 8.05, 8.59, 6.60, 6.91, 7.29, 7.26, 8.58
                     ]
    red_numbers = [
                   3.92, 3.75, 3.86, 4.51, 4.56, 3.78, 3.28, 3.27, 4.11, 3.20, 
                   3.27, 3.24, 3.79, 4.40, 3.12, 3.08, 3.46, 4.39, 3.38, 4.17, 
                   4.85, 3.67, 3.46, 4.75, 4.91, 3.82
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
                     [10, 15, 27, 55, 65],
                     [4, 11, 14, 20, 23],
                     [21, 22, 26, 47, 62],
                     [16, 17, 33, 37, 40],
                     [8, 43, 50, 56, 59]
                     ]
    red_numbers = [2, 8, 11, 16, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )