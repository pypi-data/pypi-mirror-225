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

from th2_data_services.interfaces.utils.resolver import EventFieldsResolver, MessageFieldsResolver
from th2_data_services.data_source.lwdp.struct import http_event_struct, http_message_struct


class LwdpEventFieldsResolver(EventFieldsResolver):
    @staticmethod
    def get_id(event):
        return event[http_event_struct.EVENT_ID]

    @staticmethod
    def get_parent_id(event):
        return event[http_event_struct.PARENT_EVENT_ID]

    @staticmethod
    def get_status(event):
        return event[http_event_struct.STATUS]

    @staticmethod
    def get_name(event):
        return event[http_event_struct.NAME]

    @staticmethod
    def get_batch_id(event):
        return event[http_event_struct.BATCH_ID]

    @staticmethod
    def get_is_batched(event):
        return event[http_event_struct.IS_BATCHED]

    @staticmethod
    def get_type(event):
        return event[http_event_struct.EVENT_TYPE]

    @staticmethod
    def get_start_timestamp(event):
        return event[http_event_struct.START_TIMESTAMP]

    @staticmethod
    def get_end_timestamp(event):
        return event[http_event_struct.END_TIMESTAMP]

    @staticmethod
    def get_attached_messages_ids(event):
        return event[http_event_struct.ATTACHED_MESSAGES_IDS]

    @staticmethod
    def get_body(event):
        return event[http_event_struct.BODY]


class LwdpMessageFieldsResolver(MessageFieldsResolver):
    @staticmethod
    def get_subsequence(message):
        raise NotImplementedError

    @staticmethod
    def get_direction(message):
        return message[http_message_struct.DIRECTION]

    @staticmethod
    def get_session_id(message):
        return message[http_message_struct.SESSION_ID]

    @staticmethod
    def get_type(message):
        return message[http_message_struct.MESSAGE_TYPE]

    @staticmethod
    def get_connection_id(message):
        return message[http_message_struct.BODY]["metadata"]["id"][
            http_message_struct.CONNECTION_ID
        ]

    @staticmethod
    def get_session_alias(message):
        return message[http_message_struct.BODY]["metadata"]["id"][
            http_message_struct.CONNECTION_ID
        ][http_message_struct.SESSION_ALIAS]

    @staticmethod
    def get_sequence(message):
        return message[http_message_struct.BODY]["metadata"]["id"][http_message_struct.SEQUENCE]

    @staticmethod
    def get_timestamp(message):
        return message[http_message_struct.TIMESTAMP]

    @staticmethod
    def get_body(message):
        return message[http_message_struct.BODY]

    @staticmethod
    def get_body_base64(message):
        return message[http_message_struct.BODY_BASE64]

    @staticmethod
    def get_id(message):
        return message[http_message_struct.MESSAGE_ID]

    @staticmethod
    def get_attached_event_ids(message):
        return message[http_message_struct.ATTACHED_EVENT_IDS]

    @staticmethod
    def get_fields(message):
        return message[http_message_struct.BODY]["fields"]

    @staticmethod
    def expand_message(message):
        """Extract compounded message into list of individual messages.
        Args:
            message: Th2Message
        Returns:
            Iterable[Th2Message]
        """
        if "/" not in LwdpMessageFieldsResolver.get_type(message):
            return [message]
        result = []
        fields = LwdpMessageFieldsResolver.get_body(message)["fields"]
        for field in fields:
            msg_index = len(result)
            msg_type = field
            if "-" in field:
                msg_type = msg_type[: msg_type.index("-")]
                # TODO: Remove or keep this line?
                # m_index = int(k[k.index("-") + 1:])

            new_msg = {}
            new_msg.update(message)
            new_msg[http_message_struct.MESSAGE_TYPE] = msg_type
            new_msg[http_message_struct.BODY] = {}
            new_msg[http_message_struct.BODY]["metadata"] = {}
            new_msg[http_message_struct.BODY]["metadata"].update(
                LwdpMessageFieldsResolver.get_body(message)["metadata"]
            )
            new_msg[http_message_struct.BODY]["metadata"]["id"] = {}
            new_msg[http_message_struct.BODY]["metadata"]["id"].update(
                LwdpMessageFieldsResolver.get_body(message)["metadata"]["id"]
            )
            new_msg[http_message_struct.BODY]["metadata"][http_message_struct.MESSAGE_TYPE] = msg_type
            new_msg[http_message_struct.BODY]["metadata"]["id"][http_message_struct.SUBSEQUENCE] = [
                LwdpMessageFieldsResolver.get_body(message)["metadata"]["id"][http_message_struct.SUBSEQUENCE][
                    msg_index
                ]
            ]
            new_msg[http_message_struct.BODY]["fields"] = fields[field]["messageValue"]["fields"]
            result.append(new_msg)

        return result