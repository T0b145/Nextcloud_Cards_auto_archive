import os
import requests
import time
from datetime import datetime, timedelta


class NC_decks_worker:
    def __init__(self):
        self.user = os.environ['NC_USER']
        self.password = os.environ['NC_PASSWORD']
        self.headers = {'OCS-APIRequest': str(True), 'Content-Type': 'application/json'}
        self.url = os.environ['NC_URL']

    def stack_details(self, board_id, stack_id):
        url = '{}/index.php/apps/deck/api/v1.0/boards/{}/stacks/{}'.format(self.url, board_id, stack_id)
        r = requests.get(url, auth=(self.user, self.password), headers=self.headers)
        return r

    def archive_card(self, board_id, card):
        stack_id = card["stackId"]
        card_id = card["id"]

        url = '{}/index.php/apps/deck/api/v1.0/boards/{}/stacks/{}/cards/{}'.format(self.url,board_id, stack_id, card_id)
        card['archived'] = True
        data = card
        r = requests.put(url, auth=(self.user, self.password), headers=self.headers, json=data)
        return r


last_week = datetime.now()-timedelta(days = 1)
last_week = datetime.timestamp(last_week)

board_id = 4
stack_id = 10

nc = NC_decks_worker()
Done_stack = nc.stack_details(board_id, stack_id)

if Done_stack.status_code == 200:
    for card in Done_stack.json()["cards"]:
        if card['lastModified'] < last_week:
            nc.archive_card(board_id, card)
            #print ("Archived:", card["title"], time.ctime(card['lastModified']))
else:
    print("connection failed")


# data1 = {'title': 'Title example',
#        'description': '',
#        'stackId': 10,
#        'type': 'plain',
#        'lastModified': 1605284089,
#        'lastEditor': None,
#        'createdAt': 1604995483,
#        'labels': None,
#        'assignedUsers': [],
#        'attachments': None,
#        'attachmentCount': 0,
#        'owner': 'owner_example',
#        'order': 0,
#        'archived': True,
#        'duedate': None,
#        'deletedAt': 0,
#        'commentsUnread': 0,
#        'id': 60,
#        'overdue': 0}
