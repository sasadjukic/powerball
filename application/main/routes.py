

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
              'all-time': [2859, 2917, 5850],
              'six-months': [206, 189, 400],
              'recent-trends': [64, 66, 130]
            }

    sets = {
            'all-time' : [738, 815, 867, 886, 804, 833, 907, 5850],
            'six-months' : [53, 61, 60, 59, 59, 57, 51, 400],
            'recent-trends' : [16, 20, 21, 13, 22, 23, 15, 130]
    }

    winning_hands = {
                     'singles': [189, 12, 4], 'pairs': [603, 45, 13], 
                     'two_pairs': [224, 13, 7], 'three_of_set': [128, 9, 2], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 4, 2], 10: [78, 13, 4], 20: [104, 9, 2], 30: [98, 5, 1], 
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
              'all-time': [581, 589, 1170], 
              'six-months': [36, 44, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [415, 428, 327, 1170],
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
                       8, 8, 5, 5, 3, 10, 4, 5, 5, 2, 
                       8, 10, 6, 3, 6, 6, 8, 8, 4, 4, 
                       10, 5, 7, 5, 6, 5, 6, 7, 5, 7, 
                       6, 8, 7, 4, 5, 4, 7, 5, 6, 7, 
                       3, 1, 9, 7, 10, 5, 6, 4, 7, 6, 
                       4, 9, 5, 7, 5, 4, 8, 7, 2, 8, 
                       5, 6, 5, 6, 4, 6, 6, 2, 3
                    ]

    white_numbers_trends = [
                            0, 4, 1, 2, 1, 3, 2, 3, 0, 1, 
                            4, 3, 1, 0, 1, 2, 3, 4, 1, 1, 
                            3, 1, 5, 1, 1, 0, 2, 5, 2, 1, 
                            1, 2, 2, 1, 0, 3, 1, 2, 0, 4, 
                            0, 0, 1, 3, 2, 1, 4, 1, 6, 4, 
                            1, 2, 2, 3, 3, 2, 3, 1, 2, 5, 
                            1, 3, 2, 0, 2, 1, 0, 1, 0
                    ]

    red_numbers_6 = [
                     4, 1, 3, 2, 3, 3, 3, 2, 6, 1, 
                     1, 4, 3, 6, 4, 2, 3, 3, 1, 8, 
                     3, 4, 1, 3, 4, 2
                    ]

    red_numbers_trends = [
                          1, 0, 1, 0, 2, 1, 0, 1, 3, 0, 
                          0, 2, 1, 3, 2, 0, 1, 2, 0, 5, 
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
                     7.37, 7.51, 7.64, 6.67, 6.15, 8.20, 6.58, 6.87, 6.99, 6.58, 
                     7.18, 7.88, 5.33, 6.63, 6.86, 7.14, 7.03, 6.96, 7.73, 6.77, 
                     9.23, 6.92, 8.41, 7.51, 6.51, 5.80, 8.21, 7.59, 6.12, 7.48, 
                     7.14, 8.91, 8.82, 5.90, 6.03, 9.31, 7.77, 7.16, 8.31, 6.76, 
                     6.34, 6.62, 6.97, 7.84, 7.57, 5.55, 7.83, 6.15, 6.32, 7.08, 
                     6.49, 6.98, 7.65, 6.81, 6.85, 6.92, 6.81, 6.95, 7.79, 6.78, 
                     9.15, 8.60, 7.86, 8.45, 6.72, 6.89, 7.43, 8.21, 8.43
                     ]
    red_numbers = [
                   3.88, 3.16, 3.65, 5.04, 4.36, 3.87, 3.53, 3.52, 4.01, 3.87, 
                   3.28, 3.45, 3.73, 4.99, 3.01, 3.13, 3.53, 4.35, 3.77, 3.98, 
                   4.78, 3.68, 3.36, 4.35, 3.56, 4.16
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
                     [8, 24, 46, 58, 69],
                     [11, 34, 36, 39, 65],
                     [7, 12, 30, 49, 62],
                     [4, 19, 27, 44, 64],
                     [14, 40, 52, 53, 54]
                     ]
    red_numbers = [3, 6, 10, 21, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )