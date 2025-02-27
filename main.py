import asyncio

from bot.bot import init_bot
from database.models import init_db, OrderSchema, UserUpdateSchema

import database.requests as rq

from sqlalchemy.exc import NoResultFound

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app_: FastAPI):
    loop = asyncio.get_event_loop()
    db_task = loop.create_task(init_db())
    bot_task = loop.create_task(init_bot())
    
    try:
        yield
    finally:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            print('Бот остановлен')
        
        await db_task


app = FastAPI(title='SUPERFOOD App', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/api/items')
async def items():
    return await rq.get_items()


@app.get('/')
def hello():
    return {'message': 'Hello, World!'}


@app.post('/api/add_order')
async def add_order(order: OrderSchema):
    user = await rq.add_user(order.tg_id)
    await rq.add_order_to_database(user.id, order)
    return {'status': 'ok'}


@app.patch('/api/update_user_info')
async def update_user(update_user_data: UserUpdateSchema):
    await rq.update_user_info(update_user_data)
    return {'status': 'ok'}


@app.delete('/api/delete_user/{tg_id}')
async def delete_user(tg_id: int):
    try:
        await rq.delete_user(tg_id)
        return {"status": "ok"}
    except NoResultFound:
        return {"status": "not ok. The user was not found"}
        

if __name__ == "__main__":
    try:
        import uvicorn     
        uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True)
    except KeyboardInterrupt:
            print('Работа завершена')