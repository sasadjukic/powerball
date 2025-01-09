

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
              'all-time': [2783, 2839, 5695], 
              'six-months': [211, 183, 400], 
              'recent-trends': [69, 57, 130]
            }

    sets = {
            'all-time' : [717, 791, 846, 867, 780, 806, 888, 5695],
            'six-months' : [53, 53, 62, 71, 57, 49, 55, 400],
            'recent-trends' : [18, 15, 22, 25, 16, 17, 17, 130]
    }

    winning_hands = {
                     'singles': [185, 13, 2], 'pairs': [588, 42, 14], 
                     'two_pairs': [215, 14, 3], 'three_of_set': [125, 11, 6], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 2, 0], 10: [73, 9, 4], 20: [102, 9, 3], 30: [97, 8, 2], 
                  40: [65, 4, 1], 50: [84, 3, 2], 60: [95, 7, 2]}
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
              'all-time': [565, 574, 1139], 
              'six-months': [32, 48, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [402, 417, 320, 1139],
            'six-months' : [22, 29, 29, 80],
            'recent-trends' : [9, 8, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 6, 4, 4, 4, 6, 4, 4, 11, 3, 
                       7, 10, 6, 3, 6, 4, 5, 5, 4, 4, 
                       10, 6, 6, 7, 6, 5, 9, 3, 6, 7, 
                       12, 5, 12, 7, 6, 2, 8, 6, 6, 7, 
                       2, 4, 10, 6, 11, 7, 4, 5, 1, 4, 
                       4, 6, 3, 4, 5, 4, 9, 7, 3, 5, 
                       5, 4, 5, 8, 2, 6, 9, 4, 7
                    ]

    white_numbers_trends = [5, 0, 2, 1, 1, 4, 1, 0, 4, 0, 
                            0, 4, 3, 0, 2, 1, 3, 1, 1, 2, 
                            3, 2, 2, 2, 2, 4, 2, 2, 1, 3, 
                            3, 2, 3, 3, 4, 1, 1, 3, 2, 2, 
                            1, 1, 4, 3, 2, 2, 0, 0, 1, 1, 
                            2, 3, 0, 3, 2, 1, 3, 2, 0, 2, 
                            3, 1, 2, 2, 0, 2, 4, 0, 1
                    ]

    red_numbers_6 = [4, 1, 4, 2, 2, 1, 3, 1, 4, 2, 
                     1, 3, 4, 4, 3, 4, 5, 1, 2, 8, 
                     4, 6, 1, 3, 3, 4
                    ]

    red_numbers_trends = [3, 0, 1, 0, 1, 0, 1, 1, 2, 0, 
                          0, 2, 2, 1, 0, 1, 1, 1, 0, 1, 
                          0, 1, 0, 3, 2, 2
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
                     6.87, 7.50, 8.03, 6.57, 6.15, 7.63, 6.90, 6.71, 7.05, 7.00, 
                     7.11, 8.16, 5.45, 6.41, 7.17, 7.25, 7.53, 7.66, 7.52, 7.69, 
                     8.88, 7.02, 7.57, 7.25, 6.75, 5.93, 8.34, 7.20, 6.29, 7.00, 
                     7.20, 8.61, 9.02, 6.23, 6.87, 8.76, 8.22, 7.35, 8.44, 7.07, 
                     6.58, 6.91, 6.75, 7.45, 7.48, 6.45, 7.69, 6.07, 5.23, 6.55, 
                     6.19, 7.12, 7.50, 7.40, 6.78, 7.27, 7.10, 6.44, 7.49, 6.18, 
                     9.07, 7.91, 8.47, 8.88, 6.01, 6.98, 7.54, 7.62, 8.53
                     ]
    red_numbers = [
                   3.68, 3.36, 3.74, 5.07, 4.6, 3.91, 3.62, 3.47, 3.97, 3.84, 
                   3.39, 3.04, 3.92, 4.46, 3.3, 3.05, 3.25, 4.56, 3.28, 3.93, 
                   5.04, 3.45, 3.22, 4.84, 3.96, 4.05
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
                     [24, 31, 43, 59, 67], 
                     [8, 10, 16, 29, 47], 
                     [2, 37, 41, 48, 68], 
                     [23, 25, 53, 61, 62], 
                     [1, 14, 36, 50, 57]
                     ]
    red_numbers = [4, 11, 21, 9, 15]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )