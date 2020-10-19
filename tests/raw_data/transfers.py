new_transfers = (
    {
        'request': {
            'amount': 1000.55,
            'sourceWalletId': 1,
            'targetWalletId': 2,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'call_kwargs': {
            'amount': 1000.55,
            'source_wallet_id': 1,
            'target_wallet_id': 2,
            'transaction_code': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'amount': 1000.55,
            'sourceWalletId': 1,
            'targetWalletId': 2,
            'transactionTypeId': 1,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'sourceWalletBalance': 2000.55,
            'targetWalletBalance': 1000
        },
        'mock_response': {
            'amount': 1000.55,
            'source_wallet_id': 1,
            'target_wallet_id': 2,
            'transaction_type_id': 1,
            'transaction_code': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
            'source_wallet_balance': 2000.55,
            'target_wallet_balance': 1000
        }
    },
)

invalid_transfers = (
    {
        'request': {
            'amount': 'test',
            'sourceWalletId': 1,
            'targetWalletId': 2,
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
            'amount': 1000.55,
            'sourceWalletId': 'test',
            'targetWalletId': 2,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'sourceWalletId'
                    ],
                    'msg': 'value is not a valid integer',
                    'type': 'type_error.integer'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 1000.55,
            'sourceWalletId': 1,
            'targetWalletId': 'test',
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'targetWalletId'
                    ],
                    'msg': 'value is not a valid integer',
                    'type': 'type_error.integer'
                }
            ]
        }
    },
    {
        'request': {
            'sourceWalletId': 1,
            'targetWalletId': '2',
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
            'amount': 1000.55,
            'targetWalletId': 2,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'sourceWalletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'amount': 1000.55,
            'sourceWalletId': 1,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'targetWalletId'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    },
    {
        'request': {
            'amount': -200,
            'sourceWalletId': 1,
            'targetWalletId': 2,
            'transactionCode': '5e5d4762-c993-4adb-abd6-6bb694deeac9',
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'amount'
                    ],
                    'msg': 'amount должен быть положительным числом',
                    'type': 'value_error'
                }
            ]
        }
    },
    {
        'request': {
            'amount': -200,
            'sourceWalletId': 1,
            'targetWalletId': 2,
        },
        'response': {
            'detail': [
                {
                    'loc': [
                        'body',
                        'amount'
                    ],
                    'msg': 'amount должен быть положительным числом',
                    'type': 'value_error'
                },
                {
                    'loc': [
                        'body',
                        'transactionCode'
                    ],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                }
            ]
        }
    }
)
