
from main.models import Learning_Modules
import json

def init_database():

    with open("sql_template/sql-template-modules","r") as modules:
        lines = modules.readlines()[3:]
  
    for line in lines:
        data = json.loads(line.strip())
        existent = ''
        
        try:
            existent = Learning_Modules.objects.filter(Module_name=data['TRAIN_ID'])
        except Exception as e:
            return 0

        if len(existent) == 0 :        
            modules = Learning_Modules()
        else:
            modules = existent[0]

        with open(f"sql_template/{data['TRAIN_ID']}") as tip_file:
            modules.Module_name = data['TRAIN_ID']
            modules.Module_message = data['TRAIN_QUEST']
            modules.Module_type = data['MODULE_TYPE']
            modules.CVE_number = data['CVE_number']
            modules.Category_tag = data['CATEGORY_TAG']
            modules.Module_tips = tip_file.read()
            modules.save()
 
def run():
    init_database()

