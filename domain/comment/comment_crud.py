from datetime import datetime

from sqlalchemy.orm import Session

from domain.comment.comment_schema import CommentCreate, CommentUpdate
from models import Board, Comment, User


def create_comment(db: Session, board: Board, comment_create: CommentCreate, user: User):
    db_comment = Comment(board=board,
                       content=comment_create.content,
                       create_date=datetime.now(), user=user)
    db.add(db_comment)
    db.commit()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).get(comment_id)

def update_comment(db: Session, db_comment: Comment,
                  comment_update: CommentUpdate):
    db_comment.content = comment_update.content
    db_comment.modify_date = datetime.now()
    db.add(db_comment)
    db.commit()

def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()

def vote_comment(db: Session, db_comment: Comment, db_user: User):
    db_comment.voter.append(db_user)
    db.commit()