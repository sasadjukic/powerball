

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
              'all-time': [3030, 3081, 6195],
              'six-months': [198, 192, 400],
              'recent-trends': [68, 57, 130]
            }

    sets = {
            'all-time' : [786, 861, 919, 936, 858, 876, 959, 6195],
            'six-months' : [54, 55, 63, 54, 62, 54, 58, 400],
            'recent-trends' : [20, 20, 16, 21, 18, 12, 23, 130]
    }

    winning_hands = {
                     'singles': [204, 16, 6], 'pairs': [637, 40, 11], 
                     'two_pairs': [234, 13, 5], 'three_of_set': [136, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [82, 5, 1], 20: [112, 8, 2], 30: [102, 5, 1], 
                  40: [75, 10, 3], 50: [88, 3, 1], 60: [101, 5, 2]
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
              'all-time': [614, 625, 1239],
              'six-months': [39, 41, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [440, 445, 354, 1239],
            'six-months' : [29, 20, 31, 80],
            'recent-trends' : [11, 4, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 5, 4, 10, 6, 5, 8, 6, 5, 2, 
                       7, 7, 5, 5, 6, 8, 4, 7, 4, 6, 
                       6, 3, 14, 5, 6, 1, 4, 11, 7, 4, 
                       5, 2, 8, 7, 10, 6, 7, 2, 3, 9, 
                       4, 5, 9, 8, 6, 5, 4, 7, 5, 7, 
                       6, 10, 6, 3, 4, 3, 4, 4, 7, 6, 
                       7, 9, 7, 7, 6, 3, 4, 2, 7
                    ]

    white_numbers_trends = [
                        1, 1, 1, 3, 1, 2, 3, 5, 3, 0, 
                        3, 2, 0, 2, 3, 3, 0, 3, 4, 0, 
                        2, 2, 2, 2, 2, 0, 2, 4, 0, 0, 
                        3, 0, 5, 4, 5, 2, 1, 1, 0, 3, 
                        1, 1, 3, 1, 2, 2, 1, 2, 2, 3, 
                        2, 0, 1, 2, 0, 0, 1, 2, 1, 1, 
                        4, 3, 3, 3, 3, 0, 1, 1, 4
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 4, 3, 0, 2, 3, 1, 
                     3, 3, 3, 1, 2, 0, 1, 2, 4, 7, 
                     4, 3, 2, 5, 10, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 2, 0, 0, 2, 1, 0, 
                          0, 0, 0, 1, 0, 0, 1, 2, 0, 1, 
                          2, 2, 2, 1, 3, 0
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
                     7.20, 7.25, 7.80, 6.73, 6.69, 7.52, 7.44, 6.54, 7.73, 7.06, 
                     7.24, 7.79, 5.54, 5.78, 6.49, 7.38, 6.80, 6.94, 7.02, 7.29, 
                     9.29, 6.68, 8.74, 7.25, 6.70, 5.68, 8.25, 7.78, 6.41, 7.44, 
                     7.28, 8.70, 8.84, 7.14, 6.84, 8.05, 8.16, 6.70, 7.91, 7.52, 
                     6.33, 6.85, 6.56, 7.72, 7.26, 5.72, 8.02, 6.80, 5.53, 7.28, 
                     6.17, 7.86, 7.73, 6.75, 6.75, 7.04, 7.14, 6.07, 7.43, 6.25, 
                     9.24, 8.10, 8.57, 8.46, 5.92, 6.94, 7.78, 6.88, 9.26
                     ]
    red_numbers = [
                   4.11, 3.87, 4.05, 4.78, 4.09, 3.69, 3.41, 3.49, 4.42, 3.63, 
                   3.66, 2.93, 3.84, 4.27, 2.83, 3.21, 3.41, 4.35, 3.66, 3.86, 
                   4.78, 3.27, 3.16, 4.49, 4.75, 3.99
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
                     [7, 24, 27, 45, 58],
                     [1, 31, 36, 59, 67],
                     [6, 10, 28, 46, 49],
                     [15, 16, 17, 34, 38],
                     [5, 35, 37, 39, 63]
                     ]
    red_numbers = [2, 11, 12, 18, 20]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )