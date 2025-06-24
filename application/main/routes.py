

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
              'all-time': [2957, 3015, 6050],
              'six-months': [197, 196, 400],
              'recent-trends': [68, 59, 130]
            }

    sets = {
            'all-time' : [764, 839, 902, 913, 838, 860, 934, 6050],
            'six-months' : [52, 54, 63, 57, 63, 61, 50, 400],
            'recent-trends' : [17, 19, 22, 18, 20, 19, 15, 130]
    }

    winning_hands = {
                     'singles': [196, 12, 3], 'pairs': [625, 42, 14], 
                     'two_pairs': [229, 15, 5], 'three_of_set': [132, 9, 3], 
                     'full_house': [18, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 3], 20: [110, 8, 4], 30: [101, 5, 1], 
                  40: [72, 8, 3], 50: [86, 3, 1], 60: [99, 5, 1]
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
              'all-time': [601, 609, 1210],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [428, 440, 342, 1210],
            'six-months' : [29, 26, 25, 80],
            'recent-trends' : [6, 8, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 5, 8, 6, 9, 6, 4, 3, 3, 
                       5, 8, 4, 4, 6, 8, 8, 6, 2, 7, 
                       7, 3, 14, 3, 4, 3, 5, 8, 9, 6, 
                       5, 7, 5, 5, 7, 6, 7, 4, 5, 8, 
                       4, 5, 8, 9, 6, 4, 7, 5, 7, 6, 
                       4, 10, 8, 6, 5, 5, 6, 4, 7, 8, 
                       3, 7, 4, 6, 5, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        4, 1, 2, 2, 3, 1, 2, 0, 2, 2, 
                        0, 2, 3, 3, 2, 3, 2, 2, 0, 1, 
                        2, 0, 6, 1, 2, 1, 2, 2, 5, 2, 
                        2, 2, 1, 3, 3, 1, 3, 0, 1, 4, 
                        1, 3, 4, 2, 2, 0, 1, 3, 0, 2, 
                        1, 5, 2, 0, 0, 2, 2, 1, 4, 3, 
                        1, 2, 0, 2, 2, 1, 2, 1, 1
                    ]

    red_numbers_6 = [
                     6, 4, 3, 3, 3, 3, 1, 1, 5, 1, 
                     3, 4, 3, 4, 3, 0, 1, 3, 4, 8, 
                     2, 0, 1, 6, 7, 1
                    ]

    red_numbers_trends = [
                          0, 2, 1, 1, 1, 0, 0, 0, 1, 0, 
                          3, 0, 2, 0, 1, 0, 0, 0, 2, 2, 
                          2, 0, 0, 4, 4, 0
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
                     7.02, 7.95, 7.78, 7.01, 6.37, 7.11, 7.07, 6.83, 6.67, 7.19, 
                     7.48, 7.69, 5.33, 6.57, 7.11, 7.19, 7.12, 7.25, 7.45, 6.76, 
                     9.06, 7.05, 8.86, 7.91, 6.48, 5.72, 8.28, 7.96, 6.93, 6.73, 
                     6.82, 8.21, 8.08, 6.00, 6.72, 8.47, 7.93, 6.66, 8.24, 7.23, 
                     6.55, 6.65, 6.97, 7.63, 7.86, 6.11, 7.73, 6.61, 5.43, 6.83, 
                     6.41, 7.67, 7.87, 7.06, 7.18, 6.68, 6.98, 6.46, 7.80, 6.57, 
                     8.98, 8.02, 8.71, 8.35, 6.26, 7.26, 7.24, 7.11, 8.73
                     ]
    red_numbers = [
                   3.60, 3.58, 3.69, 4.82, 4.18, 3.63, 3.78, 3.41, 4.23, 3.42, 
                   3.92, 3.22, 3.64, 4.46, 3.03, 2.98, 3.26, 4.91, 3.55, 4.47, 
                   4.74, 3.16, 3.58, 4.64, 4.21, 3.89
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
                     [2, 4, 35, 59, 63],
                     [5, 7, 22, 50, 57],
                     [30, 46, 47, 51, 66],
                     [9, 11, 15, 63, 68],
                     [13, 17, 21, 49, 55]
                     ]
    red_numbers = [1, 4, 5, 13, 15]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )