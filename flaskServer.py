import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask, render_template, request
from dictWork import prepare_dict_from_csv

app = Flask(__name__)

data = prepare_dict_from_csv("CO2.csv")

def create_plot(data):

    days = list(data.keys())
    co2_levels = [float(value) for value in data.values()]
    colors = ["red" if level >= 2000 else "green" for level in co2_levels]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(days, co2_levels, label="CO2 levels", color=colors, linewidth=2.0, width=0.5)
    ax.set(xlabel="Day", ylabel="CO2 Concentration (ppm)", title="CO2 Levels Over Days")

    ax.set_xticks(days)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_ylim(min(co2_levels) - 10, max(co2_levels) + 10)

    ax.grid(True)
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode("utf-8")
    plt.close(fig)

    return plot_url


def get_co2_level(day):
    print(day)
    print(data.get(str(day)))
    temp = data.get(str(day))
    if temp == None:
        return None
    else:
        return temp


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/day", methods=["GET", "POST"])
def day():
    co2_level = None  # Ensure the variable exists in all cases

    if request.method == "POST":
        try:
            day = int(request.form["day"])
            co2_level = get_co2_level(day)

            if co2_level is not None:
                co2_level = int(
                    co2_level
                )  # Convert to integer before passing to template
                return render_template("day.html", day=day, co2_level=co2_level)
            else:
                return render_template(
                    "day.html", error="Diena netika atrasta.", co2_level=co2_level
                )
        except ValueError:
            return render_template(
                "day.html",
                error="Lūdzu, ievadiet derīgu dienas numuru.",
                co2_level=co2_level,
            )

    return render_template("day.html", co2_level=co2_level)


@app.route("/chart", methods=["GET", "POST"])
def chart():

    plot_url = create_plot(data)
    return render_template("chart.html", plot_url=plot_url)


if __name__ == "__main__":
    app.run(debug=True)
