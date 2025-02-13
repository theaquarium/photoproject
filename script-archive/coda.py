import requests
from config import config

headers = {
    "Authorization": "Bearer " + config['coda']['token'],
}


def insert_row_for(date, url, original_id):
    uri = f'https://coda.io/apis/v1/docs/{config['coda']
                                          ['doc']}/tables/{config['coda']['table']}/rows'
    payload = {
        'rows': [
            {
                'cells': [
                    {'column': 'c-Xfk128RzEh', 'value': date},
                    {'column': 'c-kt-4beepk6', 'value': original_id},
                    {
                        "Status": {
                            "status": {
                                "name": "New"
                            }
                        },
                        "Original ID": {
                            "type": "rich_text",
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": original_id
                                    }
                                }
                            ],
                        },
                        "Original": {
                            "type": "files",
                            "files": [
                                {
                                    "type": "external",
                                    "external": {
                                        "url": url
                                    }
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }
    req = requests.post(uri, headers=headers, json=payload)
    req.raise_for_status()
    res = req.json()

    print(f'Inserted 1 row', res)
    # => Inserted 1 row
    page = create_page({
        "Name": {
            "type": "title",
            "title": [
                    {
                        "type": "text",
                        "text": {
                                "content": "Day"
                        }
                    }
            ]
        },
        "Status": {
            "status": {
                "name": "New"
            }
        },
        "Date": {
            "date": {
                "start": date
            }
        },
        "Original ID": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": original_id
                    }
                }
            ],
        },
        "Original": {
            "type": "files",
            "files": [
                {
                    "type": "external",
                    "external": {
                        "url": url
                    }
                }
            ]
        },
    })

    return page
