

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
              'all-time': [2829, 2887, 5790], 
              'six-months': [209, 185, 400], 
              'recent-trends': [64, 63, 130]
            }

    sets = {
            'all-time' : [732, 804, 856, 881, 796, 821, 900, 5790],
            'six-months' : [57, 57, 57, 67, 57, 52, 53, 400],
            'recent-trends' : [19, 17, 15, 25, 19, 20, 15, 130]
    }

    winning_hands = {
                     'singles': [188, 14, 4], 'pairs': [596, 42, 11], 
                     'two_pairs': [221, 12, 7], 'three_of_set': [127, 11, 4], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [76, 11, 3], 20: [104, 10, 2], 30: [97, 6, 1], 
                  40: [65, 4, 0], 50: [85, 4, 2], 60: [96, 4, 2]}
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
              'all-time': [575, 583, 1158], 
              'six-months': [33, 47, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [411, 424, 323, 1158],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [11, 9, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 7, 5, 6, 5, 9, 4, 6, 6, 3, 
                       5, 10, 5, 4, 7, 6, 7, 6, 4, 3, 
                       12, 5, 5, 5, 5, 5, 8, 3, 6, 7, 
                       8, 8, 9, 6, 6, 2, 8, 7, 6, 5, 
                       3, 2, 10, 6, 10, 5, 6, 5, 5, 5, 
                       3, 8, 6, 6, 5, 4, 8, 6, 1, 7, 
                       5, 5, 4, 7, 4, 6, 8, 2, 5
                    ]

    white_numbers_trends = [1, 2, 2, 2, 1, 6, 1, 3, 1, 0, 
                            0, 3, 0, 1, 3, 3, 3, 2, 2, 1, 
                            2, 1, 2, 0, 0, 2, 3, 2, 2, 2, 
                            3, 5, 2, 1, 3, 2, 2, 3, 2, 2, 
                            1, 0, 3, 2, 2, 1, 4, 0, 4, 2, 
                            1, 2, 3, 5, 2, 2, 2, 1, 0, 3, 
                            1, 2, 0, 1, 2, 4, 1, 0, 1
                    ]

    red_numbers_6 = [3, 1, 5, 2, 3, 2, 3, 2, 5, 1, 
                     1, 3, 2, 5, 4, 3, 5, 3, 2, 8, 
                     3, 5, 1, 3, 3, 2
                    ]

    red_numbers_trends = [1, 0, 2, 1, 1, 1, 1, 1, 3, 0, 
                          0, 2, 0, 3, 1, 0, 1, 2, 0, 2, 
                          0, 0, 1, 2, 0, 1
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
                     7.49, 7.27, 7.59, 6.90, 6.69, 7.38, 6.26, 6.42, 7.31, 6.62, 
                     6.51, 7.85, 5.35, 6.76, 6.84, 7.19, 7.04, 6.87, 7.64, 7.05, 
                     8.51, 6.66, 8.51, 6.71, 6.52, 6.17, 9.18, 7.18, 6.40, 7.18, 
                     7.11, 8.79, 8.75, 6.13, 6.14, 7.98, 8.09, 7.46, 7.88, 7.01, 
                     6.87, 7.01, 7.00, 8.27, 7.71, 6.51, 8.30, 6.55, 5.86, 6.84, 
                     6.18, 7.56, 8.00, 7.37, 6.70, 7.62, 6.85, 6.53, 7.64, 6.53, 
                     8.93, 8.19, 8.26, 8.94, 6.08, 7.21, 7.52, 7.24, 8.34
                     ]
    red_numbers = [
                   3.17, 3.58, 3.96, 5.04, 4.38, 3.36, 3.78, 3.56, 4.39, 3.45, 
                   3.41, 3.07, 3.88, 4.42, 3.10, 3.11, 3.74, 4.34, 3.53, 4.19, 
                   4.83, 3.44, 3.83, 4.45, 3.90, 4.09
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
                     [24, 33, 37, 51, 56], 
                     [8, 10, 14, 63, 64], 
                     [3, 21, 27, 41, 48], 
                     [45, 50, 56, 65, 67], 
                     [9, 11, 16, 31, 39]
                     ]
    red_numbers = [4, 11, 15, 16, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )