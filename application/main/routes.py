

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
              'all-time': [2897, 2963, 5935],
              'six-months': [197, 197, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [751, 823, 881, 895, 819, 845, 921, 5935],
            'six-months' : [53, 53, 62, 56, 60, 62, 54, 400],
            'recent-trends' : [18, 17, 23, 12, 20, 22, 18, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 5], 'pairs': [612, 43, 13], 
                     'two_pairs': [224, 12, 3], 'three_of_set': [130, 11, 3], 
                     'full_house': [18, 3, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 10, 1], 20: [106, 8, 2], 30: [100, 5, 3], 
                  40: [69, 6, 3], 50: [86, 5, 1], 60: [98, 5, 1]
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
              'all-time': [592, 595, 1187],
              'six-months': [42, 38, 80], 
              'recent-trends': [17, 9, 26]
            }

    sets = {
            'all-time' : [424, 432, 331, 1187],
            'six-months' : [33, 25, 22, 80],
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
                       6, 10, 5, 2, 5, 6, 8, 7, 2, 7, 
                       8, 5, 10, 5, 4, 5, 5, 7, 6, 6, 
                       5, 7, 7, 4, 6, 5, 6, 5, 5, 6, 
                       4, 2, 8, 9, 7, 5, 6, 5, 8, 6, 
                       5, 8, 7, 7, 6, 5, 7, 7, 4, 8, 
                       6, 7, 6, 5, 3, 7, 6, 1, 5
                    ]

    white_numbers_trends = [
                        2, 2, 2, 4, 2, 2, 3, 1, 0, 0, 
                        4, 3, 1, 1, 1, 2, 2, 3, 0, 5, 
                        2, 1, 5, 2, 2, 1, 0, 3, 2, 2, 
                        0, 0, 2, 0, 1, 2, 2, 1, 2, 2, 
                        2, 1, 2, 3, 2, 3, 2, 1, 2, 2, 
                        3, 3, 3, 1, 2, 2, 2, 1, 3, 2, 
                        1, 2, 4, 2, 1, 2, 1, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 3, 3, 2, 2, 7, 1, 
                     0, 5, 3, 4, 2, 2, 3, 3, 2, 7, 
                     1, 2, 1, 4, 5, 2
                    ]

    red_numbers_trends = [
                          4, 3, 0, 1, 1, 2, 0, 0, 2, 1, 
                          0, 2, 1, 0, 1, 0, 0, 0, 2, 3, 
                          0, 0, 0, 1, 2, 0
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
                     7.07, 7.12, 7.44, 6.83, 6.45, 7.23, 6.87, 6.85, 7.15, 7.18,
                     7.37, 7.80, 5.38, 6.19, 7.11, 7.86, 7.58, 6.75, 7.41, 7.28, 
                     8.87, 6.76, 8.63, 7.04, 6.41, 6.00, 9.28, 7.71, 6.15, 7.49, 
                     7.01, 7.85, 8.90, 6.09, 6.12, 8.62, 7.50, 7.52, 8.52, 7.17, 
                     6.24, 6.44, 6.77, 7.96, 7.39, 6.26, 8.35, 6.30, 6.10, 6.96, 
                     6.41, 7.40, 8.14, 7.21, 6.71, 7.37, 6.85, 6.75, 7.36, 6.56, 
                     8.41, 7.54, 8.60, 8.51, 6.65, 7.25, 7.13, 7.10, 8.72
                     ]
    red_numbers = [
                   4.43, 3.43, 3.71, 4.54, 4.42, 3.75, 3.54, 3.42, 4.49, 3.59, 
                   3.34, 3.51, 3.84, 5.02, 2.92, 3.18, 3.67, 4.60, 3.74, 3.82, 
                   4.22, 3.24, 3.22, 4.35, 4.04, 3.97
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
                     [7, 29, 36, 44, 58],
                     [34, 37, 41, 42, 59],
                     [22, 47, 66, 67, 68],
                     [16, 23, 39, 49, 63],
                     [2, 4, 12, 15, 28]
                     ]
    red_numbers = [11, 14, 15, 16, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )