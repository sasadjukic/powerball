

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
              'all-time': [3297, 3359, 6745],
              'six-months': [195, 200, 400],
              'recent-trends': [55, 74, 130]
            }

    sets = {
            'all-time' : [854, 937, 1004, 1006, 930, 969, 1045, 6745],
            'six-months' : [50, 54, 62, 56, 50, 75, 53, 400],
            'recent-trends' : [12, 20, 15, 19, 22, 21, 21, 130]
    }

    winning_hands = {
                     'singles': [224, 16, 7], 'pairs': [701, 47, 13], 
                     'two_pairs': [250, 11, 3], 'three_of_set': [142, 4, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 3], 20: [120, 5, 2], 30: [107, 5, 1], 
                  40: [86, 6, 2], 50: [102, 11, 2], 60: [113, 8, 2]
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
              'all-time': [665, 684, 1349],
              'six-months': [37, 43, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [479, 483, 387, 1349],
            'six-months' : [30, 22, 28, 80],
            'recent-trends' : [12, 6, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 3, 6, 5, 8, 9, 8, 6, 3, 4, 
                       7, 3, 3, 5, 3, 5, 4, 12, 8, 5, 
                       8, 4, 4, 7, 5, 4, 7, 13, 5, 8, 
                       8, 4, 6, 3, 5, 10, 5, 3, 4, 4, 
                       5, 8, 6, 2, 2, 4, 9, 5, 5, 4, 
                       10, 12, 6, 4, 4, 11, 7, 9, 8, 6, 
                       3, 4, 10, 10, 6, 3, 2, 5, 4
                    ]

    white_numbers_trends = [
                        0, 0, 3, 2, 0, 2, 4, 0, 1, 2, 
                        3, 2, 2, 1, 1, 1, 2, 4, 2, 1, 
                        3, 1, 0, 4, 2, 0, 2, 1, 1, 3, 
                        3, 1, 1, 0, 1, 5, 3, 1, 1, 0, 
                        4, 5, 3, 0, 1, 2, 5, 0, 2, 0, 
                        2, 6, 1, 0, 1, 5, 3, 0, 3, 2, 
                        2, 1, 4, 5, 3, 0, 2, 1, 1
                    ]

    red_numbers_6 = [
                     8, 5, 3, 2, 4, 5, 3, 0, 0, 1, 
                     2, 2, 2, 5, 4, 1, 2, 1, 2, 4, 
                     4, 2, 8, 4, 1, 5
                    ]

    red_numbers_trends = [
                          4, 2, 2, 0, 2, 1, 1, 0, 0, 0, 
                          1, 0, 1, 1, 3, 0, 0, 0, 0, 2, 
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
                     6.72, 7.01, 7.88, 7.05, 6.20, 7.33, 6.99, 6.57, 6.75, 6.38, 
                     7.28, 7.45, 5.41, 6.99, 6.88, 7.63, 7.22, 7.24, 7.19, 6.87, 
                     8.90, 7.05, 8.41, 7.53, 6.49, 5.32, 8.74, 9.07, 6.82, 6.85, 
                     7.17, 8.28, 7.98, 5.88, 6.76, 8.26, 8.09, 6.88, 8.06, 7.44, 
                     6.65, 6.89, 7.07, 7.98, 7.37, 5.73, 7.56, 6.53, 6.01, 6.89, 
                     6.83, 8.23, 8.07, 7.03, 6.66, 7.24, 7.05, 6.95, 7.95, 6.54, 
                     8.79, 7.65, 8.25, 8.81, 5.90, 7.26, 7.58, 6.90, 8.61
                     ]
    red_numbers = [
                   4.22, 3.40, 3.63, 5.00, 4.31, 3.62, 3.41, 3.42, 3.79, 3.34, 
                   3.37, 3.08, 3.58, 4.79, 3.65, 2.79, 3.00, 4.61, 3.61, 4.46, 
                   4.66, 3.57, 4.06, 4.67, 4.24, 3.72
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
                     [1, 4, 14, 27, 34],
                     [6, 33, 36, 58, 61],
                     [2, 16, 36, 37, 49],
                     [25, 27, 28, 35, 67],
                     [2, 41, 63, 66, 69]
                     ]
    red_numbers = [4, 7, 12, 16, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )