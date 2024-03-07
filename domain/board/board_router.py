from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.board import board_schema, board_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/board",
)

@router.get("/list", response_model=board_schema.BoardList)
def board_list(db: Session = Depends(get_db),
               page: int = 0, size: int = 10, keyword: str = ''):
    total, _board_list = board_crud.get_board_list(
        db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total,
        'board_list': _board_list
    }

@router.get("/detail/{board_id}", response_model=board_schema.Board)
def board_detail(board_id: int, db: Session = Depends(get_db)):
    board = board_crud.get_board(db, board_id=board_id)
    return board

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def board_create(_board_create: board_schema.BoardCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    board_crud.create_board(db=db, board_create=_board_create,
                            user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def board_update(_board_update: board_schema.BoardUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_board = board_crud.get_board(db, board_id=_board_update.board_id)
    if not db_board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_board.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    board_crud.update_board(db=db, db_board=db_board,
                                  board_update=_board_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def board_delete(_board_delete: board_schema.BoardDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_board = board_crud.get_board(db, board_id=_board_delete.board_id)
    if not db_board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_board.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    board_crud.delete_board(db=db, db_board=db_board)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def board_vote(_board_vote: board_schema.BoardVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_board = board_crud.get_board(db, board_id=_board_vote.board_id)
    if not db_board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    board_crud.vote_board(db, db_board=db_board, db_user=current_user)