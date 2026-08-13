

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
              'all-time': [3385, 3464, 6940],
              'six-months': [179, 217, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [884, 965, 1024, 1030, 963, 1003, 1071, 6940],
            'six-months' : [52, 58, 47, 51, 65, 71, 56, 400],
            'recent-trends' : [22, 18, 16, 13, 21, 24, 16, 130]
    }

    winning_hands = {
                     'singles': [233, 17, 6], 'pairs': [720, 41, 11], 
                     'two_pairs': [258, 13, 6], 'three_of_set': [145, 7, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 4], 10: [93, 7, 1], 20: [120, 4, 0], 30: [107, 1, 0], 
                  40: [92, 10, 3], 50: [106, 7, 2], 60: [116, 7, 1]
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
              'all-time': [689, 699, 1388],
              'six-months': [46, 34, 80], 
              'recent-trends': [17, 9, 26]
            }

    sets = {
            'all-time' : [494, 500, 394, 1388],
            'six-months' : [32, 26, 22, 80],
            'recent-trends' : [13, 9, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 7, 5, 10, 6, 3, 6, 5, 
                       4, 4, 5, 9, 1, 8, 9, 8, 5, 5, 
                       6, 4, 3, 6, 4, 4, 5, 6, 4, 9, 
                       5, 3, 3, 2, 4, 10, 6, 7, 2, 4, 
                       7, 9, 6, 7, 3, 5, 9, 10, 5, 9, 
                       3, 10, 5, 6, 7, 9, 7, 6, 9, 7, 
                       5, 3, 7, 12, 7, 5, 4, 3, 3
                    ]

    white_numbers_trends = [
                        0, 3, 3, 3, 3, 4, 1, 2, 3, 2, 
                        0, 1, 1, 5, 0, 3, 4, 1, 1, 2, 
                        2, 1, 0, 1, 2, 4, 1, 1, 2, 3, 
                        0, 0, 0, 0, 1, 3, 2, 3, 1, 2, 
                        2, 1, 1, 4, 2, 2, 1, 5, 1, 5, 
                        0, 0, 3, 3, 3, 1, 2, 2, 5, 2, 
                        2, 1, 2, 1, 1, 2, 2, 1, 2
                    ]

    red_numbers_6 = [
                     6, 4, 6, 2, 5, 5, 2, 1, 1, 3, 
                     2, 5, 4, 4, 4, 1, 1, 2, 0, 5, 
                     2, 1, 2, 4, 4, 4
                    ]

    red_numbers_trends = [
                          1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 
                          1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
                          0, 0, 1, 0, 2, 0
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
                     6.79, 7.57, 7.76, 6.87, 6.54, 7.36, 6.96, 6.72, 6.77, 6.64, 
                     7.64, 7.69, 5.24, 6.60, 7.25, 8.15, 6.85, 7.19, 6.77, 6.77, 
                     7.77, 6.63, 8.21, 7.33, 6.49, 5.51, 8.56, 8.18, 6.79, 6.98, 
                     6.96, 8.42, 8.03, 5.75, 6.74, 8.48, 7.89, 6.94, 7.71, 7.89, 
                     6.47, 6.97, 7.11, 7.97, 7.45, 6.15, 7.68, 6.35, 6.05, 7.05, 
                     6.47, 8.37, 7.88, 6.99, 6.44, 6.68, 6.68, 6.68, 8.13, 7.13, 
                     8.69, 7.85, 8.20, 9.22, 6.75, 7.43, 7.81, 7.18, 8.78
                     ]
    red_numbers = [
                   3.78, 3.47, 4.24, 4.83, 4.53, 3.85, 3.58, 3.05, 3.77, 3.37, 
                   3.39, 3.32, 3.57, 4.73, 3.44, 2.83, 3.52, 4.44, 3.86, 4.49, 
                   4.51, 3.37, 3.59, 4.28, 4.32, 3.87
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
                     [21, 33, 37, 39, 48],
                     [33, 43, 53, 59, 68],
                     [16, 40, 49, 51, 65],
                     [12, 39, 46, 48, 63],
                     [9, 28, 32, 33, 43]
                     ]
    red_numbers = [2, 9, 13, 24, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )