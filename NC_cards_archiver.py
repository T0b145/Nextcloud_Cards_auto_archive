import os
import requests
import time
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


class NC_decks_worker:
    def __init__(self):
        self.user = os.environ['NC_USER']
        self.password = os.environ['NC_PASSWORD']
        self.url = os.environ['NC_URL']
        self.headers = {'OCS-APIRequest': str(True), 'Content-Type': 'application/json'}
        self.summary = {"archived":0, "duedate_changed":0}

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

    def change_duedate(self, board_id, card, duedate):
        stack_id = card["stackId"]
        card_id = card["id"]
        url = '{}/index.php/apps/deck/api/v1.0/boards/{}/stacks/{}/cards/{}'.format(self.url,board_id, stack_id, card_id)
        card['duedate'] = duedate
        data = card
        r = requests.put(url, auth=(self.user, self.password), headers=self.headers, json=data)
        return r


nc = NC_decks_worker()

# Archive Cards of board 4 in stack 10
board_id = 4
stack_id = 10
last_week = datetime.now()-timedelta(days = 1)
last_week = datetime.timestamp(last_week)
try:
    Done_stack = nc.stack_details(board_id, stack_id)
except:
    logging.error("Request failed")
    exit()
if Done_stack.status_code == 200:
    if "cards" in Done_stack.json().keys():
        for card in Done_stack.json()["cards"]:
            if card['lastModified'] < last_week:
                nc.archive_card(board_id, card)
                nc.summary["archived"] += 1
                logging.debug("Archived: " + card["title"] +str(time.ctime(card['lastModified'])))
    else:
        logging.debug("Empty Stack")
else:
    logging.error("Connection failed")

# Today cards of board 4 in stack 10
board_id = 4
stack_id = 9
today = datetime.now()
today = today.replace(hour=21).replace(minute=55).replace(second=0).replace(microsecond=0).replace(tzinfo=timezone.utc).isoformat()
Today_stack = nc.stack_details(board_id, stack_id)
if Today_stack.status_code == 200:
    if "cards" in Today_stack.json().keys():
        for card in Today_stack.json()["cards"]:
            if card["duedate"] != today:
                nc.change_duedate(board_id, card, today)
                nc.summary["duedate_changed"] += 1
                logging.debug("Duedate changed: " + card["title"])
    else:
        logging.debug("Empty Stack")
else:
    logging.error("Connection failed")


#Summary
logging.info("Archived: {}".format(nc.summary["archived"]))
logging.info("Due date changed: {}".format(nc.summary["duedate_changed"]))

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
