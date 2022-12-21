choice_sex = {"one_time": True,
            "buttons": [[{
                "action":{
                      "type":"text",
                      "label":"Женский"
            },
                "color":"primary"
        }
            ],
            [
                {
                    "action":{
                      "type":"text",
                      "label":"Мужской"
            },
                    "color":"primary"
            }
        ]
    ]
}

start = {"one_time": True,
            "buttons": []
}

next_people = {"one_time": True,
            "buttons": [[{
                "action":{
                      "type":"text",
                      "label":"Следующий"
            },
                "color":"primary"
        }
            ],
[
                {
                    "action":{
                      "type":"text",
                      "label":"Добавить в избранное"
            },
                    "color":"primary"
            }
        ],
[
                    {
                        "action": {
                            "type": "text",
                            "label": "Вывести список избранных"
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Заново"
                        },
                        "color": "primary"
                    }
                ]
         ]
}

again = {"one_time": False,
            "buttons": [[{
                "action":{
                      "type":"text",
                      "label":"Заново"
            },
                "color":"primary"
            }
        ]
    ]
}


favorite_people = {"one_time": True,
                "buttons": [[{
                "action":{
                      "type": "text",
                      "label": "Следующий"
            },
                "color":"primary"
        }
            ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Заново"
                        },
                        "color": "primary"
                    }
                ]
         ]
}