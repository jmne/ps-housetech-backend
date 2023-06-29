import json

from .tracker import Tracker
# import xmltodict


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
        self.url = 'https://cris-api-staging.uni-muenster.de/'
        self.base_picture_url = '''https://www.uni-muenster.de/converis/
                                    ws/public/infoobject/get/Picture/'''
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
                'chair_id': '31914156', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Informationsmanagement (Prof. Becker)'
                ),
            },
            {
                'chair_id': '31923392', 'chair_name': (
                    'Institut für'
                    ' Wirtschaftsinformatik'
                ),
            },
            {
                'chair_id': '40279283', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Interorganisationssysteme (Prof. Klein)'
                ),
            },
            {
                'chair_id': '40279346', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Logistik (Prof. Hellingrath)'
                ),
            },
            {
                'chair_id': '40279415', 'chair_name': (
                    'Institut für'
                    ' Wirtschaftsinformatik - Mathematik für Wirtschaftswissenschaftler'
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
                'chair_id': '40279220', 'chair_name': (
                    'Professur für'
                    ' Statistik und Optimierung (Prof. Trautmann)'
                ),
            },
            {
                'chair_id': '59575309', 'chair_name': (
                    'Professur für'
                    ' Maschinelles Lernen und Data Engineering (Prof. Gieseke)'
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
                'chair_id': '77369668', 'chair_name': (
                    'Professur für'
                    ' Digitale Innovation und der öffentliche Sektor (Prof. Brandt)'
                ),
            },
            {
                'chair_id': '40279346', 'chair_name': (
                    'Lehrstuhl für'
                    ' Wirtschaftsinformatik und Logistik (Prof. Hellingrath)'
                ),
            },
            {
                'chair_id': '55472869', 'chair_name': (
                    'Juniorprofessur für'
                    ' IT-Sicherheit (Prof. Hupperich)'
                ),
            },
        ]
        self.employees = []  # list of dicts with employee_id and employees chair
        self.result = []  # to return

    def split_list(self, input_list, max_length):
        """Splitting the input list into lists with len(max_length).

        returns the list a list of lists with max_length.
        """
        return [input_list[i:i+max_length] for i in range(0, len(input_list), max_length)]

    def update_employees(self):
        """Append all employee_ids of the chairs to cris instance.

        TODO: if len(response) > 100:
        --> query again for the chair beginning with
        the endcursor of the last query.
        """
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

    def update_result(self):
        """Appends dicts with infos about employees to result list."""
        employee_ids = [item['id'] for item in self.employees]
        # splitted employee ids up in list of 100 entries
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
            for chair, person in zip(response['chairs'], persons):
                emails = []
                phones = []
                roomNumber = None
                for edge in person['connections']['cards']['edges']:
                    email = edge['node']['email']
                    phone = edge['node']['phone']
                    if email not in emails and email is not None:
                        emails.append(email)
                    if phone not in phones and phone is not None:
                        phones.append(phone)
                    if roomNumber is None and edge['node']['roomNumber'] is not None:
                        roomNumber = edge['node']['roomNumber']

                picture_id = None
                if person['connections']['pictures']['edges']:  # noqa: 501
                    picture_id = person['connections']['pictures']['edges'][0]['node']['id']  # noqa: 501

                self.result.append({
                    'academicTitle': person['node']['academicTitle'],
                    'cfFirstNames': person['node']['cfFirstNames'],
                    'cfFamilyNames': person['node']['cfFamilyNames'],
                    'roomNumber': roomNumber,
                    'emails': emails,
                    'phones': phones,
                    'chair': chair,
                    'image': picture_id,
                })
        return

    def remove_duplicate_employees(self):
        """Function that removes duplicates from employee list.

        Keeps the first entry and removes all subsequent entries.
        """
        temp_dict = {i['id']: i for i in reversed(self.employees)}
        result = list(temp_dict.values())[::-1]
        return result

    def add_addresses(self):
        """Function that adds addresses for every employee.

        Address depends on the chair the person is working in.
        TODO: Outsource the chair address matching to config file
        """
        for card in self.result:
            if 'Prof. Klein' in card['chair'] or 'Prof. Berger' in card['chair']:
                card['address'] = 'Leonardo-Campus 11'
            else:
                card['address'] = 'Leonardo-Campus 3'
        return

    '''
    def add_pictures(self):
        """Function that adds picture base 64 blob for every employee.

        The function overwrites the image value with the base 64 blob.
        """
        for card in self.result:
            if card['image'] is None:
                continue
            response = self.session.get(
                f'{self.base_picture_url}{str(card["image"])}',
            )
            if response.status_code != 200:
                card['image'] = None
                continue
            response_list = xmltodict.parse(response.text)
            for attr in response_list['infoObject']['attribute']:
                if attr['@name'] != 'File data':
                    continue
                card['image'] = attr['data']'''

    def get_cris_data(self):
        """Function that returns the desired result."""
        self.update_employees()
        self.employees = self.remove_duplicate_employees()
        print(len(self.employees))
        self.update_result()
        self.add_addresses()
        # self.add_pictures()
        return self.result
