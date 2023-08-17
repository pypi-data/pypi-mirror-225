import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")

from MobileHelperService.api import (MobileHelper as Api,
                                     MobileSession,
                                     MobileOutput,
                                     MobileInput,
                                     MobileUserInput,
                                     MobileMarkInput,
                                     InternalInterrupt,
                                     AddressedInterruption,
                                     Flags)
from pih import A
from pih import PIH, Stdin, NotFound, SubscribtionResult
from pih.tools import (ParameterList, 
                        BitMask as BM, 
                        nl,
                        if_else,
                        j)
from pih.rpc_collection import ServiceDescription
from pih.collection import WhatsAppMessage, User
from MobileHelperService.const import SD

from threading import Thread
from collections import defaultdict
from typing import Callable, Any

SC = A.CT_SC

DEFAULT_COUNT: int = 10

#version 0.8

DEVELOPER_ALIAS: str = "developer"
COUNT_ALIAS: str = "count"

class MobileHelperService():

    _is_develpoer: bool = False

    @staticmethod
    def is_developer() -> bool:
        host: str = A.OS.host()
        return MobileHelperService._is_develpoer or A.D.contains(host, A.CT_H.DEVELOPER.NAME)

    @staticmethod
    def count() -> int:
        return A.SE.named_arg(COUNT_ALIAS)

    NAME: str = "MobileHelper"

    A.U.for_service(SD)

    mobile_helper_client_map: dict[str, Api] = {}

    def __init__(self, max_client_count: int | None, checker: Callable[[str], bool] | None = None):
        self.max_client_count: int | None = max_client_count
        self.root: str = PIH.NAME
        self.checker: Callable[[str], bool] | None = checker
        self.service_description: SD = SD
        self.allow_send_to_next_service_in_chain: dict[str, bool] = defaultdict(
            bool)

    def start(self) -> bool:
        A.SE.add_arg(DEVELOPER_ALIAS,
                     nargs="?", const="True", type=str, default="False")
        A.SE.add_arg(COUNT_ALIAS,
                     nargs="?", const=1, type=int, default=DEFAULT_COUNT)
        service_desctiption: ServiceDescription | None = A.SRV_A.create_support_service_or_master_service_description(self.service_description)
        if A.SRV.is_service_as_support(service_desctiption):
            MobileHelperService._is_develpoer = A.SE.named_arg(
                DEVELOPER_ALIAS).lower() in ["1", "true"]
        else:
            MobileHelperService._is_develpoer = False
        if not A.D_C.empty(service_desctiption):
            A.SRV_A.serve(service_desctiption, self.service_call_handler,
                            MobileHelperService.service_starts_handler)
            return True

    def create_mobile_helper(self, telephone_number: str, flags: int | None = None, recipient: str | None = None) -> Api:
        stdin: Stdin = Stdin()
        session: MobileSession = MobileSession(telephone_number, flags)
        output: MobileOutput = MobileOutput(session)
        session.say_hello(recipient)
        input: MobileInput = MobileInput(
            stdin, MobileUserInput(), MobileMarkInput(), output, session)
        return Api(PIH(input, output, session), stdin)

    @staticmethod
    def say_good_bye(mobile_helper: Api) -> str:
        mobile_helper.say_good_bye()

    def pih_handler(self, telephone_number: str, line: str | None = None, sender_user: User | None = None, flags: int | None = 0, chat_id: str | None = None) -> None:
        mobile_helper: Api | None = None
        allow_for_group: bool = telephone_number in [A.D.get(A.CT_ME_WH.GROUP.IT)]
        while True:
            try:
                if MobileHelperService.is_client_new(telephone_number):
                    A.IW.remove(
                        A.CT.MOBILE_HELPER.POLIBASE_PERSON_PIN, telephone_number)
                    if allow_for_group or Api.check_for_starts_with_pih_keyword(line):
                        self.allow_send_to_next_service_in_chain[telephone_number] = self.is_client_stack_full()
                        if not self.allow_send_to_next_service_in_chain[telephone_number]:
                            MobileHelperService.mobile_helper_client_map[telephone_number] = self.create_mobile_helper(
                                telephone_number, flags, chat_id)
                    else:
                        self.allow_send_to_next_service_in_chain[telephone_number] = False
                else:
                    self.allow_send_to_next_service_in_chain[telephone_number] = False
                if telephone_number in MobileHelperService.mobile_helper_client_map:
                    mobile_helper = MobileHelperService.mobile_helper_client_map[telephone_number]
                    if not mobile_helper.wait_for_input():
                        if not line.lower().startswith(Api.PIH_KEYWORDS):
                            line = j((Api.PIH_KEYWORDS[0], line), " ")
                    show_good_bye: bool = mobile_helper.level == 0
                    if Api.check_for_starts_with_pih_keyword(line):
                        mobile_helper.level = 0
                    if mobile_helper.do_pih(line, sender_user, flags):
                        if show_good_bye and mobile_helper.level <= 0:
                            if A.D.is_none(flags) or not BM.has(flags, Flags.SILENCE):
                                MobileHelperService.say_good_bye(mobile_helper)
                break
            except NotFound:
                break
            except InternalInterrupt as interruption:
                if interruption.type == A.CT.MOBILE_HELPER.InteraptionTypes.INTERNAL:
                    line = mobile_helper.line
                    if not Api.check_for_starts_with_pih_keyword(line):
                        MobileHelperService.say_good_bye(mobile_helper)
                        break
                else:
                    MobileHelperService.say_good_bye(mobile_helper)
                    break

    def is_client_stack_full(self) -> bool:
        max_client_count: int | None = self.max_client_count
        if A.D.is_none(max_client_count):
            max_client_count = MobileHelperService.count()
        return len(MobileHelperService.mobile_helper_client_map) == max_client_count

    def is_client_new(value: str) -> bool:
        return value not in MobileHelperService.mobile_helper_client_map

    def receive_message_handler(self, message_text: str, telephone_number: str, flags: int | None = None, chat_id: str | None = None) -> None:
        interruption: AddressedInterruption | None = None
        while True:
            try:
                if A.D_C.empty(interruption):
                    self.pih_handler(telephone_number,
                                     message_text, None, flags, chat_id)
                else:
                    for recipient_user in interruption.recipient_user_list():
                        recipient_user: User = recipient_user
                        self.pih_handler(recipient_user.telephoneNumber, " ".join(
                            [self.root, interruption.command_name]), interruption.sender_user, interruption.flags)
                    interruption = None
                break
            except AddressedInterruption as local_interruption:
                interruption = local_interruption

    def receive_message_handler_thread_handler(self, message: WhatsAppMessage) -> None:
        self.receive_message_handler(
            message.message, message.sender, None, message.chatId)

    def service_call_handler(self, sc: SC, parameter_list: ParameterList, subscribtion_result: SubscribtionResult | None) -> Any:
        if sc == A.CT_SC.send_event:
            if A.D.is_not_none(subscribtion_result) and subscribtion_result.result:
                if subscribtion_result.type == A.CT_SubT.ON_RESULT_SEQUENTIALLY:
                    message: WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(
                        parameter_list)
                    if A.D.is_not_none(message):
                        if A.D.get_by_value(A.CT_ME_WH_W.Profiles, message.profile_id) == A.CT_ME_WH_W.Profiles.IT:
                            allow_for_group: bool = not A.D_C.empty(message.chatId) and message.chatId in [
                                A.D.get(A.CT_ME_WH.GROUP.IT)]
                            if A.D.is_none(message.chatId) or allow_for_group:
                                telephone_number: str = if_else(allow_for_group, message.chatId, message.sender)
                                if allow_for_group:
                                    message.chatId = message.sender
                                    message.sender = telephone_number
                                if A.D.is_none(self.checker) or self.checker(telephone_number):
                                    if self.is_client_stack_full():
                                        return True
                                    else:
                                        if telephone_number in self.allow_send_to_next_service_in_chain:
                                            del self.allow_send_to_next_service_in_chain[telephone_number]
                                        Thread(target=self.receive_message_handler_thread_handler, args=[
                                               message]).start()
                                        while telephone_number not in self.allow_send_to_next_service_in_chain:
                                            pass
                                        return self.allow_send_to_next_service_in_chain[telephone_number]
                                else:
                                    if telephone_number in MobileHelperService.mobile_helper_client_map:
                                        del MobileHelperService.mobile_helper_client_map[telephone_number]
                                    return True
            return False
        if sc == A.CT_SC.send_mobile_helper_message:
            self.receive_message_handler(
                " ".join((self.root, parameter_list.next())), parameter_list.next(), parameter_list.next())
        return None

    @staticmethod
    def service_starts_handler() -> None:
        A.O.write_line(nl())
        A.O.blue("Configuration:")
        with A.O.make_indent(1):
            A.O.value("For developer", str(MobileHelperService.is_developer()))
            A.O.value("Count", str(MobileHelperService.count()))
        A.SRV_A.subscribe_on(A.CT_SC.send_event, A.CT_SubT.ON_RESULT_SEQUENTIALLY, MobileHelperService.NAME)
