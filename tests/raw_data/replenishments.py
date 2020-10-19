new_replenishments = (
    {
        'request': {
            'amount': 3000.55,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'walletId': 1
        },
        'call_kwargs': {
            'amount': 3000.55,
            'transaction_code': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'wallet_id': 1
        },
        'response': {
            'amount': 3000.55,
            'walletId': 1,
            'transactionTypeId': 2,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'balance': 3000.55
        },
        'mock_response': {
            'amount': 3000.55,
            'wallet_id': 1,
            'transaction_type_id': 2,
            'transaction_code': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'balance': 3000.55
        }
    },
)

invalid_replenishments = (
    {
        'request': {
            'amount': 'test',
            'walletId': 1,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'amount'
                    ],
                    'msg': 'value is not a valid decimal',
                    'type': 'type_error.decimal'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 3000.55,
            'wallet_id': 'test',
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',

        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'walletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'walletId': 1,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'amount'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 3000.55,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'walletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 3000.55,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',

        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'walletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 3000.55,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'walletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    }
)
