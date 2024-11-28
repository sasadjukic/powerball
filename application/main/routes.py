

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

        # if user number is greater or equall to 70, then flash error
        if number >= 70:
            flash('Invalid Input')
            return redirect(url_for('search'))

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
              'all-time': [2737, 2798, 5605], 
              'six-months': [201, 194, 400], 
              'recent-trends': [69, 60, 130]
            }

    sets = {
            'all-time' : [705, 780, 832, 849, 770, 791, 878, 5605],
            'six-months' : [57, 47, 53, 74, 56, 55, 58, 400],
            'recent-trends' : [17, 20, 19, 19, 20, 14, 21, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 6], 'pairs': [578, 45, 16], 
                     'two_pairs': [212, 14, 1], 'three_of_set': [121, 7, 2], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 1], 10: [70, 6, 4], 20: [101, 8, 5], 30: [95, 8, 2], 
                  40: [64, 4, 3], 50: [82, 7, 1], 60: [94, 7, 2]}
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
              'all-time': [557, 564, 1121], 
              'six-months': [34, 46, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [397, 411, 313, 1121],
            'six-months' : [26, 26, 28, 80],
            'recent-trends' : [8, 9, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [6, 7, 4, 7, 8, 4, 4, 6, 11, 4, 
                       7, 7, 5, 3, 5, 4, 3, 4, 5, 3, 
                       9, 5, 4, 6, 5, 4, 9, 2, 6, 8, 
                       11, 7, 11, 7, 5, 5, 7, 6, 7, 6, 
                       2, 3, 7, 6, 12, 6, 5, 7, 2, 4, 
                       4, 6, 5, 5, 5, 6, 7, 8, 5, 6, 
                       5, 6, 4, 9, 2, 5, 6, 5, 10
                    ]

    white_numbers_trends = [3, 3, 1, 1, 2, 2, 2, 1, 2, 1, 
                            2, 4, 3, 2, 1, 2, 1, 3, 1, 2, 
                            4, 2, 0, 2, 3, 1, 3, 0, 2, 4, 
                            2, 3, 2, 2, 1, 0, 2, 1, 2, 2, 
                            2, 0, 5, 2, 4, 2, 0, 3, 0, 1, 
                            1, 3, 2, 0, 0, 1, 2, 4, 0, 3, 
                            1, 3, 2, 4, 1, 2, 3, 0, 2
                    ]

    red_numbers_6 = [1, 2, 3, 2, 2, 1, 4, 3, 8, 2, 
                     1, 3, 2, 3, 4, 5, 4, 0, 2, 7, 
                     8, 6, 1, 0, 3, 3
                    ]

    red_numbers_trends = [0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 
                          1, 1, 0, 1, 2, 2, 1, 0, 0, 2, 
                          2, 2, 0, 0, 2, 1
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
                     6.98, 7.52, 8.27, 6.71, 6.51, 6.99, 6.36, 6.76, 7.11, 7.32, 
                     6.71, 8.13, 5.52, 6.25, 6.91, 7.33, 7.04, 7.17, 7.59, 7.41, 
                     9.76, 7.18, 8.12, 6.72, 6.62, 6.19, 8.71, 7.59, 6.02, 6.96, 
                     6.29, 8.78, 8.32, 6.15, 6.51, 8.69, 8.30, 7.19, 8.56, 7.13, 
                     6.43, 6.64, 6.38, 7.66, 7.89, 5.82, 8.38, 6.56, 5.46, 6.19, 
                     5.72, 7.24, 7.87, 7.13, 7.08, 6.95, 7.04, 6.98, 8.08, 6.91, 
                     8.81, 8.40, 8.12, 8.54, 6.29, 7.22, 7.93, 7.29, 8.61
                     ]
    red_numbers = [
                   3.67, 3.44, 3.51, 5.01, 4.13, 3.46, 3.85, 3.61, 4.50, 3.62, 
                   3.81, 3.15, 3.48, 4.12, 3.19, 2.92, 3.24, 4.54, 3.55, 3.73, 
                   4.62, 3.80, 3.40, 4.85, 4.68, 4.12
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
                     [7, 14, 31, 51, 63], 
                     [16, 24, 34, 37, 52], 
                     [2, 21, 27, 45, 48], 
                     [11, 32, 50, 68, 69], 
                     [6, 41, 42, 57, 59]
                     ]
    red_numbers = [12, 9, 16, 25, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )