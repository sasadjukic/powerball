
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def per_year(all_winners: list[int]) -> dict[int, int]:
    years = {}
    all_winners[:] = [year for year in all_winners if year != 2015]
    for draw in all_winners:
        if draw not in years:
            years[draw] = 1
        else:
            years[draw] += 1

    return years

def white_yearly_winners(n: int, yearly_winners: dict[int, int]):

    years = list(yearly_winners.keys())
    total = list(yearly_winners.values())

    color = '#FFC470'
    tick_color = '#DD5746'
    highlight_color = '#6C0345'

    fig, ax = plt.subplots()

    ax.bar(
        years,
        total,
        color=color,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(tick_color)
    ax.spines['bottom'].set_color(tick_color)

    plt.xticks(color = tick_color)
    plt.yticks(color = tick_color)

    plt.xlabel('Years', color=highlight_color)
    plt.ylabel('Time Drawn', color=highlight_color)
    plt.title(f'White Ball {n} per Year since 2016', color=highlight_color)

    for i in range(len(total)):
        plt.text(years[i], total[i], total[i], ha='center', va='bottom')

    # Convert chart to base64 for embedding in HTML
    import io
    import base64

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    return chart_data