

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
              'all-time': [2905, 2969, 5950],
              'six-months': [198, 195, 400],
              'recent-trends': [62, 66, 130]
            }

    sets = {
            'all-time' : [751, 827, 883, 898, 822, 846, 923, 5950],
            'six-months' : [53, 55, 60, 58, 59, 61, 54, 400],
            'recent-trends' : [16, 19, 21, 15, 22, 20, 17, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 5], 'pairs': [615, 43, 15], 
                     'two_pairs': [224, 12, 2], 'three_of_set': [130, 11, 2], 
                     'full_house': [18, 3, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 1], 10: [79, 10, 2], 20: [107, 8, 3], 30: [100, 5, 3], 
                  40: [70, 6, 4], 50: [86, 5, 1], 60: [98, 5, 1]
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
              'all-time': [592, 598, 1190],
              'six-months': [41, 39, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [424, 433, 333, 1190],
            'six-months' : [33, 25, 23, 80],
            'recent-trends' : [13, 7, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       7, 5, 6, 7, 4, 11, 5, 4, 4, 2, 
                       6, 10, 4, 3, 6, 7, 8, 7, 2, 7, 
                       8, 4, 11, 5, 4, 5, 4, 7, 5, 7, 
                       5, 6, 7, 5, 7, 5, 6, 5, 5, 8, 
                       4, 2, 7, 9, 7, 5, 6, 3, 8, 6, 
                       5, 8, 7, 7, 6, 5, 7, 5, 5, 8, 
                       5, 7, 6, 5, 4, 8, 5, 1, 5
                    ]

    white_numbers_trends = [
                        2, 1, 2, 3, 2, 2, 3, 1, 0, 1, 
                        4, 3, 1, 2, 2, 2, 2, 2, 0, 4, 
                        3, 1, 5, 1, 2, 1, 0, 2, 2, 3, 
                        0, 0, 2, 1, 2, 2, 2, 1, 2, 3, 
                        2, 1, 2, 3, 3, 3, 2, 1, 2, 1, 
                        3, 2, 3, 1, 2, 1, 2, 1, 4, 2, 
                        1, 2, 2, 2, 1, 3, 1, 0, 3
                    ]

    red_numbers_6 = [
                     7, 3, 2, 3, 3, 3, 2, 2, 7, 1, 
                     0, 5, 3, 4, 2, 2, 2, 3, 3, 8, 
                     1, 1, 1, 5, 5, 2
                    ]

    red_numbers_trends = [
                          4, 3, 0, 1, 1, 2, 0, 0, 2, 1, 
                          0, 2, 0, 0, 1, 0, 0, 0, 3, 2, 
                          0, 0, 0, 2, 2, 0
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
                     6.67, 7.55, 7.80, 6.49, 6.44, 7.71, 6.71, 6.20, 6.54, 7.45, 
                     6.76, 8.18, 5.08, 6.17, 7.12, 7.27, 7.21, 6.93, 7.58, 7.76, 
                     8.86, 7.07, 8.52, 6.68, 6.40, 6.10, 8.17, 7.59, 6.47, 7.44, 
                     7.27, 8.96, 8.56, 6.24, 6.02, 8.78, 7.99, 7.01, 8.19, 7.12, 
                     6.66, 6.39, 6.98, 7.66, 7.92, 5.76, 7.95, 6.05, 6.10, 7.43, 
                     6.56, 7.14, 8.09, 7.59, 6.82, 7.26, 6.20, 6.12, 7.82, 6.71, 
                     9.17, 7.94, 9.05, 8.67, 6.41, 6.94, 7.81, 7.06, 8.68
                     ]
    red_numbers = [
                   3.72, 3.52, 3.99, 5.00, 4.11, 3.77, 3.73, 3.41, 4.39, 3.83, 
                   3.11, 3.45, 3.81, 4.20, 3.37, 3.06, 3.31, 4.45, 3.69, 4.08, 
                   4.64, 3.16, 3.11, 4.72, 4.17, 4.20
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
                     [15, 40, 48, 50, 51],
                     [10, 13, 16, 17, 64],
                     [3, 5, 33, 60, 67],
                     [31, 34, 43, 55, 61],
                     [9, 27, 29, 39, 52]
                     ]
    red_numbers = [12, 14, 15, 19, 20]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )