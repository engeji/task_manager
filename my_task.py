from dispatcher import *
from CRUD import Crud

@dp.message_handler(commands='my_task')
async def projtask_list(message: types.Message ):
    res = '\n'.join([
        str(task)
    for task in Crud().get_task_by_chat_id(message.chat.id)])
    await message.answer(res)