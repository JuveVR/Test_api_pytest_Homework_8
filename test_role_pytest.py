from Homework_6.Exercise_1 import book_dict, role_dict, base_url_book, base_url_role, add_new_item, add_item_id, check_item_in_list, \
    compare_dicts, check_new_item, role_update_and_check, delete_item_finally
import pytest
import uuid
import random


class TestAddNewRole:
    @pytest.fixture()
    def setup_and_teardown(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        self.role_dict = role_dict
        role_dict["book"] = "{}{}".format(base_url_book, self.book_id)
        yield
        delete_item_finally(base_url_role, self.role_id)
        delete_item_finally(base_url_book, self.book_id)

    def test_new_role_id_type(self, setup_and_teardown):
        self.role_id = add_new_item(base_url_role, role_dict)
        assert type(self.role_id) == str

    def test_new_role_id_emptiness(self, setup_and_teardown):
        self.role_id = add_new_item(base_url_role, role_dict)
        assert self.role_id

    def test_creation_without_level(self, setup_and_teardown):
        wrong_role = {"name": "Mtsiri",
                      "type": "classic",
                      "book": "{}{}".format(base_url_book, self.book_id),
                      "level": None
                      }
        self.role_id = add_new_item(base_url_role, wrong_role)
        assert type(self.role_id) == str

    def test_creation_without_book(self, setup_and_teardown):
        wrong_role = {"name": "Mtsiri",
                      "type": "classic",
                      "book": None,
                      "level": 122
                      }
        self.role_id = add_new_item(base_url_role, wrong_role)
        assert self.role_id


class TestAddNewRoleExept:
    def test_creation_without_name(self, wrong_roles_test):
        (wrong_role_dict, error) = wrong_roles_test
        with pytest.raises(Exception) as ex:
             add_new_item(base_url_role, wrong_role_dict)
        assert error == str(ex.value)


class TestAddItemIdFunc:
    def test_correct_addition(self, param_test):
        (input, expected_output) = param_test
        add_item_id(input, expected_output)
        assert input["id"] == expected_output


class TestDictCompareFunc:
    @pytest.fixture()
    def setup(self):
        self.dict1 = {"name": "Mtsiri", "type": "classic", "book": "http://pulse-rest-testing.herokuapp.com/books/6631", "level": 1212, "id": 22}
        self.dict2 = {"name": "Mtsiri", "type": "classic", "book": "http://pulse-rest-testing.herokuapp.com/books/6631", "level": 1212, "id": 22}
        self.dict3 = {"name": "Mtsiri", "type": "classic", "book": "http://pulse-rest-testing.herokuapp.com/books/6631", "level": 1212, "id": 14}

    def test_compare_equal(self,setup):
        result = compare_dicts(self.dict1, self.dict2)
        assert result is None

    def test_compare_not_equal(self, setup):
        with pytest.raises(Exception) as ex:
            compare_dicts(self.dict2, self.dict3)
        assert "Dicts are not equal" == str(ex.value)


class TestCheckNewItemRole:
    def setup_method(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        self.role_dict = role_dict
        role_dict["book"] = "{}{}".format(base_url_book, self.book_id)
        self.role_id = add_new_item(base_url_role, role_dict)

    def teardown_method(self):
        delete_item_finally(base_url_book, self.book_id)
        delete_item_finally(base_url_role, self.role_id)

    def test_check_correct_data(self):
        result = check_new_item(base_url_role, self.role_id, role_dict)
        assert result is None

    def test_check_with_wrong_id(self):
        with pytest.raises(Exception) as ex:
            check_new_item(base_url_role, str(random.randint(4000000000, 9120000001)), role_dict)
        assert "Wrong request" == str(ex.value)

    def test_role_in_list(self):
        result = check_item_in_list(base_url_role, self.role_id, role_dict)
        assert result is None

    def test_role_in_list_wrong_id(self):
        with pytest.raises(Exception) as ex:
            check_item_in_list(base_url_role, str(random.randint(4000000000, 9120000001)), role_dict)
        assert "The item is not in the list" == str(ex.value)


class TestRoleUpdate:
    def setup_method(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        self.role_dict = role_dict
        role_dict["book"] = "{}{}".format(base_url_book, self.book_id)
        self.role_id = add_new_item(base_url_role, role_dict)

    def teardown_method(self):
        delete_item_finally(base_url_book, self.book_id)
        delete_item_finally(base_url_role, self.role_id)

    def test_updated_data(self):
        result = role_update_and_check(base_url_role, self.role_id, role_dict, new_name=str(uuid.uuid4()),
                                       new_type=str(uuid.uuid4()), new_book=role_dict["book"], new_level=random.randint(40000000, 2147483647))
        assert result is None

    def test_update_one_parameter(self):
        result = role_update_and_check(base_url_role, self.role_id, role_dict, new_name="vova", new_book=role_dict["book"])
        assert result is None

    def test_update_attempt_wrong_id(self):
        with pytest.raises(Exception) as ex:
            role_update_and_check(base_url_role, str(random.randint(4000000000, 9120000001)), role_dict,
                                           new_name=str(uuid.uuid4()), new_type=str(uuid.uuid4()))
        assert "Wrong request" == str(ex.value)

    def test_attempt_update_wrong_url(self):
        with pytest.raises(Exception) as ex:
            role_update_and_check(base_url_role+"wrong", str(random.randint(4000000000, 9120000001)), role_dict,
                                           new_name=str(uuid.uuid4()), new_type=str(uuid.uuid4()))
        assert "Wrong request" == str(ex.value)


class TestDeleteItemFunc:
    @pytest.fixture()
    def setup(self):
        self.book_id = add_new_item(base_url_book, book_dict)
        self.role_dict = role_dict
        role_dict["book"] = "{}{}".format(base_url_book, self.book_id)
        self.role_id = add_new_item(base_url_role, role_dict)
        yield
        delete_item_finally(base_url_book, self.book_id)

    def test_delete_existent(self, setup):
        # new_test_id = add_new_item(base_url_role, role_dict)
        result = delete_item_finally(base_url_role, self.role_id)
        assert result is None

    def test_try_delete_with_id_none(self):
        with pytest.raises(Exception) as ex:
            delete_item_finally(base_url_role, None)
        assert "Item id is None" == str(ex.value)

    def test_try_delete_with_wrong_id(self):
        with pytest.raises(Exception) as ex:
            delete_item_finally(base_url_role, str(random.randint(4000000000, 9120000001)))
        assert "Wrong request status code. Item hasn't been deleted" == str(ex.value)
