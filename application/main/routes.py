

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
              'all-time': [3383, 3461, 6935],
              'six-months': [178, 218, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [883, 965, 1023, 1030, 963, 1003, 1068, 6935],
            'six-months' : [51, 58, 47, 52, 66, 73, 53, 400],
            'recent-trends' : [22, 19, 15, 13, 22, 26, 13, 130]
    }

    winning_hands = {
                     'singles': [233, 17, 6], 'pairs': [720, 42, 12], 
                     'two_pairs': [258, 13, 6], 'three_of_set': [144, 6, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 4], 10: [93, 7, 1], 20: [120, 4, 0], 30: [107, 1, 0], 
                  40: [92, 10, 3], 50: [106, 8, 3], 60: [116, 7, 1]
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
              'all-time': [688, 699, 1387],
              'six-months': [46, 34, 80], 
              'recent-trends': [17, 9, 26]
            }

    sets = {
            'all-time' : [493, 500, 394, 1387],
            'six-months' : [32, 26, 22, 80],
            'recent-trends' : [13, 9, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 6, 5, 10, 6, 3, 6, 5, 
                       4, 4, 5, 9, 1, 8, 9, 8, 5, 5, 
                       6, 4, 3, 6, 5, 3, 5, 6, 4, 9, 
                       5, 3, 3, 2, 4, 11, 6, 7, 2, 4, 
                       7, 10, 6, 7, 3, 5, 9, 10, 5, 9, 
                       4, 10, 5, 6, 7, 9, 7, 7, 9, 7, 
                       5, 3, 7, 12, 7, 4, 3, 3, 2
                    ]

    white_numbers_trends = [
                        0, 3, 4, 2, 3, 4, 1, 2, 3, 2, 
                        0, 1, 2, 5, 0, 3, 4, 1, 1, 2, 
                        2, 1, 0, 1, 2, 3, 1, 1, 2, 3, 
                        0, 0, 0, 0, 1, 3, 2, 3, 1, 2, 
                        2, 1, 1, 5, 2, 2, 1, 5, 1, 6, 
                        0, 0, 4, 3, 3, 1, 2, 2, 5, 2, 
                        2, 1, 2, 1, 1, 1, 1, 1, 1
                    ]

    red_numbers_6 = [
                     6, 4, 6, 2, 5, 6, 2, 1, 0, 3, 
                     2, 5, 4, 4, 4, 1, 1, 2, 0, 5, 
                     2, 1, 2, 4, 4, 4
                    ]

    red_numbers_trends = [
                          1, 2, 3, 2, 2, 1, 1, 1, 0, 1, 
                          1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
                          0, 0, 1, 0, 2, 0
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
                     7.28, 7.07, 7.65, 6.74, 6.19, 7.79, 7.20, 7.05, 7.00, 7.21, 
                     6.97, 7.75, 4.95, 6.94, 6.93, 7.66, 7.57, 6.83, 7.47, 6.81, 
                     9.46, 6.36, 8.26, 7.41, 6.52, 5.79, 8.29, 8.58, 5.96, 7.28, 
                     6.77, 8.00, 8.27, 6.33, 6.28, 8.17, 7.70, 6.88, 7.17, 6.83, 
                     6.02, 7.16, 7.12, 7.92, 7.07, 6.30, 8.06, 6.51, 5.55, 7.80, 
                     6.33, 8.19, 8.31, 7.29, 6.18, 7.40, 7.11, 6.31, 8.14, 7.02, 
                     9.63, 7.89, 8.71, 8.95, 6.07, 6.81, 7.22, 7.35, 8.21
                     ]
    red_numbers = [
                   4.57, 3.68, 3.88, 4.48, 4.38, 3.80, 3.24, 3.11, 3.90, 3.19, 
                   3.55, 3.65, 3.87, 4.70, 3.45, 2.96, 3.10, 3.99, 3.61, 4.01, 
                   4.62, 3.25, 3.84, 4.48, 4.41, 4.28
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
                     [16, 23, 38, 39, 54],
                     [3, 7, 8, 20, 29],
                     [22, 36, 39, 52, 59],
                     [5, 10, 13, 14, 28],
                     [9, 17, 18, 25, 27]
                     ]
    red_numbers = [4, 7, 10, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )