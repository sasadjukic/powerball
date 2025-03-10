

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
              'all-time': [2843, 2903, 5820],
              'six-months': [208, 187, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [735, 808, 862, 883, 800, 826, 906, 5820],
            'six-months' : [54, 60, 59, 62, 56, 55, 54, 400],
            'recent-trends' : [19, 17, 17, 18, 21, 20, 18, 130]
    }

    winning_hands = {
                     'singles': [188, 13, 3], 'pairs': [600, 45, 13], 
                     'two_pairs': [222, 12, 7], 'three_of_set': [128, 9, 3], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [74, 4, 2], 10: [77, 12, 4], 20: [104, 9, 2], 30: [97, 6, 1], 
                  40: [66, 5, 1], 50: [85, 4, 1], 60: [97, 5, 2]}
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
              'all-time': [576, 588, 1164], 
              'six-months': [33, 47, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [411, 426, 327, 1164],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [9, 9, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       9, 8, 5, 5, 3, 9, 4, 5, 6, 4, 
                       6, 10, 5, 4, 6, 7, 7, 7, 4, 4, 
                       11, 5, 6, 5, 5, 5, 7, 5, 6, 7, 
                       7, 8, 7, 6, 5, 3, 8, 5, 6, 6, 
                       3, 1, 9, 7, 10, 4, 5, 5, 6, 5, 
                       3, 9, 5, 6, 6, 5, 8, 6, 2, 8, 
                       5, 6, 6, 6, 5, 6, 7, 2, 3
                    ]

    white_numbers_trends = [
                            1, 4, 2, 3, 1, 4, 1, 3, 0, 1, 
                            1, 2, 0, 1, 2, 4, 2, 3, 1, 2, 
                            2, 1, 4, 1, 0, 0, 2, 3, 2, 1, 
                            2, 4, 1, 1, 1, 3, 2, 2, 1, 3, 
                            1, 0, 2, 3, 2, 0, 4, 1, 5, 3, 
                            0, 3, 3, 3, 2, 2, 2, 1, 1, 4, 
                            1, 3, 2, 1, 3, 2, 0, 1, 1
                    ]

    red_numbers_6 = [
                     3, 1, 4, 2, 3, 2, 3, 2, 5, 1, 
                     1, 3, 3, 6, 3, 3, 4, 3, 1, 10, 
                     3, 4, 1, 3, 4, 2
                    ]

    red_numbers_trends = [
                          0, 0, 1, 1, 1, 1, 1, 1, 3, 0, 
                          0, 1, 1, 3, 1, 0, 1, 2, 0, 5, 
                          0, 0, 1, 1, 1, 0
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
                     7.16, 7.02, 7.74, 6.74, 6.51, 7.28, 6.27, 6.75, 7.07, 6.91, 
                     6.98, 8.07, 5.02, 6.81, 6.52, 7.57, 7.03, 7.13, 7.82, 7.39, 
                     9.14, 5.88, 8.41, 7.06, 6.27, 6.12, 8.30, 7.99, 5.96, 7.21, 
                     7.34, 8.43, 8.42, 6.10, 6.29, 8.52, 7.95, 7.30, 7.96, 7.21, 
                     6.77, 6.36, 6.73, 7.85, 7.80, 6.42, 8.31, 6.31, 6.21, 7.46, 
                     6.61, 7.01, 7.46, 7.11, 7.02, 7.34, 7.43, 6.75, 7.65, 6.99, 
                     8.96, 8.06, 8.41, 8.10, 6.32, 6.82, 7.66, 7.91, 8.52
                     ]
    red_numbers = [
                   3.67, 3.41, 3.85, 4.47, 4.30, 3.55, 3.47, 3.45, 4.34, 3.80, 
                   3.60, 3.20, 3.75, 4.55, 3.06, 3.05, 3.22, 4.61, 3.49, 4.71, 
                   4.67, 3.53, 3.44, 4.71, 4.11, 3.99
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
                     [2, 9, 13, 34, 42],
                     [17, 45, 57, 59, 64],
                     [22, 26, 27, 39, 68],
                     [8, 33, 36, 51, 54],
                     [19, 24, 45, 49, 60]
                     ]
    red_numbers = [4, 9, 12, 15, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )