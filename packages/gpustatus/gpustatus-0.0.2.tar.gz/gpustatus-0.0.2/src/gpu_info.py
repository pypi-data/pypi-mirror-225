import os


class GPU_list:
    def __init__(self, gpu_num=8):
        self.gpu_num = gpu_num
        self.gpu_list = [GPU(0)] * self.gpu_num
    def add_gpu(self, gpu, idx):
        self.gpu_list[idx] = gpu
    def get_gpu_list(self):
        return self.gpu_list
    def get_gpu(self, idx):
        return self.gpu_list[idx]
    def show_gpu(self,idx=None):
        if idx is None:
            idx = range(self.gpu_num)
        for i in idx:
            print('GPU: {}'.format(i))
            self.gpu_list[i].show_gpu_info()


class GPU:
    def __init__(self, idx, process_num=0):
        self.process_num = process_num
#         self.gpu_info = [[]]*self.process_num
        self.gpu_info = []
        self.idx = idx
    def add_process(self, proc):
        self.gpu_info.append(proc)
    def get_process_list(self):
        return self.gpu_info
    def get_idx(self):
        return self.idx
    def get_process_by_pid(self, pid):
        for proc in self.gpu_info:
            if proc.get_pid() == pid:
                return proc
        return None
    def show_gpu_info(self):
        for proc in self.gpu_info:
            # print('Process: {}'.format(proc))
            proc.show_process_info()
        print('='*60)
    def get_user(self):
        user_list = {}
        for proc in self.gpu_info:
            user = proc.get_user()
            user_list.setdefault(user, []).append(proc.get_pid())
        return user_list
    

class GPU_Process:
    def __init__(self,GPU_instance_ID,Computer_instance_ID,Process_ID,Type,Name,Used_GPU_Memory):
        self.GPU_instance_ID = GPU_instance_ID
        self.Computer_instance_ID = Computer_instance_ID
        self.Process_ID = Process_ID
        self.Type = Type
        self.Name = Name
        self.Used_GPU_Memory = Used_GPU_Memory
        self.USER = None
        self.PID = None
        self.CPU = None
        self.MEM = None
        self.VSZ = None
        self.RSS = None
        self.TTY = None
        self.STAT = None
        self.TIME = None
        self.COMMAND = None
    def update(self, USER, PID, CPU, MEM, VSZ, RSS, TTY, STAT, TIME, COMMAND):
        self.USER = USER
        self.PID = PID
        self.CPU = CPU
        self.MEM = MEM
        self.VSZ = VSZ
        self.RSS = RSS
        self.TTY = TTY
        self.STAT = STAT
        self.TIME = TIME
        self.COMMAND = COMMAND
        if self.Process_ID != self.PID:
            print('Process ID is not matched!')
    def get_pid(self):
        return self.Process_ID
    def get_user(self):
        return self.USER
    def get_memory(self):
        return int(self.Used_GPU_Memory.split(' ')[0])
    def show_process_info_all(self):
        print("GPU_instance_ID: ", self.GPU_instance_ID)
        print("Computer_instance_ID: ", self.Computer_instance_ID)
        print("Process_ID: ", self.Process_ID)
        print("Type: ", self.Type)
        print("Name: ", self.Name)
        print("Used_GPU_Memory: ", self.Used_GPU_Memory)
        print("USER: ", self.USER)
        print("PID: ", self.PID)
        print("CPU: ", self.CPU)
        print("MEM: ", self.MEM)
        print("VSZ: ", self.VSZ)
        print("RSS: ", self.RSS)
        print("TTY: ", self.TTY)
        print("STAT: ", self.STAT)
        print("TIME: ", self.TIME)
        print("COMMAND: ", self.COMMAND)
        print('-'*60)
    def show_process_info(self,GPU_instance_ID=False,Computer_instance_ID=False,Type=False,Name=False,Used_GPU_Memory=True,USER=True,CPU=False,MEM=False,VSZ=False,RSS=False,TTY=False,STAT=False,TIME=False,COMMAND=True):
        print("Process_ID: ", self.Process_ID)
        if USER:
            print("USER: ", self.USER) 
        if Used_GPU_Memory:
            print("Used_GPU_Memory: ", self.Used_GPU_Memory)   
        if GPU_instance_ID:
            print("GPU_instance_ID: ", self.GPU_instance_ID)
        if Computer_instance_ID:
            print("Computer_instance_ID: ", self.Computer_instance_ID)
        if Type:
            print("Type: ", self.Type)
        if Name:
            print("Name: ", self.Name)
        if CPU:
            print("CPU: ", self.CPU)
        if MEM:
            print("MEM: ", self.MEM)
        if VSZ:
            print("VSZ: ", self.VSZ)
        if RSS:
            print("RSS: ", self.RSS)
        if TTY:
            print("TTY: ", self.TTY)
        if STAT:
            print("STAT: ", self.STAT)
        if TIME:
            print("TIME: ", self.TIME)
        if COMMAND:
            print("COMMAND: ", self.COMMAND)

        print('-'*60)
    def show_process_info_simple(self):
        print("Process_ID: ", self.Process_ID)
        print("USER: ", self.USER)
        print("Used_GPU_Memory: ", self.Used_GPU_Memory)
        print('-'*60)

