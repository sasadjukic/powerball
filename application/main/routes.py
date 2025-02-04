

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
              'all-time': [2810, 2866, 5750], 
              'six-months': [211, 182, 400], 
              'recent-trends': [63, 63, 130]
            }

    sets = {
            'all-time' : [727, 799, 849, 878, 788, 814, 895, 5750],
            'six-months' : [59, 56, 57, 68, 56, 49, 55, 400],
            'recent-trends' : [18, 19, 11, 28, 18, 23, 13, 130]
    }

    winning_hands = {
                     'singles': [186, 13, 2], 'pairs': [592, 41, 13], 
                     'two_pairs': [219, 13, 6], 'three_of_set': [127, 12, 5], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [75, 10, 5], 20: [103, 9, 1], 30: [97, 6, 2], 
                  40: [65, 4, 1], 50: [84, 3, 2], 60: [95, 6, 1]}
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
              'all-time': [571, 579, 1150], 
              'six-months': [34, 46, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [408, 420, 322, 1150],
            'six-months' : [25, 29, 26, 80],
            'recent-trends' : [11, 7, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 7, 4, 5, 5, 9, 3, 7, 9, 3, 
                       5, 11, 6, 4, 8, 5, 6, 4, 4, 3, 
                       10, 5, 6, 6, 5, 5, 7, 3, 7, 6, 
                       9, 7, 11, 6, 7, 1, 8, 7, 6, 6, 
                       3, 3, 10, 5, 9, 6, 6, 5, 3, 3, 
                       4, 7, 6, 6, 5, 3, 8, 6, 1, 6, 
                       6, 4, 4, 8, 3, 6, 9, 3, 6
                    ]

    white_numbers_trends = [3, 1, 1, 1, 1, 6, 0, 3, 2, 0, 
                            0, 5, 1, 1, 4, 2, 4, 1, 1, 1, 
                            1, 1, 2, 0, 0, 2, 2, 1, 1, 2, 
                            4, 4, 4, 1, 4, 1, 3, 3, 2, 3, 
                            1, 1, 3, 2, 1, 1, 3, 0, 3, 1, 
                            2, 3, 3, 5, 3, 1, 3, 2, 0, 1, 
                            2, 0, 0, 2, 1, 4, 2, 0, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 3, 2, 3, 2, 5, 2, 
                     1, 3, 3, 5, 3, 3, 5, 2, 2, 8, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [3, 0, 1, 1, 1, 1, 2, 1, 1, 0, 
                          0, 1, 0, 2, 0, 0, 2, 2, 0, 2, 
                          0, 1, 1, 3, 0, 1
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
                     7.23, 6.93, 7.46, 6.32, 6.45, 7.49, 6.72, 6.75, 7.24, 6.78, 
                     6.84, 7.89, 5.46, 6.61, 6.62, 6.86, 7.07, 6.50, 7.48, 7.18, 
                     9.43, 7.02, 8.02, 6.70, 6.20, 5.57, 9.12, 7.55, 6.44, 6.89, 
                     7.39, 9.17, 8.51, 5.95, 6.56, 8.65, 8.35, 7.85, 8.60, 7.43, 
                     6.77, 6.67, 6.78, 7.90, 7.56, 6.53, 7.85, 6.22, 5.70, 7.20, 
                     5.86, 6.96, 7.86, 6.99, 6.72, 7.08, 7.37, 6.93, 7.33, 6.35, 
                     9.07, 8.20, 8.54, 8.17, 6.11, 7.49, 7.73, 7.37, 9.41
                     ]
    red_numbers = [
                   3.69, 3.41, 4.04, 5.27, 4.01, 4.02, 3.47, 3.78, 4.21, 3.41, 
                   3.34, 3.08, 3.76, 4.72, 3.35, 3.23, 3.38, 4.55, 3.61, 3.77, 
                   4.48, 3.43, 3.2, 4.78, 4.01, 4.00
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
                     [6, 15, 21, 28, 65], 
                     [11, 27, 31, 49, 59], 
                     [16, 36, 39, 42, 62], 
                     [2, 44, 50, 51, 67], 
                     [1, 23, 48, 54, 66]
                     ]
    red_numbers = [5, 10, 16, 23, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )