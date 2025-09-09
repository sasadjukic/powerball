

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
              'all-time': [3040, 3091, 6215],
              'six-months': [201, 189, 400],
              'recent-trends': [67, 59, 130]
            }

    sets = {
            'all-time' : [788, 863, 925, 936, 861, 878, 964, 6215],
            'six-months' : [55, 56, 64, 53, 61, 52, 59, 400],
            'recent-trends' : [18, 21, 18, 18, 21, 10, 24, 130]
    }

    winning_hands = {
                     'singles': [204, 16, 5], 'pairs': [641, 42, 14], 
                     'two_pairs': [234, 12, 3], 'three_of_set': [136, 8, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [82, 5, 1], 20: [114, 9, 4], 30: [102, 5, 1], 
                  40: [75, 9, 2], 50: [88, 3, 0], 60: [103, 6, 4]
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
              'all-time': [616, 627, 1243],
              'six-months': [41, 39, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [442, 446, 355, 1243],
            'six-months' : [31, 21, 28, 80],
            'recent-trends' : [11, 5, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 4, 5, 10, 6, 5, 8, 7, 5, 2, 
                       8, 7, 5, 5, 6, 9, 4, 6, 4, 5, 
                       6, 3, 15, 4, 7, 2, 4, 10, 8, 4, 
                       5, 2, 8, 7, 10, 5, 7, 2, 3, 9, 
                       5, 5, 9, 8, 6, 5, 4, 6, 4, 6, 
                       6, 9, 8, 3, 3, 2, 4, 4, 7, 5, 
                       9, 9, 6, 8, 5, 3, 4, 2, 8
                    ]

    white_numbers_trends = [
                        0, 1, 2, 3, 0, 2, 2, 6, 2, 0, 
                        4, 2, 0, 2, 3, 4, 0, 3, 3, 0, 
                        1, 2, 4, 2, 2, 1, 2, 3, 1, 0, 
                        3, 0, 4, 3, 4, 2, 1, 1, 0, 4, 
                        2, 1, 3, 2, 2, 2, 1, 2, 2, 2, 
                        2, 0, 3, 1, 0, 0, 1, 0, 1, 1, 
                        5, 4, 2, 4, 3, 0, 1, 1, 3
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 5, 3, 0, 2, 4, 1, 
                     3, 3, 3, 1, 2, 0, 2, 2, 4, 4, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 2, 0, 0, 1, 2, 0, 
                          0, 0, 0, 1, 0, 0, 2, 2, 0, 1, 
                          1, 3, 2, 1, 2, 0
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
                     7.53, 7.51, 7.72, 6.59, 6.82, 7.80, 7.06, 6.46, 6.93, 6.65, 
                     7.06, 7.68, 5.45, 6.31, 7.41, 7.12, 7.14, 6.81, 7.13, 7.35, 
                     9.21, 7.16, 8.75, 7.11, 6.53, 5.82, 8.21, 7.68, 6.22, 6.96, 
                     6.74, 8.34, 8.30, 6.77, 6.59, 7.98, 8.05, 6.52, 8.06, 7.28, 
                     6.61, 6.81, 7.24, 7.96, 7.67, 5.87, 7.72, 6.33, 5.89, 7.58, 
                     5.91, 7.27, 8.27, 7.24, 6.77, 6.96, 6.72, 6.67, 7.41, 6.39, 
                     9.14, 8.35, 8.69, 8.41, 6.55, 7.17, 7.78, 7.19, 8.62
                     ]
    red_numbers = [
                   3.60, 3.61, 4.05, 4.80, 4.30, 3.42, 3.45, 3.45, 4.00, 3.56, 
                   3.15, 3.41, 3.95, 4.84, 2.88, 3.09, 3.57, 4.50, 3.52, 4.15, 
                   5.08, 3.30, 3.57, 4.29, 4.69, 3.77
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
                     [4, 12, 17, 44, 46],
                     [3, 5, 27, 55, 56],
                     [31, 35, 45, 61, 66],
                     [7, 14, 25, 29, 60],
                     [16, 26, 32, 63, 64]
                     ]
    red_numbers = [7, 10, 11, 14, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )