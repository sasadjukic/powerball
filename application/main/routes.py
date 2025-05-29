

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
              'all-time': [2929, 2989, 5995],
              'six-months': [197, 195, 400],
              'recent-trends': [62, 66, 130]
            }

    sets = {
            'all-time' : [755, 835, 891, 905, 830, 852, 927, 5995],
            'six-months' : [54, 56, 59, 57, 62, 61, 51, 400],
            'recent-trends' : [14, 19, 20, 16, 25, 17, 19, 130]
    }

    winning_hands = {
                     'singles': [193, 9, 3], 'pairs': [622, 45, 17], 
                     'two_pairs': [226, 14, 2], 'three_of_set': [130, 10, 2], 
                     'full_house': [18, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 0], 10: [81, 11, 3], 20: [109, 8, 4], 30: [101, 6, 2], 
                  40: [71, 7, 5], 50: [86, 4, 1], 60: [99, 5, 2]
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
              'all-time': [598, 601, 1199],
              'six-months': [43, 37, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [427, 437, 335, 1199],
            'six-months' : [31, 27, 22, 80],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 5, 5, 8, 5, 10, 6, 4, 4, 3, 
                       5, 9, 5, 4, 7, 7, 7, 7, 2, 7, 
                       6, 3, 12, 4, 3, 4, 4, 9, 7, 6, 
                       5, 6, 6, 5, 8, 5, 6, 4, 6, 9, 
                       4, 4, 7, 8, 7, 4, 7, 4, 8, 6, 
                       5, 9, 7, 7, 6, 4, 7, 4, 6, 9, 
                       5, 5, 6, 5, 4, 7, 5, 1, 4
                    ]

    white_numbers_trends = [
                        2, 1, 2, 4, 2, 0, 2, 0, 1, 2, 
                        0, 3, 2, 3, 3, 3, 1, 2, 0, 4, 
                        1, 1, 4, 2, 1, 1, 1, 2, 3, 3, 
                        1, 1, 1, 3, 2, 0, 3, 0, 2, 3, 
                        3, 3, 3, 3, 3, 2, 1, 3, 1, 1, 
                        2, 4, 2, 0, 1, 1, 1, 1, 4, 3, 
                        0, 2, 2, 3, 1, 3, 2, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 4, 3, 2, 1, 5, 1, 
                     2, 5, 4, 4, 3, 0, 2, 3, 3, 8, 
                     1, 1, 1, 5, 5, 1
                    ]

    red_numbers_trends = [
                          3, 3, 0, 2, 1, 0, 0, 0, 1, 1, 
                          2, 0, 1, 0, 1, 0, 0, 0, 3, 2, 
                          1, 0, 0, 2, 3, 0
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
                     6.86, 7.41, 7.91, 6.52, 6.16, 7.59, 7.01, 6.08, 6.95, 7.11, 
                     7.51, 7.92, 5.19, 6.10, 6.99, 7.20, 7.32, 7.10, 6.96, 7.89, 
                     8.83, 7.37, 8.48, 7.34, 5.67, 5.47, 7.99, 8.12, 6.25, 7.02, 
                     6.92, 8.44, 8.43, 6.34, 6.09, 8.77, 8.01, 6.89, 8.39, 6.90, 
                     6.74, 6.64, 7.07, 7.50, 8.12, 5.71, 8.27, 6.30, 5.93, 7.44, 
                     5.90, 6.75, 8.15, 7.38, 7.14, 6.97, 6.68, 6.63, 8.14, 6.70, 
                     8.97, 7.94, 8.49, 8.47, 6.42, 7.65, 8.01, 7.29, 9.10
                     ]
    red_numbers = [
                   3.95, 3.69, 3.71, 4.80, 4.06, 3.89, 3.70, 3.45, 4.54, 3.74, 
                   3.35, 3.20, 3.86, 4.31, 3.07, 3.00, 2.83, 4.50, 3.65, 4.05, 
                   4.46, 3.50, 3.46, 4.71, 4.30, 4.22
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
                     [7, 47, 54, 55, 58],
                     [11, 33, 39, 40, 69],
                     [19, 32, 50, 51, 60],
                     [5, 43, 45, 64, 66],
                     [1, 12, 13, 61, 68]
                     ]
    red_numbers = [9, 10, 11, 15, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )