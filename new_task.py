from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from CRUD import Crud, Task
from dispatcher import *
import re

class Task_state(StatesGroup):
    wait_proj_name = State()
    wait_task_name = State()
    wait_discript = State()
    wait_executror = State()
    wait_deadline = State()


@dp.message_handler(commands='new_task', state='*')
async def proj_name(message: types.Message, state: FSMContext):
    crud = Crud()
    req_proj_list = crud.get_project_list()
    proj_list = [dict_proj['name'] for dict_proj in req_proj_list]
    task_obj = Task()
    task_obj.auther = crud.get_employee_by_chat_id(message.chat.id)[0]
    async with state.proxy() as data:
        data['proj_list'] = proj_list
        data['task_obj'] = task_obj
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in proj_list:
        keyboard.add(name)
    await state.set_state(Task_state.wait_proj_name)
    await message.answer("Выберите проект:", reply_markup=keyboard)

@dp.message_handler(state=Task_state.wait_proj_name)
async def task_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    proj_list = user_data['proj_list']
    if message.text not in proj_list:
        await message.answer("Пожалуйста, выберите проект, используя клавиатуру ниже.")
        return
    async with state.proxy() as data:
        cur_task:Task = data['task_obj']
        cur_task.project = message.text
    await state.set_state(Task_state.wait_task_name)
    await message.answer("Название задачи:", reply_markup= types.ReplyKeyboardRemove())

@dp.message_handler(state=Task_state.wait_task_name)
async def task_discript(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_obj'].title = message.text
    await state.set_state(Task_state.wait_discript)
    await message.answer("Описание задачи:")

@dp.message_handler(state=Task_state.wait_discript)
async def task_executor(message: types.Message, state: FSMContext):
    req_employee_list = Crud().get_empolyee_list()
    async with state.proxy() as data:
        data['task_obj'].discription = message.text 
        data['empolyee_list'] = req_employee_list
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for empl in req_employee_list:
        keyboard.add(str(empl))
    await state.set_state(Task_state.wait_executror)
    await message.answer("Исполнитель:",reply_markup=keyboard)

@dp.message_handler(state=Task_state.wait_executror)
async def task_deadline(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text not in [str(empl) for empl in user_data['empolyee_list']]:
        await message.answer("Пожалуйста, выберите исполнителя, используя клавиатуру ниже.")
        return
    async with state.proxy() as data:

        data['task_obj'].empl = next(filter(lambda empl: str(empl) == message.text, data['empolyee_list']))
    await state.set_state(Task_state.wait_deadline)
    await message.answer("Срок задачи в формате (dd.mm.yyyy):", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Task_state.wait_deadline)
async def task_done(message: types.Message, state: FSMContext):
    if not re.match('\d{2}[.]\d{2}[.]\d{4}', message.text):
        await message.answer("Неверный формат, нужный формат dd.mm.yyyy:")
        return
    user_data = await state.get_data()
    await state.finish()
    task_obj:Task = user_data['task_obj']
    task_obj.deadline = message.text
    await message.answer(repr(task_obj), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(Crud().set_task(task_obj, message.chat.id))
    await bot.send_message(task_obj.empl.chat_id, str(task_obj))