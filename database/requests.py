from sqlalchemy import select, update, delete, func

from database.models import (
    async_session,
    User,
    Item,
    Order,
    ItemSchema,
    OrderSchema,
    UserUpdateSchema
)

async def add_order_to_database(user_id: int, order: OrderSchema):
    async with async_session() as session:
        new_order = Order(
            user=user_id,
            tg_id=order.tg_id,
            items=order.items,
            total_cost=order.total_cost,
            type_of_pay=order.type_of_pay,
            type_of_delivery=order.type_of_delivery,
            address=order.address,
            description=order.description
        )
        session.add(new_order)
        
        await session.commit()
        await session.refresh(new_order)
        

async def get_orders(user_id):
    async with async_session() as session:
        orders = await session.scalars(
            select(Order).where(Order.user == user_id)
        )
        
        serialized_orders = [
            OrderSchema.model_validate(i).model_dump() for i in orders
        ]
        
        return serialized_orders
        

async def add_user(tg_id):
    async with async_session() as session:
        
        user = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )
        
        if user:
            return user
        
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        
        await session.commit()
        await session.refresh(new_user)
        
        return new_user


async def update_user_info(new_info: UserUpdateSchema):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == new_info.tg_id).values(
                name=new_info.name,
                phone=new_info.phone,
                email=new_info.email
            )
        )
        await session.commit()


async def delete_user(tg_id: int):
    async with async_session() as session:
        await session.execute(
            delete(User).where(User.tg_id == tg_id)
        )
        await session.commit()


async def get_items():
    async with async_session() as session:
        
        items = await session.scalars(
            select(Item)
        )
        
        serialized_items = [
            ItemSchema.model_validate(i).model_dump() for i in items
        ]
        
        return serialized_items