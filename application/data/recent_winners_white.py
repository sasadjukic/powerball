

# *****Time Filtered Search*****
# This will show top 10 winning numbers white numbers in last 6 months
from application.data.main_data import powerball_explode_6
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def recent_white_winners():
    # Top 10 White balls in last 6 months
    white_balls_6 = powerball_explode_6['Winning Numbers'].value_counts().head(10)

    white_numbers = white_balls_6.index.tolist()
    white_numbers[:] = [str(x) for x in white_numbers]
    white_values = white_balls_6.values.tolist()

    white_numbers.reverse()
    white_values.reverse()
    color = '#FFC470'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'

    # create matplotlib bar chart
    fig, ax = plt.subplots()

    ax.barh(
        white_numbers,
        white_values,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Frequency', color = highlight_color)
    plt.ylabel('White Numbers', color = highlight_color)
    plt.title('Top 10 White Numbers in Last 6 Months', color = highlight_color)

    for index, value in enumerate(white_values):
        plt.text(
            value, 
            index, 
            str(value),
            position = (value - 0.75, index - 0.1),
            color = highlight_color
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