from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.database import Event, Ticket
from app.operations import (
    create_event,
    create_ticket,
    delete_ticket,
    get_all_tickets_for_show,
    get_ticket,
    update_ticket,
)


async def assert_tickets_table_is_empty(
    db_session: AsyncSession,
):
    async with db_session as session:
        result = await session.execute(select(Ticket))
    assert result.all() == []


async def test_create_ticket_for_rolling_stones(
    db_session_test,
):
    await assert_tickets_table_is_empty(db_session_test)

    ticket_id = await create_ticket(
        db_session_test, "Rolling Stones"
    )

    async with db_session_test as session:
        result = await session.execute(select(Ticket))
        items = result.scalars().all()

    assert ticket_id == 1
    assert len(items) == 1
    assert items[0].show == "Rolling Stones"


async def test_read_tickets_for_rolling_stone_show(
    fill_database_with_tickets, db_session_test
):
    tickets = await get_all_tickets_for_show(
        db_session_test, "The Rolling Stones Concert"
    )
    assert len(tickets) == 10


async def test_get_ticket(
    add_special_ticket, db_session_test
):
    ticket = await get_ticket(db_session_test, 1234)

    assert ticket.id == 1234
    assert ticket.show == "Special Show"


async def test_delete_ticket(
    add_special_ticket, db_session_test
):
    assert (
        await delete_ticket(db_session_test, 5555)
        is False
    )  # non existing ticket

    assert (
        await delete_ticket(db_session_test, 1234)
        is True
    )  # existing ticket

    await assert_tickets_table_is_empty(db_session_test)


async def test_update_ticket_price(
    add_special_ticket, db_session_test
):
    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"price": 100},
    )
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.price == 100

    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"price": None},
    )

    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.price is None


async def test_update_ticket_details(
    add_special_ticket, db_session_test
):
    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"details": {"seat": "A1"}},
    )
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.details.seat == "A1"

    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"details": {"seat": None}},
    )

    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.details.seat is None


async def test_create_event_without_tickets(
    db_session_test,
):
    await create_event(db_session_test, "Event 1")
    async with db_session_test as session:
        result = await session.execute(
            select(Event).options(
                joinedload(Event.tickets)
            )
        )
        event = result.scalars().first()
    assert event.name == "Event 1"
    assert len(event.tickets) == 0


async def test_create_event_with_10_tickets(
    db_session_test,
):
    await create_event(db_session_test, "Event 2", 10)
    async with db_session_test as session:
        result = await session.execute(
            select(Event).options(
                joinedload(Event.tickets)
            )
        )
        event = result.scalars().first()

    assert event.name == "Event 2"
    assert len(event.tickets) == 10
    assert event.tickets[0].show == "Event 2"
