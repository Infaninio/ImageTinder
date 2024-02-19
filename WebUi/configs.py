import base64
import io
from datetime import datetime

import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request

bp = Blueprint("configs", __name__, url_prefix="/configs")


@bp.route("/overview", methods=("GET", "POST"))
def overview():
    """Overviewpage of the configurations."""
    return render_template(
        "configs/overview.html",
        configs=[
            {"name": "Amerika", "url": "/configs/Amerika"},
            {"name": "Irland", "url": "/configs/Griechenland"},
            {"name": "Amerika", "url": "/configs/Griechenland"},
        ],
    )


@bp.route("/<config_name>", methods=("GET", "POST"))
def show_config(config_name: str):
    """Display the overview of a specific configuration."""
    if request.method == "POST":
        print(f"Button gedrueckt {request.form}")

    example_config = {
        "name": config_name,
        "sum_images": 120,
        "reviewed_images": 20,
        "start_date": datetime.today().strftime("%Y-%m-%d"),
        "end_date": datetime.today().strftime("%Y-%m-%d"),
    }
    # Data for the pie chart
    labels = ["Nicht Bewertet", "Positiv Bewertet", "Negativ Bewertet"]
    sizes = [100, 6, 14]

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template(
        "configs/configuration.html", config=example_config, plot_url=plot_url
    )
