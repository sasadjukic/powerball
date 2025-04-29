

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
              'all-time': [2894, 2961, 5930],
              'six-months': [196, 198, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [748, 823, 881, 895, 819, 843, 921, 5930],
            'six-months' : [51, 54, 62, 56, 62, 61, 54, 400],
            'recent-trends' : [16, 17, 24, 13, 22, 20, 18, 130]
    }

    winning_hands = {
                     'singles': [193, 11, 5], 'pairs': [612, 44, 14], 
                     'two_pairs': [224, 12, 3], 'three_of_set': [130, 11, 3], 
                     'full_house': [17, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 10, 1], 20: [106, 9, 2], 30: [100, 5, 3], 
                  40: [69, 7, 4], 50: [86, 5, 1], 60: [98, 5, 1]
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
              'all-time': [591, 595, 1186],
              'six-months': [41, 39, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [423, 432, 331, 1186],
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
                       6, 4, 5, 7, 4, 11, 5, 5, 4, 2, 
                       6, 11, 5, 2, 5, 6, 8, 7, 2, 7, 
                       8, 5, 10, 5, 4, 5, 5, 7, 6, 6, 
                       5, 7, 7, 4, 6, 5, 6, 5, 5, 7, 
                       4, 2, 8, 9, 8, 5, 6, 5, 8, 6, 
                       6, 8, 7, 7, 6, 5, 6, 7, 3, 8, 
                       6, 7, 6, 5, 3, 7, 6, 1, 5
                    ]

    white_numbers_trends = [
                        1, 2, 1, 4, 2, 2, 3, 1, 0, 0, 
                        4, 3, 1, 1, 1, 2, 2, 3, 0, 5, 
                        2, 1, 6, 2, 2, 1, 0, 3, 2, 2, 
                        0, 0, 2, 0, 1, 3, 2, 1, 2, 2, 
                        2, 1, 2, 4, 2, 3, 2, 1, 3, 2, 
                        3, 3, 3, 1, 2, 2, 1, 1, 2, 2, 
                        1, 2, 4, 2, 1, 2, 1, 0, 3
                    ]

    red_numbers_6 = [
                     7, 4, 2, 3, 3, 3, 2, 2, 6, 1, 
                     0, 5, 3, 4, 3, 2, 3, 3, 2, 7, 
                     1, 2, 1, 4, 5, 2
                    ]

    red_numbers_trends = [
                          4, 3, 0, 1, 1, 2, 0, 0, 1, 1, 
                          0, 2, 1, 0, 1, 0, 0, 0, 2, 3, 
                          0, 0, 0, 1, 3, 0
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
                     7.57, 7.40, 7.81, 6.86, 6.58, 7.72, 6.65, 5.79, 7.09, 6.69, 
                     7.50, 7.92, 5.38, 6.34, 6.65, 7.37, 7.38, 7.22, 7.66, 7.61, 
                     9.22, 7.37, 8.39, 7.09, 5.88, 6.06, 8.29, 8.08, 6.01, 7.34, 
                     6.63, 8.05, 8.22, 5.78, 6.03, 7.75, 8.24, 7.03, 8.18, 7.64, 
                     6.75, 6.60, 7.47, 7.73, 7.35, 6.25, 7.92, 6.49, 6.04, 7.26, 
                     6.17, 7.39, 7.99, 7.46, 7.08, 6.93, 7.14, 7.11, 7.78, 6.77, 
                     8.38, 7.73, 8.43, 8.27, 6.26, 7.52, 7.70, 7.39, 8.17
                     ]
    red_numbers = [
                   3.94, 3.56, 3.60, 4.81, 4.19, 3.95, 3.91, 3.40, 4.05, 3.58, 
                   3.34, 3.50, 3.86, 4.23, 3.11, 2.91, 3.27, 4.75, 4.04, 3.96, 
                   4.50, 3.41, 3.38, 4.49, 4.48, 3.78
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
                     [1, 12, 20, 36, 67],
                     [17, 23, 33, 55, 62],
                     [27, 40, 58, 59, 68],
                     [2, 10, 41, 49, 69],
                     [7, 31, 35, 60, 61]
                     ]
    red_numbers = [11, 15, 16, 18, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )