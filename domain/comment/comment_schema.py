import datetime
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User


class CommentCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    board_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

class CommentUpdate(CommentCreate):
    comment_id: int

class CommentDelete(BaseModel):
    comment_id: int

class CommentVote(BaseModel):
    comment_id: int