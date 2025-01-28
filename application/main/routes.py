

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
              'all-time': [2802, 2859, 5735], 
              'six-months': [211, 182, 400], 
              'recent-trends': [65, 61, 130]
            }

    sets = {
            'all-time' : [726, 797, 847, 873, 786, 813, 893, 5735],
            'six-months' : [59, 55, 57, 69, 56, 50, 54, 400],
            'recent-trends' : [21, 17, 15, 24, 16, 22, 15, 130]
    }

    winning_hands = {
                     'singles': [185, 12, 1], 'pairs': [591, 42, 13], 
                     'two_pairs': [219, 14, 7], 'three_of_set': [126, 11, 5], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [75, 10, 5], 20: [102, 8, 1], 30: [97, 8, 2], 
                  40: [65, 4, 1], 50: [84, 3, 2], 60: [95, 6, 1]}
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
              'all-time': [570, 577, 1147], 
              'six-months': [34, 46, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [407, 418, 322, 1147],
            'six-months' : [25, 29, 26, 80],
            'recent-trends' : [10, 7, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 7, 5, 5, 5, 9, 3, 6, 9, 3, 
                       6, 9, 6, 4, 8, 5, 6, 4, 4, 3, 
                       10, 5, 6, 6, 5, 5, 8, 3, 6, 7, 
                       9, 6, 11, 7, 7, 1, 9, 6, 6, 7, 
                       3, 3, 10, 6, 9, 6, 5, 5, 2, 4, 
                       4, 7, 6, 5, 5, 3, 8, 7, 1, 5, 
                       5, 4, 4, 9, 3, 6, 9, 3, 6
                    ]

    white_numbers_trends = [4, 1, 2, 2, 1, 6, 0, 2, 3, 0, 
                            0, 3, 1, 1, 4, 2, 4, 1, 1, 1, 
                            1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 
                            3, 3, 3, 1, 4, 1, 2, 2, 3, 3, 
                            1, 1, 3, 2, 1, 1, 2, 0, 2, 1, 
                            2, 3, 3, 4, 3, 1, 3, 2, 0, 0, 
                            3, 0, 1, 2, 1, 4, 3, 0, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 3, 2, 4, 1, 5, 2, 
                     1, 3, 3, 5, 3, 4, 5, 1, 2, 8, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [3, 0, 1, 1, 1, 1, 2, 0, 1, 0, 
                          0, 1, 2, 2, 0, 0, 1, 1, 0, 2, 
                          0, 1, 1, 3, 1, 1
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
                     7.08, 7.23, 7.54, 6.32, 6.37, 7.47, 6.66, 6.39, 7.11, 7.05, 
                     6.86, 7.74, 5.40, 6.32, 7.08, 7.38, 7.65, 6.87, 7.49, 7.13, 
                     8.03, 7.41, 8.28, 7.02, 6.47, 5.82, 8.55, 7.75, 6.49, 7.32, 
                     7.73, 8.37, 8.63, 6.44, 6.83, 8.04, 8.36, 7.17, 8.12, 6.85, 
                     6.89, 6.79, 6.84, 7.42, 7.70, 5.96, 8.25, 6.28, 4.93, 7.05, 
                     6.01, 7.09, 8.24, 7.68, 6.88, 7.11, 7.11, 6.81, 7.49, 6.02, 
                     9.48, 7.66, 8.65, 8.87, 6.06, 7.48, 7.74, 7.61, 9.08
                     ]
    red_numbers = [
                   3.51, 3.34, 4.01, 5.14, 4.61, 3.60, 3.56, 3.27, 4.29, 3.13, 
                   3.55, 3.08, 4.19, 4.28, 3.22, 3.36, 3.61, 4.64, 3.73, 4.31, 
                   4.73, 3.27, 3.35, 4.54, 3.70, 3.98
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
                     [13, 24, 33, 59, 68], 
                     [7, 9, 25, 47, 58], 
                     [1, 10, 18, 45, 61], 
                     [20, 34, 39, 50, 63], 
                     [11, 29, 42, 53, 69]
                     ]
    red_numbers = [1, 10, 11, 15, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )