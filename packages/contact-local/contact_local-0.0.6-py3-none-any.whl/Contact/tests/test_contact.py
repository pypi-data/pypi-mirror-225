import os
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

from dotenv import load_dotenv
from db import contactView
from contact_api.contact import contact
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum


load_dotenv()

obj = {
    'component_id': 123,
    'component_name':'contact-local',
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework' : LoggerComponentEnum.testingFramework.pytest.value
    
}
logger_local.init(object=obj)


def test_insert_select():
    object1 = {
            'first_name': "ai"
        }
    logger_local.start(object=object1)
    contact.insert("ai","bye","0539229102","","sami@gmail.com","haifa","sniper","wha")
    contactRes = contactView.get_contact_by_first_name('ai')
    contactRes is not None
    logger_local.info("contact added "+"ai")




def test_update():
    object1 = {
           'name' :'mesiko'
        }
    logger_local.start(object=object1)
    contact.insert("mesiko","refael","05211313111","","","asa","mouse","organ")
    id=contactView.get_contact_by_first_name("mesiko")[0]
    contact.update(11, "sami", "ve", "sumo", "ars", id)
    contactRes = contactView.get_contact_by_id(99)
    print(contactRes[3])
    assert contactRes[3] == 11
    assert contactRes[6] == "sami"
    assert contactRes[7] == "ve"
    assert contactRes[8] == "sumo"
    assert contactRes[17] == "ars"
    logger_local.info("contact updated"+str(id))



def test_select_valid():
    logger_local.start()
    contactRes = contactView.get_contact_by_id(99)
    assert contactRes is not None 
    logger_local.end("contact selected")



def test_select_invalid():
    logger_local.start()
    contactRes = contactView.get_contact_by_id(12121231765)
    assert contactRes is None
    logger_local.end("contact not selected")


