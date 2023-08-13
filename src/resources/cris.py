import json
import os

import i18n
import yaml
from flask import make_response

from .tracker import Tracker


valid_job_titles = [
    'Professoren', 'Außerplanmäßige Professoren', 'Vertretungsprofessoren',
    'Honorarprofessoren', 'Gastprofessoren', 'Juniorprofessoren',
    'Seniorprofessoren', 'Privatdozenten', 'Sekretariat', 'PostDoc',
    'Akademische Direktoren', 'Akademische Oberräte', 'Akademische Räte',
    'Wissenschaftliche Mitarbeiter', 'Mitarbeiter', 'Systemadministration',
    'Bibliothek', 'Geschäftsführer', 'Professor', 'Apl. Professor', 'Dekan',
    'TM_Professor_Supervisor',
]


class CrisTracker(Tracker):
    """
    CRIS class using the API of Uni-Muenster.

    DOCS: https://cris-api-staging.uni-muenster.de/
    """

    def __init__(self):
        """
        Initilization of CrisTracker class.

        Args:
            self
        """
        super().__init__()
        self.translations = {}

        self.url = 'https://cris-api-staging.uni-muenster.de/'
        self.header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://cris-api-staging.uni-muenster.de',
        }
        self.chairs = [
            {
                'chair_id': '84240358', 'chair_name': (
                    'Professur für Wirtschaftsinformatik,'
                    ' insbesondere Geschäftsprozessmanagement (Prof. vom Brocke)'
                ),
            },
            {
                'chair_id': '55472869', 'chair_name': (
                    'Juniorprofessur für'
                    ' IT-Sicherheit (Prof. Hupperich)'
                ),
            },
            {
                'chair_id': '77369668', 'chair_name': (
                    'Professur für'
                    ' Digitale Innovation und der öffentliche Sektor (Prof. Brandt)'
                ),
            },
            {
                'chair_id': '59575309', 'chair_name': (
                    'Professur für'
                    ' Maschinelles Lernen und Data Engineering (Prof. Gieseke)'
                ),
            },
            {
                'chair_id': '79139069', 'chair_name': (
                    'Juniorprofessur für'
                    ' Wirtschaftsinformatik, insbesondere Digitale Transformation'
                    ' und Gesellschaft (Prof. Berger)'
                ),
            },
            {
                'chair_id': '31914156', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Informationsmanagement (Prof. Becker)'
                ),
            },
            {
                'chair_id': '40279283', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Interorganisationssysteme (Prof. Klein)'
                ),
            },
            {
                'chair_id': '40279415', 'chair_name': (
                    'Institut für'
                    ' Wirtschaftsinformatik - Mathematik für Wirtschaftswissenschaftler'
                ),
            },
            {
                'chair_id': '40279346', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Logistik (Prof. Hellingrath)'
                ),
            },
            {
                'chair_id': '40279220', 'chair_name': (
                    'Professur für'
                    ' Statistik und Optimierung (Prof. Trautmann)'
                ),
            },
            {
                'chair_id': '40279157', 'chair_name': (
                    'Lehrstuhl für'
                    ' Praktische Informatik in der Wirtschaft (Prof. Kuchen)'
                ),
            },
            {
                'chair_id': '31921637', 'chair_name': (
                    'Lehrstuhl für'
                    ' Informatik (Prof. Vossen)'
                ),
            },
            {
                'chair_id': '31923392', 'chair_name': (
                    'Institut für'
                    ' Wirtschaftsinformatik'
                ),
            },
        ]
        self.employees = []  # list of dicts with an employee_id and employees chair
        self.result = []  # to return
        self.chair_keys = {
            chair['chair_name']: 'chair' +
            str(index + 1) for index, chair in enumerate(self.chairs)
        }

    def split_list(self, input_list, max_length):
        """Splitting the input list into lists with len(max_length).

        Returns the list a list of lists with max_length.
        """
        return [input_list[i:i+max_length] for i in range(0, len(input_list), max_length)]

    def update_employees(self):
        """Append all employee_ids of the chairs to cris instance."""
        for chair in self.chairs:
            request_is_necessary = True
            paginator = ''
            while request_is_necessary:
                payload = {
                    'query': f"""
                            query {{
                                organisation(id:{chair["chair_id"]}){{
                                    connections{{
                                        persons(first:100, after:"{paginator}"){{
                                        pageInfo{{
                                        startCursor
                                        endCursor }}
                                            edges{{
                                                node{{
                                                    id
                                                    status
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                            """,
                }
                response = json.loads(
                    self.session.post(
                        self.url, headers=self.header, json=payload,
                    ).text,
                )

                if len(
                    response['data']['organisation']
                    ['connections']['persons']['edges'],
                ) != 100:
                    request_is_necessary = False
                else:
                    paginator = (
                        response['data']['organisation']
                        ['connections']['persons']['pageInfo']['endCursor']
                    )

                for employee in (
                    response['data']['organisation']
                    ['connections']['persons']['edges']
                ):
                    # only people with status 3 => active
                    if employee['node']['status'] != 3:
                        continue

                    self.employees.append({
                        'id': employee['node']['id'],
                        'chair': chair['chair_name'],
                    })

        return

    def update_result(self):  # noqa: 901
        """Appends dicts with infos about employees to result list."""
        employee_ids = [item['id'] for item in self.employees]
        # split employee ids up in list of 100 entries
        employee_ids_splitted = self.split_list(employee_ids, 100)
        employee_chairs = [item['chair'] for item in self.employees]
        employee_chairs_splitted = self.split_list(employee_chairs, 100)
        for loids, lochairs in zip(
            employee_ids_splitted,
            employee_chairs_splitted,
        ):
            payload = {
                'query':
                f"""
                                query {{
                                  nodes(ids: {list(map(int,loids))}) {{
                                    ... on Person {{
                                      node {{
                                      academicTitle
                                      cfFirstNames
                                      cfFamilyNames
                                      status
                                      }}
                                      connections {{
                                        cards {{
                                          edges {{
                                            node {{
                                              roomNumber
                                              email
                                              phone
                                              status
                                              id
                                              jobTitle
                                            }}
                                          }}
                                        }}
                                      }}
                                      connections {{
                                        pictures{{
                                          edges{{
                                            node{{
                                              id
                                            }}
                                          }}
                                        }}
                                      }}
                                    }}
                                  }}
                                }}
                            """,
            }
            response = {
                'persons': json.loads(
                    self.session.post(
                        self.url, headers=self.header, json=payload,
                    ).text,
                ),
                'chairs': lochairs,
            }

            persons = response['persons']['data']['nodes']
            for person in persons:
                emails = []
                phones = []
                cards = []
                job_titles = []
                room_number = None
                for edge in person['connections']['cards']['edges']:
                    # JOB TITLES OF INACTIVE CARDS ALSO GET ADDED
                    # DUE TO SOME PEOPLE HAVING JOBTITLE=NULL IN THEIR ACTIVE CARD
                    job_title = edge['node']['jobTitle']
                    if job_title not in job_titles and job_title is not None:
                        job_titles.append(job_title)
                    # only active cards
                    if int(edge['node']['status']) != 3:
                        continue
                    email = edge['node']['email']
                    phone = edge['node']['phone']
                    card = edge['node']['id']
                    if email not in emails and email is not None:
                        emails.append(email)
                    if phone not in phones and phone is not None:
                        phones.append(phone)
                    if card not in cards and card is not None:
                        cards.append(card)
                    if room_number is None and edge['node']['roomNumber'] is not None:
                        room_number = edge['node']['roomNumber']
                picture_id = None
                if person['connections']['pictures']['edges']:  # noqa: 501
                    picture_id = person['connections']['pictures']['edges'][0]['node']['id']  # noqa: 501

                self.result.append({
                    'academicTitle': person['node']['academicTitle'],
                    'cfFirstNames': person['node']['cfFirstNames'],
                    'cfFamilyNames': person['node']['cfFamilyNames'],
                    'roomNumber': room_number,
                    'emails': emails,
                    'phones': phones,
                    'card_ids': cards,
                    'jobTitle': job_titles,
                    'image': picture_id,
                    'chairs': [],
                })
        return

    def remove_duplicate_employees(self):
        """Function that removes duplicates from an employee list.

        Keeps the first entry and removes all subsequent entries.
        """
        temp_dict = {i['id']: i for i in reversed(self.employees)}
        result = list(temp_dict.values())[::-1]
        return result

    def add_chairs(self):
        """Function that bulk queries the cards and adds chair info."""
        all_card_ids = [
            {'index': index, 'card_id': card_id} for index, result in enumerate(
                self.result,
            ) for card_id in result['card_ids']
        ]
        print(len(all_card_ids))
        all_ids = [
            card_id for result in self.result for card_id in result['card_ids']
        ]
        list_of_lists = self.split_list(all_ids, 100)

        card_index = 0  # Counter to keep track of the current card in all_card_ids
        for loc in list_of_lists:
            payload = {
                'query':
                f"""query{{
                      nodes(ids: {list(map(int,loc))}) {{
                        ... on Card {{
                          connections {{
                            organisations {{
                              edges {{
                                node {{
                                  cfName
                                }}
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}""",
            }
            response = json.loads(
                self.session.post(
                    self.url, headers=self.header, json=payload,
                ).text,
            )

            for result in response['data']['nodes']:
                # Get the corresponding card from all_card_ids
                card = all_card_ids[card_index]
                chair_name = (
                    result['connections']['organisations']
                    ['edges'][0]['node']['cfName']
                )
                self.result[card['index']]['chairs'].append(
                    chair_name,
                )  # index from current card["index"]
                card_index += 1  # Increment the card_index for the next iteration

    def filter_and_add_keys(self):
        """Function that filters and adds keys.

        Address depends on the chair the person is working in.
        """
        new_result = []
        for card in self.result:
            # filter out all people that do not have at
            # least one valid jobTitle
            if not any(job_title in valid_job_titles for job_title in card['jobTitle']):
                continue
            # filter out all people that do not have at
            # least one of the pre-defined chairs
            if not any(
                chair['chair_name'] in
                '\t'.join(card['chairs']) for chair in self.chairs
            ):
                continue
            card['cfFullName'] = f'{card["cfFirstNames"]} {card["cfFamilyNames"]}'
            if (
                'Prof. Klein' in '\t'.join(card['chairs']) or
                'Prof. Berger' in '\t'.join(card['chairs'])
            ):
                card['address'] = 'Leonardo-Campus 11'
            else:
                card['address'] = 'Leonardo-Campus 3'
            new_result.append(card)
        self.result = new_result
        return

    def get_translation(self, lang):
        """
        Translates chair names from German to English using i18n package.

        Args:
            lang: Language code (e.g., 'en' for English, 'de' for German)

        Returns:
          None
        """
        i18n.set('locale', lang)
        i18n.set('fallback', 'de')

        # Get the directory containing this script
        base_dir = os.path.dirname(__file__)

        # Construct the path to the YAML file
        yaml_file = os.path.join(base_dir, 'cris.en.yaml')
        # Load translations from the YAML file
        with open(yaml_file) as f:
            translations = yaml.safe_load(f)

        for chair in self.chairs:
            chair_key = self.chair_keys[chair['chair_name']]

            translation = translations.get(lang, {}).get(
                chair_key, chair['chair_name'],
            )
            chair['chair_name_en'] = translation

    def get_cris_data(self, lang):
        """Function that returns the desired result."""
        self.update_employees()
        self.employees = self.remove_duplicate_employees()
        self.update_result()
        self.add_chairs()
        if lang == 'en':
            self.get_translation(lang)

        self.filter_and_add_keys()

        for card in self.result:
            for chair in self.chairs:
                if card['chairs'] == chair['chair_name']:
                    if lang == 'en':
                        card['chairs'] = chair['chair_name_en']
                    break

        return make_response(
            json.dumps(self.result, ensure_ascii=False), 200,
            {'Content-Type': 'application/json', 'charset': 'utf-8'},
        )
