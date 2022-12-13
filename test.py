from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = ""

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


params = {}
k = 0
sex = ['мужской', 'женский']
city = ['москва']
ages = [10, 90]

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # print(dir(event))
        if event.to_me:
            request = event.text
            if request == "Начать":
                k = 0
                write_msg(event.user_id, f"Привет")
                write_msg(event.user_id, f"Введите пол")
                k += 1
            elif k == 1:
                if request.lower() in sex:
                    params["sex"] = request
                    print(params["sex"])
                    write_msg(event.user_id, f"Введите город")
                    k += 1
                else:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif k == 2:
                if request.lower() in city:
                    params["city"] = request
                    print(params["city"])
                    write_msg(event.user_id, f"Введите минимальный возраст")
                    k += 1
                else:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif k == 3:
                try:
                    years = int(request)
                    if years >= ages[0] and years <= ages[1]:
                        params["min_age"] = years
                        print(params["min_age"])
                        write_msg(event.user_id, f"Введите максимальный возраст")
                        k += 1
                    else:
                        write_msg(event.user_id, f"Неверно введено значеие, введите заново")
                except ValueError:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif k == 4:
                try:
                    years = int(request)
                    if years >= ages[0] and years <= ages[1]:
                        params["max_age"] = years
                        print(params["max_age"])
                        k += 1
                        write_msg(event.user_id, f"Ищем людей по вашему запросу")




                    else:
                        write_msg(event.user_id, f"Неверно введено значеие, введите заново")
                except ValueError:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")