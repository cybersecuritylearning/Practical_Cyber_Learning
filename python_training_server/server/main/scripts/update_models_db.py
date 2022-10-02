
from main.models import Learning_Modules
import json,os

def init_database():

    with open("sql_template/sql-template-modules","r") as modules:
        lines = modules.readlines()[3:]
    
    for line in lines:
        data = json.loads(line.strip())
        modules = Learning_Modules()
        modules.Module_name = data['TRAIN_ID']
        modules.Module_message = data['TRAIN_QUEST']
        modules.save()
 
def run():
    init_database()

