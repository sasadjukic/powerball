

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
              'all-time': [3016, 3075, 6175],
              'six-months': [194, 196, 400],
              'recent-trends': [61, 63, 130]
            }

    sets = {
            'all-time' : [784, 855, 916, 932, 856, 875, 957, 6175],
            'six-months' : [55, 52, 63, 51, 63, 57, 59, 400],
            'recent-trends' : [21, 16, 15, 19, 20, 15, 24, 130]
    }

    winning_hands = {
                     'singles': [203, 16, 7], 'pairs': [635, 40, 11], 
                     'two_pairs': [233, 13, 4], 'three_of_set': [136, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [81, 5, 0], 20: [111, 8, 1], 30: [102, 5, 1], 
                  40: [75, 10, 4], 50: [88, 3, 2], 60: [101, 5, 2]
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
              'all-time': [614, 621, 1235],
              'six-months': [40, 40, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [440, 443, 352, 1235],
            'six-months' : [30, 20, 30, 80],
            'recent-trends' : [12, 3, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 5, 3, 11, 6, 6, 9, 6, 4, 3, 
                       7, 6, 5, 4, 6, 7, 4, 7, 3, 6, 
                       7, 2, 14, 5, 6, 1, 3, 12, 7, 4, 
                       5, 2, 7, 6, 10, 6, 6, 2, 3, 9, 
                       3, 5, 9, 9, 6, 5, 4, 7, 6, 8, 
                       5, 11, 6, 3, 4, 3, 5, 4, 8, 7, 
                       6, 9, 7, 6, 7, 3, 4, 3, 7
                    ]

    white_numbers_trends = [
                        1, 2, 0, 4, 2, 2, 3, 5, 2, 0, 
                        2, 2, 1, 1, 3, 2, 0, 2, 3, 0, 
                        2, 0, 2, 2, 3, 0, 1, 5, 0, 0, 
                        3, 0, 4, 2, 6, 2, 1, 1, 0, 3, 
                        0, 2, 4, 3, 2, 2, 0, 2, 2, 3, 
                        2, 2, 1, 2, 1, 0, 1, 2, 1, 1, 
                        4, 4, 3, 2, 4, 0, 1, 1, 4
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 4, 3, 0, 2, 4, 1, 
                     3, 3, 3, 2, 3, 0, 0, 1, 4, 8, 
                     4, 2, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 2, 1, 0, 2, 1, 0, 
                          0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 
                          2, 2, 2, 1, 2, 0
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
                     6.63, 7.34, 7.04, 6.87, 6.38, 7.43, 6.73, 6.61, 6.82, 7.01, 
                     6.95, 7.43, 5.39, 6.67, 6.99, 7.66, 7.67, 6.92, 7.33, 7.73, 
                     8.71, 6.56, 9.34, 7.42, 6.53, 5.89, 8.55, 8.24, 6.48, 7.43, 
                     6.83, 8.28, 9.49, 5.98, 6.56, 8.84, 7.71, 6.87, 7.85, 7.34, 
                     6.76, 6.41, 6.97, 7.70, 7.10, 5.88, 7.75, 6.51, 5.67, 6.64, 
                     6.28, 7.78, 7.97, 6.96, 6.84, 6.45, 6.91, 6.67, 8.37, 7.17, 
                     8.87, 8.27, 8.40, 8.53, 6.66, 6.88, 7.34, 7.20, 8.56
                     ]
    red_numbers = [
                   4.12, 3.92, 3.72, 4.86, 4.36, 3.81, 2.99, 3.44, 4.36, 3.53, 
                   3.48, 3.13, 3.54, 4.40, 3.25, 3.25, 3.21, 4.37, 3.53, 3.97, 
                   4.78, 2.98, 3.64, 4.84, 4.57, 3.95
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
                     [45, 58, 60, 63, 64],
                     [29, 38, 52, 53, 59],
                     [1, 12, 42, 48, 57],
                     [10, 29, 34, 47, 69],
                     [2, 6, 35, 54, 66]
                     ]
    red_numbers = [3, 7, 11, 14, 17]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )