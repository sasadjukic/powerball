

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
              'all-time': [2725, 2786, 5580], 
              'six-months': [198, 192, 395], 
              'recent-trends': [72, 58, 130]
            }

    sets = {
            'all-time' : [701, 776, 831, 845, 766, 790, 871, 5575],
            'six-months' : [57, 46, 53, 75, 54, 55, 55, 395],
            'recent-trends' : [16, 22, 24, 18, 21, 14, 15, 130]
    }

    winning_hands = {
                     'singles': [183, 12, 6], 'pairs': [576, 45, 18], 
                     'two_pairs': [212, 15, 1], 'three_of_set': [119, 6, 0], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 2], 10: [69, 6, 4], 20: [101, 8, 6], 30: [95, 9, 2], 
                  40: [64, 5, 3], 50: [82, 7, 1], 60: [93, 6, 1]}
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
              'all-time': [554, 562, 1116], 
              'six-months': [33, 46, 79], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [395, 410, 311, 1116],
            'six-months' : [26, 26, 27, 79],
            'recent-trends' : [7, 10, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [6, 7, 4, 7, 8, 4, 4, 6, 11, 4, 
                       7, 6, 3, 3, 5, 4, 3, 5, 6, 3, 
                       9, 5, 4, 6, 5, 5, 8, 2, 6, 7, 
                       10, 7, 12, 6, 5, 7, 8, 6, 7, 5, 
                       1, 4, 7, 5, 11, 6, 5, 8, 2, 4, 
                       4, 5, 5, 5, 5, 6, 7, 8, 6, 4, 
                       5, 5, 3, 10, 2, 5, 6, 6, 9
                    ]

    white_numbers_trends = [3, 4, 2, 1, 1, 1, 1, 1, 2, 1, 
                            4, 3, 2, 2, 2, 1, 2, 3, 2, 2, 
                            6, 3, 0, 3, 4, 2, 2, 0, 2, 3, 
                            1, 3, 2, 1, 0, 0, 4, 1, 3, 1, 
                            1, 0, 5, 1, 6, 3, 1, 3, 0, 1, 
                            1, 3, 2, 0, 0, 1, 2, 4, 0, 1, 
                            1, 2, 1, 3, 1, 2, 2, 1, 1
                    ]

    red_numbers_6 = [1, 2, 3, 3, 2, 1, 4, 2, 8, 2, 
                     1, 2, 2, 3, 4, 5, 4, 0, 3, 7, 
                     8, 6, 1, 1, 2, 2
                    ]

    red_numbers_trends = [0, 1, 1, 1, 0, 1, 1, 0, 2, 1, 
                          1, 0, 0, 2, 2, 2, 1, 0, 1, 2, 
                          3, 3, 0, 0, 1, 0
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
                     6.94, 7.84, 7.84, 6.23, 6.32, 7.58, 6.86, 6.14, 7.06, 7.05, 
                     7.28, 7.47, 5.23, 6.10, 7.19, 7.75, 7.40, 7.45, 8.06, 7.24, 
                     9.55, 6.95, 8.19, 7.76, 6.41, 5.80, 8.76, 7.42, 6.04, 7.85, 
                     6.97, 8.54, 8.55, 6.49, 6.02, 9.13, 7.92, 7.18, 8.20, 6.50, 
                     6.40, 7.46, 6.56, 7.24, 7.50, 6.15, 8.12, 5.96, 5.48, 7.20, 
                     6.13, 7.24, 8.37, 6.93, 6.66, 6.97, 6.41, 6.87, 7.67, 6.06, 
                     9.09, 8.51, 8.71, 8.1, 6.03, 6.93, 7.74, 7.42, 8.83
                     ]
    red_numbers = [
                   3.57, 3.75, 3.95, 5.30, 4.34, 3.82, 3.45, 3.62, 4.03, 3.68, 
                   3.39, 2.93, 4.49, 4.28, 3.06, 3.15, 3.53, 4.71, 3.83, 3.44, 
                   4.67, 3.40, 3.49, 4.22, 3.83, 4.07
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
                     [6, 14, 35, 53, 63], 
                     [24, 32, 37, 66, 69], 
                     [2, 45, 50, 51, 57], 
                     [9, 10, 17, 43, 48], 
                     [11, 26, 30, 44, 47]
                     ]
    red_numbers = [21, 15, 1, 26, 11]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )