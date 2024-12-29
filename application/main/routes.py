

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
              'all-time': [2771, 2827, 5670], 
              'six-months': [208, 181, 395], 
              'recent-trends': [68, 59, 130]
            }

    sets = {
            'all-time' : [714, 788, 843, 859, 777, 804, 885, 5670],
            'six-months' : [54, 50, 61, 69, 55, 52, 54, 395],
            'recent-trends' : [16, 18, 22, 19, 17, 21, 17, 130]
    }

    winning_hands = {
                     'singles': [184, 12, 2], 'pairs': [585, 40, 15], 
                     'two_pairs': [215, 16, 3], 'three_of_set': [124, 10, 5], 
                     'full_house': [16, 1, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [72, 2, 0], 10: [73, 9, 5], 20: [102, 9, 4], 30: [96, 7, 1], 
                  40: [65, 4, 2], 50: [83, 3, 2], 60: [94, 6, 1]}
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
              'all-time': [564, 570, 1134], 
              'six-months': [32, 47, 79], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [401, 416, 317, 1134],
            'six-months' : [22, 28, 29, 79],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [9, 7, 4, 4, 6, 5, 4, 4, 11, 3, 
                       7, 9, 6, 3, 6, 4, 4, 5, 3, 3, 
                       10, 6, 6, 7, 6, 6, 9, 2, 6, 7, 
                       12, 6, 12, 6, 6, 1, 8, 4, 7, 7, 
                       2, 4, 8, 6, 11, 6, 4, 5, 2, 4, 
                       5, 6, 3, 4, 7, 3, 10, 7, 3, 5, 
                       6, 4, 5, 8, 2, 4, 8, 4, 8
                    ]

    white_numbers_trends = [4, 0, 2, 1, 1, 4, 1, 0, 3, 1, 
                            1, 4, 4, 0, 2, 1, 3, 2, 0, 1, 
                            3, 3, 2, 3, 2, 3, 2, 1, 2, 3, 
                            3, 1, 3, 2, 3, 0, 2, 1, 1, 2, 
                            1, 1, 3, 3, 3, 1, 0, 2, 1, 2, 
                            2, 3, 1, 2, 2, 1, 3, 5, 0, 2, 
                            4, 2, 2, 2, 0, 1, 3, 0, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 2, 1, 3, 1, 5, 2, 
                     1, 3, 4, 3, 3, 4, 5, 1, 2, 8, 
                     5, 7, 1, 1, 4, 3
                    ]

    red_numbers_trends = [2, 1, 1, 1, 1, 0, 1, 1, 2, 0, 
                          0, 2, 2, 0, 0, 2, 1, 1, 0, 1, 
                          1, 2, 0, 1, 2, 1
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
                     7.55, 7.11, 7.57, 6.87, 6.46, 7.53, 6.43, 6.21, 6.87, 7.39, 
                     7.17, 7.64, 5.46, 6.46, 6.89, 6.98, 7.07, 6.39, 7.47, 7.03, 
                     8.92, 7.51, 8.18, 7.35, 6.71, 6.12, 8.74, 7.71, 6.44, 7.20, 
                     6.56, 9.09, 8.37, 6.07, 6.41, 7.75, 8.21, 7.04, 8.28, 7.39, 
                     6.64, 7.36, 6.96, 7.41, 8.18, 6.02, 7.45, 6.10, 5.57, 6.76, 
                     6.42, 7.31, 7.85, 6.94, 6.81, 7.18, 6.89, 6.88, 7.65, 6.29, 
                     9.92, 8.38, 8.93, 8.43, 6.27, 6.97, 7.59, 7.33, 8.91
                     ]
    red_numbers = [
                   3.36, 3.21, 4.03, 5.12, 4.39, 3.42, 3.68, 3.43, 3.95, 3.38, 
                   4.18, 3.21, 3.92, 4.42, 3.30, 3.20, 3.38, 4.82, 3.68, 3.54, 
                   4.80, 3.62, 3.29, 4.55, 4.35, 3.77
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
                     [17, 36, 47, 64, 69], 
                     [3, 8, 21, 43, 54], 
                     [6, 12, 33, 38, 67], 
                     [16, 24, 27, 44, 59], 
                     [19, 30, 45, 56, 61]
                     ]
    red_numbers = [6, 15, 25, 9, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )