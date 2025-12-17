import pytest

@pytest.mark.carts
def test_add_items_to_cart(carts_api, products_api):
    res = products_api.search_products("phone"); assert res.status_code==200
    product_id = res.json().get("products")[0].get("id")
    payload={
        "userId": 1,
        "products": [
            {
                "id": product_id,
                "quantity": 2
            }
        ]
    }
    res=carts_api.post_add_items_to_cart(payload); assert res.status_code==201
    assert res.json().get("products")[0].get("id") == product_id