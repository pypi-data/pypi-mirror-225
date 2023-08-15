import os
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

import pytest
from dotenv import load_dotenv
from datetime import datetime
from Contact.db import contactView
from Contact.contact_api import contact


load_dotenv()


def test_insert_select():
    contact.insert("ai","bye","0539229102","","sami@gmail.com","haifa","sniper","wha")
    contactRes = contactView.get_contact_by_first_name('ai')
    contactRes is not None



def test_update():
    contact.update(11, "sami", "ve", "sumo", "ars", 99)
    contactRes = contactView.get_contact_by_id(99)
    assert contactRes['person_id'] == 11
    assert contactRes['name_prefix'] == "sami"
    assert contactRes['first_name'] == "ve"
    assert contactRes['additional_name'] == "sumo"
    assert contactRes['job_title'] == "ars"



def test_select_valid():
    contactRes = contactView.get_contact_by_id(99)
    contactRes is not None


def test_select_valid():
    contactRes = contactView.get_contact_by_id(12121231765)
    contactRes is None

