from boxcraft.controller import Box
from time import sleep as time_sleep
from os import environ

def hello(instance=None, action=None):
    print(f"Action: {action} Instance: {instance}")

if __name__ == "__main__":
    try:
        # env 1
        action = environ.get('ACTION', "create").lower().strip()
        instances = environ.get('INSTANCES', "3").strip()
        name = environ.get('INSTANCE_NAME', "poc").strip()
        # create
        tasks = { 'action': action, 'name': name, 'instances': instances }
        # delete
        tasks = { 'action': 'delete', 'name': 'poc-*', 'instances': str(["node-01", "node-02", "node-03", "node-04", "node-05"]) }

        print(tasks)
        #print(eval(tasks['instances']), type(eval(tasks['instances'])))

        ctx = Box()
        print(f"Node: {ctx._node_name} - Role: {ctx.role} - ID: {ctx._id}")
        # publish data
        ctx.publish(tasks)
        # runner
        while True:
            # getting data
            task = ctx.getting()
            if task == None:
                break
                #print("waiting for signal from the leader...")
                #if ctx.alive() == False:
                #    break
                #time_sleep(2)
            else:
                print(f"Task: {task}")
                ctx.runner(target=hello, kwargs={"instance": task['instances'], "action": task['action']})
                time_sleep(2)
    except Exception as err:
        print(err)