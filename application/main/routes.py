

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
              'all-time': [2960, 3021, 6060],
              'six-months': [195, 197, 400],
              'recent-trends': [66, 60, 130]
            }

    sets = {
            'all-time' : [766, 840, 902, 915, 839, 862, 936, 6060],
            'six-months' : [53, 53, 61, 59, 62, 61, 51, 400],
            'recent-trends' : [18, 17, 21, 20, 20, 19, 15, 130]
    }

    winning_hands = {
                     'singles': [198, 14, 5], 'pairs': [625, 40, 13], 
                     'two_pairs': [229, 15, 5], 'three_of_set': [132, 9, 2], 
                     'full_house': [18, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 3], 20: [110, 8, 4], 30: [101, 5, 1], 
                  40: [72, 7, 3], 50: [86, 3, 1], 60: [99, 5, 1]
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
              'all-time': [602, 610, 1212],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [428, 441, 343, 1211],
            'six-months' : [28, 26, 26, 80],
            'recent-trends' : [5, 9, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 6, 5, 9, 6, 9, 6, 4, 3, 3, 
                       5, 8, 4, 4, 6, 8, 7, 6, 2, 7, 
                       6, 2, 14, 3, 4, 3, 5, 8, 9, 6, 
                       5, 7, 5, 5, 8, 6, 8, 4, 5, 8, 
                       4, 4, 9, 8, 6, 4, 7, 5, 7, 6, 
                       5, 11, 8, 6, 5, 5, 5, 3, 7, 8, 
                       4, 8, 4, 5, 5, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        3, 2, 2, 3, 3, 1, 2, 0, 2, 2, 
                        0, 2, 3, 2, 2, 3, 2, 1, 0, 1, 
                        2, 0, 6, 1, 2, 0, 2, 2, 5, 2, 
                        2, 2, 1, 3, 4, 1, 4, 0, 1, 4, 
                        1, 3, 4, 2, 2, 0, 1, 3, 0, 2, 
                        1, 6, 2, 0, 0, 1, 2, 1, 4, 2, 
                        2, 3, 0, 2, 2, 1, 2, 1, 0
                    ]

    red_numbers_6 = [
                     5, 4, 3, 3, 3, 3, 1, 1, 5, 1, 
                     3, 5, 3, 4, 3, 0, 1, 2, 4, 8, 
                     2, 1, 1, 6, 7, 1
                    ]

    red_numbers_trends = [
                          0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 
                          3, 1, 2, 0, 1, 0, 0, 0, 2, 2, 
                          2, 1, 0, 3, 4, 0
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
                     7.80, 7.37, 7.77, 6.74, 6.94, 7.38, 6.75, 6.71, 6.60, 6.16, 
                     7.30, 7.86, 5.39, 7.08, 6.70, 7.05, 7.41, 6.86, 7.69, 7.21, 
                     9.10, 6.70, 9.20, 6.80, 5.81, 5.97, 8.56, 7.96, 6.93, 7.26, 
                     7.12, 8.27, 8.57, 6.09, 6.32, 8.69, 7.95, 6.58, 8.16, 7.71, 
                     7.17, 6.89, 6.78, 8.24, 7.68, 6.02, 8.21, 5.94, 5.37, 6.57, 
                     6.17, 7.59, 7.42, 7.39, 6.85, 7.85, 6.95, 6.51, 7.89, 7.04, 
                     8.61, 8.03, 8.47, 8.07, 6.25, 7.12, 7.44, 6.63, 8.33
                     ]
    red_numbers = [
                   3.96, 3.38, 3.76, 4.67, 4.20, 3.78, 3.05, 3.50, 4.18, 3.68, 
                   3.63, 3.49, 4.01, 4.52, 3.08, 2.97, 3.31, 4.56, 3.83, 4.05, 
                   4.54, 3.43, 3.44, 4.62, 4.59, 3.77
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
                     [9, 27, 30, 37, 57],
                     [18, 21, 42, 61, 64],
                     [25, 48, 49, 50, 56],
                     [1, 8, 22, 31, 35],
                     [7, 19, 62, 63, 66]
                     ]
    red_numbers = [1, 5, 17, 18, 20]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )