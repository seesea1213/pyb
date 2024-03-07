from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.comment import comment_schema, comment_crud
from domain.board import board_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/comment",
)


@router.post("/create/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(board_id: int,
                  _comment_create: comment_schema.CommentCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # create comment
    board = board_crud.get_board(db, board_id=board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    comment_crud.create_comment(db, board=board,
                              comment_create=_comment_create,
                               user=current_user)

@router.get("/detail/{comment_id}", response_model=comment_schema.Comment)
def comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id=comment_id)
    return comment

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def comment_update(_comment_update: comment_schema.CommentUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id=_comment_update.comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_comment.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    comment_crud.update_comment(db=db, db_comment=db_comment,
                              comment_update=_comment_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(_comment_delete: comment_schema.CommentDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id=_comment_delete.comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_comment.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    comment_crud.delete_comment(db=db, db_comment=db_comment)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def comment_vote(_comment_vote: comment_schema.CommentVote,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id=_comment_vote.comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    comment_crud.vote_comment(db, db_comment=db_comment, db_user=current_user)