from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

from app.core.db import Base


class Message(Base):
    id = Column(Integer, primary_key=True)
    message = Column(String)
    write_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('user.id'))
    meeting_room_id = Column(Integer, ForeignKey('meetingroom.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}