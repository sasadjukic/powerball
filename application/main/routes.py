

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
              'all-time': [3301, 3365, 6755],
              'six-months': [196, 199, 400],
              'recent-trends': [52, 77, 130]
            }

    sets = {
            'all-time' : [856, 938, 1004, 1008, 932, 969, 1048, 6755],
            'six-months' : [51, 55, 60, 57, 49, 73, 55, 400],
            'recent-trends' : [13, 17, 13, 21, 23, 20, 23, 130]
    }

    winning_hands = {
                     'singles': [224, 15, 6], 'pairs': [703, 48, 15], 
                     'two_pairs': [250, 11, 3], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 3], 20: [120, 5, 2], 30: [107, 5, 1], 
                  40: [87, 6, 3], 50: [102, 11, 2], 60: [114, 9, 3]
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
              'all-time': [666, 685, 1351],
              'six-months': [38, 42, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [479, 485, 387, 1351],
            'six-months' : [30, 24, 26, 80],
            'recent-trends' : [11, 8, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 3, 6, 6, 8, 8, 8, 7, 3, 4, 
                       7, 3, 4, 5, 3, 5, 4, 12, 8, 5, 
                       8, 4, 4, 7, 5, 4, 7, 12, 4, 8, 
                       8, 4, 6, 4, 5, 10, 6, 3, 3, 5, 
                       5, 8, 5, 2, 2, 4, 9, 4, 5, 4, 
                       9, 12, 6, 4, 4, 11, 7, 8, 8, 6, 
                       4, 4, 10, 10, 7, 3, 2, 5, 4
                    ]

    white_numbers_trends = [
                        0, 0, 3, 3, 0, 2, 3, 1, 1, 1, 
                        3, 2, 3, 0, 1, 1, 2, 3, 1, 0, 
                        2, 1, 0, 4, 2, 0, 2, 1, 1, 3, 
                        3, 1, 1, 1, 1, 5, 4, 1, 1, 1, 
                        4, 5, 3, 1, 1, 2, 4, 0, 2, 0, 
                        2, 5, 1, 0, 1, 5, 3, 0, 3, 2, 
                        3, 1, 4, 5, 5, 0, 2, 1, 0
                    ]

    red_numbers_6 = [
                     8, 5, 3, 2, 4, 5, 3, 0, 0, 1, 
                     2, 3, 2, 5, 4, 1, 2, 2, 2, 4, 
                     4, 2, 6, 4, 1, 5
                    ]

    red_numbers_trends = [
                          3, 2, 2, 0, 2, 1, 1, 0, 0, 0, 
                          1, 1, 1, 1, 3, 0, 0, 1, 0, 1, 
                          0, 1, 0, 1, 1, 3
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
                     7.04, 7.38, 7.94, 6.99, 6.16, 7.60, 7.14, 6.26, 7.05, 6.66, 
                     7.27, 8.00, 5.35, 6.42, 6.56, 7.42, 7.05, 7.29, 7.36, 7.00, 
                     8.68, 6.68, 7.93, 7.56, 6.07, 5.89, 8.38, 8.39, 6.84, 7.31, 
                     7.08, 8.44, 8.97, 6.06, 6.40, 8.71, 7.96, 6.48, 7.98, 7.13, 
                     6.34, 7.75, 7.13, 8.19, 7.39, 5.75, 7.94, 6.36, 5.87, 7.06, 
                     6.50, 8.17, 8.36, 6.88, 6.50, 7.26, 7.68, 6.51, 7.80, 6.55, 
                     8.29, 7.59, 8.51, 8.48, 6.62, 7.50, 7.30, 6.83, 8.01
                     ]
    red_numbers = [
                   4.30, 3.64, 3.96, 5.05, 3.91, 3.95, 3.67, 3.44, 3.95, 3.38, 
                   3.72, 3.32, 3.61, 4.87, 3.39, 3.26, 2.92, 4.71, 3.55, 4.26, 
                   4.28, 3.58, 3.13, 4.29, 4.27, 3.59
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
                     [10, 33, 41, 44, 58],
                     [5, 22, 36, 52, 68],
                     [31, 34, 52, 61, 64],
                     [27, 36, 37, 44, 57],
                     [17, 36, 52, 61, 62]
                     ]
    red_numbers = [8, 10, 21, 22, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )