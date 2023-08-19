# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""


from socket import gethostname
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
from multiprocessing.managers import BaseManager
from multiprocessing import Queue, Process
from time import sleep
import psutil

PORT_D = 9000
KEY_D = b"key"


class QueueManager(BaseManager):
    """
    QueueManager
    """


def run_queue_server(
    queuename: str, port: int, hostname: str = None, key: str = b"key"
):
    """
    run_queue_server
    """
    if not hostname:
        hostname = gethostname()
    manager = QueueManager(address=(hostname, port), authkey=key)
    queue = Queue()
    QueueManager.register(queuename, callable=lambda: queue)
    queue_done = Queue()
    QueueManager.register(queuename + "_done", callable=lambda: queue_done)
    queue_server = manager.get_server()
    # stopper = Timer(1, lambda: server.shutdown)
    # QueueManager.register(queuename + "_server", callable=lambda: server)
    print(f"Server Started (Host, Queue, Port) = ({hostname}, {queuename}, {port})")
    queue_server.serve_forever()


def connect_to_queue(
    queuename: str, hostname: str = None, port: int = PORT_D, key: str = KEY_D
):
    """
    connect_to_queue
    """
    if not hostname:
        hostname = gethostname()
    QueueManager.register(queuename)
    manager = QueueManager(address=(hostname, port), authkey=key)
    manager.connect()
    queue_function = getattr(manager, queuename)
    queue = queue_function()
    return queue


def kill_id(pid: int, reason: str = ""):
    """
    kill_id
    """
    if psutil.pid_exists(pid):
        if len(reason) > 0:
            print(f"Killing process due to {reason}: {pid}")
        process = psutil.Process(pid)
        for childproc in process.children(recursive=True):
            childproc.kill()
        process.kill()


def get_from_queue(
    server_id: int,
    queuename: str,
    hostname: str = None,
    port: int = PORT_D,
    key: str = KEY_D,
    stop: str = None,
):
    """
    get_from_queue
    """
    if not psutil.pid_exists(server_id):
        # [f"Process {server_id} Does Not Exist: {err}\n"]
        return False, False
    if not hostname:
        hostname = gethostname()
    if stop is not None:
        kill_id(server_id, reason=stop)
        return [f"Killed Process: {server_id}\n"], False
    try:
        queue = connect_to_queue(queuename, hostname=hostname, port=port, key=key)
        queue_done = connect_to_queue(
            queuename + "_done", hostname=hostname, port=port, key=key
        )
    except ConnectionRefusedError as err:  # ,OSError,ConnectionResetError
        outstring = f"!!!! No Connection with (Host,Queue,Port) = ({hostname},{queuename},{port})"
        return [f"{outstring}\n    Process {server_id} Killed: {err}\n"], False
    queueitems = []
    if (not queue_done.empty()) and queue.empty():
        _done = queue_done.get()
        return [" "], False  # f"\n\ndone message: {_done}"
    while (not queue.empty()) and (len(queueitems) < 100):
        queueitem = queue.get()
        queueitems.append(queueitem)
    return queueitems, True


def sub_stdout_stream(command: str, queuename: str, port: int):
    """
    sub_stdout_stream
    """
    queue = connect_to_queue(queuename, port=port)
    queue_done = connect_to_queue(queuename + "_done", port=port)
    # print(f"\nsub_stdout_stream Command:    {command}")
    process = Popen(
        command,
        stdout=PIPE,
        stderr=STDOUT,
        # shell=True,
        errors="ignore",
        encoding="utf-8",
        text=True,
    )
    for line in iter(process.stdout.readline, ""):
        if len(line) > 0:
            queue.put(line)
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        queue_done.put("error")
        return CalledProcessError(return_code, command)
    queue_done.put("success")
    return


def stream_queue(queuename: str, command: str, port: int = PORT_D):
    """
    stream_queue
    """
    server_proc = Process(target=run_queue_server, args=(queuename, port))
    server_proc.start()
    stream_proc = Process(target=sub_stdout_stream, args=(command, queuename, port))
    stream_proc.start()
    print(
        f"\nServer Process ID = {server_proc.pid}, Stream Process ID = {stream_proc.pid}"
    )
    stream_proc.join()
    server_proc.join()
    return server_proc, stream_proc


def test():
    """
    test
    """
    queuename = "test_server"
    testpath = "C:\\Users\\jkris\\OneDrive\\2022_onward\\2023\\python\\myrepo\\dash\\codenav\\codenav\\queue_test.py"
    serverpath = "C:\\Users\\jkris\\OneDrive\\2022_onward\\2023\\python\\myrepo\\dash\\codenav\\codenav\\shell_server.py"
    activate = (
        "C:\\ProgramData\\Anaconda3\\Scripts\\activate.bat && conda activate py39"
    )
    runpycmd = f'{activate} && python ""{testpath}""'
    server_args = f'"{serverpath}" "{queuename}" "{runpycmd}"'
    runserver = f"{activate} && python {server_args}"
    print(f"\nServer Command:\n{runserver}")
    parent_proc = Popen(runserver, shell=True)
    print("\nParent Process Started")
    pid = parent_proc.pid
    i = 0
    increment = 0.25
    status = True
    while status:  # psutil.pid_exists(pid) and
        lines, status = get_from_queue(pid, queuename, port=PORT_D)
        print(
            f"\n    time={i} : proc[{pid}]={psutil.pid_exists(pid)} : Status={status}"
        )
        print("".join(lines))
        i += increment
        sleep(increment)
    print("\nLoop Finished")
    lines, status = get_from_queue(pid, queuename, port=PORT_D, stop=True)
    print(f"\n    time={i} : proc[{pid}]={psutil.pid_exists(pid)} : Status={status}")
    print("".join(lines))
    # parent_proc.wait()
    print("\nFinal Check")
    lines, status = get_from_queue(pid, queuename, port=PORT_D, stop=True)
    print(f"\n    time={i} : proc[{pid}]={psutil.pid_exists(pid)} : Status={status}")
    if lines:
        print("".join(lines))


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 1:
        test()
    else:
        PORT = PORT_D
        if len(argv) > 3:
            PORT = int(argv[3])
        stream_queue(argv[1], argv[2], PORT)
