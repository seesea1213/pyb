from datetime import datetime

from domain.board.board_schema import BoardCreate, BoardUpdate
from sqlalchemy import and_
from models import Board, User, Comment
from sqlalchemy.orm import Session


def get_board_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    board_list = db.query(Board)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Comment.board_id, Comment.content, User.username) \
            .outerjoin(User, and_(Comment.user_id == User.id)).subquery()
        board_list = board_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.board_id == Board.id)) \
            .filter(Board.subject.ilike(search) |        # 질문제목
                    Board.content.ilike(search) |        # 질문내용
                    User.username.ilike(search) |           # 질문작성자
                    sub_query.c.content.ilike(search) |     # 답변내용
                    sub_query.c.username.ilike(search)      # 답변작성자
                    )
    total = board_list.distinct().count()
    board_list = board_list.order_by(Board.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, board_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_board(db: Session, board_id: int):
    board = db.query(Board).get(board_id)
    return board

def create_board(db: Session, board_create: BoardCreate, user: User):
    db_board =  Board(subject=board_create.subject,
                           content=board_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_board)
    db.commit()

def update_board(db: Session, db_board: Board, board_update: BoardUpdate):
    db_board.subject = board_update.subject
    db_board.content = board_update.content
    db_board.modify_date = datetime.now()
    db.add(db_board)
    db.commit()

def delete_board(db: Session, db_board: Board):
    db.delete(db_board)
    db.commit()

def vote_board(db: Session, db_board: Board, db_user: User):
    db_board.voter.append(db_user)
    db.commit()