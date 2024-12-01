

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
              'all-time': [2740, 2780, 5610], 
              'six-months': [200, 190, 395], 
              'recent-trends': [69, 60, 130]
            }

    sets = {
            'all-time' : [706, 780, 834, 850, 770, 791, 879, 5610],
            'six-months' : [57, 46, 55, 72, 55, 53, 57, 395],
            'recent-trends' : [17, 19, 21, 19, 19, 14, 21, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 5], 'pairs': [579, 44, 17], 
                     'two_pairs': [212, 14, 1], 'three_of_set': [121, 7, 2], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 1], 10: [70, 6, 3], 20: [102, 9, 6], 30: [95, 7, 2], 
                  40: [64, 4, 2], 50: [82, 7, 1], 60: [94, 6, 2]}
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
              'all-time': [557, 565, 1122], 
              'six-months': [33, 46, 79], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [397, 411, 314, 1122],
            'six-months' : [25, 26, 28, 79],
            'recent-trends' : [8, 9, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [6, 7, 4, 8, 8, 4, 4, 6, 10, 4, 
                       7, 7, 5, 3, 5, 4, 2, 4, 5, 3, 
                       9, 5, 4, 7, 5, 4, 9, 2, 7, 7, 
                       11, 7, 11, 6, 5, 5, 7, 6, 7, 6, 
                       2, 3, 7, 6, 12, 6, 5, 7, 1, 4, 
                       4, 6, 5, 5, 5, 5, 7, 8, 4, 5, 
                       4, 6, 5, 9, 2, 5, 6, 5, 10
                    ]

    white_numbers_trends = [3, 3, 1, 2, 2, 2, 2, 1, 1, 1, 
                            1, 4, 3, 2, 1, 2, 1, 3, 1, 2, 
                            4, 2, 0, 3, 3, 1, 3, 0, 3, 3, 
                            2, 3, 2, 2, 1, 0, 2, 1, 3, 2, 
                            2, 0, 4, 2, 4, 2, 0, 3, 0, 1, 
                            1, 3, 2, 0, 0, 1, 2, 4, 0, 3, 
                            1, 3, 3, 4, 1, 2, 3, 0, 1
                    ]

    red_numbers_6 = [1, 2, 3, 2, 2, 1, 4, 3, 7, 2, 
                     1, 3, 2, 3, 4, 5, 4, 0, 2, 7, 
                     7, 6, 1, 0, 4, 3
                    ]

    red_numbers_trends = [0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 
                          1, 1, 0, 1, 2, 2, 1, 0, 0, 1, 
                          2, 2, 0, 0, 3, 1
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
                     7.17, 7.90, 8.04, 6.23, 6.58, 7.58, 6.43, 6.66, 7.12, 6.75, 
                     7.27, 7.87, 5.50, 6.52, 6.84, 7.47, 6.85, 7.05, 7.31, 7.45, 
                     8.95, 7.21, 8.18, 7.21, 6.39, 6.08, 9.02, 7.56, 5.80, 6.83, 
                     7.48, 8.27, 8.74, 6.42, 5.94, 9.03, 7.49, 7.21, 8.20, 6.60, 
                     6.47, 6.96, 6.55, 7.82, 7.54, 6.49, 7.88, 6.19, 5.77, 7.04, 
                     6.50, 6.65, 7.64, 7.29, 6.79, 6.88, 6.88, 6.41, 7.98, 6.34, 
                     9.17, 8.15, 9.42, 8.96, 6.12, 7.11, 7.61, 7.37, 8.82
                     ]
    red_numbers = [
                   3.69, 3.68, 3.81, 5.17, 4.20, 3.19, 3.25, 3.64, 4.32, 3.77, 
                   3.80, 3.10, 3.73, 4.31, 3.42, 3.36, 3.35, 4.77, 3.88, 3.72, 
                   4.54, 3.64, 3.59, 4.14, 3.99, 3.94
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
                     [17, 37, 44, 55, 64], 
                     [3, 9, 40, 53, 59], 
                     [6, 12, 24, 45, 47], 
                     [10, 22, 33, 38, 67], 
                     [27, 56, 59, 61, 68]
                     ]
    red_numbers = [2, 15, 20, 6, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )