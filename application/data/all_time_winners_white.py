
# *****Time Filtered Search*****
# This will show top 10 winning numbers white numbers in last 6 months
from application.data.main_data import powerball_exploded
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def all_time_white_winners():
    # Top 10 White Numbers of ALL TIME
    white_numbers = powerball_exploded['Winning Numbers'].value_counts().head(10)

    # convert white numbers index(keys) to list to use with matplotlib
    w_numbers = white_numbers.index.tolist()
    # modify list in place to get string elements instead of integers
    w_numbers[:] = [str(x) for x in w_numbers]
    # convert white numbers values to list to use with matplotlib
    w_values = white_numbers.values.tolist()

    w_numbers.reverse()
    w_values.reverse()
    color = '#FFC470'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'

    # display white numbers with matplotlib
    fig, ax = plt.subplots()

    ax.barh(
        w_numbers,
        w_values,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Frequency', color=highlight_color)
    plt.ylabel('White Numbers', color=highlight_color)
    plt.title('Top 10 White Numbers of ALL TIME', color=highlight_color)

    for index, value in enumerate(w_values):
        plt.text(
            value, 
            index, 
            str(value),
            position = (value - 5, index - 0.1),
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