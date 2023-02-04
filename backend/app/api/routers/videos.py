from api import logger, schemas, dependencies, config
from api.crud import crud_videos, crud_videouserlinks
from api.tools import twitter_tools

from typing import List

from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v2/videos",
    tags=["videos"],
    responses={404: {"description": "Not found"}},
)


# GET
@router.get("/{video_id}", response_model=schemas.Video)
async def read_video(
    video_id: str = Path(min_length=3, regex="^[0-9]*$"),
    db: Session = Depends(dependencies.get_db),
):
    """Get a video

    Args:
        video_id (str): Video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.Video: schemas.Video instance
    """
    db_video = crud_videos.get_video_by_tweet_id(db=db, tweet_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video


@router.get("/{video_id}/users_link", response_model=List[schemas.VideoUserLink])
async def get_links_between_user_and_video_by_tweet_id(
    video_id: str = Path(min_length=3, regex="^[0-9]*$"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=0),
    db: Session = Depends(dependencies.get_db),
):
    """Get videouserlinks between by tweet_id

    Args:
        video_id (str): Video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        List[schemas.VideoUserLink]: list of schemas.VideoUserLink instances
    """
    db_videouserlinks = crud_videouserlinks.get_videouserlinks_by_tweet_id(
        db=db, tweet_id=video_id, skip=skip, limit=limit
    )
    if not db_videouserlinks:
        raise HTTPException(status_code=404, detail="Video not requested")
    return db_videouserlinks


@router.get("/{video_id}/videos_count", response_model=schemas.UserVideoCountTweetId)
async def get_video_count_of_video(
    video_id: str = Path(min_length=3, regex="^[0-9]*$"),
    db: Session = Depends(dependencies.get_db),
):
    """Get the request count of a video

    Args:
        video_id (str): video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Returns:
        schemas.UserVideoCountTweetId: schemas.UserVideoCountTweetId instance
    """
    video_count = crud_videouserlinks.get_videouserlinks_count_by_tweet_id(
        db=db, tweet_id=video_id
    )
    if video_count == 0:
        raise HTTPException(status_code=404, detail="This video was not requested")
    result = {"tweet_id": video_id, "videos_count": video_count}
    return result


# POST
@router.post("", response_model=schemas.Video)
async def create_video(
    video: schemas.VideoCreate, db: Session = Depends(dependencies.get_db)
):
    """Create a video

    Args:
        video (schemas.VideoCreate): VideoCreate instance.
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 400

    Returns:
        schemas.Video: schemas.Video instance
    """
    db_video = crud_videos.get_video_by_tweet_id(db=db, tweet_id=video.tweet_id)
    if db_video:
        raise HTTPException(
            status_code=400,
            detail=f"Video with tweet_id : {video.tweet_id} already registred",
        )
    return crud_videos.create_video(db=db, video=video)


# DELETE
@router.delete("/{video_id}", response_model=schemas.VideoDeleted)
async def delete_video(
    video_id: str = Path(min_length=3, regex="^[0-9]*$"),
    tweet: bool = Query(default=False),
    db: Session = Depends(dependencies.get_db),
    settings: config.Settings = Depends(config.get_settings),
    current_admin: schemas.Admin = Depends(dependencies.get_current_admin),
):
    """Delete a video (in Video and VideoUserLink tables)

    Args:
        video_id (str): video tweet_id. Defaults to Path(min_length=3, regex="^[0-9]*$").
        tweet (bool): true to delete reply tweets, flase either. Defaults to Query(default=False).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).
        settings (config.Settings, optional): app settings. Defaults to Depends(config.get_settings).
        current_admin (schemas.Admin, optional): to check admin authentication. Defaults to Depends(dependencies.get_current_admin).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.VideoDeleted: schemas.VideoDeleted instance
    """

    # Check if the video exists
    db_video = crud_videos.get_video_by_tweet_id(db=db, tweet_id=video_id)
    db_videouserlinks = crud_videouserlinks.get_videouserlinks_by_tweet_id(
        db=db, tweet_id=video_id, limit=10000000
    )
    if (db_video is None) and (not db_videouserlinks):
        raise HTTPException(status_code=404, detail="Video not found")

    # Delete videouserlinks
    videouserlinks_deleted = crud_videouserlinks.delete_videouserlinks_by_tweet_id(
        db=db, tweet_id=video_id
    )

    # Delete video
    if db_video:
        crud_videos.delete_video(db=db, db_video=db_video)

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
