

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
              'all-time': [2818, 2873, 5765], 
              'six-months': [214, 180, 400], 
              'recent-trends': [68, 59, 130]
            }

    sets = {
            'all-time' : [728, 802, 852, 879, 790, 816, 898, 5765],
            'six-months' : [59, 57, 59, 67, 54, 48, 56, 400],
            'recent-trends' : [18, 21, 14, 26, 16, 19, 16, 130]
    }

    winning_hands = {
                     'singles': [187, 13, 3], 'pairs': [594, 42, 14], 
                     'two_pairs': [219, 12, 5], 'three_of_set': [127, 12, 4], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [76, 11, 6], 20: [103, 9, 1], 30: [97, 6, 2], 
                  40: [65, 4, 1], 50: [84, 3, 1], 60: [96, 6, 2]}
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
              'all-time': [573, 580, 1153], 
              'six-months': [34, 46, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [410, 421, 322, 1153],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [13, 8, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 8, 4, 5, 5, 8, 3, 7, 9, 3, 
                       5, 11, 5, 4, 8, 5, 7, 5, 4, 3, 
                       10, 5, 7, 6, 5, 5, 8, 3, 7, 7, 
                       9, 7, 10, 6, 6, 1, 8, 7, 6, 5, 
                       3, 2, 11, 5, 9, 6, 5, 5, 3, 4, 
                       3, 7, 6, 5, 5, 3, 8, 6, 1, 6, 
                       5, 6, 4, 8, 3, 6, 9, 3, 6
                    ]

    white_numbers_trends = [2, 2, 1, 1, 1, 6, 0, 3, 2, 0, 
                            0, 5, 0, 1, 4, 2, 5, 2, 2, 1, 
                            1, 1, 3, 0, 0, 2, 3, 1, 2, 3, 
                            3, 4, 4, 1, 3, 1, 2, 3, 2, 2, 
                            1, 1, 3, 2, 0, 1, 3, 0, 3, 1, 
                            1, 2, 3, 4, 2, 1, 3, 2, 0, 2, 
                            2, 2, 0, 2, 1, 4, 2, 0, 1
                    ]

    red_numbers_6 = [3, 1, 5, 2, 3, 2, 3, 2, 5, 2, 
                     1, 2, 3, 6, 3, 3, 5, 2, 2, 7, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [3, 0, 2, 1, 1, 1, 2, 1, 2, 0, 
                          0, 1, 0, 3, 0, 0, 2, 2, 0, 1, 
                          0, 0, 1, 2, 0, 1
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
                     7.38, 7.33, 7.18, 6.49, 7.02, 7.56, 6.38, 6.63, 6.95, 6.68, 
                     7.23, 8.01, 4.95, 6.80, 7.36, 7.42, 7.01, 6.74, 7.55, 7.25, 
                     8.69, 6.98, 8.32, 7.12, 6.65, 6.35, 8.73, 7.68, 6.06, 7.12, 
                     7.06, 9.25, 9.05, 5.91, 6.87, 8.40, 7.77, 7.28, 8.43, 6.94, 
                     6.90, 6.63, 7.01, 7.60, 7.11, 6.11, 7.59, 6.06, 5.64, 7.29, 
                     6.12, 7.10, 7.84, 7.46, 6.59, 6.68, 6.87, 6.69, 7.48, 6.50, 
                     8.91, 7.93, 8.77, 8.51, 6.28, 7.92, 7.73, 7.02, 9.09
                     ]
    red_numbers = [
                   3.75, 3.31, 4.01, 5.05, 4.22, 3.72, 3.58, 3.58, 4.74, 3.64, 
                   3.28, 3.12, 3.43, 4.62, 3.11, 3.44, 3.21, 4.45, 3.53, 4.12, 
                   4.49, 3.25, 3.61, 4.84, 3.92, 3.99
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
                     [15, 22, 24, 35, 45], 
                     [5, 29, 42, 67, 69], 
                     [11, 29, 30, 36, 50], 
                     [10, 11, 45, 64, 68], 
                     [4, 15, 23, 41, 55]
                     ]
    red_numbers = [5, 11, 14, 15, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )