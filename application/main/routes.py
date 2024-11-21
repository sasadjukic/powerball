

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
              'all-time': [2729, 2792, 5590], 
              'six-months': [201, 194, 400], 
              'recent-trends': [70, 60, 130]
            }

    sets = {
            'all-time' : [701, 777, 832, 847, 767, 791, 875, 5590],
            'six-months' : [57, 46, 54, 75, 54, 55, 59, 400],
            'recent-trends' : [15, 20, 23, 19, 20, 15, 18, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 6], 'pairs': [576, 44, 17], 
                     'two_pairs': [212, 15, 1], 'three_of_set': [120, 7, 1], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 2], 10: [69, 6, 4], 20: [101, 8, 6], 30: [95, 9, 2], 
                  40: [64, 5, 3], 50: [82, 7, 1], 60: [93, 6, 1]}
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
              'all-time': [554, 564, 1118], 
              'six-months': [33, 47, 80], 
              'recent-trends': [8, 18, 26]
            }

    sets = {
            'all-time' : [395, 410, 313, 1118],
            'six-months' : [26, 25, 29, 80],
            'recent-trends' : [6, 9, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [6, 7, 4, 7, 8, 4, 4, 6, 11, 4, 
                       7, 6, 3, 3, 5, 5, 3, 5, 5, 3, 
                       9, 5, 4, 6, 5, 5, 9, 2, 6, 8, 
                       11, 7, 12, 6, 5, 6, 7, 6, 7, 5, 
                       2, 3, 7, 5, 11, 6, 5, 8, 2, 4, 
                       4, 6, 5, 5, 5, 6, 7, 8, 5, 5, 
                       5, 6, 3, 11, 2, 5, 6, 6, 10
                    ]

    white_numbers_trends = [2, 4, 2, 1, 1, 1, 1, 1, 2, 1, 
                            3, 3, 2, 2, 2, 2, 1, 3, 1, 2, 
                            5, 2, 0, 3, 4, 2, 3, 0, 2, 4, 
                            2, 3, 2, 1, 0, 0, 3, 1, 3, 1, 
                            2, 0, 5, 1, 5, 3, 0, 3, 0, 1, 
                            1, 4, 2, 0, 0, 1, 2, 4, 0, 2, 
                            1, 3, 1, 4, 1, 2, 2, 0, 2
                    ]

    red_numbers_6 = [1, 2, 3, 3, 2, 1, 4, 2, 8, 2, 
                     1, 2, 2, 3, 4, 5, 4, 0, 2, 7, 
                     8, 6, 1, 1, 3, 3
                    ]

    red_numbers_trends = [0, 1, 1, 1, 0, 1, 0, 0, 2, 1, 
                          1, 0, 0, 1, 2, 2, 1, 0, 1, 2, 
                          3, 3, 0, 0, 2, 1
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
                     7.18, 7.83, 7.86, 6.12, 6.18, 7.11, 6.98, 6.26, 6.72, 7.20, 
                     6.80, 7.54, 5.45, 6.72, 7.08, 7.18, 7.71, 6.92, 7.65, 7.64, 
                     8.53, 7.18, 8.58, 7.08, 6.33, 5.78, 9.34, 7.39, 6.31, 7.20, 
                     7.13, 8.21, 8.70, 6.11, 6.00, 8.25, 8.48, 7.03, 8.22, 6.62, 
                     6.93, 6.74, 6.80, 7.33, 7.49, 6.09, 7.58, 6.63, 5.56, 7.11, 
                     6.41, 6.98, 7.87, 6.47, 6.33, 7.41, 6.65, 6.84, 8.16, 6.63, 
                     9.36, 8.24, 9.17, 8.47, 6.16, 7.31, 7.67, 8.04, 8.97
                     ]
    red_numbers = [
                   3.40, 3.28, 4.06, 4.79, 4.31, 4.13, 3.59, 3.92, 4.10, 3.91, 
                   3.63, 2.92, 3.77, 4.07, 2.92, 3.21, 3.30, 4.61, 3.72, 3.99, 
                   4.57, 3.80, 3.22, 4.34, 4.15, 4.29
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
                     [12, 32, 45, 50, 60], 
                     [2, 7, 25, 53, 59], 
                     [6, 14, 16, 47, 48], 
                     [34, 37, 51, 63, 66], 
                     [5, 11, 21, 28, 41]
                     ]
    red_numbers = [2, 12, 20, 4, 16]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )