

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
              'all-time': [3050, 3106, 6240],
              'six-months': [197, 193, 400],
              'recent-trends': [64, 62, 130]
            }

    sets = {
            'all-time' : [790, 866, 928, 939, 865, 883, 969, 6240],
            'six-months' : [55, 52, 63, 53, 63, 52, 62, 400],
            'recent-trends' : [16, 21, 17, 19, 18, 13, 26, 130]
    }

    winning_hands = {
                     'singles': [205, 17, 4], 'pairs': [643, 41, 14], 
                     'two_pairs': [235, 11, 4], 'three_of_set': [137, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 2, 0], 10: [82, 4, 1], 20: [114, 10, 4], 30: [102, 4, 1], 
                  40: [75, 9, 2], 50: [90, 5, 2], 60: [103, 6, 3]
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
              'all-time': [619, 629, 1248],
              'six-months': [39, 41, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [445, 447, 356, 1248],
            'six-months' : [30, 21, 29, 80],
            'recent-trends' : [13, 5, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 4, 5, 9, 6, 5, 9, 7, 5, 2, 
                       6, 6, 4, 6, 8, 8, 3, 5, 4, 5, 
                       6, 3, 13, 5, 7, 2, 4, 9, 9, 5, 
                       5, 3, 7, 7, 10, 4, 8, 1, 3, 8, 
                       5, 7, 9, 8, 7, 5, 3, 6, 5, 7, 
                       5, 9, 10, 3, 2, 2, 4, 3, 7, 4, 
                       9, 10, 5, 10, 5, 4, 5, 2, 8
                    ]

    white_numbers_trends = [
                        0, 2, 2, 2, 0, 2, 3, 3, 2, 0, 
                        3, 1, 0, 3, 5, 3, 0, 3, 3, 0, 
                        0, 2, 4, 2, 2, 1, 2, 2, 2, 1, 
                        3, 1, 2, 3, 4, 2, 2, 1, 0, 4, 
                        2, 2, 2, 2, 2, 1, 1, 0, 2, 4, 
                        1, 0, 5, 1, 0, 0, 1, 0, 1, 1, 
                        4, 5, 1, 6, 3, 1, 2, 1, 2
                    ]

    red_numbers_6 = [
                     5, 7, 2, 4, 5, 2, 0, 2, 3, 1, 
                     3, 3, 2, 1, 2, 0, 2, 2, 5, 5, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          2, 2, 1, 2, 3, 0, 0, 1, 2, 0, 
                          0, 0, 0, 1, 0, 0, 2, 1, 1, 1, 
                          1, 2, 2, 0, 2, 0
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
                     6.94, 7.01, 7.35, 6.80, 5.86, 7.56, 6.68, 6.57, 7.02, 6.72, 
                     7.29, 7.63, 5.52, 6.36, 6.94, 7.62, 6.74, 6.98, 7.04, 7.67, 
                     8.85, 6.75, 9.53, 7.30, 6.43, 5.66, 8.65, 7.71, 6.39, 7.54, 
                     6.89, 8.53, 9.03, 5.95, 6.42, 8.86, 7.95, 6.80, 8.16, 7.67, 
                     6.92, 6.90, 7.12, 8.15, 7.30, 6.24, 8.18, 6.66, 5.65, 6.97, 
                     6.28, 7.36, 8.22, 7.69, 6.39, 6.78, 6.61, 6.32, 7.45, 6.29, 
                     9.45, 8.14, 7.71, 8.62, 6.21, 7.57, 7.58, 7.21, 8.66
                     ]
    red_numbers = [
                   3.91, 3.43, 3.85, 4.73, 4.21, 3.70, 3.48, 3.85, 4.25, 3.57, 
                   3.37, 3.26, 3.64, 4.25, 2.97, 3.09, 3.32, 4.40, 3.88, 4.55, 
                   4.68, 3.70, 3.02, 4.73, 4.33, 3.83
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
                     [15, 16, 31, 53, 67],
                     [7, 18, 50, 55, 66],
                     [2, 26, 41, 47, 49],
                     [8, 11, 25, 62, 63],
                     [20, 45, 51, 60, 61]
                     ]
    red_numbers = [1, 2, 21, 24, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )