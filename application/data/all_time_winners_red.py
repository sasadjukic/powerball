
# Display top ten winning Red Numbers of ALL TIME
from application.data.main_data import powerball
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def all_time_red_winners():
    # Top 10 Red Numbers of ALL TIME
    red_numbers = powerball['Red Ball'].value_counts().head(10)

    # Convert red numbers index(keys) to list to use with matplotlib
    r_numbers = red_numbers.index.tolist()
    # Modify list in place to get string elements instead of integers
    r_numbers[:] = [str(x) for x in r_numbers]
    # Convert red numbers values to list to use with matplotlib
    r_values = red_numbers.values.tolist()

    r_numbers.reverse()
    r_values.reverse()
    color = '#6C0345'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'
    numbers_color = '#FFC470'

    # Display red numbers with matplotlib
    fig, ax = plt.subplots()

    ax.barh(
        r_numbers,
        r_values,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Number of Times Drawn', color = highlight_color)
    plt.ylabel('Powerball', color = highlight_color)
    plt.title('Top 10 Powerball (Red) Numbers of ALL TIME', color = highlight_color)

    for index, value in enumerate(r_values):
        plt.text(
            value, 
            index, 
            str(value),
            position = (value, index),
            ha = 'left',
            va = 'center',
            color = tick_color
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