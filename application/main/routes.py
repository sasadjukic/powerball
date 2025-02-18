

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
              'all-time': [2823, 2883, 5780], 
              'six-months': [210, 184, 400], 
              'recent-trends': [63, 64, 130]
            }

    sets = {
            'all-time' : [730, 803, 853, 881, 795, 820, 898, 5780],
            'six-months' : [57, 58, 56, 68, 59, 51, 51, 400],
            'recent-trends' : [18, 18, 14, 25, 20, 21, 14, 130]
    }

    winning_hands = {
                     'singles': [187, 13, 3], 'pairs': [595, 41, 12], 
                     'two_pairs': [221, 13, 7], 'three_of_set': [127, 12, 4], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [76, 11, 4], 20: [103, 9, 1], 30: [97, 6, 1], 
                  40: [65, 4, 1], 50: [85, 4, 2], 60: [96, 4, 2]}
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
              'all-time': [577, 581, 1156], 
              'six-months': [34, 46, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [411, 423, 322, 1156],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [12, 9, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 8, 5, 6, 5, 8, 3, 6, 6, 3, 
                       5, 11, 5, 4, 8, 6, 7, 5, 4, 3, 
                       11, 4, 6, 5, 5, 5, 8, 3, 6, 7, 
                       9, 8, 9, 6, 6, 2, 8, 7, 6, 5, 
                       3, 2, 11, 6, 11, 6, 6, 5, 4, 4, 
                       3, 8, 6, 6, 5, 4, 8, 6, 1, 6, 
                       5, 5, 4, 7, 3, 6, 8, 2, 5
                    ]

    white_numbers_trends = [2, 2, 2, 2, 1, 5, 0, 3, 1, 0, 
                            0, 4, 0, 1, 3, 3, 4, 1, 2, 1, 
                            2, 1, 2, 0, 0, 2, 3, 1, 2, 2, 
                            3, 5, 2, 1, 3, 2, 2, 3, 2, 2, 
                            1, 1, 3, 3, 2, 1, 4, 0, 3, 1, 
                            1, 2, 3, 5, 2, 2, 3, 2, 0, 2, 
                            1, 2, 0, 2, 1, 4, 1, 0, 1
                    ]

    red_numbers_6 = [3, 1, 5, 2, 3, 2, 3, 2, 5, 2, 
                     1, 3, 2, 5, 3, 3, 5, 3, 2, 7, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [2, 0, 2, 1, 1, 1, 1, 1, 3, 0, 
                          0, 2, 0, 3, 0, 0, 1, 3, 0, 1, 
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
                     7.12, 7.51, 7.84, 7.02, 6.69, 7.91, 6.36, 6.34, 6.93, 7.46, 
                     7.31, 7.88, 5.02, 6.07, 7.19, 7.35, 6.91, 6.64, 7.82, 7.41, 
                     8.80, 6.92, 8.25, 7.14, 5.95, 6.30, 8.53, 7.72, 6.18, 7.40, 
                     6.66, 8.69, 8.46, 6.15, 6.20, 8.76, 8.25, 7.12, 8.38, 7.18, 
                     6.55, 6.89, 6.83, 7.84, 7.88, 5.71, 7.98, 6.03, 5.58, 7.06, 
                     6.02, 7.08, 7.69, 7.04, 6.39, 7.15, 7.04, 6.67, 7.60, 6.67, 
                     9.86, 7.50, 8.52, 8.39, 6.08, 7.27, 7.89, 7.74, 9.23
                     ]
    red_numbers = [
                   3.56, 3.12, 4.35, 4.85, 3.77, 3.82, 3.74, 3.73, 4.27, 3.83, 
                   3.59, 3.07, 3.95, 4.43, 3.13, 3.15, 3.19, 4.72, 3.69, 4.18, 
                   4.71, 3.47, 3.21, 4.48, 3.77, 4.22
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
                     [21, 24, 28, 34, 40], 
                     [9, 16, 19, 42, 50], 
                     [35, 37, 41, 61, 64], 
                     [5, 16, 24, 36, 44], 
                     [31, 32, 53, 62, 67]
                     ]
    red_numbers = [5, 7, 15, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )