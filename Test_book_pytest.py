from Homework_6.Exercise_1 import book_dict, base_url_book, add_new_item, add_item_id, check_item_in_list, \
    compare_dicts, check_new_item, book_update_and_check, delete_item_finally
import pytest
import uuid
import random


class TestAddNewBook:
    def setup_method(self):
        self.book_dict = book_dict

    def teardown_method(self):
        delete_item_finally(base_url_book, self.book_id)

    def test_new_book_id_type(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        assert type(self.book_id) == str

    def test_new_book_id_emptiness(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        assert bool(self.book_id) == True, "value is False or None, the string shouldn't be empty"


class TestAddNewBookNegative:
    def test_creation_without_title(self):
        wrong_book = {"title": None, "author": "Myauthor"}
        with pytest.raises(Exception) as exepinfo:
            add_new_item(base_url_book, wrong_book)
        assert "Item hasn't been added" in str(exepinfo.value)


    def test_creation_without_author(self):
        wrong_book = {"title": "Mytitle", "author": None}
        with pytest.raises(Exception) as exepinfo:
            add_new_item(base_url_book, wrong_book)
        assert "Item hasn't been added" in str(exepinfo.value)


class TestAddItemIdFunc:
    def test_correct_addition(self):
        book = {"title": "Mytitle", "author": "My_author"}
        add_item_id(book, 22)
        assert book["id"] == 22

    def test_correct_id_update(self):
        book = {"title": "Mytitle", "author": "My_author", "id": 100}
        add_item_id(book, 1)
        assert book["id"] == 1


class TestDictCompareFunc:
    @pytest.fixture()
    def setup(self):
        self.dict1 = {"title": "Mytitle", "author": "My_author", "id": 100}
        self.dict2 = {"title": "Mytitle", "author": "My_author", "id": 100}
        self.dict3 = {"title": "Mytitle", "author": "My_author", "id": 20200}

    def test_compare_equal(self,setup):
        result = compare_dicts(self.dict1, self.dict2)
        assert result is None

    def test_compare_not_equal(self,setup):
        with pytest.raises(Exception) as exepinfo:
            compare_dicts(self.dict2, self.dict3)
        assert "Dicts are not equal" in str(exepinfo.value)


class TestCheckNewItemBook:
    @pytest.fixture()
    def setup_and_teardown(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        yield
        delete_item_finally(base_url_book, self.book_id)

    def test_check_correct_data(self, setup_and_teardown):
        result = check_new_item(base_url_book, self.book_id, book_dict)
        assert result is None

    def test_check_with_wrong_id(self, setup_and_teardown):
        with pytest.raises(Exception) as ex:
            check_new_item(base_url_book, str(random.randint(4000000000, 9120000001)), book_dict)
        assert "Wrong request" == str(ex.value)

    def test_book_in_list(self, setup_and_teardown):
        result = check_item_in_list(base_url_book, self.book_id, book_dict)
        assert result is None

    def test_book_in_list_wrong_id(self, setup_and_teardown):
        with pytest.raises(Exception) as ex:
            check_item_in_list(base_url_book, str(random.randint(4000000000, 9120000001)), book_dict)
        assert "The item is not in the list" == str(ex.value)


class TestBookUpdate:
    def setup_method(self):
        self.book_id = add_new_item(base_url_book, book_dict)

    def teardown_method(self):
        delete_item_finally(base_url_book, self.book_id)

    def test_updated_data(self):
        result = book_update_and_check(base_url_book, self.book_id, book_dict, new_title=str(uuid.uuid4()),
                                       new_author=str(uuid.uuid4()))
        assert result is None

    def test_update_one_parameter(self):
        result = book_update_and_check(base_url_book, self.book_id, book_dict, new_title=str(uuid.uuid4()))
        assert result is None

    def test_update_attempt_wrong_id(self):
        with pytest.raises(Exception) as ex:
            book_update_and_check(base_url_book, str(random.randint(4000000000, 9120000001)), book_dict,
                                           new_title=str(uuid.uuid4()), new_author=str(uuid.uuid4()))
        assert "Wrong request" == str(ex.value)

    def test_attempt_update_wrong_url(self):
        with pytest.raises(Exception) as ex:
            book_update_and_check(base_url_book+"wrong", str(random.randint(4000000000, 9120000001)), book_dict,
                                           new_title=str(uuid.uuid4()), new_author=str(uuid.uuid4()))
        assert "Wrong request", str(ex.value)


class TestDeleteItemFunc:
    @pytest.fixture()
    def setup(self):
        self.book_id = add_new_item(base_url_book, book_dict)

    def test_delete_existent(self, setup):
        result = delete_item_finally(base_url_book, self.book_id)
        assert result is None

    def test_try_delete_with_id_none(self):
        with pytest.raises(Exception) as ex:
            delete_item_finally(base_url_book, None)
        assert "Item id is None" == str(ex.value)

    def test_try_delete_with_wrong_id(self):
        with pytest.raises(Exception) as ex:
            delete_item_finally(base_url_book, str(random.randint(4000000000, 9120000001)))
        assert "Wrong request status code. Item hasn't been deleted" == str(ex.value)


