import pytest

@pytest.mark.products
def test_get_all_products(products_api):
    res=products_api.get_all_products(); assert res.status_code==200
    assert len(res.json().get("products"))>0

@pytest.mark.products    
def test_get_product_id(products_api):
    res=products_api.get_product(1); assert res.status_code==200
    assert (res.json().get("id")) == 1

@pytest.mark.products    
def test_search_product(products_api):
    res=products_api.search_products("phone"); assert res.status_code==200
    keywords = ["mobile", "phone", "apple", "samsung"]
    assert any(kw.lower() in (res.json().get("products")[0].get("title") or "").lower() for kw in keywords)