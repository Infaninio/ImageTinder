from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint("images", __name__, url_prefix="/images")


@bp.route("/", methods=("GET", "POST"))
def overview():
    """Overviewpage of the configurations."""
    return render_template(
        "configs/overview.html",
        configs=[
            {"name": "Amerika", "url": "/configs/Amerika"},
            {"name": "Irland", "url": "/configs/Irland"},
            {"name": "Griechenland", "url": "/configs/Griechenland"},
        ],
    )


@bp.route("image/<image_name>", methods=("GET", "POST"))
def image(image_name: str):
    """Display image deciding site.

    Parameters
    ----------
    image_name : str
        Name of the image.

    """
    if request.method == "POST":
        if "decline" in request.form:
            return redirect(url_for("images.image", image_name="nice_image"))
        if "accept" in request.form:
            return redirect(url_for("images.image", image_name="nice_image"))
    return render_template("image_view.html")
