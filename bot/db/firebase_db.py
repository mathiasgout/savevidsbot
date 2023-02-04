from db import logger
from db.outils import get_new_requested_videos
from helpers.logger import exception
from helpers.retry import retry

import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


GCP_CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "gcp_credentials.json")


@exception(logger)
@retry(Exception, tries=4, delay=10, logger=logger)
def init_firebase_app():
    """Initialisation of Firebase app
    """
    cred = credentials.Certificate(GCP_CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred)

@exception(logger)
def _get_client_firestore():
    """Return the Firestore client
    Returns:
        google.cloud.firestore_v1.client.Client: Firestore client
    """
    client_firestore = firestore.client()
    return client_firestore

@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_document(collection_name: str, document_name: str, **kwargs) -> None:
    """Create a document named "document_name" in the collection "collection_name"
    Document's fields are **kwargs
    Args:
        collection_name (str): the collection name
        document_name (str): the document name
    """
    client_firestore = _get_client_firestore()
    client_firestore.collection(collection_name).document(document_name).set(kwargs)
    logger.info(f"firestore document created. collection : {collection_name}, document : {document_name}")

@exception(logger)
@retry(Exception, tries=3, delay=5, logger=logger)
def edit_video_document(collection_name: str, document_name: str, **kwargs) -> int:
    client_firestore = _get_client_firestore()
    
    video_ref = client_firestore.collection(collection_name).document(document_name)
    video = video_ref.get()
    if video.exists:
        video_values = video.to_dict()
        video_ref.update({"asked_count": firestore.Increment(1)})
        logger.info(f"asked_count updated. collection : {collection_name}, document : {document_name}")
        return video_values["asked_count"]+1
    else:
        create_document(collection_name=collection_name, document_name=document_name, asked_count=1, **kwargs)
        return 1

@exception(logger)
@retry(Exception, tries=3, delay=5, logger=logger)
def edit_user_document(collection_name: str, document_name: str, **kwargs) -> None:
    client_firestore = _get_client_firestore()
    
    user_ref = client_firestore.collection(collection_name).document(document_name)
    user = user_ref.get()
    if user.exists:
        user_values = user.to_dict()
        requested_video = kwargs["requested_video"]
        
        # On vire les vidéos doublons (si l'utilisateur a demandé la vidéos plusieurs fois)
        new_requested_videos = get_new_requested_videos(video_id=requested_video["video_id"], requested_videos=user_values["requested_videos"])

        user_ref.update({"requested_videos": [requested_video] + new_requested_videos})
        logger.info(f"requested_videos updated. collection : {collection_name}, document : {document_name}")
    else:
        requested_video = kwargs.pop("requested_video")
        create_document(collection_name=collection_name, document_name=document_name, requested_videos=[requested_video], **kwargs)

@exception(logger)
@retry(Exception, tries=3, delay=2, logger=logger)
def get_document(collection_name: str, document_name: str) -> Optional[dict]:
    """Get a document from the collection : collection_name (to_dict format)
    Args:
        collection_name (str): Collection name
        document_name (str): Document Name
    Returns:
        Optional[dict]: document in dict format or None
    """
    client_firestore = _get_client_firestore()
    video_ref = client_firestore.collection(collection_name).document(document_name)
    video = video_ref.get()
    if video.exists:
        logger.info(f"Found a firestore document. Collection : {collection_name}, Document : {document_name}")
        return video.to_dict()
    logger.info(f"No document found. Collection : {collection_name}, Document : {document_name}")
    return None
