

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
              'all-time': [2809, 2862, 5745], 
              'six-months': [212, 181, 400], 
              'recent-trends': [66, 60, 130]
            }

    sets = {
            'all-time' : [727, 798, 849, 877, 787, 813, 894, 5745],
            'six-months' : [59, 55, 58, 69, 55, 50, 54, 400],
            'recent-trends' : [19, 18, 14, 27, 17, 22, 13, 130]
    }

    winning_hands = {
                     'singles': [185, 12, 1], 'pairs': [592, 41, 13], 
                     'two_pairs': [219, 14, 6], 'three_of_set': [127, 12, 6], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [75, 10, 5], 20: [103, 9, 1], 30: [97, 7, 2], 
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
              'all-time': [571, 578, 1149], 
              'six-months': [35, 45, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [408, 419, 322, 1149],
            'six-months' : [26, 28, 26, 80],
            'recent-trends' : [11, 7, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 7, 4, 5, 5, 9, 3, 7, 9, 3, 
                       5, 10, 6, 4, 8, 5, 6, 4, 4, 3, 
                       10, 5, 7, 6, 5, 5, 7, 3, 7, 6, 
                       9, 7, 11, 7, 7, 1, 8, 7, 6, 6, 
                       3, 3, 10, 5, 9, 6, 5, 5, 3, 4, 
                       4, 7, 6, 5, 5, 3, 8, 7, 1, 5, 
                       6, 4, 4, 8, 3, 6, 9, 3, 6
                    ]

    white_numbers_trends = [4, 1, 1, 1, 1, 6, 0, 3, 2, 0, 
                            0, 4, 1, 1, 4, 2, 4, 1, 1, 1, 
                            1, 1, 3, 0, 1, 2, 2, 2, 1, 2, 
                            4, 4, 4, 1, 4, 1, 2, 3, 2, 3, 
                            1, 1, 3, 2, 1, 1, 2, 0, 3, 1, 
                            2, 3, 3, 4, 3, 1, 3, 2, 0, 0, 
                            3, 0, 0, 2, 1, 4, 2, 0, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 3, 2, 4, 2, 5, 2, 
                     1, 3, 3, 5, 3, 3, 4, 2, 2, 8, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [3, 0, 1, 1, 1, 1, 2, 1, 1, 0, 
                          0, 1, 1, 2, 0, 0, 1, 2, 0, 2, 
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
                     6.94, 7.17, 7.42, 6.22, 6.26, 7.91, 6.88, 6.50, 7.62, 7.03, 
                     6.57, 7.76, 5.27, 6.50, 7.52, 7.22, 6.80, 6.99, 7.68, 7.54, 
                     9.66, 7.01, 8.63, 7.27, 6.49, 6.44, 9.13, 7.38, 6.26, 7.35, 
                     6.98, 8.09, 8.81, 6.32, 6.15, 8.20, 8.19, 7.24, 8.21, 7.28, 
                     6.87, 6.80, 6.44, 7.57, 7.47, 6.18, 7.71, 6.24, 5.31, 6.82, 
                     6.19, 6.55, 8.16, 6.82, 6.96, 6.92, 6.73, 7.21, 7.23, 6.44, 
                     9.66, 7.61, 8.99, 8.55, 6.28, 7.52, 7.78, 7.29, 8.81
                     ]
    red_numbers = [
                   3.78, 3.52, 3.38, 4.89, 4.03, 3.79, 3.82, 3.71, 4.27, 4.12, 
                   3.45, 2.82, 3.84, 4.52, 3.11, 3.18, 3.46, 4.69, 4.02, 3.72, 
                   4.73, 3.36, 2.98, 4.81, 4.07, 3.93
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
                     [15, 27, 47, 59, 62], 
                     [7, 31, 42, 44, 54], 
                     [5, 21, 36, 39, 65], 
                     [8, 11, 16, 53, 58], 
                     [4, 28, 66, 67, 69]
                     ]
    red_numbers = [6, 10, 13, 19, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )