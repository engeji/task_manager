from dispatcher import dp, log, bot, types
from CRUD import Crud

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    log.info(f'try fo auth with {message.from_user.full_name}')
    try:
        cur_id = message.chat.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Авторизация 👋', request_contact=True))            
        await bot.send_message(message.chat.id, 'Необходимо пройти авторизацю по номеру телефона.', reply_markup=keyboard)                
    except Exception as e:
        await bot.send_message(message.chat.id, str(e))
    
@dp.message_handler(content_types=['contact'])
async def check_contact(message:types.Message):
    crud = Crud()
    empl = crud.get_employee_by_phone(int(message.contact.phone_number))
    if len(empl) == 1:
        await bot.send_message(message.chat.id,
        f'''
        Приветствую, {empl[0].name} {empl[0].middle_name}!
        Меня зовут TaskManager Александрович 
        и я постараюсь усложнить Вам жизнь
        и повысить эффективность работу начальников.        
        ''', reply_markup=types.ReplyKeyboardRemove())
    elif len(empl) == 0:
        await bot.send_message(message.chat.id, 'Я вас не звал')
    else:
        await bot.send_message(message.chat.id, empl)
    auth = crud.set_chat_id(int(message.chat.id), int(message.contact.phone_number) )
    await bot.send_message(message.chat.id, auth)