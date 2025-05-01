

# *****Time Filtered Search*****
# This will show top 10 winning red numbers in last 6 months
from application.data.main_data import powerball_6_months
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def recent_red_winners():
    # Top 10 Red Balls in last 6 months
    red_balls_6 = powerball_6_months['Red Ball'].value_counts().head(10)

    red_numbers = red_balls_6.index.tolist()
    red_numbers[:] = [str(x) for x in red_numbers]
    red_values = red_balls_6.values.tolist()

    red_numbers.reverse()
    red_values.reverse()
    color = '#6C0345'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'
    numbers_color = '#FFC470'

    # create matplotlib bar chart
    fig, ax = plt.subplots()

    ax.barh(
        red_numbers,
        red_values,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Frequency')
    plt.ylabel('Powerball')
    plt.title('Top 10 Powerball (Red) Numbers in Last 6 Months')

    for index, value in enumerate(red_values):
        plt.text(
            value, 
            index, 
            str(value),
            position = (value - 0.25, index - 0.1),
            color = numbers_color
            )

    # Convert chart to base64 for embedding in HTML
    import io
    import base64

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    return chart_data