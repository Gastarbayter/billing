new_clients = (
    {
        'request': {
            'login': 'Ivanov',
            'firstName': 'Ivan',
            'lastName': 'Ivanov',
            'passportSeries': '0001',
            'passportNumber': '000001'
        },
        'call_kwargs': {
            'login': 'Ivanov',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'passport_series': '0001',
            'passport_number': '000001'
        },
        'response': {
            'login': 'Ivanov',
            'firstName': 'Ivan',
            'lastName': 'Ivanov',
            'passportSeries': '0001',
            'passportNumber': '000001',
            'clientId': 1,
            'walletId': 1
        },
        'mock_response': {
            'login': 'Ivanov',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'passport_series': '0001',
            'passport_number': '000001',
            'clientId': 1,
            'walletId': 1
        }
    },
)

invalid_clients = (
    {
        'request': {
            'login': 1,
            'firstName': 1,
            'lastName': 1,
            'passportSeries': 1,
            'passportNumber': 1
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'passportSeries'
                    ],
                    'msg': 'ensure this value has at least 4 characters',
                    'type': 'value_error.any_str.min_length',
                    'ctx': {
                        'limit_value': 4
                    }
                },
                {
                    'loc': [
                        'body',
                        'passportNumber'
                    ],
                    'msg': 'ensure this value has at least 4 characters',
                    'type': 'value_error.any_str.min_length',
                    'ctx': {
                        'limit_value': 4
                    }
                }
            ]
        }
    },
    {
        'request': {
            'firstName': 'Ivan',
            'lastName': 'Petrov',
            'passportSeries': '0001',
            'passportNumber': '000001'
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'login'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'login': 'Ivanov',
            'firstName': 'Ivan',
            'lastName': 'Petrov'
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'passportSeries'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                },
                {
                    'loc': [
                        'body',
                        'passportNumber'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
)

clients = [
    {
        'login': 'Ivanov',
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'passport_series': '0001',
        'passport_number': '000001'
    },
    {
        'login': 'Petrov',
        'first_name': 'Peter',
        'last_name': 'Petrov',
        'passport_series': '0002',
        'passport_number': '000002'
    }
]

client_not_serialized = {
    'login': 'Ivanov',
    'firstName': 'Ivan',
    'lastName': 'Ivanov',
    'passportSeries': '0001',
    'passportNumber': '000001'
}
