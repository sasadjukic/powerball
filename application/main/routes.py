

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
              'all-time': [3295, 3356, 6740],
              'six-months': [194, 201, 400],
              'recent-trends': [55, 74, 130]
            }

    sets = {
            'all-time' : [854, 937, 1003, 1005, 930, 967, 1044, 6740],
            'six-months' : [51, 54, 61, 55, 50, 74, 55, 400],
            'recent-trends' : [13, 20, 14, 19, 23, 21, 20, 130]
    }

    winning_hands = {
                     'singles': [224, 16, 7], 'pairs': [700, 46, 13], 
                     'two_pairs': [250, 11, 3], 'three_of_set': [142, 5, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 3], 20: [120, 5, 2], 30: [107, 5, 1], 
                  40: [86, 6, 2], 50: [101, 10, 2], 60: [113, 8, 2]
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
              'all-time': [665, 683, 1348],
              'six-months': [38, 42, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [479, 482, 387, 1348],
            'six-months' : [30, 22, 28, 80],
            'recent-trends' : [12, 5, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 3, 7, 5, 8, 9, 8, 6, 3, 4, 
                       7, 3, 3, 5, 3, 5, 4, 12, 8, 5, 
                       8, 3, 4, 7, 5, 4, 7, 13, 5, 8, 
                       7, 4, 6, 3, 5, 10, 5, 3, 4, 4, 
                       5, 8, 6, 2, 2, 4, 9, 5, 5, 4, 
                       10, 11, 7, 4, 4, 10, 7, 9, 8, 7, 
                       3, 5, 10, 10, 6, 3, 1, 6, 4
                    ]

    white_numbers_trends = [
                        0, 0, 3, 2, 0, 2, 4, 0, 2, 2, 
                        3, 2, 2, 1, 1, 1, 2, 4, 2, 1, 
                        3, 0, 0, 4, 2, 0, 2, 1, 1, 4, 
                        2, 1, 1, 0, 1, 5, 3, 1, 1, 0, 
                        4, 6, 3, 0, 1, 2, 5, 0, 2, 1, 
                        2, 6, 1, 0, 1, 4, 3, 0, 3, 2, 
                        2, 1, 4, 5, 3, 0, 1, 1, 1
                    ]

    red_numbers_6 = [
                     8, 5, 3, 2, 4, 5, 3, 0, 0, 1, 
                     3, 2, 2, 5, 3, 1, 2, 1, 2, 4, 
                     4, 2, 8, 4, 1, 5
                    ]

    red_numbers_trends = [
                          4, 2, 2, 0, 2, 1, 1, 0, 0, 0, 
                          1, 0, 1, 1, 2, 0, 0, 0, 0, 2, 
                          1, 1, 0, 1, 1, 3
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
                     6.95, 6.82, 7.98, 7.34, 6.71, 7.77, 6.80, 6.21, 6.86, 6.65, 
                     7.66, 7.63, 5.34, 6.22, 7.03, 7.31, 6.71, 7.18, 7.94, 7.25, 
                     8.96, 6.35, 8.84, 7.40, 6.21, 5.47, 8.96, 9.07, 6.23, 6.88, 
                     7.26, 8.44, 7.85, 5.83, 6.93, 8.71, 7.33, 6.40, 7.77, 7.41, 
                     6.43, 7.14, 7.39, 7.24, 6.99, 6.09, 7.87, 6.19, 5.88, 7.44, 
                     6.72, 8.22, 8.01, 7.14, 6.30, 7.75, 7.04, 6.90, 7.54, 6.97, 
                     8.78, 8.23, 8.53, 8.99, 6.18, 6.91, 7.43, 6.95, 8.09
                     ]
    red_numbers = [
                   4.32, 3.80, 3.99, 4.35, 4.07, 4.08, 3.13, 3.35, 4.03, 3.43, 
                   3.06, 3.43, 3.74, 4.75, 3.24, 2.70, 3.18, 4.30, 3.85, 3.74, 
                   4.42, 3.68, 3.93, 4.87, 4.64, 3.92
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
                     [2, 6, 11, 28, 30],
                     [29, 37, 38, 57, 69],
                     [8, 24, 27, 46, 50],
                     [3, 21, 42, 43, 46],
                     [5, 9, 25, 28, 60]
                     ]
    red_numbers = [6, 8, 14, 16, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )