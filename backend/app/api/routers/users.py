from api import logger, schemas, dependencies, config
from api.crud import crud_users, crud_videouserlinks, crud_videos, crud_banned
from api.tools import twitter_tools

from typing import List

from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v2/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# GET
@router.get("/{screen_name}", response_model=schemas.User)
async def read_user(
    screen_name: str = Path(min_length=1), db: Session = Depends(dependencies.get_db)
):
    """Get a user

    Args:
        screen_name (str, optional): user screen_name. Defaults to Path(min_length=5).
        db (Session, optional): DB Session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.User: schemas.User instance
    """
    db_user = crud_users.get_user_by_screen_name(db, screen_name=screen_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get(
    "/{screen_name}/videos_link/{video_id}", response_model=schemas.VideoUserLink
)
async def get_link_between_user_and_video_by_screen_name_and_tweet_id(
    screen_name: str = Path(min_length=1),
    video_id: str = Path(min_length=1, regex="^[0-9]*$"),
    db: Session = Depends(dependencies.get_db),
):
    """Get videouserlink by user screen_name and video tweet_id

    Args:
        screen_name (str, optional): user screen_name. Defaults to Path(min_length=5).
        video_id (str, optional): video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.VideoUserLink: schemas.VideoUserLink instance
    """
    db_videouserlink = (
        crud_videouserlinks.get_videouserlink_by_screen_name_and_tweet_id(
            db, screen_name=screen_name, tweet_id=video_id
        )
    )
    if db_videouserlink is None:
        raise HTTPException(
            status_code=404,
            detail=f"Link between user : '{screen_name}' and video : '{video_id}' not found",
        )
    return db_videouserlink


@router.get("/{screen_name}/videos_link", response_model=List[schemas.VideoUserLink])
async def get_links_between_user_and_video_by_screen_name(
    screen_name: str = Path(min_length=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=0, le=12),
    db: Session = Depends(dependencies.get_db),
):
    """Get videouserlinks by screen_name

    Args:
        screen_name (str): user screen_name. Defaults to Path(min_length=5).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        List[schemas.VideoUserLink]: list of schemas.VideoUserLink instances
    """
    db_videouserlinks = crud_videouserlinks.get_videouserlinks_by_screen_name(
        db=db, screen_name=screen_name, skip=skip, limit=limit
    )
    if not db_videouserlinks:
        raise HTTPException(status_code=404, detail="User does not requested videos")
    return db_videouserlinks


@router.get(
    "/{screen_name}/videos_count", response_model=schemas.UserVideoCountScreenName
)
async def get_video_count_of_user(
    screen_name: str = Path(min_length=1), db: Session = Depends(dependencies.get_db)
):
    """Get the count of videos requested by an user

    Args:
        screen_name (str): user screen_name. Defaults to Path(min_length=5).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Returns:
        schemas.UserVideoCountScreenName: schemas.UserVideoCountScreenName instance
    """
    video_count = crud_videouserlinks.get_videouserlinks_count_by_screen_name(
        db=db, screen_name=screen_name
    )
    if video_count == 0:
        raise HTTPException(status_code=404, detail="No videos requested by user")
    result = {"screen_name": screen_name, "videos_count": video_count}
    return result


@router.get("/{screen_name}/videos", response_model=schemas.UserVideos)
async def get_videos_requested_by_user_by_screen_name(
    screen_name: str = Path(min_length=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=0, le=12),
    db: Session = Depends(dependencies.get_db),
):
    """Get video requested by user

    Args:
        screen_name (str): user screen_name. Defaults to Path(min_length=5).
        skip (int, optional): number of videos to skip. Defaults to Query(default=0, ge=0).
        limit (int, optional): number of videos to request. Defaults to Query(default=100, ge=0).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.UserVideos: schemas.UserVideos instance
    """
    db_videos = crud_videos.get_videos_of_user_by_screen_name(
        db=db, screen_name=screen_name, skip=skip, limit=limit
    )
    if not db_videos:
        raise HTTPException(status_code=404, detail="No videos requested by user")
    results = {
        "screen_name": screen_name,
        "videos": db_videos,
    }
    return results


# POST
@router.post("", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db),
    current_admin: schemas.Admin = Depends(dependencies.get_current_admin),
):
    """Create an user

    Args:
        user (schemas.UserCreate): UserCreate instance
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).
        current_admin (schemas.Admin, optional): to check admin authentication. Defaults to Depends(dependencies.get_current_admin).

    Raises:
        HTTPException: HTTP 400

    Returns:
        schemas.User: schemas.User instance
    """
    db_user = crud_users.get_user_by_screen_name(db, screen_name=user.screen_name)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with screen_name='{db_user.screen_name}' already registered",
        )
    return crud_users.create_user(db=db, user=user)


@router.post("/{screen_name}/videos_link", response_model=schemas.VideoUserLink)
async def create_link_between_user_and_video(
    videouserlink: schemas.VideoUserLinkCreate,
    screen_name: str = Path(min_length=1),
    db: Session = Depends(dependencies.get_db),
    current_admin: schemas.Admin = Depends(dependencies.get_current_admin),
):
    """Create a link between an user and a video

    Args:
        screen_name (str): user screen_name
        videouserlink (schemas.VideoUserLinkCreate): video information and twitter reply tweet id.
        db (Session, optional): DB Session. Defaults to Depends(dependencies.get_db).
        current_admin (schemas.Admin, optional): to check admin authentication. Defaults to Depends(dependencies.get_current_admin).

    Raises:
        HTTPException: HTTP 404
        HTTPException: HTTP 404

    Returns:
        schemas.VideoUserLink: schemas.VideoUserLink instance
    """

    # Check if the user and the video exist in DB
    db_user = crud_users.get_user_by_screen_name(db, screen_name=screen_name)
    db_video = crud_videos.get_video_by_tweet_id(db, tweet_id=videouserlink.tweet_id)
    if (db_user is None) or (db_video is None):
        raise HTTPException(status_code=404, detail="User or video not found")

    # Check if the videouserlink exists
    db_videouserlink = crud_videouserlinks.get_videouserlink_by_reply_tweet_id(
        db=db, reply_tweet_id=videouserlink.reply_tweet_id
    )
    if db_videouserlink:
        raise HTTPException(
            status_code=400,
            detail="Videouserlink already registered with this reply_tweet_id",
        )

    # If all good, create the videouserlink
    return crud_videouserlinks.create_videouserlink(
        db=db, videouserlink=videouserlink, screen_name=screen_name
    )


# DELETE
@router.delete("/{screen_name}", response_model=schemas.UserDeleted)
async def delete_user(
    screen_name: str = Path(min_length=1),
    tweet: bool = Query(default=False),
    db: Session = Depends(dependencies.get_db),
    settings: config.Settings = Depends(config.get_settings),
    current_admin: schemas.Admin = Depends(dependencies.get_current_admin),
):
    """Delete an user (in User and VideoUserLink tables)

    Args:
        screen_name (str): user screen_name. Defaults to Path(min_length=5).
        tweet (bool): true to delete reply tweets, flase either. Defaults to Query(default=False).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).
        settings (config.Settings, optional): app settings. Defaults to Depends(config.get_settings).
        current_admin (schemas.Admin, optional): to check admin authentication. Defaults to Depends(dependencies.get_current_admin).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.UserDeleted (dict): schemas.UserDeleted instance (dict format)
    """

    # Check if the user exists
    db_user = crud_users.get_user_by_screen_name(db=db, screen_name=screen_name)
    db_videouserlinks = crud_videouserlinks.get_videouserlinks_by_screen_name(
        db=db, screen_name=screen_name, limit=10000000
    )
    if (db_user is None) and (not db_videouserlinks):
        raise HTTPException(status_code=404, detail="User not found")

    # Delete banned
    if db_user:
        db_banned = crud_banned.get_banned_by_used_id(db=db, user_id=db_user.user_id)
        if db_banned:
            crud_banned.delete_banned(db=db, db_banned=db_banned)

    # Delete vieouserlinks
    videouserlinks_deleted = crud_videouserlinks.delete_videouserlinks_by_screen_name(
        db=db, screen_name=screen_name
    )

    # Delete user
    if db_user:
        crud_users.delete_user(db=db, db_user=db_user)

    # Deleted reply tweets
    if tweet:
        for db_videouserlink in db_videouserlinks:
            try:
                twitter_tools.delete_tweet(
                    settings=settings, tweet_id=db_videouserlink.reply_tweet_id
                )
            except Exception as e:
                logger.error(
                    f"Tweet with ID : {db_videouserlink.reply_tweet_id} could not be deleted, Error : {e}"
                )
    return videouserlinks_deleted


@router.delete(
    "/{screen_name}/videos_link/{video_id}", response_model=schemas.VideoUserLink
)
async def delete_link_between_user_and_video_by_screen_name_and_tweet_id(
    screen_name: str = Path(min_length=1),
    tweet: bool = Query(default=False),
    video_id: str = Path(min_length=1, regex="^[0-9]*$"),
    db: Session = Depends(dependencies.get_db),
    settings: config.Settings = Depends(config.get_settings),
    current_admin: schemas.Admin = Depends(dependencies.get_current_admin),
):
    """Delete videouserlink by screen_name and tweet_id

    Args:
        screen_name (str): user screen_name. Defaults to Path(min_length=5).
        tweet (bool): true to delete reply tweets, flase either. Defaults to Query(default=False).
        video_id (str): video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).
        settings (config.Settings, optional): app settings. Defaults to Depends(config.get_settings).
        current_admin (schemas.Admin, optional): to check admin authentication. Defaults to Depends(dependencies.get_current_admin).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.VideoUserLink: schemas.VideoUserLink instance
    """

    # Check if the videouserlink exists
    db_videouserlink = (
        crud_videouserlinks.get_videouserlink_by_screen_name_and_tweet_id(
            db=db, screen_name=screen_name, tweet_id=video_id
        )
    )
    if db_videouserlink is None:
        raise HTTPException(status_code=404, detail="Videouserlink not found")

    # Deleted reply tweets
    if tweet:
        try:
            twitter_tools.delete_tweet(
                settings=settings, tweet_id=db_videouserlink.reply_tweet_id
            )
        except Exception as e:
            logger.error(
                f"Tweet with ID : {db_videouserlink.reply_tweet_id} could not be deleted, Error : {e}"
            )
    return crud_videouserlinks.delete_videouserlink(
        db=db, db_videouserlink=db_videouserlink
    )
