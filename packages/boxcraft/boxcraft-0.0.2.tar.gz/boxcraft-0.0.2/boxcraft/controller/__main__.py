from os import environ
import random
import string
from boxcraft.store import RedisStore
from datetime import datetime

class Core:
    store = RedisStore(
        host=environ.get('BOX_REDIS_HOST'),
        password=environ.get('BOX_REDIS_PASS')
    )

    _role = None
    _node_name = environ.get("HOSTNAME", "default.box")
    _alive = int(environ.get("BOX_LEADER_ALIVE", "2400"))
    
    long_key = 30
    _id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = long_key))
    timestamp_format = "%Y-%m-%dT%H:%M:%S%z"

    def _heartbeat(self, task, leader_stream=None):

        if task == 'get_timestamp':
            return datetime.now().strftime(self.timestamp_format)
        elif task == 'get_hearbeat':
            calc_timestamp = datetime.strptime(f"{self._heartbeat('get_timestamp')}", "%Y-%m-%dT%H:%M:%S") - datetime.strptime(f"{leader_stream['heartbeat']}", "%Y-%m-%dT%H:%M:%S")
            if int(calc_timestamp.total_seconds()) > self._alive:
                print(f"Leader UnHealthy - {leader_stream['node']}")
                return True
            else:
                print(f"Leader Healthy - {leader_stream['node']}")
                self._leader = leader_stream['node']
                return False

    def _add_node(self):
        # register node
        print("Add Node")
        nodes = self.store.get_json('nodes')
        if nodes == None:
            print("Initializing Collection /nodes")
            self.store.set_json('nodes', [self.role._metadata])
        else:
            print(f"Leader: {self._leader}")
            node = list(filter(lambda item: item.get("node", "") == self._node_name, nodes))

            # exists node
            if len(node) != 0 and node[0]['node'] == self.role._metadata['node']:
                print("Recovery Node")
                # get id
                self._id = node[0]['id']
                # update nodes role
                index = [str(index) for index, d in enumerate(nodes) if d.get('node') == self.role._metadata['node']]
                nodes[int(''.join(index))]['role'] = self.role._metadata['role']
                self.store.set_json('nodes', nodes)
                print("Updating Collection /nodes")
            else:
                print("Register Node")
                nodes.append(self.role._metadata)
                self.store.set_json('nodes', nodes)
                print("Updating Collection /nodes")

    def alive(self):
        
        nodes = self.store.get_json('nodes')
        node = list(filter(lambda item: item.get("node", "") == self._node_name, nodes))
        alive = node[0]['alive']
        if type(self.role) == Leader:
            pass
        elif type(self.role) == Reader:
            pass

        return alive
    
    def __repr__(self):
        return f"{self._role.capitalize()}[{self._node_name}]"

class Leader(Core):

    _role = 'leader'

    def __init__(self):
        self._metadata = {
            'node': self._node_name,
            'id': self._id,
            'created_at': self._heartbeat("get_timestamp"),
            'alive': True,
            'role': 'leader'
        }

    def _init_leader(self):
        # write stream leader
        stream = self._metadata.copy()
        stream['heartbeat'] = self._heartbeat("get_timestamp")
        self.store.set_json('leader', stream)
        print("Initializing Collection /leader")

    def _renove_hearbeat(self):
        renove = self.store.get_json('leader')
        renove['heartbeat'] = self._heartbeat("get_timestamp")
        # write stream
        self.store.set_json('leader', renove)
        print("Updating Heartbeat /leader")

    def _promote_node(self):
        stream = self._metadata.copy()
        stream['heartbeat'] = self._heartbeat("get_timestamp")
        self.store.set_json('leader', stream)
        print("Updating Collection /leader")

    def _runtime_status(self):
        pass
        

class Reader(Core):

    _role = 'reader'

    def __init__(self):
        self._metadata = {
            'node': self._node_name,
            'id': self._id,
            'created_at': self._heartbeat("get_timestamp"),
            'alive': True,
            'role': 'reader'
        }

class Box(Reader, Leader):

    role = None

    def __init__(self):
        # get_role
        ## leader
        leader_stream = self.store.get_json('leader')
        if leader_stream == None:
            self._role('leader')
            self.role._init_leader()
        else:
            # check role base time_alive
            if self._heartbeat('get_hearbeat', leader_stream=leader_stream):
                print(f"Leader: {leader_stream['node']} ID: {leader_stream['id']} Last-HearBeat: {leader_stream['heartbeat']}")
                self._role('leader')
                if leader_stream['node'] != self._node_name:
                    print(f"Promote to Leader {self._node_name}")
                    self.role._promote_node()
                else:
                    print("Renove to Leader")
                    self.role._renove_hearbeat()
            else:
                if leader_stream['node'] == self._node_name:
                    self._role('leader')
                    print("Select Role Leader")
                else:
                    self._role('reader')
                    print("Select Role Reader")
            # add_node
            self._add_node()
    
    def _role(self, role):
        setattr(self, f"_{role}", self._node_name)
        self.role = globals()[role.capitalize()]()

    def publish(self, tasks):

        if type(self.role) != Leader:
            print('task ignored by readers')
        else:
            tasks['metadata'] = tasks.copy()
            tasks['metadata']['created_at'] = self._heartbeat("get_timestamp")
            store_stream = self.store.get_json('tasks')
            if store_stream == None:
                # write tasks
                self.store.set_json('tasks', tasks)
                print("Initializing Collection /tasks")
            else:
                if store_stream == tasks:
                    print("Data is equal not update collections")
                    print(f"Not Update Collection /tasks")
                else:
                    print('Data is not equal, updating collections')
                    # history_tasks
                    history_stream = self.store.get_json('history_tasks')
                    store_stream['indexed_at'] = self._heartbeat("get_timestamp")
                    if history_stream == None:
                        # write tasks
                        self.store.set_json('history_tasks', [store_stream])
                        print("Initializing Collection /history_tasks")
                    else:
                        history_stream.append(store_stream)
                        self.store.set_json('history_tasks', history_stream)
                        print("Updating Collection /history_tasks")
                    # update tasks
                    self.store.set_json('tasks', tasks)
                    print("Updating Collection /tasks")
    
    def getting(self):
        tasks = self.store.get_json('tasks')
        #print(f"Tasks: {tasks}", type(eval(tasks['instances'])))
        task = None
        # type_data
        if type(eval(tasks['instances'])) == int:
            # int
            if int(tasks['instances']) > 0:
                task = tasks.copy() # generate_task
                task['instances'] = int(int(tasks['instances']) / int(tasks['instances']))
                tasks['instances'] = str(int(tasks['instances']) - 1)
                task['total'] = tasks['instances']
            else:
                print("Completed")
                # return {'state': 'finish'}
        elif type(eval(tasks['instances'])) == list:
            if len(eval(tasks['instances'])) != 0:
                #print("Stream All",tasks)
                task = tasks.copy() # generate_task
                task['instances'] = str(eval(tasks['instances']).pop(0))
                tasks['instances'] = str(eval(tasks['instances'])[1:])
                #print("Task Generated",task)
                #print("Task Remove Item",tasks)
            else:
               print("Completed")
        elif type(eval(tasks['instances'])) is None:
            print("Completed")
        
        # write change
        if not task is None:
            self.store.set_json('tasks', tasks)
            print("Getting Task /tasks")
        
        return task

    #@staticmethod
    #def _alive():
    #    def wrapper(fn):
    #        @wraps(fn)
    #        def decorator(*args, **kwargs):
    #            return fn(*args, **kwargs)
    #        return decorator
    #    return wrapper

    #@_alive()
    def runner(self, target=None, args=(), kwargs={}):
        if target:
            target(*args, **kwargs)