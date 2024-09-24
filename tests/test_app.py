import pytest
from httpx import AsyncClient

from tests.conftest import client


def test_making_product():
    response1 = client.post("/products/", json={
        "name": "Carrot",
        "description": "Orange and yummy",
        "count": 10,
    })
    response2 = client.post("/products/", json={
        "name": "Potato",
        "description": "Yellow circle",
        "count": 15,
    })
    assert response1.status_code == 200 and response2.status_code == 200, "Not created products"
    assert response1.json()['id'] == 1
    assert response2.json()['id'] == 2

async def test_making_order(ac: AsyncClient):
    response1 = await ac.post("/orders/", json={
        "order_items": [
            {
                "product_id": 1,
                "count": 5
            },
            {
                "product_id": 2,
                "count": 7
            }
        ]
    })
    response2 = await ac.post("/orders/", json={
        "order_items": [
            {
                "product_id": 1,
                "count": 999
            }
        ]
    })
    response3 = await ac.post("/orders/", json={
        "order_items": [
            {
                "product_id": 6,
                "count": 2
            }
        ]
    })
    assert response1.status_code == 200, "Not created orders"
    assert response2.status_code == 400, "Error not recognized"
    assert response3.status_code == 404, "Error not recognized"

async def test_getting_items(ac: AsyncClient):
    response1 = await ac.get('/products/')
    response2 = await ac.get('/products/1')
    response3 = await ac.get('/orders/')
    response4 = await ac.get('/orders/1')
    assert response1.status_code == response2.status_code == \
           response3.status_code == response4.status_code == 200

async def test_updating_items(ac: AsyncClient):
    response1 = await ac.put('/products/2', json={
        "name": "Repa",
        "count": 20,
    })
    response2 = await ac.patch('/orders/1/status', json={
        "status": "sent"
    })
    assert response1.status_code == response2.status_code == 200, "Not created orders"
    assert response1.json()['count'] == 20, "Not changed entry"
    assert response2.json()['status'] == "sent", "Not changed entry"

async def test_deleting_items(ac: AsyncClient):
    await ac.delete('/products/2')
    response = await ac.get('/products/2')
    assert response.status_code == 404, "Object not deleted"
