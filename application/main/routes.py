

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
              'all-time': [2884, 2946, 5905],
              'six-months': [200, 194, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [745, 819, 879, 892, 815, 840, 915, 5905],
            'six-months' : [52, 55, 63, 57, 60, 59, 54, 400],
            'recent-trends' : [16, 16, 26, 11, 22, 22, 17, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 6], 'pairs': [609, 45, 14], 
                     'two_pairs': [224, 13, 4], 'three_of_set': [128, 9, 1], 
                     'full_house': [17, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 11, 2], 20: [106, 10, 3], 30: [99, 5, 2], 
                  40: [68, 6, 3], 50: [85, 4, 0], 60: [98, 6, 2]
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
              'all-time': [589, 592, 1181], 
              'six-months': [40, 40, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [421, 432, 328, 1181],
            'six-months' : [30, 29, 21, 80],
            'recent-trends' : [11, 9, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 5, 7, 4, 11, 5, 5, 4, 2, 
                       6, 10, 5, 2, 5, 7, 8, 7, 3, 7, 
                       8, 5, 10, 5, 4, 4, 6, 7, 7, 7, 
                       5, 7, 7, 4, 6, 5, 5, 5, 6, 7, 
                       4, 2, 7, 9, 8, 4, 6, 5, 8, 6, 
                       4, 8, 7, 7, 6, 4, 7, 7, 3, 8, 
                       6, 8, 4, 8, 3, 6, 7, 1, 3
                    ]

    white_numbers_trends = [
                        0, 2, 1, 4, 2, 3, 3, 1, 0, 1, 
                        5, 2, 1, 0, 0, 2, 2, 3, 0, 5, 
                        3, 2, 6, 2, 1, 0, 0, 5, 2, 2, 
                        0, 0, 1, 1, 1, 3, 1, 1, 1, 2, 
                        2, 1, 1, 4, 1, 2, 3, 2, 4, 3, 
                        1, 4, 3, 1, 3, 1, 2, 1, 3, 3, 
                        1, 3, 2, 2, 2, 1, 1, 1, 1
                    ]

    red_numbers_6 = [
                     6, 3, 2, 3, 3, 3, 2, 2, 6, 1, 
                     1, 5, 3, 5, 4, 2, 3, 3, 2, 7, 
                     1, 2, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          3, 2, 0, 1, 1, 2, 0, 0, 2, 1, 
                          0, 2, 1, 1, 2, 0, 0, 0, 2, 4, 
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
                     7.18, 7.46, 7.74, 6.22, 6.42, 7.99, 6.67, 6.24, 6.66, 6.66, 
                     7.38, 7.46, 5.55, 6.46, 6.81, 7.41, 6.93, 6.38, 7.03, 8.01, 
                     9.24, 6.61, 8.13, 6.92, 6.56, 5.72, 8.21, 7.75, 6.45, 6.91, 
                     6.74, 8.85, 8.83, 6.61, 6.25, 8.19, 8.25, 7.16, 8.32, 6.97, 
                     6.63, 6.97, 6.83, 7.74, 7.42, 5.88, 8.00, 6.45, 5.77, 7.07, 
                     6.03, 7.13, 8.35, 7.64, 6.66, 6.99, 6.82, 7.01, 7.97, 6.71, 
                     9.29, 8.35, 9.09, 8.34, 6.29, 7.15, 7.82, 7.46, 8.81
                     ]
    red_numbers = [
                   4.01, 3.52, 4.03, 4.79, 3.92, 3.75, 3.45, 3.83, 4.02, 3.97, 
                   3.53, 3.40, 4.08, 4.44, 3.42, 2.87, 3.32, 4.86, 3.79, 3.79, 
                   4.35, 3.29, 3.10, 4.04, 4.27, 4.16
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
                     [24, 28, 36, 41, 63],
                     [11, 12, 33, 39, 66],
                     [5, 6, 14, 43, 69],
                     [17, 36, 49, 57, 68],
                     [15, 19, 21, 38, 62]
                     ]
    red_numbers = [3, 11, 17, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )