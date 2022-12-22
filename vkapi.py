import requests
from pprint import pprint
from tokens import token_of_user as token, token_of_community as tok


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_users(self, q, city, sex, age_to, age_from, sorting=0):
        '''

        :param q:
        :param city:
        :param sex:
        :param age_to:
        :param age_from:
        :param sorting:

        :return:
        Возвращает список vk_id людей с подходящими параметрами, переданными в функцию
        '''
        users_search_url = self.url + 'users.search'
        users_search_params = {
            'q': q,
            'sort': sorting,
            'count': 300,
            'city': city,
            'sex': sex,
            'age_to': age_to,
            'age_from': age_from,
            'fields': "city, bdate"
        }
        req = requests.get(users_search_url, params={**self.params, **users_search_params}).json()
        req = [elem for elem in req['response']['items'] if "city" in elem.keys() and elem["city"]['id'] == city]
        req = [elem["id"] for elem in req]

        return req


    def get_data_of_people(self, vk_id):
        '''

        :param vk_id:

        :return:
        Возвращает кортеж данных о человеке с vk_id равным vk_id, переданным  функцию
        '''
        users_get_url = self.url + "users.get"
        users_get_params =\
        {
            'user_ids': vk_id,
            'fields': "about"
        }

        photos_get_url = self.url + "photos.getAll"
        photos_get_params = \
        {
            "owner_id": vk_id,
            "extended": 1
        }

        req = requests.get(users_get_url, params={**self.params, **users_get_params}).json()
        req2 = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()

        first_name = req['response'][0]['first_name']
        last_name = req['response'][0]['last_name']
        url = f"https://vk.com/id{vk_id}"
        id = []
        likes = []
        for elem in req2['response']['items']:
            id.append(elem['id'])
            likes.append(elem['likes']['count'])
        fotos_ids = self._foto_sorting(likes, id)[:3]
        attachments = []
        for id in fotos_ids:
            attachments.append('photo{}_{}'.format(vk_id, id))

        return (first_name, last_name, url, attachments)


    def _foto_sorting(self, l1, l2):
        '''

        :param l1:
        :param l2:

        :return:
        Возвращает отсортированный по убыванию массив l2, с помощью масива l1 с соответсвующими элементами
        '''
        for i in range(len(l1) - 1):
            for j in range(len(l1) - i - 1):
                if l1[j] < l1[j + 1]:
                    l1[j], l1[j + 1] = l1[j + 1], l1[j]
                    l2[j], l2[j + 1] = l2[j + 1], l2[j]
        return l2


    def closed(self, vk_id):
        '''

        :param vk_id:

        :return:
        Возвращает статус открытости профиля человека с vk_id равным vk_id, переданным  функцию
        '''
        users_get_url = self.url + "users.get"
        users_get_params =\
        {
            'user_ids': vk_id,
            'fields': "about"
        }
        try:
            req = (requests.get(users_get_url, params={**self.params, **users_get_params}).json())['response'][0]['is_closed']
            return req
        except KeyError:
            return True

    def get_all_cities(self, country_id=1):
        cities_get_url = self.url + "database.getCities"
        cities_get_params = \
            {
                'country_id': country_id,
                'need_all': 0,
                'q': ''
            }
        req = requests.get(cities_get_url, params={**self.params, **cities_get_params}).json()
        dict = {}
        for elem in req['response']['items']:
            dict[elem['title'].lower()] = elem['id']
        return dict

if __name__ == '__main__':
    get_users = VkUser(token, "5.131")
    # pprint(get_users.search_users('', 1, '1', 20, 20))
    pprint(get_users.get_all_cities())
