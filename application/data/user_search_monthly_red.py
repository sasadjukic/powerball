
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def red_monthly_winners(n: int, monthly_winners: dict[int, int]):

    l_months = ['January', 'February', 'March', 
                'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 
                'November', 'December']

    months = list(monthly_winners.keys())
    months[:] = [m for m in l_months]
    winners = list(monthly_winners.values())

    color = '#6C0345'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'
    numbers_color = '#FFC470'

    fig, ax = plt.subplots()

    ax.barh(
        months,
        winners,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Times Drawn', color=highlight_color)
    plt.ylabel('Months', color=highlight_color)
    plt.title(f'Powerball (Red Ball) {n} per Month since October 2015', color=highlight_color)

    for index, value in enumerate(winners):
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