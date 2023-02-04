from app import logger
from helpers.logger import exception
from app.outils import (
    add_video_info_to_the_session,
    add_user_info_to_the_session,
    get_user_videos,
    user_deletion,
    video_deletion,
)

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
    current_app,
    flash,
    abort,
)
from flask_login import login_required


views = Blueprint("views", __name__)


@exception(logger)
@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_search = request.form.get("user_search")
        if user_search:
            user_search = user_search.replace("@", "").lower()
            user_search = user_search.replace(" ", "")
            return redirect(url_for("views.users", screen_name=user_search))
    return render_template("home.html")


@exception(logger)
@views.route("/videos/<tweet_id>", methods=["GET"])
def videos(tweet_id):

    # Check si tweet_id est un nombre
    try:
        int(tweet_id)
    except ValueError:
        return abort(404)

    # Création de la clef "tweets" et "users" dans la session
    if "users" not in session.keys():
        session["users"] = {}
    if "tweets" not in session.keys():
        session["tweets"] = {}

    # Si video_id pas dans la session (s'il n'y a pas de requête faite pour cet id dans cette session)
    if tweet_id not in session["tweets"].keys():
        if add_video_info_to_the_session(session=session, video_id=tweet_id):
            return render_template(
                "videos.html",
                video_url=session["tweets"][tweet_id]["video_url"],
                creator=session["tweets"][tweet_id]["creator"],
                tweet_url=session["tweets"][tweet_id]["tweet_url"],
                thumbnail_url=session["tweets"][tweet_id]["thumbnail_url"],
                text=session["tweets"][tweet_id]["text"],
                tweet_id=tweet_id,
            )

    # Si video_id déjà demandé dans cette session et dans la db
    else:
        return render_template(
            "videos.html",
            video_url=session["tweets"][tweet_id]["video_url"],
            creator=session["tweets"][tweet_id]["creator"],
            tweet_url=session["tweets"][tweet_id]["tweet_url"],
            thumbnail_url=session["tweets"][tweet_id]["thumbnail_url"],
            text=session["tweets"][tweet_id]["text"],
            tweet_id=tweet_id,
        )

    return abort(404)


@exception(logger)
@views.route("/users/<screen_name>/", methods=["GET"])
def users(screen_name):

    # Création de la clef "tweets" et "users" dans la session
    if "users" not in session.keys():
        session["users"] = {}
    if "tweets" not in session.keys():
        session["tweets"] = {}

    # Récupération de la page
    args = request.args
    page = args.get("page", 1, type=int)
    if page < 1:
        page = 1
    last_page = False

    # Si screen_name pas dans la session (s'il n'y a pas de requête faite pour ce screen_name dans cette session)
    if screen_name not in session["users"].keys():
        if add_user_info_to_the_session(session=session, screen_name=screen_name):
            user_videos = get_user_videos(
                session=session, screen_name=screen_name, page=page
            )
            if len(user_videos) < current_app.config["VIDEOS_PER_PAGE"]:
                last_page = True
            return render_template(
                "users.html",
                screen_name=screen_name,
                user_videos=user_videos,
                page=page,
                last_page=last_page,
            )

    else:
        user_videos = get_user_videos(
            session=session, screen_name=screen_name, page=page
        )
        if len(user_videos) < current_app.config["VIDEOS_PER_PAGE"]:
            last_page = True
        return render_template(
            "users.html",
            screen_name=screen_name,
            user_videos=user_videos,
            page=page,
            last_page=last_page,
        )

    flash(f'Usersame: "{screen_name}" not found!', category="error")
    return redirect(url_for("views.home"))


@exception(logger)
@views.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        user_delete = request.form.get("user_delete")
        video_delete = request.form.get("video_delete")

        if user_delete:
            user_delete = user_delete.replace("@", "").lower()
            user_delete = user_delete.replace(" ", "")
            user_deletion(screen_name=user_delete)

        if video_delete:
            video_delete = video_delete.replace(" ", "")
            video_deletion(video_id=video_delete)

    return render_template("admin.html")
