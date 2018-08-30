import json
import socket
import threading
import queue
from pygrot.netmessages import listing
import time


class CommSocket(threading.Thread):
    def __init__(self, local_port, target_address, target_port, in_queue, out_queue, cancel_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_port = local_port
        self.target_address = target_address
        self.target_port = target_port
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.cancel_queue = cancel_queue

    def run(self):
        print("Running CommSocket binding on " + str(self.local_port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("localhost", self.local_port))
            sock.setblocking(False)
            while True:
                try:
                    if not self.cancel_queue.empty():
                        interrupt = self.cancel_queue.get()
                        if interrupt:
                            print('Got interrupt')
                            return
                except queue.Empty:
                    pass

                try:
                    if not self.out_queue.empty():
                        messages, address = self.out_queue.get()
                        if messages:
                            print('Out Messages are not empty')
                            sock.sendto(messages, address)
                except queue.Empty:
                    pass

                try:
                    data, server = sock.recvfrom(4096)
                    if data:
                        print('Put messages in the IN queue')
                        self.in_queue.put((server, data))
                except BlockingIOError:
                    pass
        finally:
            sock.close()


class Echo(object):
    def __init__(self, local_port, target_address, target_port):
        self.in_queue = queue.Queue()
        self.out_queue = queue.Queue()
        self.cancel_queue = queue.Queue()
        self.comm_socket = CommSocket(local_port, target_address, target_port, self.in_queue, self.out_queue, self.cancel_queue)

    def get(self):
        try:
            if not self.in_queue.empty():
                remote_info, raw_messages = self.in_queue.get()
                messages = build_message(raw_messages)
                return remote_info, messages
            return None, None
        except queue.Empty:
            return None, None

    def send(self, client, messages, sender):
        capsule = listing.MessageCapsule(messages, sender)
        capsule_json = capsule.to_json()
        encoded_json_capsule = capsule_json.encode("utf8")
        self.out_queue.put((encoded_json_capsule, client.address))

    def stop(self):
        self.cancel_queue.put("STOPPING NOW")

    def start(self):
        print("Comm Socket starting")
        self.comm_socket.start()
        print("Comm Socket Started")


def build_message(data):
    decoded_data = data.decode("utf8")
    message_capsule = json.loads(decoded_data)
    messages = message_capsule.get("sub_messages")
    if messages is None:
        print("Unrecognized message " + decoded_data)
        return

    built_messages = []
    for message in messages:
        type_no = message.get("type_no")
        sub_message = message.get("message")
        if type_no is None or sub_message is None:
            print("Unrecognized sub message " + message)
            continue

        mapped_type = listing.message_mapping.get(type_no)
        instanced_type = mapped_type(**sub_message)
        built_messages.append(instanced_type)

    return built_messages
