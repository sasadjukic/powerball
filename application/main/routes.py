

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
              'all-time': [2995, 3052, 6130],
              'six-months': [194, 197, 400],
              'recent-trends': [64, 60, 130]
            }

    sets = {
            'all-time' : [778, 848, 912, 925, 848, 872, 947, 6130],
            'six-months' : [53, 51, 65, 52, 64, 61, 54, 400],
            'recent-trends' : [22, 13, 20, 19, 18, 19, 19, 130]
    }

    winning_hands = {
                     'singles': [202, 17, 8], 'pairs': [632, 41, 10], 
                     'two_pairs': [231, 13, 5], 'three_of_set': [133, 7, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 1], 10: [81, 6, 0], 20: [110, 8, 1], 30: [102, 5, 1], 
                  40: [73, 8, 2], 50: [88, 4, 2], 60: [101, 6, 2]
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
              'all-time': [608, 618, 1226],
              'six-months': [38, 42, 80], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [434, 442, 350, 1226],
            'six-months' : [27, 24, 29, 80],
            'recent-trends' : [7, 4, 15, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 7, 4, 10, 6, 4, 8, 6, 3, 3, 
                       6, 8, 5, 3, 4, 7, 5, 7, 3, 6, 
                       8, 2, 14, 4, 6, 1, 3, 12, 9, 5, 
                       4, 4, 7, 5, 9, 6, 7, 2, 3, 7, 
                       3, 5, 9, 9, 7, 4, 6, 7, 7, 8, 
                       5, 11, 6, 5, 5, 4, 6, 4, 7, 8, 
                       6, 9, 6, 5, 5, 3, 4, 2, 6
                    ]

    white_numbers_trends = [
                        2, 2, 1, 4, 3, 1, 3, 4, 2, 0, 
                        1, 2, 2, 0, 1, 2, 2, 1, 2, 0, 
                        3, 0, 4, 1, 4, 0, 1, 5, 2, 1, 
                        2, 1, 4, 1, 6, 2, 2, 0, 0, 1, 
                        0, 2, 5, 3, 2, 1, 0, 3, 1, 3, 
                        2, 5, 1, 2, 1, 0, 2, 2, 1, 0, 
                        4, 4, 2, 2, 2, 0, 2, 0, 3
                    ]

    red_numbers_6 = [
                     4, 5, 3, 2, 3, 3, 0, 3, 4, 1, 
                     3, 4, 3, 2, 3, 0, 1, 3, 4, 9, 
                     3, 2, 1, 5, 9, 0
                    ]

    red_numbers_trends = [
                          0, 1, 2, 0, 1, 1, 0, 2, 0, 0, 
                          1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 
                          2, 2, 1, 3, 5, 0
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
                     7.29, 7.58, 7.72, 7.23, 6.41, 7.46, 6.59, 6.95, 7.05, 6.61, 
                     7.22, 7.89, 4.79, 6.32, 7.19, 7.23, 7.29, 6.72, 7.45, 7.49, 
                     9.56, 6.47, 8.91, 6.85, 6.15, 6.02, 8.61, 8.84, 6.59, 7.56, 
                     6.69, 7.94, 8.21, 6.48, 6.82, 8.29, 8.45, 6.86, 7.93, 6.99, 
                     6.73, 6.71, 7.34, 7.91, 7.65, 6.23, 7.43, 6.24, 5.74, 6.97, 
                     5.77, 7.73, 8.03, 6.81, 6.99, 7.00, 6.64, 6.71, 8.36, 6.41, 
                     8.85, 8.44, 8.03, 8.21, 6.03, 7.14, 7.62, 6.82, 8.76
                     ]
    red_numbers = [
                   3.83, 3.74, 3.61, 4.58, 3.78, 3.46, 3.61, 3.62, 4.34, 3.63, 
                   3.84, 3.35, 4.25, 4.19, 3.12, 3.71, 3.17, 4.52, 3.51, 4.22, 
                   4.49, 3.24, 3.12, 4.73, 4.63, 3.71
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
                     [16, 54, 67, 68, 69],
                     [52, 59, 60, 61, 64],
                     [3, 48, 50, 55, 58],
                     [4, 37, 41, 43, 44],
                     [8, 11, 12, 24, 36]
                     ]
    red_numbers = [2, 11, 13, 14, 17]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )