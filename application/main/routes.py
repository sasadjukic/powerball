

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
              'all-time': [2864, 2921, 5860],
              'six-months': [205, 189, 400],
              'recent-trends': [63, 66, 130]
            }

    sets = {
            'all-time' : [740, 815, 870, 889, 805, 834, 907, 5860],
            'six-months' : [54, 58, 61, 61, 58, 58, 50, 400],
            'recent-trends' : [15, 18, 23, 16, 21, 23, 14, 130]
    }

    winning_hands = {
                     'singles': [189, 11, 4], 'pairs': [605, 46, 14], 
                     'two_pairs': [224, 13, 6], 'three_of_set': [128, 9, 2], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 4, 2], 10: [78, 12, 3], 20: [105, 10, 3], 30: [99, 6, 2], 
                  40: [66, 5, 1], 50: [85, 4, 1], 60: [97, 5, 2]
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
              'all-time': [583, 589, 1172], 
              'six-months': [37, 43, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [416, 429, 327, 1172],
            'six-months' : [27, 28, 25, 80],
            'recent-trends' : [9, 11, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 8, 5, 5, 4, 11, 4, 5, 5, 2, 
                       7, 10, 6, 3, 6, 6, 7, 8, 3, 5, 
                       9, 4, 8, 5, 6, 5, 6, 7, 6, 7, 
                       6, 8, 7, 4, 6, 5, 6, 5, 7, 7, 
                       3, 1, 9, 7, 9, 5, 6, 4, 7, 6, 
                       4, 9, 6, 7, 5, 4, 8, 7, 2, 8, 
                       5, 6, 5, 6, 4, 6, 6, 1, 3
                    ]

    white_numbers_trends = [
                        0, 4, 1, 2, 1, 3, 2, 2, 0, 1, 
                        4, 3, 1, 0, 0, 2, 2, 4, 1, 2, 
                        3, 1, 6, 1, 1, 0, 1, 5, 3, 1, 
                        1, 2, 2, 1, 1, 4, 1, 2, 1, 3, 
                        0, 0, 1, 3, 2, 1, 5, 1, 5, 4, 
                        1, 2, 2, 3, 3, 2, 3, 1, 2, 5, 
                        1, 3, 2, 0, 2, 0, 0, 1, 0
                    ]

    red_numbers_6 = [
                     4, 1, 3, 2, 3, 4, 2, 2, 6, 1, 
                     1, 5, 3, 5, 4, 2, 3, 3, 1, 8, 
                     3, 4, 1, 3, 4, 2
                    ]

    red_numbers_trends = [
                          1, 0, 1, 0, 1, 2, 0, 1, 3, 0, 
                          0, 3, 1, 2, 2, 0, 1, 2, 0, 5, 
                          0, 0, 0, 0, 1, 0
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
                     7.15, 7.33, 7.95, 6.39, 6.27, 8.04, 6.83, 6.61, 6.90, 6.73, 
                     7.43, 8.08, 5.60, 6.12, 6.76, 7.04, 6.93, 6.92, 6.96, 7.56, 
                     9.32, 6.80, 8.92, 7.45, 6.95, 6.07, 8.51, 8.14, 6.69, 6.86, 
                     7.21, 8.33, 8.91, 6.06, 6.06, 8.93, 8.01, 7.73, 8.53, 6.83, 
                     6.26, 6.51, 6.68, 8.19, 7.59, 6.00, 8.05, 6.10, 5.66, 6.85, 
                     6.31, 7.11, 7.92, 7.04, 6.98, 7.19, 7.04, 6.41, 7.40, 6.74, 
                     8.62, 7.93, 8.75, 8.32, 6.71, 6.45, 7.29, 7.75, 8.24
                     ]
    red_numbers = [
                   3.85, 3.37, 3.81, 5.19, 4.02, 4.13, 3.39, 3.43, 4.43, 3.41, 
                   3.74, 3.08, 3.91, 4.71, 3.19, 3.07, 3.46, 4.50, 3.60, 4.29, 
                   4.70, 3.40, 3.25, 4.20, 3.87, 4.00
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
                     [11, 31, 48, 51, 52],
                     [6, 10, 17, 25, 62],
                     [7, 15, 30, 53, 64],
                     [26, 32, 35, 41, 49],
                     [4, 23, 59, 65, 67]
                     ]
    red_numbers = [3, 9, 15, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )