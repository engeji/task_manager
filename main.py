
import new_task
import my_task
import auth
from aiogram import Bot, Dispatcher, executor, types
import json
async def process_event(event, dp:Dispatcher):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """
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
    
if __name__ == "__main__":
    new_task.executor.start_polling(new_task.dp)