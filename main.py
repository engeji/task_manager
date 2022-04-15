
import new_task
import my_task
import auth
from dispatcher import dp, log
from aiogram import Bot, Dispatcher, executor, types
import json
import os
async def process_event(event, dp:Dispatcher):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """
    commands = [
        types.bot_command.BotCommand(command="/new_task", description="Создать задачу"),
        types.bot_command.BotCommand(command="/my_task", description="Мои задачи"),
        types.bot_command.BotCommand(command="/start", description="Авторизация"),
    ]
    await dp.bot.set_my_commands(commands)
    update = json.loads(event['body'])
    log.debug('Update: ' + str(update))

    Bot.set_current(dp.bot)
    update = types.Update.to_object(update)
    await dp.process_update(update)


async def handler(event, context):
    """Yandex.Cloud functions handler."""

    if event['httpMethod'] == 'POST':
        # Bot and dispatcher initialization


        #await register_handlers(dp)
        await process_event(event, dp)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}


if __name__ == "__main__" and os.getenv("IS_PROD") == "False":
    executor.start_polling(dp)