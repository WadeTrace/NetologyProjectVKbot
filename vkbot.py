from random import randrange
import json
from keyboard import choice_sex, next_people, again, start, favorite_people
import psycopg2
from bd import B_d
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vkapi import VkUser
from tokens import token_of_user as tk, token_of_community as token


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


sex = ['мужской', 'женский']
ages = [16, 90]


def write_msg(user_id, message, keyboard=None):
    if keyboard == None:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                                'keyboard': str(json.dumps(keyboard))})


def get_people_info(get_users, vk_id, event):
    people_id = B_d.get_people(vk_id)
    people = get_users.get_data_of_people(people_id)
    write_msg(event.user_id, f"{people[0]} {people[1]} ", next_people)
    write_msg(event.user_id, f"{people[2]} ", next_people)
    for elem in people[3]:
        write_msg(event.user_id, elem, next_people)
    return people_id


def main():
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            # print(dir(event))
            if event.to_me:
                vk_id = str(event.user_id)
                request = event.text
                if request == "Начать" or request == "Заново":
                    write_msg(event.user_id, f"Привет", start)
                    B_d.add_user(vk_id)
                    B_d.del_all_data(vk_id)
                    write_msg(event.user_id, f"Выбери пол того, кого хочешь найти", choice_sex)
                    B_d.uppdate_stage(vk_id, '1')
                    B_d.add_user_in_params(vk_id)
                elif B_d.stage(vk_id) == 1:
                    print("Пользоваетль подключен")

                    if request.lower() == "мужской" or request.lower() == "женский":
                        B_d.add_sex_in_params(request, vk_id)
                        write_msg(event.user_id, f"Введите город", again)
                        B_d.uppdate_stage(vk_id)
                elif B_d.stage(vk_id) == 2:
                    vk_us = VkUser(tk, "5.131")
                    cities = vk_us.get_all_cities()
                    if request.lower() in cities.keys():
                        B_d.add_city_in_params(cities[request.lower()], vk_id)
                        write_msg(event.user_id, f"Введите минимальный возраст (от 16 лет)")
                        B_d.uppdate_stage(vk_id)
                    else:
                        write_msg(event.user_id, f"Неверно введено значение, введите заново")
                elif B_d.stage(vk_id) == 3:
                    try:
                        years = int(request)
                        if years >= ages[0] and years <= ages[1]:
                            B_d.add_min_age_in_params(years, vk_id)
                            write_msg(event.user_id, f"Введите максимальный возраст")
                            B_d.uppdate_stage(vk_id)
                        else:
                            write_msg(event.user_id, f"Неверно введено значение, введите заново")
                    except ValueError:
                        write_msg(event.user_id, f"Неверно введено значение, введите заново")
                elif B_d.stage(vk_id) == 4:
                    try:
                        years = int(request)
                        if years >= ages[0] and years <= ages[1]:
                            B_d.add_max_age_in_params(years, vk_id)
                            B_d.uppdate_stage(vk_id)
                            write_msg(event.user_id, f"Ищем людей по вашему запросу", start)
                            all_params = B_d.get_all_params(vk_id)
                            print(all_params)
                            sex = all_params[1]
                            if sex.lower() == "мужской":
                                sex = "2"
                            else:
                                sex = "1"
                            get_users = VkUser(tk, "5.131")
                            peoples = get_users.search_users("", int(all_params[0]), sex, all_params[3], all_params[2])
                            for people_id in peoples:
                                try:
                                    if not(get_users.closed(people_id)):
                                        B_d.add_people(vk_id, str(people_id))
                                        B_d.add_user_people(vk_id, str(people_id))
                                except psycopg2.errors.UniqueViolation:
                                    if not (get_users.closed(people_id)):
                                        B_d.add_user_people(vk_id, str(people_id))
                            people_id = get_people_info(get_users, vk_id, event)
                        else:
                            write_msg(event.user_id, f"Неверно введено значение, введите заново")
                    except ValueError:
                        write_msg(event.user_id, f"Неверно введено значение, введите заново ")
                elif B_d.stage(vk_id) == 5 and request.lower() == "добавить в избранное":
                    get_users = VkUser(tk, "5.131")
                    B_d.add_favorite_people(vk_id, people_id)
                    people_id = get_people_info(get_users, vk_id, event)
                elif B_d.stage(vk_id) == 5 and request.lower() == "следующий":
                    get_users = VkUser(tk, "5.131")
                    people_id = get_people_info(get_users, vk_id, event)
                elif B_d.stage(vk_id) == 5 and request.lower() == "вывести список избранных":
                    favorite_peoples = B_d.get_favorite_people(vk_id)
                    get_users = VkUser(tk, "5.131")
                    for people_id in favorite_peoples:
                        people = get_users.get_data_of_people(people_id)
                        write_msg(event.user_id, f"{people[0]} {people[1]} ", favorite_people)
                        write_msg(event.user_id, f"{people[2]} ", favorite_people)
                        for elem in people[3]:
                            write_msg(event.user_id, elem, favorite_people)
                else:
                    write_msg(event.user_id, f"Неправильно введена команда")


if __name__ == '__main__':
    main()