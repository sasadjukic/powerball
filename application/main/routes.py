

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
              'all-time': [2835, 2896, 5805], 
              'six-months': [205, 189, 400], 
              'recent-trends': [61, 67, 130]
            }

    sets = {
            'all-time' : [733, 806, 858, 883, 799, 823, 903, 5805],
            'six-months' : [55, 58, 55, 66, 59, 54, 53, 400],
            'recent-trends' : [18, 17, 15, 21, 22, 19, 18, 130]
    }

    winning_hands = {
                     'singles': [188, 14, 4], 'pairs': [599, 44, 14], 
                     'two_pairs': [221, 11, 6], 'three_of_set': [127, 10, 2], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [77, 12, 4], 20: [104, 9, 2], 30: [97, 6, 1], 
                  40: [66, 5, 1], 50: [85, 4, 2], 60: [97, 5, 3]}
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
              'all-time': [575, 586, 1161], 
              'six-months': [32, 48, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [411, 425, 325, 1161],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [9, 9, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 7, 5, 5, 4, 9, 4, 6, 6, 4, 
                       6, 10, 5, 4, 6, 6, 7, 6, 4, 3, 
                       11, 5, 5, 4, 5, 5, 7, 4, 6, 7, 
                       7, 8, 8, 7, 6, 3, 8, 6, 6, 5, 
                       3, 2, 9, 7, 10, 5, 6, 6, 6, 5, 
                       3, 8, 6, 6, 6, 4, 8, 6, 2, 8, 
                       5, 6, 4, 7, 4, 6, 7, 2, 4
                    ]

    white_numbers_trends = [1, 3, 2, 2, 1, 5, 1, 3, 0, 1, 
                            1, 3, 0, 1, 2, 3, 3, 2, 1, 1, 
                            2, 1, 3, 0, 0, 1, 2, 3, 2, 1, 
                            2, 5, 1, 2, 2, 3, 2, 2, 1, 2, 
                            1, 0, 3, 3, 2, 1, 4, 1, 5, 2, 
                            0, 2, 3, 4, 2, 2, 2, 1, 1, 4, 
                            1, 3, 0, 1, 2, 4, 1, 1, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 3, 2, 3, 2, 5, 1, 
                     1, 3, 2, 6, 3, 3, 4, 3, 2, 9, 
                     3, 5, 1, 3, 4, 2
                    ]

    red_numbers_trends = [0, 0, 1, 1, 1, 1, 1, 1, 3, 0, 
                          0, 1, 0, 4, 1, 0, 1, 2, 0, 3, 
                          0, 0, 1, 2, 1, 1
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
                     7.42, 7.84, 7.10, 6.22, 6.62, 7.52, 6.49, 6.48, 7.01, 6.71, 
                     7.05, 8.14, 5.11, 6.82, 7.26, 7.54, 6.82, 7.07, 7.45, 7.46, 
                     9.40, 6.87, 8.14, 7.37, 6.08, 5.95, 9.13, 7.43, 6.07, 7.54, 
                     7.00, 8.73, 9.06, 5.92, 6.31, 8.29, 8.20, 6.69, 8.25, 6.93, 
                     6.64, 6.82, 6.57, 7.74, 7.76, 6.38, 8.09, 6.59, 6.14, 7.22, 
                     6.28, 6.87, 7.30, 7.13, 7.01, 7.19, 7.15, 6.48, 7.59, 6.61, 
                     9.15, 8.18, 8.61, 8.15, 6.11, 7.34, 7.46, 7.50, 8.45
                     ]
    red_numbers = [
                   3.52, 3.21, 3.82, 5.40, 4.15, 3.78, 3.67, 3.30, 4.51, 3.66, 
                   3.59, 3.27, 3.76, 4.93, 3.14, 3.18, 3.50, 4.38, 3.66, 3.72, 
                   4.75, 3.15, 3.24, 4.50, 4.10, 4.11
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
                     [20, 30, 32, 37, 54], 
                     [4, 16, 24, 45, 64], 
                     [9, 24, 49, 59, 66], 
                     [29, 34, 52, 61, 62], 
                     [1, 7, 18, 40, 56]
                     ]
    red_numbers = [2, 7, 13, 17, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )