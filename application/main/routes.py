

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
              'all-time': [2925, 2984, 5985],
              'six-months': [198, 195, 400],
              'recent-trends': [64, 65, 130]
            }

    sets = {
            'all-time' : [755, 834, 889, 903, 829, 850, 925, 5985],
            'six-months' : [54, 58, 57, 57, 62, 59, 53, 400],
            'recent-trends' : [16, 19, 21, 15, 24, 17, 18, 130]
    }

    winning_hands = {
                     'singles': [193, 9, 4], 'pairs': [621, 45, 17], 
                     'two_pairs': [225, 13, 1], 'three_of_set': [130, 11, 2], 
                     'full_house': [18, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 0], 10: [81, 11, 3], 20: [109, 8, 5], 30: [101, 6, 2], 
                  40: [71, 7, 5], 50: [86, 4, 1], 60: [98, 5, 1]
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
              'all-time': [597, 600, 1197],
              'six-months': [43, 37, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [427, 436, 334, 1197],
            'six-months' : [32, 26, 22, 80],
            'recent-trends' : [12, 7, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 5, 5, 8, 5, 10, 6, 4, 4, 3, 
                       5, 10, 5, 4, 7, 8, 7, 7, 2, 7, 
                       6, 3, 11, 4, 3, 4, 3, 9, 7, 7, 
                       5, 5, 6, 6, 7, 5, 6, 4, 6, 9, 
                       4, 4, 7, 9, 7, 4, 6, 4, 8, 6, 
                       5, 8, 7, 7, 6, 4, 7, 4, 5, 10, 
                       5, 6, 6, 5, 4, 7, 5, 1, 4
                    ]

    white_numbers_trends = [
                        2, 1, 2, 4, 3, 0, 3, 0, 1, 2, 
                        1, 3, 1, 3, 3, 3, 1, 2, 0, 5, 
                        2, 1, 3, 2, 1, 1, 0, 2, 4, 3, 
                        1, 0, 1, 3, 1, 0, 3, 0, 3, 3, 
                        3, 3, 3, 3, 3, 2, 0, 3, 1, 1, 
                        2, 3, 4, 0, 1, 1, 1, 1, 3, 3, 
                        1, 2, 2, 2, 1, 3, 1, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 4, 3, 2, 2, 5, 1, 
                     1, 5, 4, 4, 3, 0, 2, 3, 3, 8, 
                     1, 1, 1, 5, 5, 1
                    ]

    red_numbers_trends = [
                          3, 4, 0, 2, 1, 1, 0, 0, 1, 1, 
                          1, 0, 1, 0, 1, 0, 0, 0, 3, 2, 
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
                     7.30, 7.39, 8.20, 6.58, 6.43, 7.79, 6.42, 6.81, 7.05, 6.48, 
                     6.85, 7.91, 5.27, 6.64, 6.84, 7.73, 6.66, 6.86, 7.09, 7.73, 
                     8.85, 6.92, 9.07, 7.46, 6.35, 6.04, 8.60, 7.94, 6.34, 7.33, 
                     6.99, 8.11, 7.98, 6.74, 6.14, 8.62, 7.74, 6.98, 8.25, 7.38, 
                     6.87, 7.08, 6.50, 7.98, 7.60, 6.31, 7.90, 6.00, 5.83, 7.10, 
                     6.57, 6.93, 7.55, 6.85, 6.95, 7.15, 6.88, 7.01, 7.58, 6.35, 
                     8.87, 7.58, 8.34, 8.03, 6.25, 7.98, 8.26, 7.00, 8.84
                     ]
    red_numbers = [
                   4.43, 3.51, 3.83, 4.69, 4.66, 3.67, 3.36, 3.63, 4.45, 3.25, 
                   3.28, 3.28, 3.77, 4.91, 3.15, 3.11, 3.31, 4.58, 3.62, 4.01, 
                   4.57, 3.33, 3.29, 4.12, 4.37, 3.82
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
                     [12, 27, 36, 51, 54],
                     [1, 23, 31, 62, 64],
                     [5, 32, 38, 41, 49],
                     [9, 21, 24, 67, 68],
                     [39, 50, 55, 61, 65]
                     ]
    red_numbers = [8, 10, 14, 15, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )