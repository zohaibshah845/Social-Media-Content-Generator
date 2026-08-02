from app.firebase import db
from datetime import datetime
from typing import List, Dict, Any

def get_user_posts(uid: str) -> List[Dict[str, Any]]:
    docs = db.collection('users').document(uid).collection('posts').order_by('created_at').stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def create_post(uid: str, post_data: dict) -> str:
    doc_ref = db.collection('users').document(uid).collection('posts').document()
    post_data['created_at'] = datetime.utcnow()
    post_data['status'] = 'draft'
    doc_ref.set(post_data)
    return doc_ref.id

def update_post(uid: str, post_id: str, update_data: dict):
    db.collection('users').document(uid).collection('posts').document(post_id).update(update_data)

def get_post(uid: str, post_id: str) -> dict:
    doc = db.collection('users').document(uid).collection('posts').document(post_id).get()
    if doc.exists:
        return {**doc.to_dict(), "id": doc.id}
    return None