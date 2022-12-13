import requests
from pprint import pprint


token = "vk1.a.Fy9cwRz_8PHbZNAx9Ep7OfsQQ_WwOe4gXjgPNpqYiE_VUWnvra2WgRWcAj1NbYM12DiE0HjFFLRlGKhf0zFye-TPdw4Dz5HpU4eEJTL9vVCG6Ty1g0cuHCXwz9v1G5ThMMXRNfcvaQ0c2jZCgtSLxeuBEK9QG1C7nzLS-KhFXB7GRcuHA9j0WALqRrolcXes5fczDYg82crNUfR--Bshwg"


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_users(self, q, city, sex, age_to, age_from, sorting=0):
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


if __name__ == '__main__':
    vk_user = VkUser(token, '5.131')
    vk_user.search_users('', 1, '2', 30, 20)