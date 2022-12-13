from random import randrange

import psycopg2
from bd import B_d
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vkapi import VkUser, token as tk


token = "vk1.a.uvSWdZR6WWdEIOHoTLCI3x77cUVvGo1KCoIgo6iegN2edSNYCmmNBHht1FPs1KdbInQ16S5RP2Cl6PBJ89lQVFzWOflLk4rO1xlfv6AIRf_zp_1f256PJgpe4AjKmusezdsKdF6PuX7VcvDmD8hw1tqg9FzYhqxQ5WsEybDf1-n9KEnOB96CWD6Ln6eK4_TlINy5HKANPJwgQjmSB9gqsA"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


params = {}
k = 0
sex = ['мужской', 'женский']
city = ['москва', '1']
ages = [10, 90]

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # print(dir(event))
        if event.to_me:
            vk_id = str(event.user_id)
            request = event.text
            if request == "Начать" or request == "Заново":
                B_d.add_user(vk_id)
                B_d.del_all_data(vk_id)
                B_d.uppdate_stage(vk_id)
                write_msg(event.user_id, f"Привет")
                write_msg(event.user_id, f"Введите пол")
                B_d.uppdate_stage(vk_id, '1')
                B_d.add_user_in_params(vk_id)
            elif B_d.stage(vk_id) == 1:
                print("Пользоваетль подключен")
                if request.lower() in sex:
                    B_d.add_sex_in_params(request, vk_id)
                    write_msg(event.user_id, f"Введите город")
                    B_d.uppdate_stage(vk_id)
                else:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif B_d.stage(vk_id) == 2:
                if request.lower() in city:
                    B_d.add_city_in_params(request, vk_id)
                    write_msg(event.user_id, f"Введите минимальный возраст")
                    B_d.uppdate_stage(vk_id)
                else:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif B_d.stage(vk_id) == 3:
                try:
                    years = int(request)
                    if years >= ages[0] and years <= ages[1]:
                        B_d.add_min_age_in_params(years, vk_id)
                        write_msg(event.user_id, f"Введите максимальный возраст")
                        B_d.uppdate_stage(vk_id)
                    else:
                        write_msg(event.user_id, f"Неверно введено значеие, введите заново")
                except ValueError:
                    write_msg(event.user_id, f"Неверно введено значеие, введите заново")
            elif B_d.stage(vk_id) == 4:
                try:
                    years = int(request)
                    if years >= ages[0] and years <= ages[1]:
                        B_d.add_max_age_in_params(years, vk_id)
                        B_d.uppdate_stage(vk_id)
                        write_msg(event.user_id, f"Ищем людей по вашему запросу")


                        all_params = B_d.get_all_params(vk_id)
                        print(all_params)
                        sex = all_params[1]
                        if sex.lower() == "мужской":
                            sex = "2"
                        else:
                            sex = "1"

                        get_users = VkUser(tk, "5.131")
                        get_users = get_users.search_users("", 1, sex, all_params[3], all_params[2])
                        print(get_users)
                        for people_id in get_users:
                            try:
                                B_d.add_people(vk_id, str(people_id))
                            except psycopg2.errors.UniqueViolation:
                                pass
                            B_d.add_user_people(vk_id, str(people_id))
                        write_msg(event.user_id, f"{get_users}")
                        write_msg(event.user_id, f"{B_d.get_people(vk_id)}")
                    else:
                        write_msg(event.user_id, f"Неверно введено значеие, введите заново")
                except ValueError:
                    write_msg(event.user_id, f"Неверно ")