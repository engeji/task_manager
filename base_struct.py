
class Task:
    def __init__(self, **kwargs):
        self.empl:Employee = kwargs.get('empl',None) 
        self.project = kwargs.get('project',None) 
        self._deadline = kwargs.get('deadline',None) 
        self.discription = kwargs.get('discription',None) 
        self.title = kwargs.get('title',None)
    @property     
    def deadline(self):
        return self._deadline if isinstance(self._deadline, str) or self._deadline is None  else self._deadline.decode('UTF-8')
    @deadline.setter
    def deadline(self, val):
        return val if isinstance(val, str) or val is None else val.decode('UTF-8')
    def __repr__(self):
        return f'''Поручение:
    название: {self.title}
    проект: {self.project}
    срок: {self.deadline}
    описание: {self.discription}
    исполнитель: {self.empl}'''
    @classmethod
    def from_my_task(cls, **kwargs):
        return cls(**kwargs, empl=Employee(**kwargs))

class Employee:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get('name', None)
        self.last_name = kwargs.get('last_name', None)
        self.middle_name = kwargs.get('middle_name', None)
        self.phone = kwargs.get('phone', None)
        self.position = kwargs.get('position', None)
        self.chat_id = kwargs.get('chat_id', None)
    def __repr__(self) -> str:
        return f'''Сотрудник:
    {self.last_name} {self.name} {self.middle_name}'''
    def __str__(self) -> str:
        return f'{self.last_name } {self.name[0]}. {self.middle_name[0]}.'