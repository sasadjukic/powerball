

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
              'all-time': [3453, 3521, 7065],
              'six-months': [186, 211, 400],
              'recent-trends': [70, 60, 130]
            }

    sets = {
            'all-time' : [900, 990, 1043, 1042, 978, 1024, 1088, 7065],
            'six-months' : [51, 61, 49, 52, 62, 67, 58, 400],
            'recent-trends' : [17, 25, 20, 12, 15, 21, 20, 130]
    }

    winning_hands = {
                     'singles': [235, 14, 2], 'pairs': [734, 41, 14], 
                     'two_pairs': [262, 15, 4], 'three_of_set': [150, 10, 6], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [87, 5, 2], 10: [96, 6, 3], 20: [121, 3, 1], 30: [109, 3, 2], 
                  40: [94, 9, 2], 50: [108, 7, 2], 60: [118, 7, 2]
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
              'all-time': [701, 712, 1413],
              'six-months': [45, 35, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [502, 511, 400, 1413],
            'six-months' : [30, 34, 16, 80],
            'recent-trends' : [9, 11, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 6, 9, 9, 6, 6, 2, 5, 6, 5, 
                       2, 3, 6, 10, 5, 10, 10, 5, 5, 3, 
                       8, 2, 3, 6, 7, 5, 5, 3, 7, 9, 
                       5, 5, 4, 2, 3, 8, 6, 7, 3, 6, 
                       5, 8, 4, 9, 5, 5, 6, 7, 7, 7, 
                       4, 6, 6, 5, 8, 6, 8, 8, 9, 6, 
                       6, 3, 6, 10, 10, 4, 6, 4, 3
                    ]

    white_numbers_trends = [
                        1, 2, 2, 4, 2, 1, 1, 2, 2, 2, 
                        2, 1, 2, 3, 4, 3, 3, 2, 3, 1, 
                        4, 0, 3, 1, 3, 2, 1, 1, 4, 2, 
                        1, 2, 3, 0, 0, 1, 1, 1, 1, 3, 
                        1, 3, 0, 2, 2, 0, 1, 0, 3, 1, 
                        1, 1, 1, 2, 3, 2, 3, 5, 2, 0, 
                        2, 1, 1, 3, 5, 1, 3, 2, 2
                    ]

    red_numbers_6 = [
                     2, 5, 8, 2, 3, 2, 4, 1, 3, 4, 
                     2, 4, 5, 7, 5, 1, 2, 3, 1, 3, 
                     0, 3, 3, 1, 3, 3
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 0, 0, 2, 0, 3, 2, 
                          0, 0, 2, 3, 1, 0, 1, 1, 1, 1, 
                          0, 2, 2, 1, 0, 0
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
                     6.51, 7.24, 8.11, 6.73, 6.52, 7.47, 6.45, 6.72, 6.74, 7.08, 
                     6.80, 7.35, 5.24, 6.86, 6.54, 7.23, 7.69, 7.43, 7.65, 7.53, 
                     9.37, 6.63, 8.94, 7.14, 6.47, 5.84, 8.05, 8.44, 6.71, 6.89, 
                     7.46, 8.18, 7.92, 6.02, 6.59, 8.15, 7.93, 6.35, 7.48, 8.07, 
                     6.63, 6.39, 7.07, 7.63, 7.37, 5.75, 7.55, 6.72, 5.92, 7.25, 
                     6.86, 6.99, 7.53, 7.01, 7.08, 7.42, 7.53, 6.65, 8.37, 7.52, 
                     8.83, 8.07, 7.91, 9.37, 6.72, 7.04, 7.79, 6.57, 7.94
                ]
    red_numbers = [
                   4.80, 3.54, 3.75, 4.57, 4.32, 3.79, 3.49, 3.24, 4.07, 3.58, 
                   3.36, 3.86, 3.34, 4.43, 3.33, 2.87, 3.21, 3.90, 3.67, 4.60, 
                   4.54, 3.36, 3.80, 4.51, 4.48, 3.59
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
                     [17, 33, 40, 43, 45],
                     [6, 19, 31, 38, 54],
                     [3, 17, 19, 38, 53],
                     [14, 18, 26, 28, 44],
                     [4, 19, 26, 38, 57]
                     ]
    red_numbers = [9, 10, 13, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )