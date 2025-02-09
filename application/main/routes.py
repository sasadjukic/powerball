

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
              'all-time': [2814, 2872, 5760], 
              'six-months': [212, 181, 400], 
              'recent-trends': [65, 62, 130]
            }

    sets = {
            'all-time' : [727, 800, 851, 879, 789, 816, 898, 5760],
            'six-months' : [59, 56, 58, 68, 54, 49, 56, 400],
            'recent-trends' : [17, 20, 13, 26, 16, 22, 16, 130]
    }

    winning_hands = {
                     'singles': [187, 14, 3], 'pairs': [593, 41, 13], 
                     'two_pairs': [219, 12, 5], 'three_of_set': [127, 12, 5], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [75, 10, 5], 20: [103, 9, 1], 30: [97, 6, 2], 
                  40: [65, 4, 1], 50: [84, 3, 1], 60: [96, 6, 2]}
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
              'all-time': [572, 580, 1152], 
              'six-months': [34, 46, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [409, 421, 322, 1152],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [12, 8, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 7, 4, 5, 5, 9, 3, 7, 9, 3, 
                       5, 11, 5, 4, 8, 5, 6, 4, 5, 3, 
                       10, 5, 7, 6, 5, 5, 8, 3, 6, 7, 
                       9, 7, 10, 6, 7, 1, 8, 7, 6, 5, 
                       3, 2, 10, 5, 9, 6, 6, 5, 3, 4, 
                       3, 7, 6, 5, 5, 3, 9, 6, 1, 6, 
                       5, 6, 4, 8, 3, 6, 9, 3, 6
                    ]

    white_numbers_trends = [2, 1, 1, 1, 1, 6, 0, 3, 2, 0, 
                            0, 5, 1, 1, 4, 2, 4, 1, 2, 1, 
                            1, 1, 3, 0, 0, 2, 3, 1, 1, 3, 
                            3, 4, 4, 1, 3, 1, 2, 3, 2, 2, 
                            1, 1, 2, 3, 0, 1, 3, 0, 3, 2, 
                            1, 3, 3, 5, 2, 1, 3, 2, 0, 2, 
                            2, 2, 0, 2, 1, 4, 2, 0, 1
                    ]

    red_numbers_6 = [3, 1, 4, 2, 3, 2, 3, 2, 6, 2, 
                     1, 2, 3, 6, 3, 3, 5, 2, 2, 7, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [3, 0, 1, 1, 1, 1, 2, 1, 2, 0, 
                          0, 1, 0, 3, 0, 0, 2, 2, 0, 2, 
                          0, 0, 1, 2, 0, 1
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
                     7.76, 7.65, 8.03, 6.89, 6.26, 7.42, 6.56, 6.83, 7.14, 6.82, 
                     7.64, 8.36, 5.07, 6.16, 6.95, 7.24, 6.83, 6.65, 7.33, 7.20, 
                     8.71, 6.97, 7.89, 6.84, 6.54, 5.78, 8.48, 7.61, 6.54, 7.17, 
                     7.51, 8.31, 8.52, 5.65, 6.57, 8.69, 7.97, 6.91, 8.28, 7.87, 
                     6.96, 6.80, 6.61, 7.93, 7.62, 5.72, 8.21, 5.99, 5.62, 6.97, 
                     6.30, 7.27, 7.90, 6.79, 7.05, 8.17, 6.92, 6.39, 8.15, 6.24, 
                     9.24, 8.54, 8.55, 8.26, 5.87, 7.13, 7.44, 7.27, 8.49
                     ]
    red_numbers = [
                   3.87, 3.20, 3.83, 5.11, 4.35, 3.71, 3.46, 3.49, 4.38, 3.66, 
                   3.69, 3.11, 3.67, 4.70, 3.02, 3.45, 3.29, 4.38, 3.52, 3.91, 
                   4.49, 3.39, 3.24, 4.63, 3.99, 4.47
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
                     [1, 32, 47, 52, 66], 
                     [25, 35, 40, 45, 57], 
                     [6, 11, 12, 19, 61], 
                     [15, 19, 34, 40, 67], 
                     [1, 24, 43, 49, 69]
                     ]
    red_numbers = [6, 8, 10, 18, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )