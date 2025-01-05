

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
              'all-time': [2779, 2833, 5685], 
              'six-months': [209, 179, 395], 
              'recent-trends': [69, 57, 130]
            }

    sets = {
            'all-time' : [716, 790, 845, 864, 778, 806, 886, 5685],
            'six-months' : [53, 52, 61, 71, 56, 49, 53, 395],
            'recent-trends' : [17, 17, 22, 23, 14, 20, 17, 130]
    }

    winning_hands = {
                     'singles': [185, 13, 2], 'pairs': [586, 40, 14], 
                     'two_pairs': [215, 14, 3], 'three_of_set': [125, 11, 6], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 2, 0], 10: [73, 9, 5], 20: [102, 9, 3], 30: [96, 7, 1], 
                  40: [65, 4, 1], 50: [84, 3, 3], 60: [94, 6, 1]}
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
              'all-time': [565, 572, 1137], 
              'six-months': [32, 47, 79], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [402, 416, 319, 1137],
            'six-months' : [22, 28, 29, 79],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 6, 4, 4, 5, 6, 4, 4, 11, 3, 
                       7, 10, 6, 3, 6, 4, 4, 5, 4, 3, 
                       10, 6, 6, 7, 6, 5, 9, 3, 6, 7, 
                       12, 6, 12, 6, 7, 1, 8, 5, 7, 7, 
                       2, 4, 9, 6, 11, 6, 4, 5, 2, 4, 
                       4, 6, 3, 4, 5, 4, 9, 7, 3, 5, 
                       5, 4, 5, 8, 2, 5, 8, 4, 7
                    ]

    white_numbers_trends = [4, 0, 2, 1, 1, 4, 1, 0, 4, 0, 
                            1, 5, 3, 0, 2, 1, 3, 1, 1, 1, 
                            3, 2, 2, 3, 2, 4, 2, 2, 1, 3, 
                            3, 2, 3, 2, 4, 0, 2, 2, 2, 2, 
                            1, 1, 3, 3, 2, 1, 0, 0, 1, 2, 
                            2, 3, 0, 3, 2, 2, 3, 3, 0, 2, 
                            3, 2, 2, 2, 0, 2, 3, 0, 1
                    ]

    red_numbers_6 = [4, 1, 4, 2, 2, 1, 3, 1, 4, 2, 
                     1, 3, 4, 3, 3, 4, 5, 1, 2, 8, 
                     5, 6, 1, 2, 3, 4
                    ]

    red_numbers_trends = [3, 0, 1, 1, 1, 0, 1, 1, 2, 0, 
                          0, 2, 2, 0, 0, 2, 1, 1, 0, 1, 
                          0, 1, 0, 2, 2, 2
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
                     7.05, 7.79, 7.76, 6.45, 6.38, 7.75, 6.52, 6.44, 7.20, 7.36, 
                     6.81, 7.62, 5.32, 6.30, 7.26, 7.41, 7.21, 7.09, 7.22, 7.70, 
                     9.50, 7.08, 8.52, 6.78, 6.73, 5.88, 8.84, 7.62, 6.39, 7.00, 
                     7.42, 8.62, 8.73, 5.53, 6.45, 8.21, 7.19, 7.18, 8.72, 7.04, 
                     6.48, 6.63, 7.11, 8.10, 7.50, 5.77, 8.10, 6.48, 5.27, 6.81, 
                     5.91, 6.87, 7.53, 7.29, 6.27, 7.72, 7.33, 6.76, 7.77, 6.44, 
                     9.91, 7.81, 8.38, 8.66, 6.36, 7.46, 7.48, 7.31, 8.42
                     ]
    red_numbers = [
                   3.75, 3.17, 3.93, 5.02, 4.37, 3.69, 3.53, 3.61, 3.98, 3.69, 
                   3.44, 3.22, 3.87, 4.28, 3.15, 2.92, 3.35, 4.56, 3.80, 4.24, 
                   4.96, 3.64, 3.25, 4.28, 4.14, 4.16
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
                     [11, 37, 41, 59, 68], 
                     [2, 8, 31, 36, 65], 
                     [17, 21, 47, 48, 51], 
                     [19, 26, 55, 61, 69], 
                     [1, 20, 24, 30, 42]
                     ]
    red_numbers = [4, 10, 15, 17, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )