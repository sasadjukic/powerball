

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
              'all-time': [2870, 2930, 5875],
              'six-months': [202, 192, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [742, 818, 871, 889, 808, 836, 911, 5875],
            'six-months' : [54, 58, 58, 59, 58, 59, 54, 400],
            'recent-trends' : [15, 20, 22, 12, 21, 23, 17, 130]
    }

    winning_hands = {
                     'singles': [190, 12, 5], 'pairs': [607, 45, 15], 
                     'two_pairs': [224, 13, 5], 'three_of_set': [128, 9, 1], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 4, 2], 10: [78, 11, 3], 20: [105, 9, 2], 30: [99, 6, 2], 
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
              'all-time': [585, 590, 1175], 
              'six-months': [39, 41, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [418, 429, 328, 1175],
            'six-months' : [29, 27, 24, 80],
            'recent-trends' : [10, 10, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 7, 4, 5, 5, 11, 5, 5, 5, 2, 
                       7, 11, 5, 3, 5, 6, 8, 8, 3, 5, 
                       9, 4, 8, 4, 5, 4, 6, 7, 6, 7, 
                       6, 8, 7, 4, 6, 5, 5, 5, 6, 7, 
                       5, 1, 9, 8, 7, 4, 6, 4, 7, 6, 
                       4, 9, 7, 7, 5, 4, 8, 7, 2, 8, 
                       6, 6, 5, 8, 4, 6, 6, 1, 4
                    ]

    white_numbers_trends = [
                        0, 3, 1, 2, 2, 3, 3, 1, 0, 1, 
                        5, 3, 1, 0, 0, 2, 3, 4, 1, 2, 
                        4, 1, 5, 1, 1, 0, 1, 5, 2, 1, 
                        0, 1, 1, 1, 1, 4, 1, 1, 1, 2, 
                        2, 0, 1, 4, 2, 1, 4, 1, 4, 4, 
                        1, 3, 2, 3, 2, 2, 3, 1, 2, 5, 
                        1, 3, 2, 2, 2, 0, 0, 1, 1
                    ]

    red_numbers_6 = [
                     5, 2, 3, 2, 3, 4, 2, 2, 6, 1, 
                     1, 5, 3, 5, 4, 2, 3, 3, 0, 8, 
                     2, 3, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          2, 1, 1, 0, 1, 2, 0, 0, 3, 0, 
                          0, 3, 1, 2, 2, 0, 1, 1, 0, 4, 
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
                     6.78, 7.13, 7.78, 6.58, 6.04, 7.96, 7.17, 6.45, 6.97, 6.49, 
                     7.23, 8.10, 5.45, 6.65, 7.25, 7.32, 7.59, 7.09, 7.67, 7.62, 
                     9.01, 6.94, 7.90, 7.07, 5.93, 6.18, 8.35, 7.80, 5.89, 7.31, 
                     6.92, 9.01, 8.42, 6.10, 6.42, 8.75, 8.53, 7.06, 8.02, 7.32, 
                     6.82, 6.24, 6.78, 7.75, 7.50, 6.07, 8.02, 6.20, 5.49, 6.79, 
                     6.49, 7.02, 8.33, 7.37, 7.01, 7.26, 7.12, 6.96, 7.82, 6.75, 
                     8.74, 7.87, 8.64, 7.99, 6.09, 6.96, 7.53, 7.23, 8.91
                     ]
    red_numbers = [
                   3.95, 3.09, 4.22, 4.84, 4.13, 3.66, 3.36, 3.64, 4.54, 3.49, 
                   3.57, 3.22, 3.42, 4.57, 3.31, 3.26, 3.24, 4.36, 3.32, 4.32, 
                   5.17, 3.59, 3.13, 4.42, 4.11, 4.07
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
                     [5, 6, 52, 58, 64],
                     [16, 25, 34, 38, 62],
                     [3, 18, 21, 29, 68],
                     [17, 19, 32, 35, 57],
                     [41, 43, 48, 53, 59]
                     ]
    red_numbers = [3, 4, 14, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )