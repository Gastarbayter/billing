from billing.db.engine import db
from billing.db.models import clients


@db.transaction()
async def get_client_by_id(client_id):
    query = clients.select().where(clients.client_id == client_id)
    res = await db.fetch_one(query=query)
    return res
