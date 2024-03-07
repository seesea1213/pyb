from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Optional
from domain.comment.comment_schema import Comment
from domain.user.user_schema import User

# 입력 모델
class BoardCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 출력 모델
class Board(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime
    comments: Optional[List[Comment]] = []
    user: User | None
    modify_date: Optional[datetime] = None
    voter: list[User] = []

    class Config:
        orm_mode = True

class BoardList(BaseModel):
    total: int = 0
    board_list: list[Board] = []

class BoardUpdate(BoardCreate):
    board_id: int

class BoardDelete(BaseModel):
    board_id: int

class BoardVote(BaseModel):
    board_id: int