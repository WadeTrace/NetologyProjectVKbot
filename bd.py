import psycopg2
from tokens import database, user, password
from vkapi import VkUser, token as tk


class B_d:
    '''
    Класс взаимодействия с базой данных.
    В данных функция присутствует понятие пользоваетля и человека
    Пользователь это user
    Человек это people (тот кого ищет пользоваетль)
    '''

    def add_user(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция добавляет запись о пользоваетеле в таблице user
        c vk_id равным vk_id, переданным в функцию.
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                try:
                    B_d.user_id_by_vk_id(vk_id)
                except IndexError:
                    cur.execute("""
                    insert into users(vk_id, count_of_req, stage_of_req)
                    values(%s, %s, %s)
                    """, (vk_id, 0, 0))
                    conn.commit()


    def _count(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает значение столбца count_of_req(количесвто людей, которое человек запрашивал)
        пользователя c vk_id равным vk_id, переданным в функцию.
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select count_of_req from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def _uppdate_count(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция увеличивает значение count_of_req на 1
        пользователя c vk_id равным vk_id, переданным в функцию.
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    update users
                    set count_of_req = %s
                    where vk_id = %s;
                    """, (int(B_d.count(vk_id)) + 1, vk_id))


    def stage(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает "уровень" - stage_of_req запроса пользователя c vk_id равным vk_id, переданным в функцию.
        stage_of_req = 0 -> пользователь вводит пол того, кого хочет найти
        Минимальное значение stage_of_req = 0 (пользоваетль вводит пол), максимальное значение stage_of_req = 5 (пользователь ищет людей)
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select stage_of_req from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def uppdate_stage(vk_id, plus="1", db=database, u=user, p=password):
        '''

        :param vk_id:
        :param plus:

        :return:
        Функция увеличивает "уровень" - stage_of_req на 1 по умолчанию и обнуляет если в plus значение None или 0
        пользователя c vk_id равным vk_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                if B_d.stage(vk_id) == None:
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, (0, vk_id))
                elif plus == 0:
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, (0, vk_id))
                else:
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, (int(B_d.stage(vk_id)) + int(plus), vk_id))


    def user_id_by_vk_id(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает user_id пользователя c vk_id равным vk_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select user_id from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def people_id_by_vk_id(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает people_id человека с vk_id равным vk_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select people_id from people
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def add_people_in_last_req(user_vk_id, people_vk_id, db=database, u=user, p=password):
        '''

        :param user_id:
        :param people_vk_id:

        :return:
        Функция добавляет people_vk_id человека, которого пользователь просмотрел последним
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update users
                set last_req= %s
                where user_id = %s
                """, (people_vk_id, B_d.user_id_by_vk_id(user_vk_id) ))
                conn.commit()


    def get_people_in_last_req(user_vk_id, db=database, u=user, p=password):
        '''

        :param user_id:

        :return:
        Функция возвращает значение last_req пользоваетля с user_id равным user_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                select last_req from users
                where user_id = %s
                """, (B_d.user_id_by_vk_id(user_vk_id), ))
                conn.commit()

                return cur.fetchall()[0][0]


    def add_user_in_params(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция добавляет запись о пользоваетеле в таблице params
        c vk_id равным vk_id, переданным в функцию.
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into params(user_id)
                values(%s)
                """, (B_d.user_id_by_vk_id(vk_id), ))
                conn.commit()


    def add_min_age_in_params(min_age, vk_id, db=database, u=user, p=password):
        '''

        :param min_age:
        :param vk_id:

        :return:
        Функция добавляет параметр min_age пользоваетлю с vk_id равным vk_id
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set min_age = %s
                where user_id = %s
                """, (min_age, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_max_age_in_params(max_age, vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:
        :param max_age:

        :return:
        Функция добавляет параметр max_age пользоваетлю с vk_id равным vk_id
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set max_age = %s
                where user_id = %s
                """, (max_age, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_sex_in_params(sex, vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:
        :param sex:

        :return:
        Функция добавляет параметр sex пользоваетлю с vk_id равным vk_id
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set sex = %s
                where user_id = %s
                """, (sex, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_city_in_params(city, vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:
        :param city:

        :return:
        Функция добавляет параметр city пользоваетлю с vk_id равным vk_id
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set city = %s
                where user_id = %s
                """, (city, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_people(user_vk_id, people_vk_id, db=database, u=user, p=password):
        '''

        :param people_vk_id:

        :return:
        Функция обавляет запись человека с people_vk_id
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into people(vk_id)
                values(%s)
                """, (people_vk_id, ))
                conn.commit()


    def add_user_people(user_vk_id, people_vk_id, db=database, u=user, p=password):
        '''

        :param people_vk_id:
        :param user_vk_id:

        :return:
        Функция добавляет связь между человеком с people_vk_id равным people_vk_id, переданным в функцию
        и пользователем с user_vk_id равным user_vk_id, переданным в функцию в таблице user_people
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into user_people(user_id, people_id)
                values(%s, %s)
                """, (B_d.user_id_by_vk_id(user_vk_id), B_d.people_id_by_vk_id(people_vk_id)))
                conn.commit()


    def add_favorite_people(user_vk_id, people_vk_id, db=database, u=user, p=password):
        '''

        :param people_vk_id:
        :param user_vk_id:

        :return:
        Функция добавляет связь между человеком с people_vk_id равным people_vk_id, переданным в функцию
        и пользователем с user_vk_id равным user_vk_id, переданным в функцию в таблице favorite
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into favorite(user_id, people_id)
                values(%s, %s)
                """, (B_d.user_id_by_vk_id(user_vk_id), B_d.people_id_by_vk_id(people_vk_id)))
                conn.commit()


    def add_params(vk_id, min_age, max_age, sex, city, db=database, u=user, p=password):
        '''

        :param vk_id:
        :param min_age:
        :param max_age:
        :param sex:
        :param city:

        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into params(user_id, city, sex, min_age, max_age)
                values(%s, %s, %s, %s, %s)
                """, (B_d.user_id_by_vk_id(vk_id), city, sex, min_age, max_age))
                conn.commit()


    def del_all_data(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция удаляет все данные о пользователе с vk_id равным vk_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                    delete from params
                    where user_id = %s
                    """, (int(B_d.user_id_by_vk_id(vk_id)), ))

                    cur.execute("""
                    update users
                    set count_of_req = 0,
                    stage_of_req = 0
                    where user_id = %s
                    """, (int(B_d.user_id_by_vk_id(vk_id)),))

                    cur.execute("""
                    delete from user_people
                    where user_id = %s
                    """, (int(B_d.user_id_by_vk_id(vk_id)),))

                    cur.execute("""
                    delete from favorite
                    where user_id = %s
                    """, (int(B_d.user_id_by_vk_id(vk_id)),))
                    conn.commit()
                except IndexError:
                    pass


    def get_all_params(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает список всех параметров пользователя с vk_id равным vk_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                           select city, sex, min_age, max_age from params
                           where user_id = %s;
                           """, (B_d.user_id_by_vk_id(vk_id),))
                return cur.fetchall()[0]


    def get_people(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Функция возвращает следующего человека, увеличивая значение count_of_req пользователя
        с vk_id равным vk_id, переданным в функцию, на 1
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select people_id from user_people
                    where user_id = %s;
                    """, (B_d.user_id_by_vk_id(vk_id),))
                B_d._uppdate_count(vk_id)

                a = cur.fetchall()[B_d._count(vk_id)][0]

                cur.execute("""
                    select vk_id from people
                    where people_id = %s;
                    """, (a,))

                return cur.fetchall()[0][0]


    def del_last_favorite_people(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select people_id from favorite
                    where user_id = %s;
                    """, (B_d.user_id_by_vk_id(vk_id),))

                a = cur.fetchall()[-1][0]

                cur.execute("""
                    delete from favorite
                    where people_id = %s and user_id = %
                    """, (a, B_d.user_id_by_vk_id(vk_id)))


    def add_all_cities(list_of_cities, db=database, u=user, p=password):
        '''

        :param list_of_cities:
:
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                for city in list_of_cities:
                    cur.execute("""
                    insert into cities(name)
                    values(%s)
                    """, (city, ))
                    conn.commit()


    def vk_id_by_people_id(people_id, db=database, u=user, p=password):
        '''

        :param people_id:

        :return:
        Функция возвращает vk_id человека с people_id равным people_id, переданным в функцию
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select vk_id from people
                    where people_id = %s;
                    """, (people_id,))
                return cur.fetchall()[0][0]


    def get_favorite_people(vk_id, db=database, u=user, p=password):
        '''

        :param vk_id:

        :return:
        Выводит список избранных пользователя с vk_id равным vk_id, переданным в функцию, на 1
        '''
        with psycopg2.connect(database=db, user=u, password=p) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select people_id from favorite
                    where user_id = %s;
                    """, (B_d.user_id_by_vk_id(str(vk_id)),))

                return [int(B_d.vk_id_by_people_id(elem[0])) for elem in cur.fetchall()]


if __name__ == "__main__":
    # print(B_d.get_people('148884720'))
    print(B_d.people_id_by_vk_id('538873157'))
