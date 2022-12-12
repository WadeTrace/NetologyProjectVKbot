import psycopg2


class B_d:
    def add_user(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                if not(B_d.user_id_by_vk_id(vk_id)):
                    cur.execute("""
                    insert into users(vk_id)
                    values(%s)
                    """, (vk_id, ))
                    conn.commit()


    def count(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select count_of_req from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def uppdate_count(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                if B_d.count(vk_id) == None:
                    cur.execute("""
                        update users
                        set count_of_req = %s
                        where vk_id = %s;
                        """, ('1', vk_id))
                else:
                    cur.execute("""
                        update users
                        set count_of_req = %s
                        where vk_id = %s;
                        """, (str(int(B_d.count(vk_id)) + 1), vk_id))


    def stage(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select stage_of_req from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def uppdate_stage(vk_id, plus="1"):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                if B_d.count(vk_id) == None:
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, ('0', vk_id))
                elif plus == '0':
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, ('0', vk_id))
                else:
                    cur.execute("""
                        update users
                        set stage_of_req = %s
                        where vk_id = %s;
                        """, (str(int(B_d.stage(vk_id)) + int(plus)), vk_id))


    def user_id_by_vk_id(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select user_id from users
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def people_id_by_vk_id(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select people_id from people
                    where vk_id = %s;
                    """, (vk_id,))
                return cur.fetchall()[0][0]


    def add_user_in_params(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into params(user_id)
                values(%s)
                """, (B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_min_age_in_params(min_age, vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set min_age = %s
                where user_id = %s
                """, (min_age, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_max_age_in_params(max_age, vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set max_age = %s
                where user_id = %s
                """, (max_age, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_sex_in_params(sex, vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set sex = %s
                where user_id = %s
                """, (sex, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_city_in_params(city, vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set city = %s
                where user_id = %s
                """, (city, B_d.user_id_by_vk_id(vk_id)))
                conn.commit()


    def add_people(user_vk_id, people_vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into people(vk_id)
                values(%s)
                """, (people_vk_id))

                cur.execute("""
                insert into user_people(user_id, people_id)
                values(%s, %s)
                """, (B_d.user_id_by_vk_id(user_vk_id), B_d.people_id_by_vk_id(people_vk_id)))
                conn.commit()


    def add_favorite_people(user_vk_id, people_vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into favorite(user_id, people_id)
                values(%s, %s)
                """, (B_d.user_id_by_vk_id(user_vk_id), B_d.people_id_by_vk_id(people_vk_id)))
                conn.commit()


    def add_params(vk_id, min_age, max_age, sex, city):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                insert into params(user_id, city, sex, min_age, max_age)
                values(%s, %s, %s, %s, %s)
                """, (B_d.user_id_by_vk_id(vk_id), city, sex, min_age, max_age))
                conn.commit()


    def del_all_data(vk_id):
        with psycopg2.connect(database="vkbotnet", user="postgres", password="Ivanov-1808") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                update params
                set city = NULL,
                sex = NULL,
                min_age = NULL,
                max_age = NULL
                where user_id = %s
                """, (int(B_d.user_id_by_vk_id(vk_id)), ))

                cur.execute("""
                update users
                set count_of_req = NULL,
                stage_of_req = NULL
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
