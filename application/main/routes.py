

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
              'all-time': [3289, 3342, 6720],
              'six-months': [197, 198, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [854, 935, 1001, 1001, 926, 964, 1039, 6720],
            'six-months' : [55, 53, 62, 52, 51, 72, 55, 400],
            'recent-trends' : [16, 21, 15, 17, 21, 23, 17, 130]
    }

    winning_hands = {
                     'singles': [224, 16, 7], 'pairs': [698, 48, 13], 
                     'two_pairs': [249, 10, 3], 'three_of_set': [141, 4, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 4], 20: [120, 5, 2], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 10, 2], 60: [112, 9, 1]
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
              'all-time': [662, 682, 1344],
              'six-months': [36, 44, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [477, 481, 386, 1344],
            'six-months' : [29, 22, 29, 80],
            'recent-trends' : [11, 6, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 4, 8, 6, 8, 9, 8, 6, 4, 4, 
                       7, 3, 3, 5, 2, 5, 5, 11, 8, 5, 
                       8, 3, 4, 7, 5, 5, 6, 13, 6, 6, 
                       7, 5, 6, 3, 5, 9, 4, 3, 4, 5, 
                       4, 7, 8, 3, 2, 3, 8, 5, 6, 4, 
                       9, 11, 7, 4, 4, 8, 8, 9, 8, 7, 
                       4, 6, 9, 9, 6, 4, 1, 5, 4
                    ]

    white_numbers_trends = [
                        0, 0, 4, 2, 0, 3, 5, 0, 2, 2, 
                        3, 2, 2, 2, 0, 1, 3, 4, 2, 1, 
                        3, 1, 1, 3, 2, 0, 1, 2, 1, 3, 
                        2, 1, 1, 0, 1, 5, 2, 1, 1, 0, 
                        3, 6, 3, 0, 1, 1, 5, 0, 2, 2, 
                        1, 6, 1, 1, 2, 3, 3, 1, 3, 1, 
                        2, 1, 4, 4, 2, 0, 1, 1, 1
                    ]

    red_numbers_6 = [
                     9, 5, 3, 2, 3, 5, 2, 0, 0, 1, 
                     3, 2, 1, 5, 3, 1, 2, 2, 2, 4, 
                     4, 2, 8, 4, 1, 6
                    ]

    red_numbers_trends = [
                          4, 2, 2, 0, 1, 2, 0, 0, 0, 0, 
                          1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 
                          1, 0, 0, 2, 1, 3
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
                     7.19, 7.07, 7.92, 6.72, 6.60, 7.79, 7.25, 6.46, 6.78, 6.42, 
                     7.71, 7.55, 5.42, 6.30, 6.48, 7.70, 7.14, 7.63, 7.32, 6.88, 
                     9.13, 6.88, 8.89, 7.16, 6.78, 5.62, 8.65, 8.81, 6.78, 7.51, 
                     6.61, 8.11, 8.47, 5.84, 6.33, 8.32, 8.19, 6.26, 8.24, 7.57, 
                     6.42, 6.95, 7.10, 7.88, 7.48, 6.01, 7.93, 6.24, 6.01, 7.54, 
                     6.53, 7.60, 8.07, 7.01, 6.94, 6.79, 6.67, 6.47, 8.00, 6.62, 
                     8.59, 7.93, 7.75, 8.64, 6.86, 7.00, 7.44, 6.72, 8.33
                     ]
    red_numbers = [
                   4.67, 3.59, 3.73, 5.02, 3.91, 3.68, 3.33, 3.01, 3.93, 3.48, 
                   3.47, 3.33, 3.78, 4.94, 3.26, 2.94, 3.02, 4.09, 4.13, 4.07, 
                   4.57, 3.61, 3.69, 4.40, 4.53, 3.82
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
                     [6, 7, 19, 23, 63],
                     [1, 2, 25, 40, 61],
                     [5, 8, 17, 45, 55],
                     [11, 24, 43, 52, 54],
                     [8, 12, 24, 28, 43]
                     ]
    red_numbers = [9, 20, 21, 24, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )