

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
              'all-time': [2732, 2794, 5595], 
              'six-months': [198, 192, 395], 
              'recent-trends': [70, 60, 130]
            }

    sets = {
            'all-time' : [701, 779, 832, 848, 768, 791, 876, 5595],
            'six-months' : [54, 46, 53, 76, 54, 55, 57, 395],
            'recent-trends' : [15, 21, 21, 19, 20, 15, 19, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 6], 'pairs': [577, 44, 17], 
                     'two_pairs': [212, 14, 1], 'three_of_set': [120, 7, 1], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 1], 10: [70, 6, 4], 20: [101, 8, 5], 30: [95, 8, 2], 
                  40: [64, 4, 3], 50: [82, 7, 1], 60: [93, 6, 1]}
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
              'all-time': [555, 564, 1119], 
              'six-months': [32, 47, 79], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [396, 410, 313, 1119],
            'six-months' : [25, 25, 29, 79],
            'recent-trends' : [7, 8, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [5, 7, 4, 7, 7, 4, 3, 6, 11, 4, 
                       7, 7, 4, 3, 5, 4, 3, 4, 5, 3, 
                       9, 5, 4, 6, 5, 4, 9, 2, 6, 8, 
                       11, 7, 12, 7, 5, 6, 7, 6, 7, 5, 
                       2, 3, 7, 6, 11, 6, 5, 7, 2, 4, 
                       4, 6, 5, 5, 5, 6, 7, 8, 5, 5, 
                       5, 6, 3, 10, 2, 5, 6, 5, 10
                    ]

    white_numbers_trends = [2, 4, 2, 1, 1, 1, 1, 1, 2, 1, 
                            3, 4, 3, 2, 1, 2, 1, 3, 1, 2, 
                            4, 2, 0, 3, 3, 2, 3, 0, 2, 4, 
                            2, 3, 2, 2, 0, 0, 2, 1, 3, 1, 
                            2, 0, 5, 2, 4, 3, 0, 3, 0, 1, 
                            1, 4, 2, 0, 0, 1, 2, 4, 0, 2, 
                            1, 3, 1, 4, 1, 2, 3, 0, 2
                    ]

    red_numbers_6 = [1, 2, 3, 2, 1, 1, 4, 3, 8, 2, 
                     1, 2, 2, 3, 4, 5, 4, 0, 2, 7, 
                     8, 6, 1, 1, 3, 3
                    ]

    red_numbers_trends = [0, 1, 1, 1, 0, 1, 0, 1, 2, 1, 
                          1, 0, 0, 1, 2, 2, 1, 0, 0, 2, 
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
                     6.70, 7.45, 7.82, 6.58, 6.45, 7.22, 7.25, 7.15, 6.81, 7.12, 
                     7.22, 7.44, 5.35, 6.41, 6.95, 7.42, 7.18, 6.98, 7.40, 7.50, 
                     8.91, 6.77, 8.30, 7.56, 6.39, 6.02, 8.65, 7.58, 6.15, 7.14, 
                     6.56, 8.37, 8.73, 6.19, 5.92, 8.52, 7.90, 6.63, 8.89, 7.22, 
                     7.17, 6.60, 6.83, 7.65, 7.48, 6.10, 8.19, 6.63, 5.29, 7.26, 
                     5.94, 6.92, 7.76, 7.01, 7.12, 7.20, 7.33, 6.62, 8.09, 5.76, 
                     9.21, 8.06, 9.11, 8.54, 6.10, 6.76, 7.77, 7.48, 9.22
                     ]
    red_numbers = [
                   3.67, 3.48, 3.65, 5.21, 4.26, 3.56, 3.38, 3.72, 4.11, 3.82, 
                   3.59, 3.01, 3.58, 5.02, 2.80, 3.41, 3.65, 4.77, 3.48, 4.01, 
                   4.75, 3.27, 3.13, 4.66, 4.07, 3.94
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
                     [13, 23, 49, 54, 68], 
                     [3, 5, 36, 52, 53], 
                     [7, 19, 45, 47, 69], 
                     [28, 31, 34, 37, 64], 
                     [8, 14, 21, 50, 58]
                     ]
    red_numbers = [1, 12, 24, 9, 18]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )