import vk_api
import requests
from pprint import pprint



token = "vk1.a.uvSWdZR6WWdEIOHoTLCI3x77cUVvGo1KCoIgo6iegN2edSNYCmmNBHht1FPs1KdbInQ16S5RP2Cl6PBJ89lQVFzWOflLk4rO1xlfv6AIRf_zp_1f256PJgpe4AjKmusezdsKdF6PuX7VcvDmD8hw1tqg9FzYhqxQ5WsEybDf1-n9KEnOB96CWD6Ln6eK4_TlINy5HKANPJwgQjmSB9gqsA"


vk = vk_api.VkApi(token=token)


params = {
    "user_ids" : "1",
    "access_token": token,
    "v": "5.131"
    }

href = "https://api.vk.com/method/"

req = requests.get(f"{href}users.get", params).json()

pprint(req)

print(int("d"))