import os
import numpy as np
from lib.block import Block
from utils.wires.wire_str import read_string,share_string
from multiprocessing import Process,Queue,Pipe
from console import Worker, Console,set_theme,StyleSheet
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
import multiprocessing
import threading
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,LoggingEventHandler
from time import sleep

#------------------- Reads path from provided arguments and loads files --------------------------#
def initialize():
    data = load_JSON('./data.json')
    return data
#-------------------------------------------------------------------------------------------------#

#---- Loads .vc JSON object ----#
def load_JSON(file_path):

    import json
    with open(file_path) as obj:
        data = json.load(obj)
    return data
#-------------------------------#

#----- Program exit Logic ------#
def end_progam():


    for process in processes:
        process.terminate()
        process.join()

    exit(0)
#-------------------------------#

#----- Frequency Monitor ------#

def monitor_frequency(memories):
    log_freq("<---------- Frequency Monitor ---------->\n")
    for memory in memories:
        message = memory.get()
        for msg in message:
            log_freq(msg)
    sleep(0.2)
    log_freq("END")


#-------------------------------#


#--------------------------- Creates Python Application from .vc File -------------------------#
def build(working_dir):

    # Reading Front-End File
    data = initialize()
    parameters = data['parameters']
    wires = data['wires']


    blocks = []
    parameters_list = []

    for hex_id, block in data['blocks'].items():
        block_type = block['type']
        new_block = Block(hex_id, block_type)
        new_block.name = block['name']
        if block_type in parameters:
            for parameter in parameters[block_type]:
                new_block.add_parameter(parameter['value'], parameter['id'])
        blocks.append(new_block)



    ###################### Setting up communication between blocks ######################
    logger.info("Setting up connections...")

    
    for wire in wires:

        src_block, src_port = wire['source']['block'], wire['source']['port']
        tgt_block, tgt_port = wire['target']['block'], wire['target']['port']
        
        wire_id = src_block+str(src_port)


        # Connecting Paramters to Blocks
        if src_port == 'constant-out':
            param_value = parameters[src_block]['value']

            for block in blocks:
                if tgt_block == block.id:
                    block.add_parameter(param_value, tgt_port)
                    break

        # Connecting Wires to Blocks
        else:

            for block in blocks:
                if tgt_block == block.id:
                    block.connect_input_wire(wire_id, tgt_port)
                    break

            for block in blocks:
                if src_block == block.id:
                    block.connect_output_wire(wire_id, src_port)
                    break
    ######################################################################################
    
    return blocks
# Configuring path for working directory
working_dir = '.'

#function to setup logger
def setLogging():
    
    logger = logging.getLogger(__name__)
    
    file_handler = logging.FileHandler(working_dir+'/logs/console.log',mode='w')

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger

class MyHandler(LoggingEventHandler):
    def __init__(self,win,working_dir):
        self.dir = working_dir
        self.w = win
    def on_modified(self, event):
        pass
    def dispatch(self,event):
        path = event.src_path
        
        if(path != working_dir+'/logs/console.log' ):
            path = working_dir+'/logs/console.log' 
        with open(path) as f:
            content = f.readlines()
            #check if content is empty before logging else .pop will give error
            if content:
                self.w.loginfo_console(content.pop())
        



#_____________________________________________________________________________________________________#
#                                                                                                     # 
# if you want to switch to adding errors to shared memory instead of logging in file                  #
# to show on console                                                                                  #
#  sh_mem_console = share_string("ERROR#LOG")                                                         #
#                                                                                                     #
#  def sendto_console(sh_mem_console,msg):                                                            #
#      to_send = np.array(msg, dtype='<U64')                                                          #
#      sh_mem_console.add(to_send)                                                                    #    
#      sleep(1)                                                                                       #
#                                                                                                     # 
#_____________________________________________________________________________________________________#


#Driver Code

if __name__ == "__main__":

#creating global queue for frequency 
    fmqueue = Queue()
    msgQueue = Queue()
#creating logger for logging errors to log file
    logger = setLogging()

    
    #function to pass to multiprocessing target to initialize console gui 
    #and start worker thread for updating gui
    def initiate():
        app = QApplication([])
        win = Console(fmqueue,msgQueue)
        win.show()
        worker = Worker(fmqueue)
        thread = QThread()
        worker.signal.connect(win.loginfo_fm)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        
        event_handler = MyHandler(win,working_dir)
        observer = Observer()
        observer.schedule(event_handler, path=working_dir+'/logs/console.log', recursive=True)
        observer.start()
        
        thread.start()
  
        app.setPalette(set_theme())
        app.setStyleSheet(StyleSheet)
        app.exec_()
#_____________________________________________________________________________________#

    #function to put freq data in global queue for freq monitor
    def log_freq(txt):
        fmqueue.put(txt+"\n")

    p1 = multiprocessing.Process(target=initiate)
    p1.daemon=True
    p1.start()
#_____________________________________________________________________________________#
    

    # root_dir = os.getcwd() 
    
    #from pathlib import Path
    # Path(working_dir).mkdir(parents=True, exist_ok=True)
    # Path(working_dir+'/modules').mkdir(parents=True, exist_ok=True)
    # Path(working_dir+'/logs').mkdir(parents=True,exist_ok=True)
    
    #let the application sleep so that observer gets started before logging for the first time
    sleep(.5)
    logger.info("Building Application...")
    blocks = build(working_dir)

    # Creating processes and assigning blocks. 
    logger.info("Creating Processes...")
    processes = []
    
    # os.chdir(working_dir)
    # mkpkg = open("modules/__init__.py", "w")
    # mkpkg.close()

    # os.chdir(root_dir)

    from importlib import import_module
    import sys
    # sys.path.append(working_dir)
    for i, element in enumerate(blocks):
        
        block_name = element.name
        try:
            method_name = 'modules.' + block_name + '.loop'
            module, function = method_name.rsplit('.',1)
        except TypeError as err:
            logger.error(str(err))
        
        try:
            mod = import_module(module)
            method = getattr(mod, function)
            element.sort_ports()
            input_args = element.input_ports
            output_args = element.output_ports
            parameters = element.parameters
            flags = [1,0,0]
            processes.append(multiprocessing.Process(target=method,
            args=(block_name, input_args, output_args, parameters, flags,)))
        except NameError as err:
            logger.error(str(err))
        

        
        
    logger.info("Starting Appilication")
    
    
    for process in processes:
        process.start()


    memories = []
    for process in processes:
        memories.append(read_string(str(process.pid)))
    def on_closing():
        end_progam
    
    while True:
        monitor_frequency(memories)
        if not msgQueue.empty():
            if msgQueue.get() == "#QUIT":
                p1.terminate()
                p1.join()
                end_progam() 




