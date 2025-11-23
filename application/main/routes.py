

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
              'all-time': [3114, 3177, 6375],
              'six-months': [196, 196, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [808, 885, 945, 955, 885, 901, 996, 6375],
            'six-months' : [54, 53, 58, 54, 58, 52, 71, 400],
            'recent-trends' : [17, 19, 16, 16, 18, 17, 27, 130]
    }

    winning_hands = {
                     'singles': [210, 17, 5], 'pairs': [658, 39, 14], 
                     'two_pairs': [239, 14, 4], 'three_of_set': [138, 8, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 2, 1], 10: [84, 4, 2], 20: [115, 6, 1], 30: [103, 3, 1], 
                  40: [81, 10, 5], 50: [92, 6, 2], 60: [105, 7, 2]
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
              'all-time': [629, 646, 1275],
              'six-months': [34, 46, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [450, 462, 363, 1275],
            'six-months' : [25, 26, 29, 80],
            'recent-trends' : [5, 14, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 6, 3, 5, 8, 8, 6, 4, 
                       5, 6, 6, 4, 6, 7, 5, 6, 4, 1, 
                       3, 4, 9, 4, 5, 2, 7, 13, 10, 2, 
                       7, 9, 7, 6, 8, 4, 6, 2, 3, 7, 
                       2, 5, 11, 8, 5, 3, 5, 6, 6, 7, 
                       7, 8, 9, 5, 2, 1, 4, 5, 4, 5, 
                       10, 10, 3, 9, 7, 7, 8, 5, 7
                    ]

    white_numbers_trends = [
                        1, 2, 5, 1, 0, 2, 3, 2, 1, 4, 
                        1, 2, 3, 1, 1, 2, 3, 2, 0, 1, 
                        0, 2, 0, 1, 0, 1, 3, 5, 3, 0, 
                        2, 6, 1, 1, 0, 1, 1, 1, 3, 2, 
                        0, 0, 4, 3, 1, 0, 3, 2, 3, 1, 
                        4, 2, 3, 2, 1, 0, 2, 2, 0, 4, 
                        2, 2, 0, 1, 3, 6, 4, 3, 2
                    ]

    red_numbers_6 = [
                     3, 6, 3, 3, 5, 1, 0, 2, 2, 2, 
                     3, 3, 1, 3, 3, 1, 2, 3, 5, 4, 
                     4, 5, 5, 3, 7, 1
                    ]

    red_numbers_trends = [
                          1, 2, 1, 1, 0, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 2, 1, 0, 1, 3, 1, 
                          1, 1, 3, 0, 0, 1
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
                     6.96, 7.69, 7.99, 7.00, 6.62, 7.34, 6.62, 6.60, 6.76, 6.48, 
                     7.13, 8.11, 5.05, 6.11, 6.72, 7.94, 7.03, 6.77, 7.21, 7.15, 
                     8.43, 6.70, 8.58, 6.52, 6.34, 5.45, 8.75, 7.98, 6.76, 7.04, 
                     6.98, 8.77, 8.70, 6.21, 6.66, 8.36, 8.10, 6.93, 7.78, 7.11, 
                     6.78, 7.03, 7.07, 7.98, 7.52, 6.21, 8.29, 6.33, 5.84, 7.03, 
                     6.63, 7.87, 8.11, 7.30, 6.36, 7.13, 7.10, 6.94, 8.05, 6.75, 
                     9.13, 7.74, 8.06, 8.47, 6.14, 7.59, 7.49, 7.26, 8.37
                     ]
    red_numbers = [
                   3.86, 3.67, 3.74, 5.02, 4.36, 3.49, 3.17, 3.48, 4.61, 3.66, 
                   3.45, 2.92, 3.82, 4.57, 2.91, 2.67, 3.62, 4.16, 3.87, 4.24, 
                   4.69, 3.11, 3.36, 4.59, 4.68, 4.28
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
                     [8, 19, 55, 59, 61],
                     [20, 21, 28, 52, 66],
                     [24, 30, 49, 51, 57],
                     [3, 34, 47, 60, 67],
                     [31, 42, 43, 53, 54]
                     ]
    red_numbers = [1, 12, 19, 22, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )