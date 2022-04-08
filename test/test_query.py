from ..CRUD import Crud, Task, Employee
import pytest


def test_get_empolyee_list():
    print(Crud().get_empolyee_list())

def test_get_task_by_chat_id():
    print(Crud().get_task_by_chat_id(118042759))

@pytest.mark.parametrize('task', [
    Task(
        empl=Employee( 
            name='Александр',
            last_name='Коробейников',
            middle_name='Владимирович',
            phone=79829197697,
            position='глав спец'
        ),
        project='Кофе',
        discription='Го, чо тупишь',
        title='Кофейный кофе',
        deadline='01.01.2022'
    ),
])
def test_set_task(task):
    print(Crud().set_task(task))