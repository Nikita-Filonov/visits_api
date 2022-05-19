from sqlalchemy import Column, Integer, String, Text

from models.model import BaseModel


class Lesson(BaseModel):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), comment='Название урока')
    content = Column(Text, comment='Контент курса (HTML)', default=None)
    editor_content = Column(Text, comment='Контент курса (JSON)', default=None)
