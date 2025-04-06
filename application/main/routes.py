

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

        # if user number is greater or equall to 70, then flash error
        if number >= 70:
            flash('Invalid Input')
            return redirect(url_for('search'))

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
              'all-time': [2873, 2932, 5880],
              'six-months': [202, 192, 400],
              'recent-trends': [63, 66, 130]
            }

    sets = {
            'all-time' : [743, 818, 872, 890, 809, 836, 912, 5880],
            'six-months' : [54, 57, 59, 59, 58, 59, 54, 400],
            'recent-trends' : [16, 19, 23, 12, 21, 22, 17, 130]
    }

    winning_hands = {
                     'singles': [191, 12, 5], 'pairs': [607, 45, 15], 
                     'two_pairs': [224, 13, 5], 'three_of_set': [128, 9, 1], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 11, 3], 20: [105, 9, 2], 30: [99, 6, 2], 
                  40: [67, 5, 2], 50: [85, 4, 1], 60: [98, 6, 3]
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
              'all-time': [586, 590, 1176], 
              'six-months': [40, 40, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [419, 429, 328, 1176],
            'six-months' : [30, 27, 23, 80],
            'recent-trends' : [11, 9, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 7, 4, 6, 5, 11, 5, 5, 4, 2, 
                       6, 11, 5, 3, 5, 6, 8, 8, 3, 5, 
                       9, 4, 9, 4, 5, 4, 6, 7, 6, 7, 
                       6, 8, 7, 4, 6, 5, 5, 5, 6, 7, 
                       5, 1, 8, 8, 7, 5, 6, 4, 7, 6, 
                       4, 9, 7, 7, 5, 4, 8, 7, 2, 8, 
                       6, 7, 5, 8, 4, 6, 6, 1, 3
                    ]

    white_numbers_trends = [
                        0, 3, 1, 3, 2, 3, 3, 1, 0, 1, 
                        5, 2, 1, 0, 0, 2, 3, 4, 1, 2, 
                        4, 1, 6, 1, 1, 0, 1, 5, 2, 2, 
                        0, 1, 1, 1, 1, 4, 0, 1, 1, 2, 
                        2, 0, 1, 4, 2, 2, 3, 1, 4, 4, 
                        1, 3, 2, 2, 2, 2, 3, 1, 2, 4, 
                        1, 4, 2, 2, 2, 0, 0, 1, 1
                    ]

    red_numbers_6 = [
                     5, 3, 3, 2, 3, 4, 2, 2, 6, 1, 
                     1, 5, 3, 5, 4, 2, 3, 3, 0, 7, 
                     2, 3, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          2, 2, 1, 0, 1, 2, 0, 0, 3, 0, 
                          0, 3, 1, 2, 2, 0, 0, 1, 0, 4, 
                          0, 0, 0, 0, 2, 0
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
                     7.28, 7.25, 7.45, 6.94, 6.54, 8.00, 6.69, 6.56, 7.28, 6.75, 
                     7.14, 7.62, 5.04, 6.69, 6.98, 7.17, 7.22, 6.57, 7.50, 7.48, 
                     8.90, 7.00, 8.56, 7.12, 6.52, 6.07, 8.20, 7.86, 6.03, 7.41, 
                     7.38, 8.25, 8.71, 6.24, 5.84, 8.78, 7.93, 6.67, 8.15, 6.97, 
                     7.07, 6.41, 6.47, 7.86, 7.37, 6.44, 8.66, 6.35, 5.95, 7.15, 
                     6.15, 6.74, 7.68, 7.28, 7.20, 7.26, 7.26, 6.94, 7.46, 6.41, 
                     9.02, 8.06, 9.10, 8.20, 6.36, 7.02, 7.58, 7.38, 8.43
                     ]
    red_numbers = [
                   3.79, 3.37, 3.88, 4.38, 3.96, 3.79, 3.58, 3.61, 4.48, 3.56, 
                   3.74, 3.39, 4.00, 4.66, 3.31, 3.16, 3.30, 4.74, 3.29, 3.86, 
                   4.84, 3.12, 3.41, 4.71, 4.16, 3.91
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
                     [23, 26, 28, 60, 63],
                     [4, 11, 30, 37, 38],
                     [14, 46, 49, 53, 62],
                     [6, 24, 45, 48, 56],
                     [3, 5, 8, 35, 61]
                     ]
    red_numbers = [5, 12, 15, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )