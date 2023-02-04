from db import logger
from helpers.logger import exception
from helpers.retry import retry

import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


GCP_CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "gcp_credentials.json"
)


@exception(logger)
@retry(Exception, tries=4, delay=10, logger=logger)
def init_firebase_app():
    """Initialisation of Firebase app"""
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
    document_ref = client_firestore.collection(collection_name).document(document_name)
    document = document_ref.get()
    if document.exists:
        logger.info(
            f"Found a firestore document. Collection : {collection_name}, Document : {document_name}"
        )
        return document.to_dict()
    logger.info(
        f"No document found. Collection : {collection_name}, Document : {document_name}"
    )
    return None


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
    logger.info(
        f"Firestore document created. Collection : {collection_name}, Document : {document_name}"
    )


@exception(logger)
@retry(Exception, tries=3, delay=5, logger=logger)
def create_banned_document(collection_name: str, document_name: str, **kwargs) -> None:
    """Create a document in the "banned" (or "banned-dev") collection (if it does not already exist)

    Args:
        collection_name (str): collection name
        document_name (str): document name
    """
    client_firestore = _get_client_firestore()

    user_ref = client_firestore.collection(collection_name).document(document_name)
    user = user_ref.get()
    if not user.exists:
        create_document(
            collection_name=collection_name, document_name=document_name, **kwargs
        )
    else:
        logger.info(
            f"Firestore document already exist. Collection : {collection_name}, Document : {document_name}"
        )


@exception(logger)
@retry(Exception, tries=3, delay=2, logger=logger)
def delete_document(collection_name: str, document_name: str) -> None:
    """Delete a document from the collection : collection_name

    Args:
        collection_name (str): collection name
        document_name (str): document name
    """
    client_firestore = _get_client_firestore()
    document_ref = client_firestore.collection(collection_name).document(document_name)
    document = document_ref.get()
    if document.exists:
        document_ref.delete()
        logger.info(
            f"Document deleted. Collection : {collection_name}, Document : {document_name}"
        )
    else:
        logger.info(
            f"No document to delete. Collection : {collection_name}, Document : {document_name}"
        )
