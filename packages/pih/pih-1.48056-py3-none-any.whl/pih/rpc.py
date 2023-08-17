import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.tools import ParameterList, BitMask as BM, j
from pih.const import CONST, ServiceRoles, SubscribtionTypes
from pih.rpc_collection import Subscribtion, SubscriberInformation, ServiceDescription, ServiceInformation, ServiceInformationBase, SubscribtionInformation, SubscribtionResult
from pih.rpc_const import ServiceCommands as SC
import pih.rpcCommandCall_pb2_grpc as pb2_grpc
import pih.rpcCommandCall_pb2 as pb2
import threading
from typing import Any, Callable
import grpc
from grpc import Server
from concurrent import futures
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
import psutil

@dataclass
class Error(BaseException):
    details: str
    code: tuple

class IService:

    def serve(self, role_or_information: ServiceRoles | ServiceInformationBase, call_handler: Callable[[str, ParameterList, Any], Any] | None = None, starts_handler: Callable[[Any | None], None] | None = None, max_workers: int | None = None, depends_on_list: list[ServiceRoles | ServiceDescription] | None = None, show_output: bool = True) -> None:
        raise NotImplemented()

    def create_subscribtions(self, information: ServiceInformationBase | None = None) -> None:
        raise NotImplemented()

    @property
    def subscribtions(self) -> list[SubscribtionInformation]:
        raise NotImplemented()

    def stop(self) -> Server:
        raise NotImplemented()

    def subscribe_on(self, sc: SC, type: int = SubscribtionTypes.ON_RESULT, name: str | None = None) -> bool:
        raise NotImplemented()

    def unsubscribe(self, commnad_list: list[SC] = None, type: int = None) -> bool:
        raise NotImplemented()

    def get_description(self) -> ServiceDescription:
        raise NotImplemented()

DEBUG: bool = False

class RPC:

    server: Server | None = None
   
    class SESSION:

        start_time: datetime
        life_time: timedelta

        thread_map: list[int] = []
       
    @staticmethod
    def create_service() -> IService:
        return RPC.Service()

    @staticmethod
    def create_error(context, message: str = "", code: Any = None) -> Any:
        context.set_details(message)
        context.set_code(code)
        return pb2.rpcCommandResult()
    
    class UnaryService(pb2_grpc.UnaryServicer):

        def __init__(self, service: IService, description: ServiceDescription, call_handler: Callable[[str, ParameterList, Any], Any] | None = None, *args, **kwargs):
            self.service_information = description
            self.call_handler = call_handler
            self.service = service
            self.subscriber_information_map: dict[SC,
                                      dict[str, SubscriberInformation]] = defaultdict(dict)

        def internal_call_handler(self, command_name: str, parameters: Any, context) -> Any:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            try:
                #A.O.value("rpc call", command_name)
                #thread_id: int = threading.get_ident()
                #A.O.value("thread", str(thread_id))
                sc: SC | None = A.D.get(SC, command_name)
                parameter_list: ParameterList = ParameterList(parameters)
                if not A.D_C.empty(sc):
                    if sc == SC.stop_service:
                        is_subscriber: bool = A.SRV.is_service_as_listener(
                            self.service_information)
                        if not is_subscriber:
                            RPC.call_service_command(
                            A.CT_SC.on_service_stops, self.service_information)
                        self.service.stop()
                        if not is_subscriber:
                            pid: int = A.OS.pid()
                            parent = psutil.Process(pid)
                            for child in parent.children(recursive=True):
                                child.kill()
                        return
                    if sc == SC.ping:
                        return A.D.fill_data_from_source(ServiceInformation(), self.service_information)
                    if sc == SC.subscribe:
                        return self.subscribe_with_parameter_list(parameter_list)
                    if sc == SC.unsubscribe:
                        return self.unsubscribe_with_parameter_list(parameter_list)
                    if sc == SC.create_subscribtions:
                        self.service.create_subscribtions(parameter_list.next(ServiceInformationBase()))
                        return True
                    if sc == SC.update_service_information:
                        A.SRV_A.update_service_information(parameter_list.next_as_list(
                            ServiceInformation), parameter_list.next())
                        return True
                    if sc == SC.heart_beat:
                        date_string: str = A.D_Ex.parameter_list(parameter_list).get()
                        date: datetime = datetime.strptime(date_string, CONST.ISO_DATETIME_FORMAT)
                        parameter_list.set(0, date)
                        RPC.SESSION.life_time = date - RPC.SESSION.start_time
                return None if A.D_C.empty(self.call_handler) else self.call_subscribers_after(sc, parameter_list, self.call_handler(
                    command_name, self.call_subscribers_before(sc, parameter_list), context))
            except Exception as error:
                A.ER.global_except_hook(type(error), error, error.__traceback__)

        def unsubscribe_all(self) -> None:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            def unsubscribe_all_internal() -> None:
                for sc in self.subscriber_information_map:
                    for service_information_name in self.subscriber_information_map[sc]:
                        subscriber_information: SubscriberInformation = self.subscriber_information_map[sc][service_information_name]
                        A.D.rpc_unrepresent(RPC.call_service(
                            subscriber_information.service_information, SC.unsubscribe, (sc, subscriber_information.name)))
                self.subscriber_information_map = defaultdict(dict)
            threading.Thread(target=unsubscribe_all_internal).start()

        def unsubscribe_with_parameter_list(self, value: ParameterList) -> None:
            description: ServiceDescription = value.next(
                ServiceDescription())
            role_description_name: str = description.name
            for service_command in self.subscriber_information_map:
                if role_description_name in self.subscriber_information_map[service_command]:
                    del self.subscriber_information_map[service_command][role_description_name]
                 
        def subscribe_with_parameter_list(self, value: ParameterList) -> bool:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            service_information: ServiceInformationBase = value.next(
                ServiceInformationBase())
            subscribtion_information: SubscribtionInformation = value.next(
                SubscribtionInformation())
            subscribtion_information.service_command = A.D.get(SC, subscribtion_information.service_command)
            return self.subscribe(service_information, subscribtion_information)
        
        def subscribe(self, service_description: ServiceDescription, subscribtion_information: SubscribtionInformation) -> bool:
            sc: SC = subscribtion_information.service_command
            name: str | None = subscribtion_information.name
            type: int = subscribtion_information.type
            if sc in self.subscriber_information_map:
                if service_description.name in self.subscriber_information_map[sc]:
                    subscriber_information: SubscriberInformation = self.subscriber_information_map[sc][service_description.name]
                    if subscriber_information.service_information == service_description and BM.has(subscriber_information.type, type):
                        self.subscriber_information_map[sc][service_description.name] = SubscriberInformation(
                            type, name, service_information=service_description)
                else:
                    self.subscriber_information_map[sc][service_description.name] = SubscriberInformation(
                        type, name, service_information=service_description)
            else:
                self.subscriber_information_map[sc][service_description.name] = SubscriberInformation(
                    type, name, service_information=service_description)
            return True

        def call_subscribers_before(self, sc: SC, in_result: ParameterList):
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            out_result: ParameterList = in_result
            if sc in self.subscriber_information_map:
                for service_information_name in list(self.subscriber_information_map[sc]):
                    subscriber_information: SubscriberInformation = self.subscriber_information_map[sc][service_information_name]
                    service_information: ServiceInformation = subscriber_information.service_information
                    if BM.has(subscriber_information.type, SubscribtionTypes.ON_PARAMETERS) and subscriber_information.enabled:
                        subscriber_information.available = RPC.check_availability(service_information)
                        if subscriber_information.available:
                            out_result = ParameterList(A.D.rpc_unrepresent(RPC.call_service(
                                service_information, sc, (in_result, SubscribtionResult(None, SubscribtionTypes.ON_PARAMETERS, True)))))
                        else:
                            del self.subscriber_information_map[sc][service_information_name]
            return out_result

        def call_subscribers_after(self, sc: SC, parameter_list: ParameterList, result: Any) -> Any:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            def internal_call_subscribers_after_sequentially(sc: SC, subscriber_list: list[SubscriberInformation], parameter_list: ParameterList, result: Any):
                for subscriber in subscriber_list:
                    role_description_item: ServiceDescription = subscriber.service_information
                    subscriber.available = RPC.check_availability(role_description_item)
                    if subscriber.available:
                        result = RPC.call_service(
                            role_description_item, sc, (parameter_list, SubscribtionResult(result, SubscribtionTypes.ON_RESULT_SEQUENTIALLY, True)))
                    else:
                        if A.D.if_is_in(self.subscriber_information_map[sc], role_description_item.name):
                            del self.subscriber_information_map[sc][role_description_item.name]
            def internal_call_subscribers_after(sc: SC, subscriber_information: SubscriberInformation, parameter_list: ParameterList, result: Any):
                service_information: ServiceInformationBase = subscriber_information.service_information
                subscriber_information.available = RPC.check_availability(
                    service_information)
                if subscriber_information.available:
                    RPC.call_service(
                        service_information, sc, (parameter_list, SubscribtionResult(result, SubscribtionTypes.ON_RESULT, True)))
                else:
                    if service_information.name in self.subscriber_information_map[sc]:
                        del self.subscriber_information_map[sc][service_information.name]
            if sc in self.subscriber_information_map:
                after_sequentially_subscriber_information_list: list[SubscriberInformation] = []
                for servce_information_name in list(self.subscriber_information_map[sc]):
                    subscriber_information: SubscriberInformation = self.subscriber_information_map[sc][servce_information_name]
                    if subscriber_information.enabled:
                        if BM.has(subscriber_information.type, SubscribtionTypes.ON_RESULT):
                            threading.Thread(target=internal_call_subscribers_after, args=(
                                sc, subscriber_information, parameter_list, result)).start()
                        elif BM.has(subscriber_information.type, SubscribtionTypes.ON_RESULT_SEQUENTIALLY):
                            after_sequentially_subscriber_information_list.append(subscriber_information)
                if not A.D_C.empty(after_sequentially_subscriber_information_list):
                    threading.Thread(target=internal_call_subscribers_after_sequentially, args=(
                        sc, after_sequentially_subscriber_information_list, parameter_list, result)).start()

            return result

        def rpcCallCommand(self, command, context):
            if DEBUG:
                    from pih import A
            else:
                A = sys.modules["pih.pih"].A
            parameters = command.parameters
            if not A.D_C.empty(parameters):
                parameters = A.D.rpc_unrepresent(parameters)
            result: Any = self.internal_call_handler(command.name, parameters, context)
            if context.code() is None:
                return pb2.rpcCommandResult(data=A.D.rpc_represent(result))
            return result

    class Service(IService):

        MAX_WORKERS: int = 10

        def __init__(self):
            self.description: ServiceDescription | None = None
            self.information: ServiceInformation | None = None
            self.subscribtions_map: dict[ServiceInformationBase, dict[SC, Subscribtion]] = defaultdict(dict)
            self.server: Server | None = None

        def get_description(self) -> ServiceDescription:
            return self.description

        def serve(self, role_or_information: ServiceRoles | ServiceInformationBase, call_handler: Callable[[str, ParameterList, Any], Any] | None = None, starts_handler: Callable[[IService | None], None] | None = None, max_workers: int | None = None, depends_on_list: list[ServiceRoles | ServiceDescription] | None = None, show_output: bool = True) -> None:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            max_workers = max_workers or RPC.Service.MAX_WORKERS
            service_description: ServiceDescription = role_or_information if isinstance(
                role_or_information, ServiceInformationBase) else A.CT_SR.description(role_or_information)
            self.description = service_description
            with A.ER.detect():
                if not A.SRV.is_service_as_listener(role_or_information):
                    arg_name: str = "isolated"
                    A.SE.add_arg(arg_name,
                                    help="Service isolated flag", nargs="?", const=1, type=str, default=None)
                    isolate_arg: str | None = None
                    try:
                        isolated_arg_value: str | None = A.SE.named_arg(arg_name)
                        if A.D.is_not_none(isolated_arg_value):
                            isolate_arg = str(isolated_arg_value).lower()
                    except AttributeError as error:
                        pass
                    if A.D.is_not_none(isolate_arg):
                        if A.D.is_none(self.description.isolated):
                            self.description.isolated = isolate_arg not in ["0", "no", "false"]
                        elif self.description.isolated:
                            self.description.isolated = isolate_arg not in [
                                "0", "no", "false"]
            self.description.pih_version = A.V.value
            self.description.host = A.SRV.create_host(self.description)
            self.description.port = A.SRV.create_port(self.description)
            self.information = A.D.fill_data_from_source(ServiceInformation(), self.description)
            self.information.pid = A.OS.pid()
            if A.D_C.empty(RPC.service):
                RPC.service_description = self.description
                RPC.service_information = self.information
                RPC.service = self
            if show_output:
                A.O.init()
                A.O.service_header(self.information)
                A.O.good(f"Service was started!")
            self.server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=max_workers))
            if RPC.server is None:
                RPC.server = self.server
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(self, self.description, call_handler), self.server)
            try:
                if DEBUG:
                    from pih import while_not_do
                else:
                    while_not_do = sys.modules["pih.pih"].while_not_do
                self.server.add_insecure_port(
                    ":".join((self.description.host, str(self.description.port))))
                self.server.start() 
                if not A.D.is_empty(depends_on_list):
                    A.O.write_line("Dependencies availability check...")
                    while_not_do(lambda: len(list(filter(lambda item: A.SRV.check_on_accessibility(item if isinstance(
                        item, ServiceDescription) else item.value), depends_on_list))) == len(depends_on_list))
                    A.O.write_line("All dependencies are online")  
                RPC.SESSION.start_time = datetime.now().replace(second=0, microsecond=0)
                starts_handler(self)
                self.information.subscribtions = self.subscribtions
                RPC.call_service_command(A.CT_SC.on_service_starts, self.information)
                with A.ER.detect_interruption("Выход"):
                    self.server.wait_for_termination()
            except RuntimeError as error:
                A.E.service_was_not_started(self.description, "".join(error.args))

        def create_subscribtions(self, information: ServiceInformationBase | None = None) -> None:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            def internal_create_subscribtion(subscribtions: dict[ServiceInformationBase, dict[SC, Subscribtion]], information: ServiceInformationBase):
                for sc in subscribtions[information]:
                    subscription: Subscribtion = subscribtions[information][sc]
                    RPC.call_service(information, SC.subscribe, (A.D.fill_data_from_source(ServiceInformationBase(
                    ), self.information), A.D.fill_data_from_source(SubscribtionInformation(), subscription)))
                    subscription.available = True
                    subscription.enabled = True
            for description_item in self.subscribtions_map if A.D_C.empty(information) else [information]:
                if A.SRV.check_on_accessibility(description_item):
                    internal_create_subscribtion(self.subscribtions_map, description_item)

        @property
        def subscribtions(self) -> list[Subscribtion]:
            result: list[Subscribtion] = []
            for description_item in self.subscribtions_map:
                for sc in self.subscribtions_map[description_item]:
                    result.append(self.subscribtions_map[description_item][sc])
            return result
     
        def subscribe_on(self, sc: SC, type: int = SubscribtionTypes.ON_RESULT, name: str | None = None) -> bool:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            service_description: ServiceDescription = A.SRV.description_by_command(sc)
            if not A.D_C.empty(service_description):
                if service_description != self.description:
                    subscribtion: Subscribtion | None = None
                    if sc not in self.subscribtions_map[service_description]:
                        subscribtion = Subscribtion(sc, type, name)
                        self.subscribtions_map[service_description][sc] = subscribtion
                    else:
                        subscribtion = self.subscribtions_map[service_description][sc]
                        subscribtion.type |= type
                    subscribtion.available = A.SRV.check_on_accessibility(service_description)
                    return subscribtion.available
            return False

        def unsubscribe(self, commnad_list: list[SC] = None, type: int = None) -> bool:
            if DEBUG:
                from pih import A
            else:
                A = sys.modules["pih.pih"].A
            for service_description in self.subscribtions_map:
                for sc in self.subscribtions_map[service_description]:
                    if sc in commnad_list:
                        A.D.rpc_unrepresent(RPC.call_service(service_description, SC.unsubscribe, (self.description, )))

        def unsubscribe_all(self, role_or_information: ServiceRoles | ServiceInformationBase) -> bool:
            pass
            #return self.unsubscribe(role_or_information)

        def stop(self) -> None:
            self.server.stop(0)
    
    class CommandClient():

        def __init__(self, host: str, port: int):
            self.stub = pb2_grpc.UnaryStub(grpc.insecure_channel(f"{host}:{port}"))

        def call_command(self, name: str, parameters: str | None = None, timeout: int = None):
            return self.stub.rpcCallCommand(pb2.rpcCommand(name=name, parameters=parameters), timeout=timeout)

    @staticmethod
    def ping(role_or_information: ServiceRoles | ServiceInformationBase) -> ServiceInformation:
        if DEBUG:
            from pih import A
        else:
            A = sys.modules["pih.pih"].A
        try:
            service_information: ServiceInformationBase = A.CT_SR.description(
                role_or_information)
            return A.D.fill_data_from_rpc_str(ServiceInformation(), RPC.call_service(service_information, SC.ping, ((RPC.service_information or A.CT_SR.STUB).name), ))
        except Error:
            return None
        
    @staticmethod
    def stop(role_or_information: ServiceRoles | ServiceInformationBase) -> ServiceInformation:
        if DEBUG:
            from pih import A
        else:
            A = sys.modules["pih.pih"].A
        return RPC.call_service(A.CT_SR.description(role_or_information), SC.stop_service)

    @staticmethod
    def check_availability(role_or_information: ServiceRoles | ServiceInformationBase) -> bool:
        if DEBUG:
            from pih import A
        else:
            A = sys.modules["pih.pih"].A
        return not A.D_C.empty(RPC.ping(role_or_information))
    
    @staticmethod
    def call_service(role_or_information: ServiceRoles | ServiceInformationBase | None, sc: SC, parameters: Any | None = None, timeout: int | None = None) -> str | None:
        if DEBUG:
            from pih import A
        else:
            A = sys.modules["pih.pih"].A
        information: ServiceInformationBase | None = role_or_information if role_or_information is None else A.CT_SR.description(role_or_information)
        try:
            if A.D_C.empty(information):
                information = A.SRV.description_by_command(sc)
            service_host: str | None = A.SRV.get_host(information)
            service_port: int | None = A.SRV.get_port(information)
            if A.D_C.empty(timeout):
                if A.D_C.empty(RPC.service_information) or RPC.service_information.isolated or information.isolated:
                    if sc == SC.ping:
                        timeout = CONST.RPC.TIMEOUT_FOR_PING
                    else:
                        timeout = CONST.RPC.TIMEOUT
            return RPC.CommandClient(service_host, service_port).call_command(sc.name, A.D.rpc_represent(parameters), timeout).data
        except grpc.RpcError as error:
            code: tuple = error.code()
            details: str = f"Service role name: {information.name}\nHost: {service_host}:{service_port}\nCommand: {sc.name}\nDetails: {error.details()}\nCode: {code}"
            A.O.init()
            A.ER.rpc_error_handler(details, code, information, sc)

    @staticmethod
    def call_service_command(command: SC, parameters: Any | None = None, timeout: int | None = None) -> str | None:
        return RPC.call_service(None, command, parameters, timeout)
    
    service: Service | None = None
    service_description: ServiceDescription | None = None
    service_information: ServiceInformation | None = None
