

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
              'all-time': [2968, 3028, 6075],
              'six-months': [194, 199, 400],
              'recent-trends': [66, 61, 130]
            }

    sets = {
            'all-time' : [768, 842, 905, 916, 840, 867, 937, 6075],
            'six-months' : [53, 53, 62, 54, 63, 63, 52, 400],
            'recent-trends' : [17, 17, 22, 19, 19, 22, 14, 130]
    }

    winning_hands = {
                     'singles': [199, 15, 6], 'pairs': [627, 42, 13], 
                     'two_pairs': [229, 14, 5], 'three_of_set': [132, 7, 2], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 3], 20: [110, 8, 3], 30: [101, 5, 1], 
                  40: [72, 7, 2], 50: [88, 5, 2], 60: [99, 5, 1]
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
              'all-time': [604, 611, 1215],
              'six-months': [39, 41, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [430, 441, 344, 1215],
            'six-months' : [28, 25, 27, 80],
            'recent-trends' : [6, 8, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 6, 5, 9, 6, 8, 7, 4, 2, 3, 
                       5, 8, 5, 4, 5, 8, 7, 6, 2, 7, 
                       7, 2, 14, 3, 4, 2, 4, 10, 9, 5, 
                       4, 7, 4, 6, 7, 6, 8, 3, 4, 8, 
                       4, 4, 9, 9, 6, 4, 7, 5, 7, 7, 
                       4, 12, 8, 6, 5, 5, 5, 4, 7, 8, 
                       4, 8, 5, 5, 5, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        3, 1, 1, 3, 3, 1, 3, 0, 2, 1, 
                        0, 2, 4, 2, 2, 2, 2, 1, 1, 1, 
                        2, 0, 5, 1, 2, 0, 2, 4, 5, 2, 
                        2, 2, 1, 3, 3, 1, 4, 0, 1, 3, 
                        1, 3, 4, 3, 1, 0, 1, 3, 0, 3, 
                        1, 7, 2, 1, 1, 1, 1, 2, 3, 2, 
                        2, 3, 1, 2, 1, 0, 2, 1, 0
                    ]

    red_numbers_6 = [
                     4, 4, 2, 3, 3, 4, 1, 2, 5, 1, 
                     3, 4, 3, 4, 3, 0, 1, 2, 4, 8, 
                     3, 1, 1, 6, 7, 1
                    ]

    red_numbers_trends = [
                          0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 
                          3, 1, 2, 0, 1, 0, 0, 0, 1, 2, 
                          3, 1, 0, 2, 4, 0
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
                     6.94, 7.74, 7.88, 7.09, 6.74, 7.68, 6.51, 6.28, 7.07, 6.52, 
                     7.00, 7.96, 5.57, 6.74, 6.76, 7.42, 7.77, 6.78, 7.07, 7.96, 
                     9.16, 6.84, 8.88, 6.94, 5.92, 5.51, 8.93, 7.24, 6.49, 6.98, 
                     7.26, 8.48, 8.61, 6.07, 6.65, 7.97, 7.98, 7.20, 7.98, 7.09, 
                     6.43, 6.80, 7.29, 8.05, 7.66, 5.89, 7.63, 6.39, 5.49, 7.18, 
                     6.10, 7.85, 7.63, 7.44, 6.96, 6.86, 7.25, 6.60, 7.64, 6.24, 
                     9.02, 8.15, 8.04, 8.15, 6.09, 7.56, 7.45, 7.22, 9.28
                     ]
    red_numbers = [
                   3.67, 3.41, 3.91, 5.03, 4.51, 4.00, 3.46, 3.47, 4.35, 3.50, 
                   3.83, 3.37, 3.63, 4.28, 3.36, 2.99, 3.18, 4.31, 3.88, 4.23, 
                   4.27, 3.23, 3.10, 4.89, 4.28, 3.86
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
                     [15, 21, 46, 59, 68],
                     [20, 23, 24, 57, 63],
                     [29, 31, 51, 55, 61],
                     [1, 4, 12, 42, 50],
                     [17, 30, 34, 36, 69]
                     ]
    red_numbers = [2, 7, 24, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )