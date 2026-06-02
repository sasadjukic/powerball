

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
              'all-time': [3315, 3380, 6785],
              'six-months': [192, 202, 400],
              'recent-trends': [53, 75, 130]
            }

    sets = {
            'all-time' : [860, 942, 1007, 1012, 939, 974, 1051, 6785],
            'six-months' : [49, 54, 60, 56, 54, 72, 55, 400],
            'recent-trends' : [14, 14, 14, 23, 25, 18, 22, 130]
    }

    winning_hands = {
                     'singles': [227, 16, 7], 'pairs': [705, 47, 13], 
                     'two_pairs': [251, 11, 4], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 1], 10: [91, 7, 1], 20: [120, 5, 2], 30: [107, 4, 1], 
                  40: [88, 7, 3], 50: [102, 10, 1], 60: [115, 10, 4]
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
              'all-time': [669, 688, 1357],
              'six-months': [39, 41, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [479, 489, 389, 1357],
            'six-months' : [28, 26, 26, 80],
            'recent-trends' : [9, 12, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 6, 7, 9, 7, 5, 5, 3, 4, 
                       7, 2, 4, 6, 2, 5, 5, 12, 7, 5, 
                       9, 4, 4, 7, 5, 3, 8, 11, 4, 8, 
                       8, 4, 5, 4, 6, 9, 6, 3, 3, 5, 
                       6, 9, 5, 3, 2, 5, 9, 6, 4, 3, 
                       8, 13, 5, 4, 4, 11, 8, 8, 8, 7, 
                       4, 4, 10, 11, 7, 3, 2, 4, 3
                    ]

    white_numbers_trends = [
                        1, 1, 3, 3, 1, 2, 1, 1, 1, 1, 
                        0, 0, 3, 1, 1, 2, 3, 2, 1, 0, 
                        2, 1, 0, 4, 2, 0, 3, 1, 1, 4, 
                        3, 2, 1, 1, 2, 4, 4, 1, 1, 1, 
                        3, 5, 2, 2, 1, 3, 4, 2, 2, 0, 
                        3, 5, 1, 0, 0, 3, 4, 1, 1, 3, 
                        2, 1, 3, 4, 5, 1, 2, 1, 0
                    ]

    red_numbers_6 = [
                     8, 4, 2, 2, 4, 5, 3, 0, 0, 2, 
                     2, 4, 3, 5, 4, 1, 2, 2, 1, 4, 
                     3, 2, 5, 4, 2, 6
                    ]

    red_numbers_trends = [
                          2, 1, 2, 0, 2, 1, 1, 0, 0, 1, 
                          1, 2, 2, 2, 3, 0, 0, 1, 0, 0, 
                          0, 1, 0, 0, 1, 3
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
                     6.83, 7.08, 7.75, 6.54, 6.71, 7.72, 6.88, 7.04, 6.27, 6.82, 
                     7.05, 6.94, 5.28, 6.10, 7.06, 7.59, 7.22, 7.10, 7.06, 6.67, 
                     9.61, 7.13, 8.38, 7.16, 6.61, 5.55, 8.97, 8.45, 6.15, 7.13, 
                     7.15, 8.19, 8.37, 6.02, 6.65, 8.13, 7.87, 6.37, 8.27, 7.35, 
                     6.36, 7.06, 6.92, 7.54, 7.30, 6.14, 7.82, 6.38, 5.65, 7.66, 
                     7.00, 8.35, 7.90, 6.86, 6.42, 7.56, 7.37, 7.10, 7.62, 6.76, 
                     9.11, 8.07, 8.47, 8.63, 6.48, 7.32, 7.59, 6.82, 8.52
                     ]
    red_numbers = [
                   4.04, 4.35, 3.79, 4.74, 3.95, 3.43, 3.02, 3.43, 3.65, 3.32, 
                   3.35, 3.56, 3.59, 4.39, 3.38, 3.06, 3.35, 4.19, 3.69, 4.32, 
                   4.76, 3.75, 3.57, 4.62, 4.45, 4.25
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
                     [5, 6, 18, 38, 56],
                     [17, 24, 28, 42, 50],
                     [10, 11, 17, 27, 28],
                     [34, 39, 55, 59, 67],
                     [2, 5, 10, 20, 50]
                     ]
    red_numbers = [2, 8, 11, 13, 14]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )