## BoxCraft
<p align="left">
    <a href="#">
        <img src="https://img.shields.io/github/actions/workflow/status/Lucho00Cuba/boxcraft/tests.yaml" alt="unittest"/>
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/license/Lucho00Cuba/boxcraft" alt="license"/>
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/last-commit/Lucho00Cuba/boxcraft" alt="last-commit"/>
    </a>
</p>
<hr>

Este es un proyecto que implementa el modulo `BoxCraft` para disponer de un sistema para el procesamiento distribuido, basado en la administración de nodos y tareas que aprovecha la flexibilidad de Python y la velocidad de Redis.

## Características
- Sistema de nodos que permite roles de líder y lector para una gestión eficiente.
- Gestiona y supervisa tareas a través de un sistema dinámico basado en Redis.
- Sistema para administrar tareas y su estado.

## Requisitos

- Python 3.x
- `Redis` instalado y configurado

## Instalación

1. Clona el repositorio:

```bash
user@node: git clone https://github.com/Lucho00Cuba/boxcraft.git
user@node: cd boxcraft
```

## Uso
```python
from boxcraft.controller import Box
from time import sleep as time_sleep
from os import environ

def hello(instance=None, action=None):
    print(f"Action: {action} Instance: {instance}")

if __name__ == "__main__":
    try:
        tasks = { 'action': 'delete', 'name': 'poc-*', 'instances': str(["node-01", "node-02", "node-03", "node-04", "node-05"]) }
        ctx = Box()
        print(f"Node: {ctx._node_name} - Role: {ctx._role} - ID: {ctx._id}")
        # publish data
        ctx.publish(tasks)
        # runner
        while True:
            # getting data
            task = ctx.getting()
            if task == None:
                break
            else:
                print(f"Task: {task}")
                # logic to execute the task... 
                ctx.runner(target=hello, kwargs={"instance": task['instances'], "action": task['action']})
                time_sleep(2)
    except Exception as err:
        print(err)
```