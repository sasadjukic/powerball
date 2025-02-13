

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
              'all-time': [2820, 2876, 5770], 
              'six-months': [213, 181, 400], 
              'recent-trends': [67, 60, 130]
            }

    sets = {
            'all-time' : [728, 802, 853, 881, 792, 816, 898, 5770],
            'six-months' : [58, 57, 59, 68, 56, 48, 54, 400],
            'recent-trends' : [18, 19, 14, 28, 18, 18, 15, 130]
    }

    winning_hands = {
                     'singles': [187, 13, 3], 'pairs': [594, 41, 13], 
                     'two_pairs': [220, 13, 6], 'three_of_set': [127, 12, 4], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {1: [73, 3, 1], 10: [76, 11, 5], 20: [103, 9, 1], 30: [97, 6, 2], 
                  40: [65, 4, 1], 50: [84, 3, 1], 60: [96, 5, 2]}
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
              'all-time': [573, 581, 1154], 
              'six-months': [33, 47, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [410, 422, 322, 1154],
            'six-months' : [25, 30, 25, 80],
            'recent-trends' : [12, 9, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [10, 8, 4, 5, 5, 8, 3, 7, 8, 3, 
                       5, 11, 5, 4, 8, 5, 7, 5, 4, 3, 
                       11, 5, 7, 5, 5, 5, 8, 3, 7, 7, 
                       9, 8, 9, 6, 6, 2, 8, 7, 6, 5, 
                       3, 2, 11, 5, 10, 6, 5, 5, 4, 4, 
                       3, 7, 6, 5, 5, 3, 8, 6, 1, 6, 
                       5, 6, 4, 7, 3, 6, 9, 3, 5
                    ]

    white_numbers_trends = [2, 2, 1, 1, 1, 6, 0, 3, 2, 0, 
                            0, 4, 0, 1, 4, 2, 4, 2, 2, 1, 
                            2, 1, 2, 0, 0, 2, 3, 1, 2, 3, 
                            3, 5, 4, 1, 3, 2, 2, 3, 2, 2, 
                            1, 1, 3, 2, 1, 1, 3, 0, 4, 1, 
                            1, 1, 3, 4, 2, 1, 3, 2, 0, 2, 
                            2, 2, 0, 2, 1, 4, 1, 0, 1
                    ]

    red_numbers_6 = [3, 1, 5, 2, 3, 2, 3, 2, 4, 2, 
                     1, 2, 3, 6, 3, 3, 5, 3, 2, 7, 
                     3, 6, 1, 3, 3, 2
                    ]

    red_numbers_trends = [2, 0, 2, 1, 1, 1, 2, 1, 2, 0, 
                          0, 1, 0, 3, 0, 0, 2, 3, 0, 1, 
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
                     7.19, 7.53, 7.63, 6.30, 6.77, 7.49, 6.43, 7.19, 7.29, 6.64, 
                     6.74, 7.46, 5.04, 6.63, 7.29, 7.09, 7.58, 6.66, 7.60, 7.48, 
                     8.85, 6.75, 8.13, 7.04, 6.42, 6.16, 8.70, 7.62, 6.03, 7.18, 
                     7.19, 8.62, 8.45, 6.32, 6.24, 8.65, 8.74, 6.83, 8.28, 6.92, 
                     6.79, 6.90, 6.41, 7.89, 7.30, 6.00, 7.80, 6.46, 5.90, 6.97, 
                     6.22, 7.28, 8.08, 7.43, 6.86, 6.84, 7.12, 6.59, 7.26, 6.86, 
                     9.38, 8.20, 8.56, 8.73, 6.46, 7.18, 7.54, 7.57, 8.27
                     ]
    red_numbers = [
                   3.88, 3.52, 3.86, 4.88, 4.25, 3.89, 3.70, 3.62, 4.45, 3.70, 
                   3.84, 3.13, 3.85, 4.59, 3.12, 3.28, 3.26, 4.54, 3.38, 3.87, 
                   4.56, 3.63, 3.30, 4.28, 3.77, 3.85
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
                     [11, 25, 27, 37, 61], 
                     [19, 35, 42, 56, 63], 
                     [10, 14, 45, 51, 60], 
                     [2, 12, 37, 54, 67], 
                     [1, 8, 22, 29, 55]
                     ]
    red_numbers = [8, 10, 16, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )