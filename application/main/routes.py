

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
              'all-time': [3331, 3404, 6825],
              'six-months': [184, 211, 400],
              'recent-trends': [53, 75, 130]
            }

    sets = {
            'all-time' : [863, 948, 1011, 1017, 945, 983, 1058, 6825],
            'six-months' : [48, 53, 56, 55, 57, 73, 58, 400],
            'recent-trends' : [11, 15, 13, 24, 21, 23, 23, 130]
    }

    winning_hands = {
                     'singles': [228, 15, 6], 'pairs': [710, 47, 13], 
                     'two_pairs': [253, 12, 5], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 7, 1], 20: [120, 5, 1], 30: [107, 3, 1], 
                  40: [90, 9, 4], 50: [104, 10, 3], 60: [115, 9, 3]
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
              'all-time': [673, 692, 1365],
              'six-months': [39, 41, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [481, 493, 391, 1365],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [6, 15, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 4, 9, 7, 8, 7, 5, 4, 3, 3, 
                       7, 3, 4, 5, 2, 7, 5, 11, 6, 5, 
                       9, 3, 3, 8, 6, 2, 8, 9, 3, 7, 
                       8, 3, 4, 5, 5, 9, 6, 5, 3, 5, 
                       6, 9, 6, 4, 2, 4, 8, 7, 6, 5, 
                       7, 12, 7, 4, 7, 10, 8, 7, 6, 9, 
                       5, 5, 9, 12, 7, 4, 2, 3, 2
                    ]

    white_numbers_trends = [
                        1, 1, 4, 3, 1, 0, 0, 1, 0, 1, 
                        0, 1, 2, 2, 1, 4, 1, 2, 1, 1, 
                        1, 1, 0, 3, 2, 1, 2, 1, 1, 4, 
                        4, 3, 1, 2, 2, 3, 3, 2, 0, 1, 
                        2, 3, 1, 4, 0, 2, 2, 3, 3, 2, 
                        3, 4, 2, 0, 3, 3, 4, 1, 1, 4, 
                        2, 2, 2, 4, 4, 2, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 3, 2, 4, 5, 2, 0, 0, 2, 
                     2, 6, 3, 6, 5, 0, 2, 2, 1, 5, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 1, 0, 1, 0, 0, 1, 
                          1, 4, 2, 3, 3, 0, 0, 1, 0, 1, 
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
                     6.95, 6.35, 8.14, 7.20, 6.69, 7.34, 6.85, 6.20, 6.97, 6.72, 
                     7.23, 7.87, 5.42, 6.64, 6.52, 7.86, 7.29, 7.70, 7.88, 6.81, 
                     8.57, 6.83, 8.40, 6.85, 6.30, 5.89, 8.24, 8.68, 6.61, 7.49, 
                     7.42, 8.42, 7.93, 5.81, 6.37, 7.81, 8.10, 6.50, 7.71, 7.20, 
                     6.52, 6.77, 7.78, 8.07, 6.97, 6.18, 8.72, 6.46, 5.95, 7.34, 
                     6.61, 7.71, 7.64, 6.98, 6.56, 7.21, 7.05, 7.16, 7.36, 6.63, 
                     9.08, 8.14, 8.26, 8.35, 6.51, 6.83, 7.54, 6.97, 8.89
                     ]
    red_numbers = [
                   4.71, 3.79, 3.69, 4.59, 4.20, 3.76, 3.35, 3.26, 3.91, 3.36, 
                   3.35, 3.69, 3.62, 4.41, 3.40, 2.94, 3.11, 4.33, 3.92, 4.21, 
                   4.31, 3.61, 3.83, 4.59, 4.17, 3.89
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
                     [5, 35, 43, 63, 66],
                     [1, 9, 19, 29, 47],
                     [37, 47, 57, 58, 65],
                     [3, 27, 29, 43, 56],
                     [24, 27, 35, 44, 64]
                     ]
    red_numbers = [2, 9, 13, 20, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )