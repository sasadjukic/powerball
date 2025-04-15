

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
              'all-time': [2882, 2943, 5900],
              'six-months': [201, 193, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [745, 819, 877, 892, 812, 840, 915, 5900],
            'six-months' : [53, 56, 62, 57, 58, 60, 54, 400],
            'recent-trends' : [17, 17, 24, 11, 20, 24, 17, 130]
    }

    winning_hands = {
                     'singles': [193, 12, 6], 'pairs': [609, 45, 15], 
                     'two_pairs': [224, 13, 4], 'three_of_set': [128, 9, 1], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 11, 2], 20: [106, 10, 3], 30: [99, 5, 2], 
                  40: [68, 6, 3], 50: [85, 4, 1], 60: [98, 6, 2]
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
              'all-time': [589, 591, 1180], 
              'six-months': [41, 39, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [421, 431, 328, 1180],
            'six-months' : [31, 28, 21, 80],
            'recent-trends' : [11, 9, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 5, 7, 5, 11, 5, 5, 4, 2, 
                       6, 10, 5, 3, 5, 7, 8, 7, 3, 7, 
                       8, 5, 10, 4, 4, 4, 6, 7, 7, 7, 
                       5, 7, 7, 4, 6, 5, 5, 5, 6, 7, 
                       5, 1, 6, 9, 8, 4, 6, 5, 7, 6, 
                       4, 8, 7, 7, 6, 4, 8, 7, 3, 8, 
                       6, 8, 4, 8, 3, 6, 7, 1, 3
                    ]

    white_numbers_trends = [
                        0, 2, 2, 4, 2, 3, 3, 1, 0, 1, 
                        5, 2, 1, 0, 0, 3, 2, 3, 0, 4, 
                        3, 2, 6, 1, 1, 0, 0, 5, 2, 2, 
                        0, 0, 1, 1, 1, 3, 1, 1, 1, 2, 
                        2, 0, 0, 4, 2, 2, 3, 2, 3, 3, 
                        1, 4, 3, 2, 3, 2, 2, 1, 3, 3, 
                        1, 3, 2, 2, 2, 1, 1, 1, 1
                    ]

    red_numbers_6 = [
                     6, 3, 2, 3, 3, 4, 2, 2, 6, 1, 
                     1, 5, 3, 5, 4, 2, 3, 3, 1, 7, 
                     1, 2, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          3, 2, 0, 1, 1, 2, 0, 0, 2, 1, 
                          0, 3, 1, 1, 2, 0, 0, 0, 1, 4, 
                          0, 0, 0, 0, 2, 0
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
                     6.59, 7.64, 7.94, 6.86, 6.24, 8.13, 6.33, 6.92, 7.13, 6.63, 
                     7.01, 7.80, 5.26, 6.23, 6.82, 7.37, 7.15, 6.78, 7.05, 7.86, 
                     9.63, 6.47, 8.36, 7.43, 5.97, 5.98, 8.60, 7.83, 6.24, 7.25, 
                     6.74, 8.71, 8.55, 5.77, 6.48, 8.82, 7.84, 6.91, 7.98, 7.01, 
                     6.79, 6.74, 6.44, 7.88, 7.34, 6.07, 8.03, 6.26, 5.41, 7.09, 
                     6.48, 7.39, 8.17, 7.12, 7.39, 7.01, 7.62, 6.76, 7.94, 6.58, 
                     9.29, 8.27, 8.28, 8.09, 6.40, 7.29, 7.36, 7.27, 8.93
                     ]
    red_numbers = [
                   4.26, 3.40, 4.10, 5.28, 4.39, 3.43, 3.68, 3.31, 4.23, 3.65, 
                   3.34, 2.98, 3.80, 4.15, 3.12, 3.12, 3.44, 4.69, 3.31, 4.15, 
                   4.88, 3.19, 3.43, 4.20, 4.20, 4.27
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
                     [24, 48, 49, 52, 68],
                     [17, 20, 21, 36, 59],
                     [13, 15, 22, 30, 41],
                     [3, 29, 42, 63, 67],
                     [10, 14, 56, 62, 66]
                     ]
    red_numbers = [6, 14, 19, 21, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )