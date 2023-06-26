from aiogram.utils.executor import start_webhook
from bot import dp, bot,token
from functions_bot import start,registration_user, edit_profile, raport, admin
from datadase.models import Base, engine
from Middleware.throttling import ThrottlingMiddleware
from Middleware.checking_user_registration import RegistrationMiddleware
from aiogram import executor

start.register_start_command(dp)
registration_user.register_registration_command(dp)
registration_user.regiser_callbak_query(dp)
edit_profile.register_edit_command(dp)
edit_profile.register_edit_callback_query(dp)

raport.register_create_raport_command(dp)
raport.register_create_raport_callback_query(dp)

admin.register_count_user(dp)
# webhook settings
WEBHOOK_HOST = 'https://212.113.123.25'  # имя домена
WEBHOOK_PATH ='/webhook/'  # адрес, который будет обрабатывать запросы
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '212.113.123.25'  # or ip
WEBAPP_PORT = 80

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()



if __name__ == '__main__':
   Base.metadata.create_all(bind=engine)
   dp.middleware.setup(ThrottlingMiddleware())
   executor.start_polling(dp)
    # dp.middleware.setup(RegistrationMiddleware())
#    start_webhook(
#        dispatcher=dp,
#        webhook_path=WEBHOOK_PATH,
#        on_startup=on_startup,
#        on_shutdown=on_shutdown,
#        skip_updates=True,
#        host="0.0.0.0",
#        port=WEBAPP_PORT,
#    )
