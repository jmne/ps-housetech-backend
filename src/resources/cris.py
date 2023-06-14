import json

import requests

from .proxy_config import proxies


class CrisTracker:
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
        self.session = requests.session()
        self.session.proxies.update(proxies)

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
        TODO: there may be duplicates, not handled yet.
        """
        for chair in self.chairs:
            payload = {
                'query': f"""
                                    query {{
                                        organisation(id:{chair["chair_id"]}){{
                                            connections{{
                                                persons(first:100){{
                                                    edges{{
                                                        node{{
                                                            id
                                                            cfFirstNames
                                                            cfFamilyNames
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
            # print(response)
            for employee in (
                response['data']['organisation']
                ['connections']['persons']['edges']
            ):
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
            response = json.loads(
                self.session.post(
                    self.url, headers=self.header, json=payload,
                ).text,
            )
            for index, (chair, employee_data) in enumerate(zip(lochairs, response['data']['nodes'])):  # noqa: E501
                for edge in response['data']['nodes'][index]['connections']['cards']['edges']:  # noqa: E501
                    # hier logik abändern
                    if (
                        edge['node']['email'] is None
                        or edge['node']['email'] is None
                    ):
                        continue
                    else:
                        try:
                            self.result.append({
                                'academicTitle': employee_data['node']['academicTitle'],
                                'cfFirstNames': employee_data['node']['cfFirstNames'],
                                'cfFamilyNames': employee_data['node']['cfFamilyNames'],
                                'roomNumber':  edge['node']['roomNumber'],
                                'email': edge['node']['email'],
                                'phone': edge['node']['phone'],
                                'chair': chair,
                                'image':
                                employee_data['connections']['pictures']['edges'][0]['node']['id'],  # noqa: E501

                            })
                            break
                        except IndexError as e:
                            print(
                                employee_data['node']['cfFirstNames'],
                                employee_data['node']['cfFamilyNames'],
                            )
                            print(e)
                            break

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
        """
        pass

    def get_cris_data(self):
        """Function that returns the desired result."""
        self.update_employees()
        print(len(self.employees))
        self.employees = self.remove_duplicate_employees()
        print(len(self.employees))
        self.update_result()
        self.add_addresses()
        return self.result


if __name__ == '__main__':
    cristracker = CrisTracker()
    print(cristracker.get_cris_data())
    '''
    cristracker.update_chairs()
    print(cristracker.chairs)
    cristracker.update_employees()
    cristracker.update_result()
    print(cristracker.result, len(cristracker.result))
    print(len(cristracker.employees))'''
