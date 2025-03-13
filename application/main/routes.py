

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
              'all-time': [2847, 2909, 5830],
              'six-months': [206, 189, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [735, 811, 863, 883, 802, 830, 906, 5830],
            'six-months' : [53, 61, 59, 59, 58, 57, 53, 400],
            'recent-trends' : [16, 20, 17, 14, 22, 24, 17, 130]
    }

    winning_hands = {
                     'singles': [188, 12, 3], 'pairs': [600, 44, 12], 
                     'two_pairs': [224, 14, 8], 'three_of_set': [128, 9, 3], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [74, 4, 2], 10: [77, 12, 4], 20: [104, 9, 2], 30: [97, 5, 0], 
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
              'all-time': [578, 588, 1166], 
              'six-months': [35, 45, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [413, 426, 327, 1166],
            'six-months' : [27, 28, 25, 80],
            'recent-trends' : [10, 9, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       9, 8, 5, 5, 3, 9, 3, 5, 6, 3, 
                       7, 10, 6, 3, 6, 7, 8, 7, 4, 4, 
                       10, 5, 6, 5, 5, 5, 7, 6, 6, 7, 
                       7, 8, 6, 5, 5, 3, 7, 5, 6, 7, 
                       3, 1, 9, 7, 10, 4, 6, 5, 6, 6, 
                       4, 9, 5, 6, 6, 5, 8, 7, 1, 8, 
                       5, 6, 5, 6, 5, 6, 7, 2, 3
                    ]

    white_numbers_trends = [
                            0, 4, 1, 3, 1, 3, 1, 3, 0, 1, 
                            2, 2, 1, 1, 2, 4, 3, 3, 1, 1, 
                            2, 1, 4, 1, 0, 0, 2, 4, 2, 1, 
                            2, 3, 1, 1, 1, 2, 1, 1, 1, 4, 
                            1, 0, 1, 3, 2, 0, 5, 1, 5, 4, 
                            1, 3, 3, 3, 3, 2, 2, 2, 1, 4, 
                            1, 3, 2, 1, 2, 2, 0, 1, 1
                    ]

    red_numbers_6 = [
                     4, 1, 4, 2, 3, 3, 3, 2, 5, 1, 
                     1, 3, 3, 6, 3, 3, 4, 3, 1, 8, 
                     3, 4, 1, 3, 4, 2
                    ]

    red_numbers_trends = [
                          1, 0, 1, 0, 1, 2, 1, 1, 3, 0, 
                          0, 1, 1, 3, 1, 0, 1, 2, 0, 5, 
                          0, 0, 1, 0, 1, 0
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
                     6.77, 7.73, 7.33, 7.15, 6.35, 7.31, 6.37, 6.44, 6.55, 6.94, 
                     6.90, 7.82, 5.01, 6.44, 7.21, 7.30, 7.29, 6.98, 7.80, 7.35, 
                     9.33, 7.24, 8.30, 7.43, 6.34, 5.87, 8.63, 7.81, 6.18, 6.55, 
                     7.14, 8.39, 8.72, 6.08, 6.18, 8.74, 8.38, 7.40, 8.56, 6.87, 
                     6.47, 6.63, 6.94, 7.74, 7.57, 6.17, 8.14, 5.40, 6.18, 7.49, 
                     6.49, 7.24, 7.34, 7.23, 6.73, 7.16, 7.17, 6.69, 7.62, 6.97, 
                     9.11, 7.82, 8.28, 8.09, 6.58, 7.48, 7.59, 7.49, 9.01
                     ]
    red_numbers = [
                   4.06, 3.79, 3.97, 4.67, 4.04, 3.77, 3.40, 3.55, 4.83, 3.27, 
                   3.27, 3.02, 4.01, 4.25, 3.12, 3.12, 3.13, 4.58, 3.38, 4.28, 
                   4.92, 3.39, 3.25, 4.93, 4.21, 3.79
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
                     [6, 14, 27, 45, 57],
                     [22, 24, 32, 39, 40],
                     [14, 17, 44, 64, 69],
                     [3, 12, 33, 54, 55],
                     [1, 4, 30, 36, 61]
                     ]
    red_numbers = [4, 11, 14, 18, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )