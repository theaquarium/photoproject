from utils import *
from config import config
import requests

headers = {
    "Authorization": "Bearer " + config['notion']['token'],
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {
            "database_id": config['notion']['db'],
        },
        "properties": data
    }

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.json())
    return res


def create_notion_page_for(date, url, original_id):
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
