from sqlalchemy import Integer, Column, String, Text, ForeignKey

from models.model import BaseModel


class Course(BaseModel):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), comment='Название курса')
    image = Column(String(500), comment='Ссылка на изображение', default=None)
    description = Column(String(2000), comment='Описание курса', default=None)
    content = Column(Text, comment='Контент курса (HTML)', default=None)
    editor_content = Column(Text, comment='Контент курса (JSON)', default=None)
    user_id = Column(Integer, ForeignKey('user.id'), comment='Пользователь', default=None)

    def __str__(self):
        return self.title