class Process:
    def __init__(self,USER,PID,CPU,MEM,VSZ,RSS,TTY,STAT,START,TIME,COMMAND):
        self.USER = USER
        self.PID = PID
        self.CPU = CPU
        self.MEM = MEM
        self.VSZ = VSZ
        self.RSS = RSS
        self.TTY = TTY
        self.STAT = STAT
        self.START = START
        self.TIME = TIME
        self.COMMAND = COMMAND
    def show_process_info(self):
        print("USER: ", self.USER)
        print("PID: ", self.PID)
        print("CPU: ", self.CPU)
        print("MEM: ", self.MEM)
        print("VSZ: ", self.VSZ)
        print("RSS: ", self.RSS)
        print("TTY: ", self.TTY)
        print("STAT: ", self.STAT)
        print("START: ", self.START)
        print("TIME: ", self.TIME)
        print("COMMAND: ", self.COMMAND)
        print('-'*60)

class Process_list:
    def __init__(self):
        self.process_list = {}
    def add_process(self, proc):
        self.process_list[proc.PID] = proc
    def get_by_pid(self, pid):
        return self.process_list[pid]
    def show_process_lists(self):
        for pid in self.process_list.keys():
            print('Process: {}'.format(pid))
            self.process_list[pid].show_process_info()



class GPU_Monitor:
    def __init__(self):
        self.gpu_list = self.get_GPU_info()
        self.process_list = self.get_process_info()
        self.update_gpu_process()
        self.user = self.get_user()
    def update(self):
        self.gpu_list = self.get_GPU_info()
        self.process_list = self.get_process_info()
        self.update_gpu_process()
        self.user = self.get_user()
    def get_GPU_info(self):
        nvidia_smi = os.popen('nvidia-smi -q -d PIDS |grep -A8 GPU').read().split('\n\n')
        # nvidia_smi[0] = nvidia_smi[0][46:]
        gpu_list_info = [i.split('\n') for i in nvidia_smi][1:-1]
        gpu_num = len(gpu_list_info)+1
        gpu_list = GPU_list(gpu_num)
        for g in range(len(gpu_list_info)):
            gpu_info = gpu_list_info[g]
            gpu = GPU(g)
            process_num = int((len(gpu_info)-2)/6)
            if process_num == 0:
                gpu_list.add_gpu(gpu,g)
                continue
            for p in range(process_num):
                proc_info = gpu_info[2+p*6:8+p*6]
                proc = GPU_Process(proc_info[0].split(':')[1].strip(),proc_info[1].split(':')[1].strip(),proc_info[2].split(':')[1].strip(),proc_info[3].split(':')[1].strip(),proc_info[4].split(':')[1].strip(),proc_info[5].split(':')[1].strip())
                gpu.add_process(proc)
            gpu_list.add_gpu(gpu,g)
        return gpu_list
    def get_process_info(self):
        ps = os.popen('ps -aux').read().split('\n')[1:]
        process_list = Process_list()
        for p in ps:
            if p == '':
                continue
            p = p.split()
            proc = Process(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],' '.join(p[10:]))
            process_list.add_process(proc)
        return process_list
    def get_user(self):
        user = {}
        for g in self.gpu_list.get_gpu_list():
            for p in g.get_process_list():
                user.setdefault(p.get_user(),{}).setdefault(g.get_idx(),[]).append(p.get_pid())
        return user
    def update_gpu_process(self):
        for g in self.gpu_list.get_gpu_list():
            for p in g.get_process_list():
                proc = self.process_list.get_by_pid(p.get_pid())
                p.update(proc.USER, proc.PID, proc.CPU, proc.MEM, proc.VSZ, proc.RSS, proc.TTY, proc.STAT, proc.TIME, proc.COMMAND)
    def show_gpu_info(self):
        self.update()
        self.gpu_list.show_gpu()
    def show_process_info(self):
        self.update()
        self.process_list.show_process_lists()
    def show_all_info(self):
        self.update()
        self.show_gpu_info()
        self.show_process_info()
    def get_process_by_pid(self, pid):
        self.update()
        return self.process_list.get_by_pid(pid)
    def get_gpu_by_idx(self, idx):
        self.update()
        return self.gpu_list.get_gpu(idx)
    def show_by_gpu(self,idx=None):
        self.update()
        if idx is None:
            idx = range(len(self.gpu_list.get_gpu_list()))
        for i in idx:
            print('GPU {}: '.format(i))
            gpu = self.gpu_list.get_gpu(i)
            print('Total process in this GPU: {}'.format(len(gpu.get_process_list())))
            print('Total user in this GPU: {}'.format(len(gpu.get_user())))
            for usr, proc_list in gpu.get_user().items():
                mem = 0
                for proc in proc_list:
                    mem += gpu.get_process_by_pid(proc).get_memory()
                print('User: {} has {} process, totally memory used: {} MiB'.format(usr, len(proc_list), mem))
            print('='*60)
            for proc in gpu.get_process_list():
                proc.show_process_info()
    def show_by_user(self, usr=None):
        self.update()
        if usr is None:
            usr = self.user.keys()
        print('Total user: {}'.format(len(self.user.keys())))
        print('+'*60)
        for u in usr:
            print('User: {}'.format(u))
            print('Total GPU: {}'.format(len(self.user[u].keys())))
            print('Total process: {}'.format(sum([len(self.user[u][g]) for g in self.user[u].keys()])))
            print('Total Memory use: {}'.format(sum([sum([self.gpu_list.get_gpu(g).get_process_by_pid(p).get_memory() for p in self.user[u][g]]) for g in self.user[u].keys()])))
            print('='*60)
            for g in self.user[u].keys():
                print('GPU: {}'.format(g))
                for p in self.user[u][g]:
                    proc = self.gpu_list.get_gpu(g).get_process_by_pid(p)
                    proc.show_process_info()
        print('='*60)