

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
              'all-time': [2926, 2988, 5990],
              'six-months': [197, 196, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [755, 835, 889, 903, 830, 851, 927, 5990],
            'six-months' : [54, 58, 57, 56, 63, 60, 52, 400],
            'recent-trends' : [15, 20, 19, 14, 25, 17, 20, 130]
    }

    winning_hands = {
                     'singles': [193, 9, 4], 'pairs': [622, 46, 17], 
                     'two_pairs': [225, 13, 1], 'three_of_set': [130, 10, 2], 
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
              'all-time': [597, 601, 1198],
              'six-months': [43, 37, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [427, 436, 335, 1198],
            'six-months' : [32, 26, 22, 80],
            'recent-trends' : [11, 7, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 5, 5, 8, 5, 10, 6, 4, 4, 3, 
                       5, 10, 6, 4, 7, 7, 7, 7, 2, 7, 
                       6, 3, 11, 4, 3, 4, 3, 9, 7, 6, 
                       5, 5, 6, 6, 7, 5, 6, 4, 6, 9, 
                       4, 4, 7, 9, 7, 4, 7, 4, 8, 6, 
                       5, 9, 7, 7, 6, 4, 7, 4, 5, 9, 
                       5, 5, 6, 5, 4, 7, 6, 1, 4
                    ]

    white_numbers_trends = [
                        2, 1, 2, 4, 2, 0, 3, 0, 1, 2, 
                        1, 3, 2, 3, 3, 3, 1, 2, 0, 4, 
                        2, 1, 3, 2, 1, 1, 0, 2, 3, 3, 
                        1, 0, 1, 3, 1, 0, 3, 0, 2, 3, 
                        3, 3, 3, 3, 3, 2, 1, 3, 1, 1, 
                        2, 4, 3, 0, 1, 1, 1, 1, 3, 3, 
                        1, 2, 2, 3, 1, 3, 2, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 4, 3, 2, 2, 5, 1, 
                     1, 5, 4, 4, 3, 0, 2, 3, 3, 8, 
                     1, 1, 1, 5, 5, 1
                    ]

    red_numbers_trends = [
                          3, 4, 0, 2, 1, 0, 0, 0, 1, 1, 
                          1, 0, 1, 0, 1, 0, 0, 0, 3, 2, 
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
                     7.52, 7.33, 7.34, 7.13, 6.65, 7.89, 6.80, 6.56, 6.80, 6.94, 
                     7.40, 8.23, 5.55, 6.25, 6.69, 7.42, 6.66, 7.07, 7.04, 7.40, 
                     9.30, 6.91, 8.14, 6.61, 6.48, 5.78, 8.49, 7.75, 6.61, 6.72, 
                     6.42, 8.37, 8.68, 6.01, 6.28, 8.31, 8.10, 6.64, 8.54, 7.71, 
                     6.96, 6.96, 6.93, 7.37, 7.73, 5.94, 8.05, 6.52, 5.86, 7.22, 
                     6.67, 7.27, 7.30, 7.01, 6.46, 7.14, 7.00, 6.88, 8.01, 6.66, 
                     8.97, 8.14, 8.74, 8.01, 6.18, 7.85, 7.66, 7.19, 8.80
                     ]
    red_numbers = [
                   3.85, 3.40, 3.70, 4.94, 4.14, 3.95, 4.05, 3.30, 4.45, 3.66, 
                   3.58, 3.30, 3.74, 4.48, 3.24, 3.15, 3.72, 4.23, 3.89, 3.81, 
                   4.37, 3.06, 3.28, 4.61, 4.12, 3.98
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
                     [8, 11, 12, 45, 49],
                     [20, 46, 47, 67, 69],
                     [28, 37, 50, 55, 57],
                     [6, 13, 39, 42, 62],
                     [15, 21, 32, 61, 63]
                     ]
    red_numbers = [1, 2, 13, 19, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )