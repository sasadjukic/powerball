

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
              'all-time': [2750, 2814, 5635], 
              'six-months': [202, 188, 395], 
              'recent-trends': [66, 62, 130]
            }

    sets = {
            'all-time' : [710, 781, 838, 853, 774, 797, 882, 5635],
            'six-months' : [58, 45, 57, 70, 56, 52, 57, 395],
            'recent-trends' : [17, 17, 22, 18, 19, 16, 21, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 2], 'pairs': [580, 40, 16], 
                     'two_pairs': [214, 16, 3], 'three_of_set': [123, 9, 4], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 0], 10: [70, 6, 3], 20: [102, 9, 6], 30: [95, 6, 1], 
                  40: [64, 3, 2], 50: [83, 5, 2], 60: [94, 6, 2]}
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
              'all-time': [559, 568, 1127], 
              'six-months': [32, 47, 79], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [397, 413, 317, 1127],
            'six-months' : [23, 25, 31, 79],
            'recent-trends' : [6, 10, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [8, 7, 4, 8, 8, 4, 4, 4, 11, 3, 
                       7, 7, 6, 3, 5, 4, 2, 4, 4, 3, 
                       9, 5, 5, 7, 6, 5, 9, 2, 6, 7, 
                       12, 7, 10, 6, 5, 4, 8, 4, 7, 7, 
                       2, 3, 8, 6, 11, 6, 5, 7, 1, 5, 
                       4, 5, 5, 4, 6, 5, 8, 7, 3, 5, 
                       6, 6, 5, 8, 2, 5, 7, 4, 9
                    ]

    white_numbers_trends = [4, 1, 2, 2, 1, 2, 2, 1, 2, 1, 
                            1, 3, 4, 1, 1, 2, 1, 2, 1, 1, 
                            3, 2, 1, 3, 3, 2, 3, 1, 3, 2, 
                            2, 2, 2, 2, 2, 0, 2, 1, 3, 3, 
                            1, 0, 3, 3, 5, 1, 0, 3, 0, 2, 
                            2, 2, 1, 1, 1, 1, 2, 4, 0, 3, 
                            3, 3, 2, 4, 0, 1, 4, 0, 1
                    ]

    red_numbers_6 = [1, 2, 3, 2, 2, 1, 4, 2, 6, 2, 
                     1, 2, 4, 3, 3, 4, 4, 0, 2, 8, 
                     7, 7, 1, 1, 4, 3
                    ]

    red_numbers_trends = [0, 1, 0, 1, 1, 0, 0, 1, 2, 0, 
                          1, 1, 2, 1, 2, 2, 1, 0, 0, 2, 
                          1, 2, 0, 1, 3, 1
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
                     7.28, 7.63, 7.93, 6.98, 7.28, 7.02, 6.51, 6.41, 6.91, 6.66, 
                     7.29, 7.95, 5.49, 6.78, 7.18, 7.59, 6.48, 6.56, 7.52, 7.53, 
                     9.48, 6.69, 8.00, 7.44, 6.51, 6.32, 8.77, 7.54, 6.20, 7.42, 
                     7.04, 8.35, 8.73, 6.24, 6.57, 8.48, 8.20, 6.68, 8.49, 6.86, 
                     6.81, 6.68, 6.73, 7.79, 7.66, 6.32, 7.34, 6.83, 5.91, 7.03, 
                     6.17, 6.46, 8.12, 7.19, 6.15, 6.95, 6.80, 7.36, 7.62, 5.96, 
                     9.74, 7.85, 8.46, 8.24, 6.02, 7.09, 7.76, 7.42, 8.55
                     ]
    red_numbers = [
                   3.49, 3.35, 4.17, 5.29, 4.34, 3.64, 3.42, 3.75, 4.21, 3.87, 
                   3.74, 2.92, 4.12, 4.36, 3.20, 3.41, 3.51, 4.32, 3.18, 3.72, 
                   4.78, 3.36, 3.35, 4.37, 3.97, 4.16
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
                     [16, 27, 49, 59, 68], 
                     [6, 33, 40, 47, 55], 
                     [10, 18, 39, 65, 66], 
                     [1, 11, 21, 32, 38], 
                     [8, 24, 42, 50, 53]
                     ]
    red_numbers = [3, 10, 5, 7, 15]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )