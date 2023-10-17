import os
import time
import requests
import schedule
import pytz

from dotenv import load_dotenv
from datetime import datetime, timezone

from services.email import send_email

load_dotenv() 

def job():
    
    contracts = get_active_contracts()
    todoist_tasks = get_todoist_tasks()

    date_format = '%Y-%m-%d'
    
    if len(contracts) > 0:
        
        for contract in contracts:
            for task in todoist_tasks:
                
                if contract["task_id"] == task["task_id"]:
                    
                    print("Verificando contrato: {}".format(contract["id"]))
                    
                    #Obtenemos la tarea de todoist
                    todoist_task = get_todoist_task(task["task_id"])
                    
                    """ Diferentes escenarios.
                    1. Si la fecha de la tarea, es la misma que la fecha de hoy, entonces el contrato no se cumplió
                    2. Si la fecha de la tarea, es menor a la fecha de hoy, entonces el contrato no se cumplió
                    3. Si la fecha de la tarea, es mayor a la fecha de hoy, entonces el contrato se cumplió
                    Si esta condición se cumple, entonces el contrato ¡NO se cumplió! """
                    if datetime.strptime(todoist_task["task_due"], date_format) <= datetime.now():
                        
                        #obtenemos el correo del supervisor y del responsable
                        email_supervisor = contract["supervisor_email"]
                        email_responsible = contract["responsible_email"]
                        
                        #se registra la penalización en la base de datos
                        register_penalty(int(contract["id"]), contract["penalty"])
                        
                        send_email(
                            supervisor_email=email_supervisor,
                            responsible_email=email_responsible,
                            subject="Contrato incumplido por parte de {}".format(contract["responsible_name"]),
                            responsible_name=contract["responsible_name"],
                            habit=contract["habit"],
                            penalty=contract["penalty"]
                        )
                            
                        return True
                    else:
                        #se registra la racha en la base de datos
                        register_streak(contract["id"])
    else:
        print("No hay contratos activos")
            
                    
# obtenemos todos los contratos          
def get_active_contracts():
    response = requests.get("https://commitgrow-production.up.railway.app/api/active-contracts")
    return response.json()         
          
#obtenemos las tareas de todoist con el label commit-grow          
def get_todoist_tasks():
    response = requests.get("https://commitgrow-production.up.railway.app/api/todoist-tasks")
    return response.json()

#obtenemos una tarea de todoist por su id
def get_todoist_task(id: str):
    response = requests.get(f"https://commitgrow-production.up.railway.app/api/todoist-task/{id}")
    return response.json()

def register_penalty(contract_id, penalty):
    response = requests.post("https://commitgrow-production.up.railway.app/api/penalty", json={ "id": contract_id, "penalty": penalty }, headers={ "Content-Type": "application/json" })
    return response.json()
    
def register_streak(contract_id):
    response = requests.post("https://commitgrow-production.up.railway.app/api/streak", json={ "id": contract_id })
    return response.json()

if __name__ == "__main__":
    print("Iniciando el programa")
    
    # Obtener la hora actual en UTC
    now = datetime.utcnow()
    
    # Convertir la hora a la zona horaria UTC-5
    utc_5 = timezone.utc_offset(-3600)
    
    print(now.astimezone(utc_5))
    print(now.time())
    
    schedule.every().day.at("23:59").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)