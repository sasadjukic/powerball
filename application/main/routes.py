

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
              'all-time': [2889, 2956, 5920],
              'six-months': [197, 197, 400],
              'recent-trends': [60, 69, 130]
            }

    sets = {
            'all-time' : [747, 820, 880, 895, 818, 841, 919, 5920],
            'six-months' : [52, 52, 64, 57, 61, 60, 54, 400],
            'recent-trends' : [15, 16, 24, 14, 22, 20, 19, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 5], 'pairs': [611, 45, 15], 
                     'two_pairs': [224, 12, 3], 'three_of_set': [129, 10, 2], 
                     'full_house': [17, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 10, 2], 20: [106, 10, 2], 30: [100, 5, 3], 
                  40: [69, 7, 4], 50: [85, 4, 0], 60: [98, 5, 2]
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
              'all-time': [590, 594, 1184],
              'six-months': [40, 40, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [422, 432, 330, 1184],
            'six-months' : [31, 27, 22, 80],
            'recent-trends' : [11, 8, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 5, 7, 4, 11, 5, 5, 4, 2, 
                       6, 10, 5, 1, 6, 6, 8, 6, 2, 7, 
                       8, 5, 10, 5, 5, 4, 6, 7, 7, 6, 
                       5, 7, 7, 4, 6, 5, 6, 5, 6, 7, 
                       4, 2, 7, 9, 8, 5, 6, 5, 8, 6, 
                       5, 8, 7, 7, 6, 4, 7, 7, 3, 7, 
                       6, 8, 6, 6, 3, 7, 6, 1, 4
                    ]

    white_numbers_trends = [
                        0, 2, 1, 4, 2, 2, 3, 1, 0, 1, 
                        5, 2, 1, 0, 1, 2, 2, 2, 0, 5, 
                        2, 1, 6, 2, 2, 0, 0, 4, 2, 2, 
                        0, 0, 2, 1, 1, 3, 2, 1, 2, 2, 
                        2, 1, 1, 4, 2, 3, 2, 2, 3, 2, 
                        2, 3, 3, 1, 3, 1, 1, 1, 3, 2, 
                        1, 3, 4, 2, 1, 2, 1, 1, 2
                    ]

    red_numbers_6 = [
                     7, 3, 2, 3, 3, 3, 2, 2, 6, 1, 
                     0, 5, 3, 4, 4, 2, 3, 3, 2, 8, 
                     1, 2, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          4, 2, 0, 1, 1, 2, 0, 0, 1, 1, 
                          0, 2, 1, 1, 1, 0, 0, 0, 2, 4, 
                          0, 0, 0, 0, 3, 0
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
                     6.95, 7.63, 8.19, 6.85, 6.68, 7.84, 6.39, 6.44, 7.15, 6.84, 
                     7.59, 7.80, 5.57, 6.07, 7.19, 7.49, 7.24, 6.71, 7.58, 7.67, 
                     8.73, 7.23, 9.03, 7.10, 6.85, 5.57, 8.32, 8.03, 5.94, 7.46, 
                     6.75, 8.30, 8.75, 6.23, 5.78, 8.34, 8.01, 7.12, 8.09, 7.33, 
                     6.35, 6.91, 6.74, 7.75, 7.39, 6.08, 7.86, 5.91, 5.48, 6.81, 
                     6.60, 7.21, 7.67, 7.39, 6.90, 6.75, 6.91, 6.30, 7.47, 6.64, 
                     8.88, 8.64, 8.60, 8.46, 6.14, 7.11, 8.27, 7.08, 8.87
                     ]
    red_numbers = [
                   3.93, 3.81, 3.92, 5.08, 3.96, 4.11, 3.53, 3.53, 4.01, 3.67, 
                   3.33, 3.13, 3.87, 4.16, 3.04, 3.03, 3.38, 4.51, 3.87, 4.25, 
                   4.24, 3.36, 3.27, 4.72, 4.48, 3.81
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
                     [14, 21, 24, 37, 55],
                     [8, 17, 36, 39, 44],
                     [6, 11, 33, 50, 53],
                     [2, 28, 45, 61, 63],
                     [5, 15, 26, 27, 69]
                     ]
    red_numbers = [7, 11, 16, 18, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )