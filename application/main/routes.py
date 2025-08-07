

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
              'all-time': [3004, 3057, 6145],
              'six-months': [195, 195, 400],
              'recent-trends': [67, 57, 130]
            }

    sets = {
            'all-time' : [781, 851, 913, 930, 850, 873, 947, 6145],
            'six-months' : [54, 53, 64, 53, 63, 60, 53, 400],
            'recent-trends' : [22, 15, 20, 21, 16, 19, 17, 130]
    }

    winning_hands = {
                     'singles': [202, 17, 7], 'pairs': [633, 41, 10], 
                     'two_pairs': [232, 13, 5], 'three_of_set': [134, 7, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [81, 6, 0], 20: [110, 7, 1], 30: [102, 5, 1], 
                  40: [74, 9, 3], 50: [88, 4, 2], 60: [101, 6, 2]
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
              'all-time': [610, 619, 1229],
              'six-months': [39, 41, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [436, 442, 351, 1229],
            'six-months' : [28, 23, 29, 80],
            'recent-trends' : [9, 4, 13, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 6, 4, 10, 6, 5, 8, 6, 4, 3, 
                       6, 7, 5, 3, 5, 7, 5, 8, 4, 6, 
                       8, 2, 13, 4, 6, 1, 4, 12, 8, 5, 
                       4, 3, 6, 6, 10, 7, 7, 2, 3, 6, 
                       3, 5, 10, 9, 8, 4, 5, 7, 6, 8, 
                       5, 11, 6, 5, 4, 4, 6, 4, 7, 8, 
                       5, 9, 6, 5, 5, 3, 4, 2, 6
                    ]

    white_numbers_trends = [
                        1, 2, 1, 4, 2, 2, 2, 5, 3, 0, 
                        1, 2, 2, 0, 2, 2, 1, 2, 3, 0, 
                        3, 0, 3, 1, 4, 0, 2, 5, 2, 1, 
                        2, 1, 4, 2, 6, 2, 2, 1, 0, 1, 
                        0, 2, 5, 2, 2, 1, 0, 2, 1, 3, 
                        2, 5, 2, 2, 1, 0, 1, 2, 1, 0, 
                        3, 3, 2, 2, 2, 0, 2, 0, 3
                    ]

    red_numbers_6 = [
                     4, 6, 3, 2, 3, 3, 0, 2, 5, 1, 
                     3, 4, 3, 2, 3, 0, 1, 2, 4, 8, 
                     4, 2, 1, 5, 9, 0
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 1, 1, 0, 2, 1, 0, 
                          1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 
                          2, 2, 1, 2, 4, 0
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
                     7.01, 6.96, 7.90, 6.87, 6.07, 7.51, 6.41, 6.43, 7.14, 7.08, 
                     6.53, 7.73, 4.92, 6.36, 7.34, 7.63, 7.03, 7.03, 7.22, 7.97, 
                     9.22, 6.71, 8.82, 6.89, 6.32, 5.83, 8.81, 7.98, 6.26, 6.72, 
                     7.55, 8.55, 8.78, 6.22, 6.95, 8.55, 7.94, 6.88, 8.24, 7.96, 
                     5.97, 6.81, 6.54, 7.98, 7.57, 6.26, 8.05, 6.38, 5.61, 6.88, 
                     6.48, 7.69, 7.49, 7.50, 6.36, 6.43, 7.04, 6.58, 8.23, 6.34, 
                     8.86, 8.48, 8.90, 8.68, 6.22, 6.79, 7.21, 7.64, 8.71
                     ]
    red_numbers = [
                   4.11, 3.33, 3.81, 4.77, 4.04, 4.02, 3.62, 3.63, 4.03, 3.31, 
                   3.76, 3.19, 3.81, 4.43, 2.82, 3.28, 3.25, 4.38, 3.42, 4.27, 
                   4.86, 3.19, 3.53, 5.04, 4.63, 3.47
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
                     [24, 31, 39, 44, 52],
                     [5, 9, 22, 64, 66],
                     [28, 45, 48, 57, 68],
                     [19, 25, 49, 56, 60],
                     [3, 14, 40, 41, 50]
                     ]
    red_numbers = [5, 11, 12, 15, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )