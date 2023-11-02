from api import PetFriends
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet_with_valid_data(name="Артемис", animal_type="Кит",
                                      age='3', pet_photo="cat.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_update_pet_info_successfully(name="Шакал", animal_type="dog", age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_delete_pet_successfully():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_new_pet(auth_key, "Терминатор", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_create_pet_simple_successfully(name="Крыса", animal_type="Мышь", age="1"):
    '''Проверка метода простого добавления питомца (без фото) с валидными данными'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet_with_valid_data(self, pet_photo="images/kit.jpg"):
    '''Проверка метода добавления фото к существующему питомцу с валидными данными'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Lipa", "cat", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] is not None


def test_get_api_key_for_invalid_user(email="not_real_email@1secmail.net", password="not_real_password"):
    ''' Получение api-ключа с данными незарегистрированного пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password="sf_test"):
    '''Получение api-ключа с данными зарегистрированного пользователя с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_invalid_user_valid_password(email="surzhin@gmail.ru", password=valid_password):
    '''Получение api-ключа с опечаткой в электронной почте и правильным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
     ''' Получение списка питомцев с несуществующим api-ключом
     (замена api-ключа на несуществующий у существующего пользователя)'''
     _, auth_key = pf.get_api_key(valid_email, valid_password)
     auth_key = invalid_auth_key

     status, result = pf.get_list_of_pets(auth_key, filter)
     assert status != 200


def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Получение списка "моих питомцев" зарегистрированного пользователя'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_create_pet_simple_wrong_age(name="Тортилла", animal_type="черепаха", age="очень много"):
    '''Добавление питомца с неверно возрастом введеным текстом'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age


def test_post_new_pet_with_invalid_photo(name="Текст", animal_type="текстовый файл",
                                      age='мин', pet_photo="images/text.txt"):
    '''Добавления питомца с текстовым файлом вместо фото.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None


def test_create_pet_simple_invalid_data(name="", animal_type="", age=""):
    ''' Проверка метода простого добавления питомца (без фото) с пустыми полями.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name