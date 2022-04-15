from CRUD import Crud, Task, Employee
# from ..base_struct import Task, Employee
import pytest

def test_get_empolyee_list():
    print(Crud().get_empolyee_list())

def test_get_task_by_chat_id():
    que1 = Crud().get_task_by_chat_id_to_me(891577752)
    que2 = Crud().get_task_by_chat_id_from_me(891577752)
    print(que1)
    print(que2)
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
    print(Crud().set_task(task,118042759))


@pytest.mark.parametrize('line', [
    '34-3456',
    '12-05-2007',
    '65-58-3015',
    '56-4532',
    '11-11-2011',
    '67-8945',
    '12-01-2009',
    '12.01.2009',
    '12.01.4009',
    '12.41.2009',
    '31.02.2009',
    '1.02.2009',
    '1.2.2009',
])
def test_re(line):
    import re
    assert re.match('\d{2}[.]\d{2}[.]\d{4}',line )
    # assert re.match('(^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.)([1-9]|0[1-9]|1[0-2])(\.)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$)',line )