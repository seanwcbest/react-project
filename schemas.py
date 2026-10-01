from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from models import (
    InvitePermission,
    EventStatus,
    DayOfWeek,
    RSVPStatus,
    FriendRequestStatus,
    GroupInviteStatus,
)

#User

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Friends
class FriendBase(BaseModel):
    user_id: int
    friend_id: int

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    id: int

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Groups
class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    start_datetime: Optional[datetime] = None
    invite_permission: InvitePermission = InvitePermission.admin
    event_creation_permission: InvitePermission = InvitePermission.admin

class GroupCreate(GroupBase):
    owner_id: int

class Group(GroupBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Group Members
class GroupMemberBase(BaseModel):
    role: str = "member"  # Default role is 'member'

class GroupMemberCreate(GroupMemberBase):
    group_id: int
    user_id: int

class GroupMember(GroupMemberBase):
    id: int
    group_id: int
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Events
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    status: EventStatus = EventStatus.planning

class EventCreate(EventBase):
    group_id: int
    created_by: int

class Event(EventBase):
    id: int
    group_id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

# Group Availability
class GroupAvailabilityBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: time
    end_time: time

class GroupAvailabilityCreate(GroupAvailabilityBase):
    group_id: int
    user_id: int

class GroupAvailability(GroupAvailabilityBase):
    id: int
    group_id: int
    user_id: int

    class Config:
        from_attributes = True  # pydantic version >=2.x

# Events RSVPs

class EventRSVPBase(BaseModel):
    status: RSVPStatus = RSVPStatus.undecided

class EventRSVPCreate(EventRSVPBase):
    event_id: int
    user_id: int

class EventRSVP(EventRSVPBase):
    id: int
    event_id: int
    user_id: int

    class Config:
        from_attributes = True  # pydantic version >=2.x

# Friend Requests
class FriendRequestCreate(BaseModel):
    sender_id: int
    receiver_id: int

class FriendRequest(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: FriendRequestStatus
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Group Invites
class GroupInviteCreate(BaseModel):
    group_id: int
    sender_id: int
    receiver_id: int

class GroupInvite(BaseModel):
    id: int
    group_id: int
    sender_id: int
    receiver_id: int
    status: GroupInviteStatus
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x

#Blocks
class BlockCreate(BaseModel):
    blocker_id: int
    blocked_id: int

class Block(BaseModel):
    id: int
    blocker_id: int
    blocked_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic version >=2.x


