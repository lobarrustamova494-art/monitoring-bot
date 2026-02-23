from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class ForwardMode(enum.Enum):
    PRIVATE = "private"
    GROUP = "group"
    BOTH = "both"

class FilterType(enum.Enum):
    ALL = "all"
    TEXT_ONLY = "text_only"
    MEDIA_ONLY = "media_only"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    groups = relationship("UserGroup", back_populates="user", cascade="all, delete-orphan")

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), index=True)
    title = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_message_id = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    subscriptions = relationship("Subscription", back_populates="channel", cascade="all, delete-orphan")

class UserGroup(Base):
    __tablename__ = "user_groups"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, nullable=False, index=True)
    group_title = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="groups")
    subscriptions = relationship("Subscription", back_populates="group")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("user_groups.id", ondelete="SET NULL"), nullable=True)
    
    forward_mode = Column(Enum(ForwardMode), default=ForwardMode.PRIVATE)
    filter_type = Column(Enum(FilterType), default=FilterType.ALL)
    keyword_filter = Column(Text)
    add_prefix = Column(String(500))
    
    is_active = Column(Boolean, default=True)
    posts_forwarded = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="subscriptions")
    channel = relationship("Channel", back_populates="subscriptions")
    group = relationship("UserGroup", back_populates="subscriptions")

class ForwardedMessage(Base):
    __tablename__ = "forwarded_messages"
    
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_message_id = Column(Integer, nullable=False)
    forwarded_message_id = Column(Integer)
    destination_chat_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
