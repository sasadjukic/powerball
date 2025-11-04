

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
              'all-time': [3098, 3153, 6335],
              'six-months': [201, 190, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [802, 882, 941, 950, 880, 893, 987, 6335],
            'six-months' : [51, 59, 60, 55, 61, 48, 66, 400],
            'recent-trends' : [14, 20, 19, 14, 21, 16, 26, 130]
    }

    winning_hands = {
                     'singles': [208, 15, 4], 'pairs': [653, 41, 14], 
                     'two_pairs': [239, 15, 5], 'three_of_set': [137, 7, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 6, 2], 20: [115, 9, 2], 30: [102, 2, 0], 
                  40: [80, 11, 5], 50: [91, 5, 3], 60: [104, 6, 2]
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
              'all-time': [627, 640, 1267],
              'six-months': [35, 45, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [449, 460, 358, 1267],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [8, 15, 3, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 8, 7, 4, 3, 7, 8, 5, 5, 
                       5, 5, 7, 6, 8, 9, 4, 6, 4, 2, 
                       4, 4, 10, 5, 5, 2, 7, 12, 9, 3, 
                       6, 8, 6, 8, 9, 3, 7, 2, 3, 10, 
                       3, 7, 10, 7, 6, 3, 4, 6, 5, 7, 
                       4, 9, 8, 5, 2, 1, 3, 4, 5, 6, 
                       9, 9, 3, 9, 7, 6, 8, 3, 6
                    ]

    white_numbers_trends = [
                        1, 3, 5, 1, 0, 0, 2, 2, 0, 3, 
                        2, 1, 3, 2, 3, 2, 2, 2, 0, 1, 
                        0, 2, 1, 2, 0, 2, 3, 5, 3, 1, 
                        1, 6, 0, 1, 0, 0, 2, 1, 2, 2, 
                        1, 3, 3, 3, 2, 1, 2, 1, 3, 2, 
                        1, 2, 4, 3, 1, 0, 1, 1, 1, 3, 
                        2, 3, 0, 4, 2, 5, 5, 1, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 4, 5, 1, 0, 2, 2, 2, 
                     3, 3, 2, 3, 4, 1, 2, 3, 5, 5, 
                     4, 5, 2, 4, 7, 0
                    ]

    red_numbers_trends = [
                          2, 1, 1, 2, 1, 0, 0, 0, 1, 2, 
                          0, 2, 0, 2, 3, 1, 1, 1, 3, 2, 
                          0, 1, 0, 0, 0, 0
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
                     6.89, 8.18, 8.01, 6.68, 6.31, 7.23, 6.96, 6.86, 6.94, 6.60, 
                     6.96, 7.63, 5.43, 6.28, 7.30, 7.75, 6.79, 6.77, 7.33, 7.07, 
                     8.90, 6.45, 9.00, 6.98, 6.32, 5.63, 9.07, 8.11, 6.46, 7.24, 
                     6.65, 8.46, 9.21, 6.39, 6.35, 8.17, 8.23, 6.16, 7.79, 7.80, 
                     6.20, 6.86, 7.47, 7.90, 7.43, 5.87, 7.72, 6.20, 5.79, 6.85, 
                     5.97, 7.46, 7.68, 7.11, 6.66, 7.21, 6.66, 6.17, 7.32, 6.91, 
                     9.58, 8.56, 8.03, 9.11, 6.32, 7.21, 8.30, 7.50, 8.61
                     ]
    red_numbers = [
                   3.78, 3.88, 4.01, 5.20, 4.13, 3.63, 3.13, 3.58, 4.28, 3.69, 
                   3.52, 3.35, 3.87, 4.67, 3.18, 3.09, 3.46, 4.63, 3.75, 3.98, 
                   4.49, 3.37, 3.20, 4.45, 4.43, 3.25
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
                     [8, 15, 46, 59, 67],
                     [7, 17, 30, 42, 66],
                     [18, 23, 29, 51, 69],
                     [10, 11, 12, 31, 48],
                     [43, 45, 60, 63, 64]
                     ]
    red_numbers = [6, 14, 20, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )