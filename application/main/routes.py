

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
              'all-time': [2931, 2992, 6000],
              'six-months': [198, 195, 400],
              'recent-trends': [63, 65, 130]
            }

    sets = {
            'all-time' : [756, 835, 892, 906, 830, 853, 928, 6000],
            'six-months' : [54, 56, 60, 57, 61, 62, 50, 400],
            'recent-trends' : [15, 18, 21, 17, 23, 17, 19, 130]
    }

    winning_hands = {
                     'singles': [194, 10, 4], 'pairs': [622, 44, 16], 
                     'two_pairs': [226, 14, 2], 'three_of_set': [130, 10, 2], 
                     'full_house': [18, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 0], 10: [81, 11, 3], 20: [109, 8, 4], 30: [101, 6, 2], 
                  40: [71, 7, 4], 50: [86, 4, 1], 60: [99, 5, 2]
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
              'all-time': [599, 601, 1200],
              'six-months': [43, 37, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [427, 438, 335, 1200],
            'six-months' : [31, 27, 22, 80],
            'recent-trends' : [10, 9, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       8, 5, 5, 8, 4, 10, 6, 4, 4, 3, 
                       5, 9, 5, 4, 7, 7, 7, 7, 2, 7, 
                       6, 3, 12, 4, 3, 4, 4, 9, 8, 6, 
                       5, 6, 6, 5, 7, 5, 7, 4, 6, 9, 
                       4, 4, 7, 8, 6, 4, 7, 4, 8, 6, 
                       5, 9, 7, 7, 6, 5, 7, 4, 6, 8, 
                       5, 5, 5, 5, 4, 7, 5, 2, 4
                    ]

    white_numbers_trends = [
                        3, 1, 2, 4, 2, 0, 2, 0, 1, 2, 
                        0, 2, 2, 3, 3, 3, 1, 2, 0, 4, 
                        1, 1, 4, 2, 1, 1, 1, 2, 4, 3, 
                        1, 1, 1, 3, 2, 0, 4, 0, 2, 3, 
                        2, 3, 3, 2, 3, 2, 1, 3, 1, 1, 
                        2, 3, 2, 0, 1, 2, 1, 1, 4, 3, 
                        0, 2, 2, 2, 1, 3, 2, 1, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 4, 3, 2, 1, 5, 1, 
                     2, 4, 5, 4, 3, 0, 2, 3, 3, 8, 
                     1, 1, 1, 5, 5, 1
                    ]

    red_numbers_trends = [
                          3, 3, 0, 2, 1, 0, 0, 0, 1, 1, 
                          2, 0, 2, 0, 1, 0, 0, 0, 3, 2, 
                          1, 0, 0, 2, 2, 0
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
                     7.60, 6.97, 8.02, 7.03, 6.30, 7.67, 6.70, 6.58, 7.14, 6.42, 
                     7.37, 7.72, 5.56, 6.30, 7.21, 7.75, 6.97, 7.01, 6.73, 7.51, 
                     8.68, 6.71, 8.45, 7.10, 6.39, 5.93, 8.74, 7.69, 6.74, 7.73, 
                     7.23, 8.71, 8.39, 6.25, 6.23, 8.88, 7.36, 7.15, 8.01, 7.17, 
                     6.72, 6.82, 7.06, 8.22, 8.14, 5.82, 7.64, 6.66, 5.48, 7.32, 
                     6.02, 7.20, 7.76, 7.46, 6.25, 7.29, 6.99, 6.84, 7.94, 6.73, 
                     8.76, 7.85, 8.15, 8.08, 5.64, 7.48, 7.30, 7.61, 8.67
                     ]
    red_numbers = [
                   3.64, 3.81, 4.00, 4.94, 4.02, 4.03, 3.52, 3.58, 4.64, 3.38, 
                   3.65, 3.26, 4.13, 4.15, 3.19, 2.84, 3.37, 4.40, 3.34, 4.27, 
                   4.56, 3.13, 3.32, 4.45, 4.39, 3.99
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
                     [10, 19, 47, 51, 60],
                     [4, 34, 35, 54, 68],
                     [2, 7, 37, 59, 61],
                     [5, 57, 62, 67, 69],
                     [16, 28, 33, 53, 56]
                     ]
    red_numbers = [12, 13, 16, 17, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )