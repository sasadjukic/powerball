

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
              'all-time': [2893, 2957, 5925],
              'six-months': [199, 195, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [748, 823, 880, 895, 818, 841, 920, 5925],
            'six-months' : [52, 55, 63, 57, 61, 59, 53, 400],
            'recent-trends' : [16, 17, 24, 13, 22, 19, 19, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 5], 'pairs': [611, 44, 14], 
                     'two_pairs': [224, 12, 3], 'three_of_set': [130, 11, 3], 
                     'full_house': [17, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 10, 1], 20: [106, 9, 2], 30: [100, 5, 3], 
                  40: [69, 7, 4], 50: [85, 4, 0], 60: [98, 5, 2]
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
              'all-time': [591, 594, 1185],
              'six-months': [41, 39, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [423, 432, 330, 1185],
            'six-months' : [32, 26, 22, 80],
            'recent-trends' : [12, 7, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 5, 7, 4, 11, 5, 5, 4, 2, 
                       6, 11, 5, 2, 6, 6, 8, 7, 2, 7, 
                       8, 5, 10, 5, 4, 4, 6, 7, 7, 6, 
                       5, 7, 7, 4, 6, 5, 6, 5, 6, 7, 
                       4, 2, 7, 9, 8, 5, 6, 5, 8, 6, 
                       5, 8, 7, 7, 6, 4, 6, 7, 3, 7, 
                       6, 7, 6, 5, 3, 7, 6, 1, 5
                    ]

    white_numbers_trends = [
                        1, 2, 1, 4, 2, 2, 3, 1, 0, 0, 
                        4, 3, 1, 1, 1, 2, 2, 3, 0, 5, 
                        2, 1, 6, 2, 2, 0, 0, 4, 2, 2, 
                        0, 0, 2, 0, 1, 3, 2, 1, 2, 2, 
                        2, 1, 1, 4, 2, 3, 2, 2, 3, 2, 
                        2, 3, 3, 1, 3, 1, 1, 1, 2, 2, 
                        1, 3, 4, 2, 1, 2, 1, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 3, 3, 2, 2, 6, 1, 
                     0, 5, 3, 4, 3, 2, 3, 3, 2, 8, 
                     1, 2, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          4, 3, 0, 1, 1, 2, 0, 0, 1, 1, 
                          0, 2, 1, 0, 1, 0, 0, 0, 2, 4, 
                          0, 0, 0, 0, 3, 0
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
                     7.25, 8.10, 7.25, 7.28, 6.67, 8.37, 6.69, 6.60, 6.79, 7.03, 
                     7.42, 7.69, 5.11, 6.38, 6.72, 6.90, 7.15, 7.13, 7.36, 7.01, 
                     9.42, 7.19, 8.77, 7.24, 6.22, 6.10, 8.15, 8.04, 6.36, 7.52, 
                     6.84, 8.59, 8.97, 5.81, 6.41, 8.72, 7.91, 6.98, 7.94, 6.86, 
                     6.46, 7.14, 6.63, 7.09, 7.25, 6.29, 8.31, 6.18, 5.72, 7.21, 
                     5.85, 7.73, 7.79, 6.86, 6.98, 6.86, 7.04, 6.66, 7.74, 6.95, 
                     8.80, 8.01, 8.65, 8.01, 6.33, 7.36, 7.56, 7.94, 7.66
                     ]
    red_numbers = [
                   4.12, 3.21, 3.96, 4.67, 4.25, 3.69, 3.59, 3.65, 4.34, 3.84, 
                   3.34, 3.42, 3.63, 4.52, 2.82, 3.14, 3.43, 4.44, 3.81, 4.52, 
                   4.63, 3.43, 3.27, 4.75, 3.56, 3.97
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
                     [14, 27, 37, 44, 61],
                     [10, 20, 41, 51, 60],
                     [7, 52, 62, 63, 68],
                     [1, 11, 30, 33, 35],
                     [21, 22, 50, 55, 56]
                     ]
    red_numbers = [11, 16, 18, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )