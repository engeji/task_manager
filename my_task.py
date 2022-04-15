from dispatcher import *
from CRUD import Crud
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

class MyTask_state(StatesGroup):
    wait_task = State()




@dp.message_handler(commands=['my_task'])
async def task_list(message: types.Message, state: FSMContext ):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Задачи мне')
    keyboard.add('Задачи от меня')
    keyboard.add('Выход')
    await state.set_state(MyTask_state.wait_task)
    await message.reply("Тип задач:", reply_markup=keyboard)

@dp.message_handler(state='*', commands=['Выход'])
@dp.message_handler(Text(equals='Выход', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    log.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Выход.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=MyTask_state.wait_task)
async def change_task_type(message: types.Message, state: FSMContext):
    if message.text == 'Задачи мне':
        task_list = Crud().get_task_by_chat_id_to_me(message.chat.id)
        if len(task_list) == 0:
            await message.answer('У вас нет задач', reply_markup= types.ReplyKeyboardRemove())
            await state.finish()
            return
        res = '\n'.join([
            str(task)
        for task in task_list])
        await message.answer(res, reply_markup= types.ReplyKeyboardRemove())
        await state.finish()
    elif message.text == 'Задачи от меня':
        task_list = Crud().get_task_by_chat_id_from_me(message.chat.id)
        if len(task_list) == 0:
            await message.answer('Вы не создали не одной задачи', reply_markup= types.ReplyKeyboardRemove())
            await state.finish()
            return
        res = '\n'.join([
            str(task)
        for task in task_list])
        await message.answer(res, reply_markup= types.ReplyKeyboardRemove())
        await state.finish()
    
    elif message.text == 'Выход':
        pass
    else:
        await MyTask_state.wait_task.set()
        await message.answer('Выбирите тип задач используя клавиатуру ниже')