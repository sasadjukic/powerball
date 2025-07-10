

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
              'all-time': [2973, 3032, 6085],
              'six-months': [194, 199, 400],
              'recent-trends': [65, 61, 130]
            }

    sets = {
            'all-time' : [770, 842, 907, 918, 840, 868, 940, 6085],
            'six-months' : [54, 52, 62, 54, 62, 62, 54, 400],
            'recent-trends' : [18, 15, 22, 19, 17, 22, 17, 130]
    }

    winning_hands = {
                     'singles': [199, 14, 6], 'pairs': [627, 41, 11], 
                     'two_pairs': [231, 16, 7], 'three_of_set': [132, 7, 2], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 2], 20: [110, 8, 2], 30: [101, 5, 1], 
                  40: [72, 7, 2], 50: [88, 4, 2], 60: [99, 5, 1]
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
              'all-time': [605, 612, 1217],
              'six-months': [40, 40, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [431, 441, 345, 1217],
            'six-months' : [29, 25, 26, 80],
            'recent-trends' : [7, 7, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 6, 5, 9, 7, 7, 7, 4, 3, 3, 
                       5, 7, 5, 4, 5, 8, 7, 6, 2, 7, 
                       7, 2, 14, 3, 5, 1, 4, 10, 9, 5, 
                       4, 6, 5, 6, 7, 6, 8, 3, 4, 8, 
                       4, 4, 8, 9, 6, 4, 7, 5, 7, 7, 
                       4, 12, 8, 5, 5, 4, 5, 5, 7, 8, 
                       5, 8, 5, 5, 5, 6, 4, 2, 6
                    ]

    white_numbers_trends = [
                        3, 1, 1, 3, 3, 1, 3, 0, 3, 1, 
                        0, 2, 4, 1, 1, 2, 2, 1, 1, 0, 
                        2, 0, 5, 1, 3, 0, 2, 4, 5, 1, 
                        2, 2, 2, 3, 4, 1, 4, 0, 0, 2, 
                        1, 2, 4, 3, 1, 0, 1, 3, 0, 3, 
                        1, 7, 2, 1, 1, 1, 1, 3, 2, 2, 
                        3, 3, 1, 2, 1, 0, 2, 1, 2
                    ]

    red_numbers_6 = [
                     4, 4, 2, 3, 4, 4, 1, 2, 5, 1, 
                     3, 4, 3, 4, 3, 0, 1, 2, 4, 8, 
                     3, 1, 1, 5, 8, 0
                    ]

    red_numbers_trends = [
                          0, 1, 1, 1, 2, 1, 0, 1, 0, 0, 
                          3, 1, 1, 0, 1, 0, 0, 0, 1, 1, 
                          3, 1, 0, 2, 5, 0
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
                     7.35, 6.79, 7.89, 6.98, 6.02, 7.67, 6.40, 7.02, 6.99, 6.84, 
                     7.54, 8.23, 5.03, 6.08, 6.85, 7.33, 7.31, 6.82, 7.27, 7.62, 
                     8.89, 7.32, 8.91, 7.37, 6.32, 5.71, 8.07, 7.77, 6.41, 7.14, 
                     7.06, 8.72, 8.25, 6.07, 6.79, 8.47, 7.97, 6.43, 7.76, 7.47, 
                     6.73, 6.52, 7.12, 8.22, 7.88, 5.92, 7.64, 6.89, 5.99, 7.08, 
                     6.13, 7.65, 7.03, 7.35, 6.82, 7.22, 6.65, 6.92, 7.78, 6.50, 
                     9.28, 8.23, 8.78, 8.41, 6.40, 6.48, 7.62, 6.76, 9.07
                     ]
    red_numbers = [
                   3.57, 3.50, 3.50, 4.72, 4.41, 3.39, 3.66, 3.59, 4.40, 3.46, 
                   3.76, 3.50, 3.67, 4.28, 3.28, 3.32, 3.14, 4.27, 3.57, 4.52, 
                   4.70, 3.25, 3.29, 4.71, 4.66, 3.88
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
                     [1, 14, 24, 27, 30],
                     [5, 10, 12, 49, 61],
                     [13, 21, 34, 47, 48],
                     [6, 25, 37, 40, 44],
                     [17, 18, 31, 54, 55]
                     ]
    red_numbers = [10, 11, 14, 16, 17]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )