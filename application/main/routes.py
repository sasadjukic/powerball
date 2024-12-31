

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
              'all-time': [2774, 2829, 5675], 
              'six-months': [210, 179, 395], 
              'recent-trends': [68, 59, 130]
            }

    sets = {
            'all-time' : [715, 789, 843, 862, 777, 804, 885, 5675],
            'six-months' : [55, 51, 60, 72, 55, 50, 52, 395],
            'recent-trends' : [17, 18, 20, 22, 16, 20, 17, 130]
    }

    winning_hands = {
                     'singles': [184, 12, 2], 'pairs': [585, 40, 14], 
                     'two_pairs': [215, 15, 3], 'three_of_set': [125, 11, 6], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 2, 0], 10: [73, 9, 5], 20: [102, 9, 3], 30: [96, 7, 1], 
                  40: [65, 4, 2], 50: [83, 3, 2], 60: [94, 6, 1]}
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
              'all-time': [565, 570, 1135], 
              'six-months': [33, 46, 79], 
              'recent-trends': [15, 12, 26]
            }

    sets = {
            'all-time' : [402, 416, 317, 1135],
            'six-months' : [23, 28, 28, 79],
            'recent-trends' : [11, 8, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 7, 4, 4, 6, 5, 4, 4, 12, 3, 
                       7, 9, 6, 3, 6, 4, 4, 5, 4, 3, 
                       10, 6, 6, 7, 6, 5, 9, 2, 6, 7, 
                       12, 6, 13, 6, 6, 1, 8, 5, 8, 7, 
                       2, 4, 8, 6, 11, 6, 4, 5, 2, 4, 
                       4, 6, 3, 3, 7, 3, 10, 7, 3, 5, 
                       5, 4, 5, 8, 2, 4, 8, 4, 7
                    ]

    white_numbers_trends = [4, 0, 2, 1, 1, 4, 1, 0, 4, 1, 
                            1, 4, 3, 0, 2, 1, 3, 2, 1, 1, 
                            3, 2, 2, 3, 2, 3, 2, 1, 1, 3, 
                            3, 1, 4, 2, 3, 0, 2, 2, 2, 2, 
                            1, 1, 2, 3, 3, 1, 0, 2, 1, 2, 
                            2, 3, 1, 2, 2, 1, 3, 4, 0, 2, 
                            4, 2, 2, 2, 0, 1, 3, 0, 1
                    ]

    red_numbers_6 = [4, 1, 4, 2, 2, 1, 3, 1, 5, 2, 
                     1, 3, 4, 3, 3, 4, 5, 1, 2, 8, 
                     5, 7, 1, 1, 3, 3
                    ]

    red_numbers_trends = [3, 1, 1, 1, 1, 0, 1, 1, 2, 0, 
                          0, 2, 2, 0, 0, 2, 1, 1, 0, 1, 
                          1, 1, 0, 1, 2, 1
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
                     7.88, 7.48, 8.19, 6.58, 6.78, 7.41, 6.76, 6.50, 7.00, 6.68, 
                     7.17, 7.72, 5.60, 6.51, 7.02, 7.32, 7.20, 6.59, 8.06, 7.35, 
                     9.11, 6.73, 8.32, 7.02, 6.64, 5.79, 8.38, 7.97, 6.08, 6.96, 
                     6.79, 8.58, 8.58, 5.97, 6.47, 8.17, 7.45, 7.21, 9.07, 7.42, 
                     6.91, 6.64, 6.52, 7.41, 7.54, 6.02, 7.70, 6.21, 5.42, 7.03, 
                     6.42, 7.07, 7.70, 7.24, 6.34, 7.44, 7.25, 6.80, 7.34, 6.10, 
                     9.42, 8.54, 8.62, 7.96, 6.52, 6.94, 7.73, 7.85, 8.81
                     ]
    red_numbers = [
                   3.61, 3.32, 4.22, 4.96, 4.24, 3.67, 3.72, 3.45, 4.23, 3.92, 
                   3.70, 3.32, 4.07, 4.24, 2.88, 3.48, 3.52, 4.57, 3.76, 3.72, 
                   4.38, 3.03, 3.28, 4.53, 4.06, 4.12
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
                     [1, 16, 44, 52, 69], 
                     [3, 7, 33, 48, 60], 
                     [25, 28, 31, 36, 59], 
                     [37, 41, 42, 54, 61], 
                     [11, 13, 18, 19, 67]
                     ]
    red_numbers = [4, 11, 14, 19, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )