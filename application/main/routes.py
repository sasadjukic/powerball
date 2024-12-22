

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
              'all-time': [2764, 2820, 5655], 
              'six-months': [209, 181, 395], 
              'recent-trends': [70, 58, 130]
            }

    sets = {
            'all-time' : [713, 787, 840, 856, 775, 800, 884, 5655],
            'six-months' : [59, 50, 58, 69, 54, 50, 55, 395],
            'recent-trends' : [17, 19, 23, 18, 18, 18, 17, 130]
    }

    winning_hands = {
                     'singles': [184, 12, 2], 'pairs': [584, 42, 17], 
                     'two_pairs': [214, 15, 2], 'three_of_set': [123, 9, 4], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 0], 10: [73, 9, 5], 20: [102, 9, 6], 30: [96, 7, 1], 
                  40: [64, 3, 2], 50: [83, 3, 2], 60: [94, 6, 1]}
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
              'all-time': [562, 569, 1131], 
              'six-months': [32, 47, 79], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [400, 414, 317, 1131],
            'six-months' : [23, 26, 30, 79],
            'recent-trends' : [9, 8, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 7, 4, 6, 8, 5, 4, 4, 12, 3, 
                       7, 9, 6, 3, 6, 4, 4, 5, 3, 3, 
                       10, 5, 6, 7, 6, 5, 8, 2, 6, 6, 
                       11, 7, 12, 6, 5, 3, 8, 4, 7, 7, 
                       2, 3, 8, 5, 11, 6, 5, 5, 2, 4, 
                       4, 6, 4, 3, 6, 4, 9, 7, 3, 5, 
                       6, 5, 5, 7, 2, 4, 8, 4, 9
                    ]

    white_numbers_trends = [4, 1, 2, 1, 1, 3, 1, 1, 3, 1, 
                            1, 5, 4, 0, 2, 1, 3, 2, 0, 1, 
                            4, 2, 2, 3, 2, 2, 3, 1, 3, 2, 
                            2, 2, 3, 2, 2, 0, 2, 1, 2, 3, 
                            1, 0, 3, 2, 4, 1, 0, 3, 1, 2, 
                            2, 3, 1, 1, 1, 1, 2, 5, 0, 2, 
                            4, 2, 2, 1, 0, 1, 4, 0, 1
                    ]

    red_numbers_6 = [3, 1, 3, 2, 2, 1, 4, 2, 5, 2, 
                     1, 2, 4, 3, 3, 4, 5, 0, 2, 8, 
                     6, 7, 1, 1, 4, 3
                    ]

    red_numbers_trends = [2, 1, 0, 1, 1, 0, 1, 1, 2, 0, 
                          0, 1, 2, 0, 1, 2, 2, 0, 0, 2, 
                          1, 2, 0, 1, 2, 1
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
                     7.29, 7.01, 8.02, 6.44, 6.41, 7.62, 7.08, 6.36, 6.94, 7.17, 
                     7.16, 7.84, 5.23, 6.17, 7.07, 6.81, 7.22, 7.13, 7.41, 7.24, 
                     9.34, 7.05, 8.62, 7.63, 6.91, 6.08, 9.06, 7.61, 6.26, 7.23, 
                     6.95, 8.25, 8.68, 6.38, 6.22, 8.47, 8.15, 6.88, 8.59, 6.97, 
                     6.56, 6.55, 7.61, 7.45, 8.01, 5.84, 7.84, 6.18, 5.41, 7.02, 
                     6.27, 6.53, 7.52, 6.67, 6.79, 6.93, 7.30, 6.58, 8.09, 6.35, 
                     9.32, 8.14, 8.66, 8.91, 5.87, 7.44, 7.71, 7.09, 8.41
                     ]
    red_numbers = [
                   3.85, 3.42, 3.94, 5.00, 3.90, 3.69, 3.52, 4.05, 3.97, 3.66, 
                   3.83, 3.18, 3.66, 4.31, 2.97, 3.57, 3.05, 4.52, 3.63, 3.80, 
                   4.99, 3.57, 3.56, 4.41, 4.01, 3.94
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
                     [22, 30, 46, 53, 69], 
                     [8, 11, 33, 36, 44], 
                     [27, 45, 56, 57, 62], 
                     [4, 14, 19, 61, 67], 
                     [2, 21, 24, 25, 40]
                     ]
    red_numbers = [12, 15, 8, 17, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )