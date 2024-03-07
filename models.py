from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

board_voter = Table(
    'board_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('board_id', Integer, ForeignKey('board.id'), primary_key=True)
)

comment_voter = Table(
    'comment_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('comment_id', Integer, ForeignKey('comment.id'), primary_key=True)
)

class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, default=func.now())
    modify_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='boards')
    comments = relationship('Comment', back_populates='board')
    voter = relationship('User', secondary=board_voter, backref='board_voters')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, default=func.now())
    modify_date = Column(DateTime, nullable=True)
    board_id = Column(Integer, ForeignKey('board.id'))
    user_id = Column(Integer, ForeignKey('user.id'))  # 글쓴이에 대한 외래 키 추가
    user = relationship('User', back_populates='comments')  # User 모델과의 관계 설정
    board = relationship('Board', back_populates='comments')
    voter = relationship('User', secondary=comment_voter, backref='comment_voters')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    boards = relationship('Board', back_populates='user')
    comments = relationship('Comment', back_populates='user')  # Comment 모델과의 관계 설정