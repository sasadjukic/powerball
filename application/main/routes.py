

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
              'all-time': [3060, 3116, 6260],
              'six-months': [196, 195, 400],
              'recent-trends': [65, 64, 130]
            }

    sets = {
            'all-time' : [793, 869, 930, 941, 869, 885, 973, 6260],
            'six-months' : [53, 54, 60, 52, 64, 51, 66, 400],
            'recent-trends' : [15, 21, 18, 16, 21, 13, 26, 130]
    }

    winning_hands = {
                     'singles': [205, 16, 3], 'pairs': [645, 40, 13], 
                     'two_pairs': [237, 13, 6], 'three_of_set': [137, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [82, 4, 1], 20: [114, 9, 4], 30: [102, 3, 0], 
                  40: [77, 11, 4], 50: [90, 5, 2], 60: [103, 6, 2]
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
              'all-time': [620, 632, 1252],
              'six-months': [37, 43, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [446, 450, 356, 1252],
            'six-months' : [30, 21, 29, 80],
            'recent-trends' : [12, 8, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 7, 9, 5, 3, 8, 6, 5, 3, 
                       5, 6, 4, 6, 9, 9, 3, 5, 4, 4, 
                       5, 3, 12, 5, 6, 2, 5, 9, 9, 5, 
                       6, 4, 7, 7, 9, 3, 8, 1, 2, 8, 
                       5, 8, 9, 8, 8, 5, 2, 6, 5, 7, 
                       5, 9, 10, 3, 2, 2, 3, 3, 7, 5, 
                       10, 10, 5, 10, 6, 5, 5, 2, 8
                    ]

    white_numbers_trends = [
                        1, 1, 4, 1, 0, 2, 2, 2, 2, 1, 
                        3, 1, 0, 3, 5, 4, 0, 2, 2, 0, 
                        0, 2, 4, 2, 1, 1, 3, 2, 3, 1, 
                        3, 2, 2, 3, 1, 1, 2, 1, 0, 4, 
                        2, 3, 1, 2, 3, 2, 1, 0, 3, 3, 
                        1, 0, 6, 1, 0, 0, 0, 0, 2, 2, 
                        5, 4, 1, 5, 3, 2, 1, 1, 2
                    ]

    red_numbers_6 = [
                     5, 7, 2, 5, 5, 1, 0, 2, 3, 1, 
                     3, 1, 2, 1, 2, 1, 2, 2, 6, 5, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          2, 2, 0, 3, 3, 0, 0, 0, 2, 0, 
                          0, 0, 0, 1, 1, 1, 2, 1, 2, 1, 
                          1, 2, 1, 0, 1, 0
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
                     6.58, 7.36, 6.98, 6.85, 6.69, 7.94, 6.51, 6.43, 7.06, 6.89, 
                     7.66, 7.96, 5.26, 6.20, 7.07, 7.41, 7.26, 6.52, 7.86, 7.39, 
                     8.97, 6.72, 8.81, 7.25, 6.02, 5.73, 8.31, 8.35, 6.48, 7.46, 
                     7.04, 8.05, 8.94, 5.86, 6.97, 8.36, 8.65, 6.75, 7.39, 7.38, 
                     6.94, 7.06, 7.18, 8.11, 7.55, 6.09, 7.86, 6.24, 5.42, 7.39, 
                     6.33, 7.65, 8.27, 7.04, 6.48, 6.60, 7.04, 6.56, 7.86, 6.28, 
                     9.41, 8.28, 8.00, 8.34, 6.36, 7.06, 7.87, 6.87, 8.49
                     ]
    red_numbers = [
                   3.94, 3.61, 3.68, 4.85, 4.83, 3.62, 3.03, 3.45, 4.35, 3.44, 
                   3.59, 3.15, 3.56, 4.52, 3.25, 3.03, 3.20, 4.51, 3.45, 4.21, 
                   4.62, 3.29, 3.51, 4.96, 4.51, 3.84
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
                     [1, 3, 9, 49, 50],
                     [8, 46, 57, 59, 64],
                     [22, 23, 30, 32, 65],
                     [13, 15, 37, 68, 69],
                     [10, 11, 33, 61, 67]
                     ]
    red_numbers = [1, 6, 14, 16, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )