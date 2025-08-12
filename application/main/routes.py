

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
              'all-time': [3011, 3060, 6155],
              'six-months': [198, 192, 400],
              'recent-trends': [69, 55, 130]
            }

    sets = {
            'all-time' : [783, 853, 915, 931, 851, 873, 949, 6155],
            'six-months' : [56, 53, 65, 52, 63, 58, 53, 400],
            'recent-trends' : [24, 16, 20, 19, 15, 17, 19, 130]
    }

    winning_hands = {
                     'singles': [203, 16, 8], 'pairs': [634, 42, 10], 
                     'two_pairs': [232, 13, 4], 'three_of_set': [134, 7, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [81, 6, 0], 20: [111, 8, 1], 30: [102, 5, 1], 
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
              'all-time': [611, 620, 1231],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [437, 443, 351, 1231],
            'six-months' : [29, 22, 29, 80],
            'recent-trends' : [9, 5, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 6, 4, 10, 6, 6, 9, 6, 4, 3, 
                       6, 6, 5, 4, 5, 8, 5, 8, 3, 6, 
                       8, 2, 14, 5, 6, 1, 3, 12, 8, 4, 
                       4, 3, 7, 6, 10, 7, 6, 2, 3, 7, 
                       3, 5, 10, 9, 8, 4, 4, 7, 6, 7, 
                       5, 11, 6, 4, 4, 4, 6, 4, 7, 8, 
                       5, 9, 6, 5, 5, 3, 4, 2, 6
                    ]

    white_numbers_trends = [
                        1, 2, 1, 4, 2, 3, 3, 5, 3, 0, 
                        1, 2, 1, 1, 2, 3, 1, 2, 3, 0, 
                        3, 0, 4, 2, 3, 0, 2, 5, 1, 0, 
                        2, 1, 4, 2, 6, 2, 1, 1, 0, 1, 
                        0, 2, 4, 2, 2, 1, 0, 2, 1, 3, 
                        2, 4, 1, 2, 1, 0, 1, 2, 1, 1, 
                        3, 4, 2, 2, 2, 0, 2, 0, 3
                    ]

    red_numbers_6 = [
                     4, 7, 3, 2, 3, 3, 0, 2, 5, 1, 
                     3, 4, 3, 2, 3, 0, 0, 2, 4, 8, 
                     4, 2, 1, 5, 9, 0
                    ]

    red_numbers_trends = [
                          0, 3, 1, 0, 1, 1, 0, 2, 1, 0, 
                          1, 1, 0, 1, 0, 0, 0, 1, 1, 2, 
                          2, 2, 1, 2, 3, 0
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
                     7.22, 7.73, 6.88, 6.63, 6.72, 7.39, 6.75, 6.86, 7.44, 6.69, 
                     6.79, 7.92, 5.01, 6.67, 7.36, 6.89, 7.32, 6.91, 7.13, 8.13, 
                     8.89, 6.77, 9.37, 7.16, 6.54, 6.12, 8.58, 7.82, 7.15, 6.86, 
                     6.48, 8.12, 8.54, 6.01, 6.14, 8.52, 8.15, 6.54, 8.18, 7.17, 
                     6.72, 7.04, 7.09, 7.84, 7.65, 6.40, 8.39, 6.35, 5.78, 7.48, 
                     6.56, 7.12, 7.54, 6.93, 7.03, 6.96, 7.57, 7.29, 7.27, 6.49, 
                     8.63, 7.88, 8.14, 8.35, 6.02, 7.03, 7.41, 6.82, 8.67
                     ]
    red_numbers = [
                   4.20, 3.58, 3.74, 4.83, 4.02, 3.42, 3.37, 3.40, 4.28, 3.76, 
                   3.83, 3.30, 3.83, 4.29, 3.00, 2.96, 3.40, 4.74, 3.63, 4.49, 
                   4.48, 3.37, 3.30, 4.47, 4.40, 3.91
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
                     [7, 17, 23, 39, 41],
                     [16, 20, 42, 56, 60],
                     [15, 24, 25, 35, 50],
                     [10, 18, 31, 46, 54],
                     [6, 12, 61, 63, 67]
                     ]
    red_numbers = [4, 6, 18, 19, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )