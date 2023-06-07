import json

import requests


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
        self.chairs = []  # list of dicts with chairs
        self.employees = []  # list of dicts with employee_id and employees chair
        self.result = []  # to return

    def split_list(self, input_list, max_length):
        """Splitting the input list into lists with len(max_length).

        returns the list a list of lists with max_length.
        """
        return [input_list[i:i+max_length] for i in range(0, len(input_list), max_length)]

    def update_chairs(self):
        """Append all active chairs (chair ids) to Cris instance."""
        payload = {
            'query': """
                        query findWIOrganisations {
                            organisationList(
                                select: {
                                    filter: [
                                        {
                                            match: {
                                                cfName: {
                                                    query: "Wirtschaftsinformatik"
                                                }
                                            }
                                        },
                                        {
                                            match: {
                                                status: {
                                                    query: "5"
                                                }
                                            }
                                        }
                                    ]
                                }
                            ) {
                                list {
                                    node {
                                        id
                                        cfName
                                        status
                                    }
                                }
                            }
                        }
                    """,
        }
        response = json.loads(
            requests.post(
                self.url, headers=self.header, json=payload,
            ).text,
        )
        for chair in response['data']['organisationList']['list']:
            self.chairs.append({
                'chair_id': chair['node']['id'],
                'chair_name': chair['node']['cfName'],
            })
        return

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
                requests.post(
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
                requests.post(
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

    def get_cris_data(self):
        """Function that returns the desired result."""
        self.update_chairs()
        self.update_employees()
        self.update_result()
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
