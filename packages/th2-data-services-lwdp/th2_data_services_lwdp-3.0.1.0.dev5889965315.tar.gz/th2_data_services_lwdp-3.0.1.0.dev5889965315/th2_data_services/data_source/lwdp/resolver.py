#  Copyright 2023 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from th2_data_services.interfaces.utils import resolver as resolver_core
from th2_data_services.data_source.lwdp.struct import event_struct, message_struct


class EventFieldResolver(resolver_core.EventFieldResolver):
    @staticmethod
    def get_id(event):
        return event[event_struct.EVENT_ID]

    @staticmethod
    def get_parent_id(event):
        return event[event_struct.PARENT_EVENT_ID]

    @staticmethod
    def get_status(event):
        return event[event_struct.STATUS]

    @staticmethod
    def get_name(event):
        return event[event_struct.NAME]

    @staticmethod
    def get_batch_id(event):
        return event[event_struct.BATCH_ID]

    @staticmethod
    def get_is_batched(event):
        return event[event_struct.IS_BATCHED]

    @staticmethod
    def get_type(event):
        return event[event_struct.EVENT_TYPE]

    @staticmethod
    def get_start_timestamp(event):
        return event[event_struct.START_TIMESTAMP]

    @staticmethod
    def get_end_timestamp(event):
        return event[event_struct.END_TIMESTAMP]

    @staticmethod
    def get_attached_messages_ids(event):
        return event[event_struct.ATTACHED_MESSAGES_IDS]

    @staticmethod
    def get_body(event):
        return event[event_struct.BODY]


class MessageFieldResolver(resolver_core.MessageFieldResolver):
    @staticmethod
    def get_direction(message):
        return message[message_struct.DIRECTION]

    @staticmethod
    def get_session_id(message):
        return message[message_struct.SESSION_ID]

    @staticmethod
    def get_type(message):
        raise NotImplementedError

    @staticmethod
    def get_sequence(message):  # <book>:<alias>:<direction>:<timestamp>:<sequence>.<\d>.<\d>
        return message[message_struct.MESSAGE_ID].split(":")[4].split(".")[0]

    @staticmethod
    def get_timestamp(message):
        return message[message_struct.TIMESTAMP]

    @staticmethod
    def get_body(message):
        return message[message_struct.BODY]

    @staticmethod
    def get_body_base64(message):
        return message[message_struct.BODY_BASE64]

    @staticmethod
    def get_id(message):
        return message[message_struct.MESSAGE_ID]

    @staticmethod
    def get_attached_event_ids(message):
        return message[message_struct.ATTACHED_EVENT_IDS]

    @staticmethod
    def expand_message(message):
        """Extract compounded message into list of individual messages.

        Args:
            message: Th2Message

        Returns:
            Iterable[Th2Message]
        """
        # TODO 
        #    - the version on Ilya from *** project. Should be reviewed later
        #    - all sub-messages will have the same MessageID
        result = []
        
        for m in message:
            for body in m['body']:
                body['fields'] = dict((k, v) for k, v in body['fields'].items() if v is not None)
                new_m = {**m, 
                         message_struct.BODY: body, 
                         message_struct.MESSAGE_TYPE: body['metadata']['messageType']}
    
                result.append(new_m)
                
        return result


class SubMessageFieldResolver(resolver_core.SubMessageFieldResolver):
    @staticmethod
    def get_metadata(sub_message):
        return sub_message["metadata"]

    @staticmethod
    def get_subsequence(sub_message):
        return SubMessageFieldResolver.get_metadata(sub_message).get(
            message_struct.SUBSEQUENCE, [1]
        )

    @staticmethod
    def get_type(sub_message):
        return SubMessageFieldResolver.get_metadata(sub_message)[message_struct.MESSAGE_TYPE]

    @staticmethod
    def get_protocol(sub_message):
        return SubMessageFieldResolver.get_metadata(sub_message).get(message_struct.PROTOCOL)

    @staticmethod
    def get_fields(sub_message):
        return sub_message["fields"]


# TODO - for backward compatibility. Should be removed some time.
LwdpEventFieldsResolver = EventFieldResolver
LwdpMessageFieldsResolver = MessageFieldResolver
