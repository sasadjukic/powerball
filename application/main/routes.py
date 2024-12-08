

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
              'all-time': [2749, 2806, 5625], 
              'six-months': [205, 186, 395], 
              'recent-trends': [70, 59, 130]
            }

    sets = {
            'all-time' : [710, 780, 838, 851, 771, 793, 882, 5625],
            'six-months' : [60, 45, 57, 70, 53, 52, 58, 395],
            'recent-trends' : [18, 17, 24, 17, 18, 14, 22, 130]
    }

    winning_hands = {
                     'singles': [184, 13, 4], 'pairs': [580, 42, 16], 
                     'two_pairs': [213, 15, 2], 'three_of_set': [122, 8, 3], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 5, 0], 10: [70, 6, 3], 20: [102, 9, 6], 30: [95, 6, 1], 
                  40: [64, 3, 2], 50: [83, 7, 2], 60: [94, 6, 2]}
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
              'all-time': [559, 566, 1125], 
              'six-months': [33, 46, 79], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [397, 413, 315, 1125],
            'six-months' : [24, 26, 29, 79],
            'recent-trends' : [7, 11, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [8, 7, 5, 8, 8, 4, 4, 5, 11, 4, 
                       7, 7, 5, 3, 5, 4, 2, 4, 4, 3, 
                       9, 5, 5, 7, 6, 5, 9, 2, 6, 7, 
                       12, 7, 11, 6, 4, 4, 7, 5, 7, 6, 
                       2, 3, 8, 5, 10, 6, 5, 7, 1, 4, 
                       3, 5, 5, 4, 6, 5, 8, 8, 4, 5, 
                       6, 6, 5, 9, 2, 5, 7, 4, 9
                    ]

    white_numbers_trends = [4, 1, 2, 2, 2, 2, 2, 1, 2, 1, 
                            1, 3, 3, 2, 1, 2, 1, 2, 1, 2, 
                            3, 2, 1, 3, 4, 2, 3, 1, 3, 2, 
                            2, 3, 2, 2, 1, 0, 1, 1, 3, 2, 
                            2, 0, 4, 2, 4, 1, 0, 3, 0, 1, 
                            1, 1, 2, 0, 1, 1, 3, 4, 0, 3, 
                            3, 3, 2, 4, 0, 2, 4, 0, 1
                    ]

    red_numbers_6 = [1, 2, 3, 2, 2, 1, 4, 2, 7, 2, 
                     1, 2, 4, 3, 4, 4, 4, 0, 2, 7, 
                     7, 7, 1, 0, 4, 3
                    ]

    red_numbers_trends = [0, 1, 0, 1, 1, 1, 0, 1, 2, 1, 
                          1, 1, 2, 1, 2, 2, 1, 0, 0, 1, 
                          1, 2, 0, 0, 3, 1
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
                     7.18, 7.43, 8.11, 6.13, 6.66, 7.52, 6.55, 6.22, 6.94, 6.83, 
                     6.98, 7.99, 5.26, 6.70, 6.69, 7.63, 6.49, 6.68, 8.36, 7.63, 
                     9.29, 6.62, 8.34, 6.89, 6.69, 5.63, 8.48, 7.83, 6.25, 7.17, 
                     6.82, 8.63, 8.83, 5.96, 6.03, 9.03, 8.33, 7.07, 8.65, 7.64, 
                     6.44, 6.55, 7.03, 7.43, 7.72, 6.48, 8.19, 6.26, 5.46, 6.93, 
                     6.36, 6.81, 8.28, 7.45, 6.62, 6.55, 6.87, 7.02, 8.23, 6.54, 
                     9.04, 8.41, 8.33, 8.44, 5.95, 6.80, 7.65, 7.47, 8.53
                     ]
    red_numbers = [
                   3.61, 3.39, 3.95, 5.12, 3.67, 3.71, 3.70, 3.92, 4.62, 3.71, 
                   3.83, 3.06, 3.85, 4.29, 3.42, 3.24, 3.13, 4.63, 3.34, 3.62, 
                   4.90, 3.31, 3.54, 4.33, 4.13, 3.98
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
                     [12, 19, 31, 43, 45], 
                     [5, 27, 53, 55, 59], 
                     [8, 11, 22, 33, 40], 
                     [32, 38, 50, 64, 69], 
                     [14, 18, 41, 42, 60]
                     ]
    red_numbers = [2, 16, 23, 6, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )