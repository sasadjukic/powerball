

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
              'all-time': [3245, 3287, 6620],
              'six-months': [203, 193, 400],
              'recent-trends': [63, 64, 130]
            }

    sets = {
            'all-time' : [843, 918, 990, 987, 909, 949, 1024, 6620],
            'six-months' : [54, 55, 64, 51, 47, 70, 59, 400],
            'recent-trends' : [19, 14, 22, 17, 16, 25, 17, 130]
    }

    winning_hands = {
                     'singles': [218, 13, 2], 'pairs': [688, 47, 16], 
                     'two_pairs': [247, 13, 5], 'three_of_set': [139, 3, 1], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [88, 6, 2], 20: [118, 4, 2], 30: [106, 4, 1], 
                  40: [84, 9, 3], 50: [100, 12, 2], 60: [111, 8, 4]
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
              'all-time': [651, 673, 1324],
              'six-months': [34, 46, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [467, 477, 380, 1324],
            'six-months' : [24, 31, 25, 80],
            'recent-trends' : [8, 9, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 9, 4, 8, 7, 7, 8, 3, 6, 
                       5, 2, 4, 6, 5, 6, 5, 10, 6, 6, 
                       5, 5, 4, 4, 3, 5, 8, 16, 8, 6, 
                       6, 9, 5, 4, 4, 5, 4, 3, 5, 6, 
                       1, 6, 6, 4, 2, 3, 7, 6, 6, 6, 
                       9, 9, 8, 7, 4, 6, 5, 10, 6, 8, 
                       3, 6, 6, 7, 5, 9, 5, 6, 4
                    ]

    white_numbers_trends = [
                        0, 3, 2, 0, 3, 4, 2, 3, 2, 1, 
                        2, 0, 0, 2, 0, 2, 2, 3, 2, 3, 
                        2, 2, 3, 0, 1, 1, 4, 4, 2, 3, 
                        2, 0, 2, 1, 3, 3, 2, 1, 0, 3, 
                        0, 3, 1, 0, 0, 1, 3, 3, 2, 3, 
                        2, 4, 1, 3, 3, 3, 1, 5, 0, 3, 
                        1, 1, 4, 3, 2, 1, 0, 2, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 2, 4, 2, 0, 0, 3, 
                     2, 4, 1, 6, 4, 2, 2, 2, 5, 5, 
                     4, 2, 8, 3, 0, 3
                    ]

    red_numbers_trends = [
                          1, 0, 0, 1, 2, 4, 0, 0, 0, 1, 
                          1, 2, 1, 1, 1, 0, 1, 1, 0, 2, 
                          2, 0, 2, 3, 0, 0
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
                     7.35, 7.02, 7.74, 7.32, 6.11, 7.54, 6.93, 6.69, 6.92, 6.92, 
                     6.87, 7.31, 4.97, 6.20, 7.04, 7.92, 6.79, 6.87, 7.36, 6.68, 
                     9.17, 6.72, 9.10, 6.77, 6.37, 5.83, 8.59, 8.70, 6.42, 7.27, 
                     6.75, 8.35, 8.89, 5.56, 6.69, 8.58, 8.18, 6.44, 8.22, 8.04, 
                     6.37, 6.53, 6.96, 7.42, 6.93, 5.48, 7.69, 6.44, 5.78, 7.72, 
                     6.82, 7.61, 8.22, 7.22, 6.44, 6.91, 6.90, 6.94, 7.30, 6.71, 
                     9.40, 8.77, 8.32, 8.68, 6.37, 7.34, 7.47, 7.16, 8.91
                     ]
    red_numbers = [
                   4.00, 4.12, 3.82, 4.66, 4.27, 3.77, 3.36, 3.62, 4.03, 3.63, 
                   3.51, 3.28, 3.53, 4.46, 3.22, 2.80, 2.79, 4.31, 3.70, 4.37, 
                   4.82, 3.53, 3.40, 4.79, 4.49, 3.72
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
                     [1, 11, 22, 62, 66],
                     [18, 37, 50, 57, 65],
                     [24, 33, 61, 63, 64],
                     [5, 6, 20, 25, 53],
                     [2, 3, 4, 51, 69]
                     ]
    red_numbers = [2, 8, 19, 22, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )