from Homework_6.Exercise_1 import book_dict,  base_url_book,  add_new_item, delete_item_finally

import random
import pytest

#Fixture with parameters for TestAddItemIdFunc
roles_list = [({"name": "Mtsiri",
                "type": "classic",
                "book": "http://pulse-rest-testing.herokuapp.com/books/6631",
                "level": 1212
                }, 22),
              ({"name": "Mtsiri",
                "type": "classic",
                "book": "http://pulse-rest-testing.herokuapp.com/books/6631",
                "level": 1212,
                "id": 22
                }, 1)]

@pytest.fixture(scope="function", params=roles_list, ids=["id_addition", "id_replace"])
def param_test(request):
    return request.param




#Fixture with parameters for TestAddNewRoleExept
@pytest.fixture()
def book_create():
    return add_new_item(base_url_book, book_dict)

book_id = book_create # looks weird, but my fixture doesn't work without this var declaration

wrong_roles_list = [({"name": None,
                    "type":"detective",
                    "book": "{}{}".format(base_url_book, book_id),
                    "level": 100500
                    }, "Item hasn't been added"),
                    ({"name": "Mtsiri",
                    "type": None,
                    "book": "{}{}".format(base_url_book, book_id),
                    "level": 100500
                    }, "Item hasn't been added"),
                    ({"name": "Mtsiri",
                    "type": "classic",
                    "book": "{}{}".format(base_url_book, book_id),
                    "level": "level"
                    }, "Item hasn't been added"),
                    ({"name": "Mtsiri",
                    "type": "classic",
                    "book": "{}{}".format(base_url_book, str(random.randint(4000000000, 9120000001))),
                    "level": 1212}, "Item hasn't been added")]

@pytest.fixture(scope="function", params=wrong_roles_list, ids=["without_name", "without_type", "str_level", "wrong_book"])
def wrong_roles_test(book_create, request):
    book_id = book_create
    yield request.param
    delete_item_finally(base_url_book, book_id)
