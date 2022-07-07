import os

import pytest

from app.posts.dao.posts_dao import PostsDAO

class TestPostDao:

    @pytest.fixture
    def posts_dao(self):
        #print(os.getcwd()) """поиск пути"""
        return PostsDAO("../../../data/posts.json")

    @pytest.fixture
    def keys_expected(self):
         return {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    #Полуение всех постов

    def test_get_all_check_type(self, posts_dao):
        posts = posts_dao.get_all()
        assert type(posts) == list, "Список постов должен быть списком"
        assert type(posts[0]) == dict, "Кажды пост должен быть словарем"

    def test_get_all_has_keys(self, posts_dao, keys_expected):
        posts = posts_dao.get_all()
        first_post = posts[0]

        first_post_keys = set(first_post.keys())
        assert first_post_keys == keys_expected, "Полученные ключи неверны"

    # Полуение одного поста

    def test_get_one_check_type(self, posts_dao):
        post = posts_dao.get_by_pk(1)
        assert type(post) == dict, "Пост должен быть словарем"

    def test_get_one_has_keys(self, posts_dao, keys_expected):
        post = posts_dao.get_by_pk(1)
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    parameters_to_get_by_pk = [1,2,3,4,5,6,7,8]
    @pytest.mark.parametrize("post_pk", parameters_to_get_by_pk)
    def test_get_one_check_type_has_correct_pk(self, posts_dao, post_pk):
        post = posts_dao.get_by_pk(post_pk)
        assert post["pk"] == post_pk, "Номер полученного поста не соотвествует номеру запрошенного"

    # Получение по пользователю

    post_parameters_by_pk = [("leo", {1, 5}), ("larry", {4, 8}), ("hank", {3, 7})]

    @pytest.mark.parametrize("poster_name, post_pks_correct", post_parameters_by_pk)
    def test_get_posts_by_pk(self, posts_dao, poster_name, post_pks_correct):
        """ Проверяет, что поиск по пользователю работает верно """

        posts = posts_dao.get_by_user(poster_name)
        post_pks = set()
        for post in posts:
            post_pks.add(post["pk"])

        assert post_pks == post_pks_correct

    ### ПОИСК ПОСТОВ

    def test_search_check_type(self, posts_dao):
        posts = posts_dao.search("a")
        assert type(posts) == list, "Результат поиска должен быть списком"
        assert type(posts[0]) == dict, "Элементы, найденные поиском должны быть словарем"

    def test_search_check_keys(self, posts_dao, keys_expected):
        post = posts_dao.search("a")[0]
        posts_keys = set(post.keys())
        assert posts_keys == keys_expected, "Полученные ключи неверны"

    queries_and_responses = [
        ("еда", [1]),
        ("дом", [2, 7, 8]),
        ("а", list(range(1, 8+1)))
    ]

    @pytest.mark.parametrize("query, post_pks", queries_and_responses)
    def test_search_correct_match(self, posts_dao, query, post_pks):
        posts = posts_dao.search(query)
        pks = []
        for post in posts:
           pks.append(post["pk"])

        assert pks == post_pks, f"Неверный поиск по запросу {query}"