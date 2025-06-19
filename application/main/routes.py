

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
              'all-time': [2952, 3010, 6040],
              'six-months': [199, 194, 400],
              'recent-trends': [66, 61, 130]
            }

    sets = {
            'all-time' : [762, 838, 901, 912, 836, 859, 932, 6040],
            'six-months' : [52, 55, 62, 59, 62, 61, 49, 400],
            'recent-trends' : [16, 19, 21, 18, 21, 19, 16, 130]
    }

    winning_hands = {
                     'singles': [195, 11, 2], 'pairs': [624, 43, 14], 
                     'two_pairs': [229, 15, 5], 'three_of_set': [132, 9, 3], 
                     'full_house': [18, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 10, 3], 20: [110, 8, 4], 30: [101, 5, 1], 
                  40: [71, 7, 3], 50: [86, 3, 1], 60: [99, 5, 1]
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
              'all-time': [601, 607, 1208],
              'six-months': [41, 39, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [428, 440, 340, 1208],
            'six-months' : [30, 27, 23, 80],
            'recent-trends' : [6, 8, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 4, 8, 5, 10, 6, 4, 4, 3, 
                       5, 8, 4, 4, 7, 7, 8, 7, 2, 7, 
                       7, 3, 14, 3, 3, 3, 5, 8, 9, 7, 
                       5, 6, 7, 5, 7, 6, 7, 4, 5, 8, 
                       4, 4, 8, 8, 6, 4, 7, 5, 8, 6, 
                       4, 9, 8, 6, 5, 5, 7, 4, 7, 8, 
                       4, 6, 4, 6, 4, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        4, 1, 1, 3, 2, 1, 2, 0, 2, 2, 
                        0, 2, 3, 3, 3, 2, 2, 2, 0, 1, 
                        2, 0, 6, 1, 1, 1, 2, 2, 5, 2, 
                        2, 1, 2, 3, 3, 1, 3, 0, 1, 4, 
                        1, 2, 4, 2, 3, 1, 1, 3, 0, 2, 
                        2, 4, 2, 0, 0, 2, 2, 1, 4, 3, 
                        1, 1, 1, 2, 1, 2, 2, 1, 2
                    ]

    red_numbers_6 = [
                     6, 4, 3, 3, 3, 3, 2, 1, 5, 1, 
                     3, 4, 3, 4, 3, 0, 2, 3, 4, 7, 
                     2, 0, 1, 5, 7, 1
                    ]

    red_numbers_trends = [
                          0, 2, 1, 1, 1, 0, 0, 0, 1, 0, 
                          3, 0, 2, 0, 1, 0, 0, 0, 2, 2, 
                          2, 0, 0, 3, 5, 0
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
                     6.86, 7.28, 7.24, 6.87, 6.42, 7.84, 6.67, 6.55, 6.85, 7.29, 
                     7.17, 7.37, 5.27, 6.62, 6.81, 7.31, 7.52, 6.65, 7.26, 7.49, 
                     8.64, 6.85, 8.96, 7.12, 6.36, 6.02, 8.56, 7.84, 6.64, 7.31, 
                     6.93, 8.42, 8.22, 5.66, 6.51, 8.42, 8.47, 6.49, 8.65, 7.57, 
                     6.89, 6.94, 6.86, 7.71, 7.52, 6.28, 8.11, 6.29, 5.91, 6.73, 
                     6.52, 7.10, 7.95, 7.10, 6.61, 7.48, 6.93, 6.72, 7.81, 6.76, 
                     8.58, 8.14, 8.31, 8.76, 5.98, 6.93, 8.02, 7.25, 8.83
                     ]
    red_numbers = [
                   3.88, 3.63, 4.11, 4.72, 3.93, 3.83, 3.25, 3.46, 4.34, 3.21, 3.53, 
                   3.73, 4.12, 4.67, 2.78, 3.17, 3.29, 4.36, 3.92, 4.22, 4.42, 3.54, 
                   3.23, 4.37, 4.38, 3.91
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
                     [25, 35, 48, 50, 55],
                     [30, 40, 41, 54, 60],
                     [15, 19, 33, 51, 52],
                     [13, 18, 21, 31, 67],
                     [5, 9, 28, 62, 64]
                     ]
    red_numbers = [6, 14, 20, 23, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )