import enum
from db import Base
from datetime import datetime
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime,
    Time,
    ForeignKey,
    Enum, 
    CheckConstraint, 
    UniqueConstraint
)
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "Profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False,unique=True, index=True)
    age=Column(Integer, nullable=True)
    bio = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")

class Friends(Base):
    __tablename__ = "Friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), index=True)
    friend_id = Column(Integer, ForeignKey("Users.id"), index=True)

    __table_args__ = (
        CheckConstraint('user_id < friend_id', name='check_user_id_less_than_friend_id'),
        UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )

    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])

class InvitePermission(enum.Enum):
    owner = "owner"
    admin = "admin"
    everyone = "everyone"

class Groups(Base):
    __tablename__ = "Groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    image_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    start_date = Column(DateTime, default=datetime.now)
    invite_permission = Column(Enum(InvitePermission), default=InvitePermission.admin, nullable=False)
    event_creation_permission = Column(Enum(InvitePermission), default=InvitePermission.admin, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner = relationship("User", foreign_keys=[owner_id])

class GroupMembers(Base):
    __tablename__ = "GroupMembers"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("Groups.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    role = Column(String, default="member", nullable=False, index=True)
    joined_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='unique_group_membership'),
    )

    group = relationship("Groups", foreign_keys=[group_id])
    user = relationship("User", foreign_keys=[user_id])

class EventStatus(enum.Enum):
    planning = "planning"
    in_progress = "in_progress"
    completed = "completed"

class Events(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("Groups.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.planning, nullable=False)
    created_by = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
    location = Column(String, nullable=True)

    group = relationship("Groups", foreign_keys=[group_id])
    creator = relationship("User", foreign_keys=[created_by])

class DayOfWeek(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

class GroupAvailability(Base):
    __tablename__ = "Availability"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("Groups.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint("start_time < end_time", name="check_start_before_end"),
        UniqueConstraint("group_id", "user_id", "day_of_week", "start_time", "end_time", name="unique_group_availability_slot"),
    )

    group = relationship("Groups", foreign_keys=[group_id])
    user = relationship("User")

class RSVPStatus(enum.Enum):
    attending = "attending"
    not_attending = "not_attending"
    maybe = "maybe"
    undecided = "undecided"

class EventRSVP(Base):
    __tablename__ = "EventRSVPs"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("Events.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    status = Column(Enum(RSVPStatus), default=RSVPStatus.undecided, nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'user_id', name='unique_event_rsvp'),
    )

    event = relationship("Events", foreign_keys=[event_id])
    user = relationship("User", foreign_keys=[user_id])

class FriendRequestStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"

class FriendRequest(Base):
    __tablename__ = "FriendRequests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    status = Column(Enum(FriendRequestStatus), default=FriendRequestStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint('sender_id != receiver_id', name='check_sender_receiver_different'),
        UniqueConstraint('sender_id', 'receiver_id', name='unique_friend_request'),
    )

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

class GroupInviteStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"

class GroupInvite(Base):
    __tablename__ = "GroupInvites"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("Groups.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    status = Column(Enum(GroupInviteStatus), default=GroupInviteStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint('sender_id != receiver_id', name='check_sender_receiver_different'),
        UniqueConstraint('group_id', 'receiver_id', name='unique_group_invite'),
    )

    group = relationship("Groups", foreign_keys=[group_id])
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

class Block(Base):
    __tablename__ = "Blocks"

    id = Column(Integer, primary_key=True, index=True)
    blocker_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    blocked_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("blocker_id != blocked_id", name="check_blocker_not_blocked"),
        UniqueConstraint("blocker_id", "blocked_id", name="unique_block"),
    )

    blocker = relationship("User", foreign_keys=[blocker_id])
    blocked = relationship("User", foreign_keys=[blocked_id])

