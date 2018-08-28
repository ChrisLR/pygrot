import json
from twisted.internet.protocol import DatagramProtocol
from pygrot.netmessages import listing


class Echo(DatagramProtocol):
    def datagramReceived(self, data, info):
        messages = build_message(data)

        return self.listener.handle_messages(info, messages)

    def send(self, client, messages, sender):
        capsule = listing.MessageCapsule(messages, sender)
        capsule_json = capsule.to_json()
        encoded_json_capsule = capsule_json.encode("utf8")
        self.echo_protocol.transport.write(encoded_json_capsule, client.address)


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
