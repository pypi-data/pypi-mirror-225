import calendar
from collections import defaultdict
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from getpass import getpass
from threading import Thread
from time import sleep
from grpc import StatusCode
import dataclasses
import importlib.util
import locale
import os
import platform
import json
import pkg_resources
import re
import subprocess
from subprocess import DEVNULL, STDOUT, CompletedProcess
import sys
from typing import Any, Callable
import colorama
from colorama import Back, Style, Fore
from prettytable import PrettyTable
import requests
from requests import ConnectTimeout, Response
import traceback
from contextlib import contextmanager
import base64
import uuid
import time
from enum import Enum
from string import Formatter
import urllib.parse
from argparse import ArgumentParser, Namespace, ArgumentError

from transliterate import translit

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.collection import  *
from pih.tools import *
from pih.const import *
from pih.rpc_collection import *
from pih.rpc import *
from pih.rpc_const import *
from pih.errors import *

class IClosable:

    def close(self) -> None:
        raise NotImplemented()

class ServiceListener:
    
    def __init__(self):
        self.service: IService | None = None
        self.service_command_list: list[ServiceCommands] = None
        self.host: str = PIH.OS.host()
        self.port: int = NetworkTool.next_free_port()

    def listen_for(self, service_command_list: list[ServiceCommands], handler: Callable[[ServiceCommands, ParameterList, IClosable], Any]) -> None:     
        self.service_command_list = service_command_list
  
        def service_starts_handler(service: IService) -> None:
            self.service = service
            for service_command in service_command_list:
                service.subscribe_on(service_command)

        PIH.SERVICE.ADMIN.serve(PIH.SERVICE.ADMIN.create_event_listener_service_description(self.host, self.port), 
                                lambda command_name, parameter_list: handler(command_name, parameter_list, self), 
                                service_starts_handler, 
                                show_output = True)
        
    def close(self) -> None:
        self.service.unsubscribe(self.service_command_list)
        PIH.SERVICE.ADMIN.stop(self.service.get_description(), False)
       

class MarkOutputAbstract:

    def by_any(self, value: str) -> None:
        raise NotImplemented()

    def result(self, result: Result[list[Mark]], caption: str, use_index: bool = False) -> None:
        raise NotImplemented()

class OutputAbstract:
    
    def set_indent(self, count: int = 1) -> None:
        raise NotImplemented()
    
    def bold(self, value: str) -> str:
        raise NotImplemented()

    def header(self, caption: str) -> None:
        raise NotImplemented()

    def reset_indent(self) -> None:
        raise NotImplemented()

    def restore_indent(self) -> None:
        raise NotImplemented()

    def init(self) -> None:
        raise NotImplemented()

    def text_color(self, color: int, text: str) -> str:
        raise NotImplemented()

    def text_black(self, text: str) -> str:
        raise NotImplemented()

    def color_str(self, color: int, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def color(self, color: int, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def write_line(self, text: str) -> None:
        raise NotImplemented()

    def index(self, index: int, text: str, max_index: int = None) -> None:
        raise NotImplemented()

    def input(self, caption: str) -> None:
        raise NotImplemented()

    def input_str(self, caption: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def value(self, caption: str, value: str, text_before: str | None = None) -> None:
        raise NotImplemented()

    def get_action_value(self, caption: str, value: str, show: bool = True) -> ActionValue:
        raise NotImplemented()

    def head(self, caption: str) -> None:
        raise NotImplemented()

    def head1(self, caption: str) -> None:
        raise NotImplemented()

    def head2(self, caption: str) -> None:
        raise NotImplemented()

    def new_line(self) -> None:
        raise NotImplemented()

    def separated_line(self) -> None:
        self.new_line()

    def error_str(self, caption: str) -> str:
        raise NotImplemented()

    def error(self, caption: str) -> None:
        raise NotImplemented()

    def notify_str(self, caption: str) -> str:
        raise NotImplemented()

    def notify(self, caption: str) -> None:
        raise NotImplemented()

    def good_str(self, caption: str) -> str:
        raise NotImplemented()

    def good(self, caption: str) -> None:
        raise NotImplemented()

    def green_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def green(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def yellow_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def yellow(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def black_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def black(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def white_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def white(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def draw_line(self, color: str = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80) -> None:
        raise NotImplemented()

    def line(self) -> None:
        raise NotImplemented()

    def magenta_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def magenta(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def cyan(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def cyan_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def red(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def red_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def blue(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def blue_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def bright(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        raise NotImplemented()

    def bright_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        raise NotImplemented()

    def get_number(self, value: int) -> str:
        raise NotImplemented()

    def write_result(self, result: Result[T], use_index: bool = True, item_separator: str = "\n", empty_result_text: str = "Не найдено", separated_result_item: bool = True, label_function:  Callable[[Any, int], str] = None, data_label_function: Callable[[int, FieldItem, Result[T], Any], tuple[bool, str]] = None, title: str | None = None) -> None:
        raise NotImplemented()

    @contextmanager
    def send_to_group(self, group: CONST.MESSAGE.WHATSAPP.GROUP) -> bool:
        raise NotImplemented()

class MarkOutputBase(MarkOutputAbstract):

    def __init__(self):
        self.parent: OutputBase


class MarkOutput(MarkOutputBase):

    def by_any(self, value: str) -> None:
        try:
            self.result(PIH.RESULT.MARK.by_any(value), "Найденные карты доступа:", True)
        except NotFound as error:
            self.parent.error(error.get_details())

    def result(self, result: Result[list[Mark]], caption: str, use_index: bool = False) -> None:
        self.parent.table_with_caption_first_title_is_centered(result, caption, use_index)


class UserOutputAbstract:

    def result(self, result: Result[list[User]], caption: str | None = None, use_index: bool = False, root_location: str = AD.ACTIVE_USERS_CONTAINER_DN) -> None:
        raise NotImplemented()

    def get_formatted_given_name(self, value: str | None = None) -> str:
        return value

class OutputExtendedAbstract:

    def pih_title(self) -> None:
        raise NotImplemented()

    def rpc_service_header(self, host: str, port: int, description: str) -> None:
        raise NotImplemented()

    def service_header(self, description: ServiceDescription) -> None:
        raise NotImplemented()

    def free_marks(self, show_guest_marks: bool, use_index: bool = False) -> None:
        raise NotImplemented()

    def guest_marks(self, use_index: bool = False) -> None:
        raise NotImplemented()

    def temporary_candidate_for_mark(self, mark: Mark) -> None:
        raise NotImplemented()

    def free_marks_group_statistics(self, use_index: bool = False, show_guest_marks: bool | None = None) -> None:
        raise NotImplemented()

    def free_marks_by_group(self, group: dict, use_index: bool = False) -> None:
        raise NotImplemented()

    def free_marks_group_statistics_for_result(self, result: Result, use_index: bool) -> None:
        raise NotImplemented()

    def free_marks_by_group_for_result(self, group: MarkGroup, result: Result, use_index: bool) -> None:
        raise NotImplemented()

    def temporary_marks(self, use_index: bool = False,) -> None:
        raise NotImplemented()

    def containers_for_result(self, result: Result, use_index: bool = False) -> None:
        raise NotImplemented()

    def table_with_caption_first_title_is_centered(self, result: Result, caption: str, use_index: bool = False, label_function: Callable = None) -> None:
        raise NotImplemented()

    def table_with_caption_last_title_is_centered(self, result: Result, caption: str, use_index: bool = False, label_function: Callable = None) -> None:
        raise NotImplemented()

    def table_with_caption(self, result: Any, caption: str | None = None, use_index: bool = False, modify_table_function: Callable = None, label_function: Callable = None) -> None:
        raise NotImplemented()

    def template_users_for_result(self, data: dict, use_index: bool = False) -> None:
        raise NotImplemented()

    def clear_screen(self) -> None:
        raise NotImplemented()
    
    def write_video(self, caption: str, video_content: str) -> None:
            raise NotImplemented()

    def write_image(self, caption: str, image_content: str) -> None:
        pass

class UserOutputBase(UserOutputAbstract):

    def __init__(self):
        self.parent: OutputBase

class UserOutput(UserOutputBase):

    def result(self, result: Result[list[User]], caption: str | None = None, use_index: bool = False, root_location: str = AD.ACTIVE_USERS_CONTAINER_DN) -> None:
        data: list = DataTool.as_list(result.data)
        fields: FieldItemList = result.fields
        base_location_list = PIH.DATA.FORMAT.location_list(
            root_location, False)
        root_base_location = base_location_list[0:2]
        root_base_location.reverse()
        base_location = AD.LOCATION_JOINER.join([".".join(
            root_base_location), AD.LOCATION_JOINER.join(base_location_list[2:])])
        location_field = fields.get_item_by_name(
            FIELD_NAME_COLLECTION.DN)
        pevious_caption: str = location_field.caption
        location_field.caption = f"{location_field.caption} ({base_location})"
        def modify_data(field: FieldItem, user: User) -> str:
            if field.name == USER_PROPERTIES.DN:
                return AD.LOCATION_JOINER.join(filter(
                    lambda x: x not in base_location_list, PIH.DATA.FORMAT.location_list(user.distinguishedName)))
            if field.name == USER_PROPERTIES.USER_ACCOUNT_CONTROL:
                return "\n".join(PIH.DATA.FORMAT.get_user_account_control_values(user.userAccountControl))
            if field.name == USER_PROPERTIES.DESCRIPTION:
                return user.description
            if field.name == USER_PROPERTIES.NAME:
                return "\n".join(user.name.split(" "))
            return None
        self.parent.table_with_caption(
            result, "Пользватели:" if len(data) > 1 else "Пользватель:", False, None, modify_data)
        location_field.caption = pevious_caption


class InputAbstract:

    def input(self, caption: str | None = None, new_line: bool = True, check_function: Callable[[str], str] | None = None) -> str:
        raise NotImplemented()

    def polibase_person_card_registry_folder(self, value: str | None = None, title: str | None = None) -> str:
        raise NotImplemented()

    def telephone_number(self, format: bool = True, telephone_prefix: str = CONST.TELEPHONE_NUMBER_PREFIX) -> str:
        raise NotImplemented()

    def email(self) -> str:
        raise NotImplemented()

    def message(self, caption: str | None = None, prefix: str | None = None) -> str:
        raise NotImplemented()

    def description(self) -> str:
        raise NotImplemented()

    def login(self, check_on_exists: bool = False) -> str:
        raise NotImplemented()

    def indexed_list(self, caption: str, name_list: list[Any], caption_list: list[str], by_index: bool = False) -> str:
        raise NotImplemented()

    def indexed_field_list(self, caption: str, list: FieldItemList) -> str:
        raise NotImplemented()

    def index(self, caption: str, data: list, label_function: Callable[[Any, int], str] = None, use_zero_index: bool = False) -> int:
        raise NotImplemented()

    def item_by_index(self, caption: str, data: list[Any], label_function: Callable[[Any, int], str] = None, use_zero_index: bool = False) -> Any:
        raise NotImplemented()

    def tab_number(self, check: bool = True) -> str:
        raise NotImplemented()

    def password(self, secret: bool = True, check: bool = False, settings: PasswordSettings = None, is_new: bool = True) -> str:
        raise NotImplemented()

    def same_if_empty(self, caption: str, src_value: str) -> str:
        raise NotImplemented()

    def name(self) -> str:
        raise NotImplemented()

    def full_name(self, one_line: bool = False) -> FullName:
        raise NotImplemented()

    def yes_no(self, text: str = " ", enter_for_yes: bool = False, yes_label: str | None = None, no_label: str | None = None, yes_checker: Callable[[str], bool] = None) -> bool:
        raise NotImplemented()

    def message_for_user_by_login(self, login: str) -> str:
        raise NotImplemented()

    def polibase_person_any(self, title: str | None = None) -> str:
        raise NotImplemented()


class UserInputAbstract:

    def container(self) -> UserBase:
        raise NotImplemented()

    def by_name(self) -> User:
        raise NotImplemented()

    def title_any(self, title: str | None = None) -> str:
        raise NotImplemented()

    def by_any(self, value: str | None = None, active: bool | None = None, title: str | None = None, use_all: bool = False) -> list[User]:
        raise NotImplemented()

    def telephone_number(self, value: str | None = None, active: bool | None = None, title: str | None = None) -> User:
        raise NotImplemented()

    def template(self) -> User:
        raise NotImplemented()

    def search_attribute(self) -> str:
        raise NotImplemented()

    def search_value(self, search_attribute: str) -> str:
        raise NotImplemented()

    def generate_login(self, full_name: FullName, ask_for_remove_inactive_user_if_login_is_exists: bool = True, ask_for_use: bool = True) -> str:
        raise NotImplemented()

    def generate_password(self, once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT) -> str:
        raise NotImplemented()


class UserInputBase(UserInputAbstract):

    def __init__(self):
        self.parent: InputBase = None


class MarkInputAbstract:

    def free(self, group: MarkGroup = None) -> Mark:
        raise NotImplemented()

    def person_division(self) -> PersonDivision:
        raise NotImplemented()

    def by_name(self) -> Mark:
        raise NotImplemented()

    def by_any(self, value: str | None = None) -> Mark:
        raise NotImplemented()

    def any(self) -> str:
        raise NotImplemented()


class MarkInputBase(MarkInputAbstract):

    def __init__(self):
        self.parent: InputBase


class InputBase(InputAbstract):

    def __init__(self):
        self.output: OutputBase
        self.mark: MarkInputBase
        self.user: UserInputBase


class OutputBase(OutputAbstract, OutputExtendedAbstract):

    def __init__(self, user_output: UserOutputBase | None = None, mark_output: MarkOutputBase | None = None):
        self.text_before: str = ""
        self.text_after: str = ""
        self.indent_symbol: str = " "
        self.indent_value: int = 0
        self.user: UserOutputBase = user_output
        self.user.parent = self
        self.mark: MarkOutputBase = mark_output
        self.mark.parent = self
        self.personalize = False


class SessionAbstract:

    def run_forever_untill_enter_not_pressed(self) -> None:
        raise NotImplemented()

    def exit(self, timeout: int = None, message: str | None = None) -> None:
        raise NotImplemented()

    def get_login(self) -> str:
        raise NotImplemented()

    def get_user(self) -> User:
        raise NotImplemented()

    def user_given_name(self) -> str:
        raise NotImplemented()

    def start(self, login: str, notify: bool = True) -> None:
        raise NotImplemented()

    def say_hello(self, telephone_number: str | None = None, greeting: bool = True) -> None:
        raise NotImplemented()
    
    @property
    def argv(self) -> list[str]:
        raise NotImplemented()

    def arg(self, index: int = None, default_value: str | None = None) -> str:
        raise NotImplemented()

    @property
    def file_path(self) -> str:
        raise NotImplemented()

    @property
    def file_name(self) -> str:
        raise NotImplemented()

    def authenticate(self, exit_on_fail: bool = True) -> bool:
        raise NotImplemented()

    def add_allowed_group(self, value: AD.Groups) -> None:
        raise NotImplemented()

class SessionBase(SessionAbstract):

    def __init__(self, input: InputBase | None = None, output: OutputBase | None = None, name: str | None = None):
        self.allowed_groups: list[AD.Groups] = []
        self.login: str | None = None
        self.user: User = None
        self.input: InputBase = input
        self.output: OutputBase = output
        self.name: str | None = name

    def add_allowed_group(self, value: AD.Groups) -> None:
        self.allowed_groups.append(value)


class Session(SessionBase):

    def __init__(self, input: InputBase = None, output: OutputBase = None):
        super().__init__(input, output)
        self.authenticated: bool = False
        self.arg_parser: ArgumentParser = ArgumentParser(description="Service help")
       
    def run_forever_untill_enter_not_pressed(self) -> None:
        try:
            self.output.green("Нажмите Ввод для выхода...")
            input()
        except KeyboardInterrupt:
            pass

    def exit(self, timeout: int = None, message: str | None = None) -> None:
        if message is not None:
            self.output.error(message)
        if timeout is None:
            timeout = 5
        sleep(timeout)
        exit()

    def get_login(self) -> str:
        if self.login is None:
            self.start(PIH.OS.get_login())
        return self.login

    def get_user(self) -> User:
        if self.user is None:
            self.user = PIH.RESULT.USER.by_login(
                self.get_login()).data
        return self.user

    @property
    def user_given_name(self) -> str:
        return FullNameTool.to_given_name(self.get_user().name)

    def start(self, login: str, notify: bool = True) -> None:
        if self.login is None:
            self.login = login
            if notify:
                PIH.EVENT.start_session()

    def say_hello(self, _: str | None = None, greeting: bool = True) -> None:
        user: User = self.get_user()
        if DataTool.is_not_none(user):
            if greeting:
                self.output.good(f"Добро пожаловать, {user.name}")
                self.output.new_line()
            return
        self.output.error(f"Ты кто такой? Давай, до свидания...")
        self.exit()

    @property
    def argv(self) -> list[str]:
        return sys.argv[1:] if len(sys.argv) > 1 else []
    
    def arg(self, index: int = 0, default_value: Any | None = None) -> str | Namespace:
        return DataTool.by_index(self.argv, index, default_value)
    
    @property
    def arg_namespace(self) -> Namespace:
        return self.arg_parser.parse_args()

    def named_arg(self, name: str) -> str | None:
        return self.arg_parser.parse_args().__getattribute__(name)
    
    def add_arg(self, *args, **kwargs) -> bool:  
        try:
            self.arg_parser.add_argument(j(("--", args[0])), **kwargs)
        except ArgumentError as error:
            return False
        return True
    
    @property
    def file_path(self) -> str:
        return sys.argv[0]

    @property
    def is_standalone(self) -> bool:
        return self.file_path.endswith(FILE.EXTENSION.EXE)

    @property
    def file_name(self) -> str:
        return PathTool.get_file_name(self.file_path)

    def authenticate(self, exit_on_fail: bool = True, once: bool = True) -> bool:
        try:
            if once and self.authenticated:
                return True
            self.output.green("Инициализация...")
            self.output.clear_screen()
            self.output.pih_title()
            if PIH.SERVICE.check_on_accessibility(ServiceRoles.AD): 
                login: str = PIH.OS.get_login()
                self.output.head1(f"{FullNameTool.to_given_name(PIH.RESULT.USER.by_login(login, cached=False).data.name)}, пожалуйста, пройдите аутентификацию...")
                self.output.new_line()
                if not self.input.yes_no(f"Использовать логин '{login}'", True):
                    login = PIH.input.login()
                password: str = PIH.input.password(is_new=False)
                if DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.authenticate, (login, password))):
                    self.authenticated = True
                    self.start(login, False)
                    PIH.EVENT.login()
                    self.output.good(self.output.text_black(
                        f"Добро пожаловать, {self.get_user().name}..."))
                    return True
                else:
                    if exit_on_fail:
                        self.exit(
                            5, "Неверный пароль или логин. До свидания...")
                    else:
                        return False
            else:
                self.output.error(
                    "Сервис аутентификации недоступен. До свидания...")
        except KeyboardInterrupt:
            self.exit(0, "Выход")



class Stdin:

    def __init__(self):
        self.data: str | None = None
        self.wait_for_data_input: bool = False
        self.interrupt_type: int = False

    def is_empty(self) -> bool:
        return DataTool.is_empty(self.data)

    def set_default_state(self) -> None:
        self.interrupt_type = False
        self.wait_for_data_input = False
        self.data = None


class Output(OutputBase):

    @contextmanager
    def make_indent(self, value: int, additional: bool = False) -> bool:
        try:
            self.set_indent([0, self.indent][additional] + value)
            yield True
        finally:
            self.set_indent([self.indent, self.indent - value][additional])

    def set_indent(self, value: int) -> None:
        self.indent_value = value
        self.text_before = self.indent_symbol * value

    def bold(self, value: str) -> str:
        return f"\033[1m{value}\033[0m"

    def italic(self, value: str) -> str:
        return value

    def reset_indent(self) -> None:
        self.indent_value = 0
        self.text_before = ""

    @property
    def indent(self) -> int:
        return self.indent_value

    def restore_indent(self) -> None:
        self.set_indent(self.indent_value)

    def init(self) -> None:
        colorama.init()

    def text_color(self, color: str, text: str) -> str:
        return f"{color}{text}{Fore.RESET}"

    def text_black(self, text: str) -> str:
        return self.text_color(Fore.BLACK, text)
    
    def text_white(self, text: str) -> str:
        return self.text_color(Fore.WHITE, text)

    def color_str(self, color: int, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        text = f" {text} "
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        return f"{text_before}{color}{text}{Back.RESET}{text_after}"

    def color(self, color: int, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.color_str(
            color, text, text_before, text_after))

    def write_line(self, text: str) -> None:
        print("\n".join(list(map(lambda item: self.text_before + item, text.splitlines()))))

    @contextmanager
    def personalized(self) -> bool:
        pass

    def index(self, index: int, text: str, max_index: int = None) -> None:
        indent: str = ""
        if max_index is not None:
            indent = " " * 2 * (len(str(max_index)) - len(str(index)))
        if index is None:
            self.write_line(f"{indent}{text}")
        else:
            self.write_line(f"{index}. {indent}{text}")

    def input(self, caption: str) -> None:
        self.write_line(self.input_str(
            caption, self.text_before, text_after=":"))

    def input_str(self, caption: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.white_str(f"{Fore.BLACK}{caption}{Fore.RESET}", text_before, text_after)

    def value(self, caption: str, value: str, text_before: str | None = None) -> None:
        text_before = text_before or self.text_before
        self.cyan(caption, text_before, f": {value}")

    def get_action_value(self, caption: str, value: str, show: bool = True) -> ActionValue:
        if show:
            self.value(caption, value)
        return ActionValue(caption, value)

    def head(self, caption: str) -> None:
        self.cyan(caption)

    def head1(self, caption: str) -> None:
        self.magenta(caption)

    def head2(self, caption: str) -> None:
        self.yellow(self.text_color(Fore.BLACK, caption))

    def new_line(self) -> None:
        print()

    def separated_line(self) -> None:
        self.new_line()

    def error_str(self, caption: str) -> str:
        return self.red_str(caption)

    def error(self, caption: str) -> None:
        self.write_line(self.error_str(caption))

    def notify_str(self, caption: str) -> str:
        return self.yellow_str(caption)

    def notify(self, caption: str) -> None:
        self.write_line(self.notify_str(caption))

    def good_str(self, caption: str) -> str:
        return self.green_str(caption)

    def good(self, caption: str) -> str:
        self.write_line(self.good_str(self.text_white(caption)))

    def green_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.GREEN, text, text_before, text_after)

    def green(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.green_str(text, text_before, text_after))

    def yellow_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.YELLOW, text, text_before, text_after)

    def yellow(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        self.write_line(self.yellow_str(text, text_before, text_after))

    def black_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.BLACK, text, text_before, text_after)

    def black(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.black_str(text, text_before, text_after))

    def white_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.WHITE, text, text_before, text_after)

    def white(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.white_str(text, text_before, text_after))

    def draw_line(self, color: str = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80) -> None:
        self.write_line("") if color is None else self.color(
            color, char*width)

    def line(self) -> None:
        self.new_line()
        self.draw_line(Back.WHITE, self.text_color(
            Fore.BLACK, "_"), width=128)
        self.new_line()

    def magenta_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.LIGHTMAGENTA_EX, text, text_before, text_after)

    def magenta(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.magenta_str(text, text_before, text_after))

    def cyan(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.cyan_str(text, text_before, text_after))

    def cyan_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.CYAN, text, text_before, text_after)

    def red(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.red_str(text, text_before, text_after))

    def red_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.LIGHTRED_EX, text, text_before, text_after)

    def blue(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.blue_str(text, text_before, text_after))

    def blue_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Back.BLUE, text, text_before, text_after)

    def bright(self, text: str, text_before: str | None = None, text_after: str | None = None) -> None:
        self.write_line(self.bright_str(text, text_before, text_after))

    def bright_str(self, text: str, text_before: str | None = None, text_after: str | None = None) -> str:
        return self.color_str(Style.BRIGHT, text, text_before, text_after)

    def get_number(self, value: int) -> str:
        return CONST.VISUAL.NUMBER_SYMBOLS[value - 1]

    def header(self, caption: str) -> None:
        self.head2(caption)

    def write_result(self, result: Result[T], use_index: bool = True, item_separator: str = "\n", empty_result_text: str = "Не найдено", separated_result_item: bool = True, label_function: Callable[[Any, int], str] | None = None, data_label_function: Callable[[int, FieldItem, T, Any], tuple[bool, str]] | None = None, title: str | None= None) -> None:
        data: list = DataTool.as_list(result.data)
        result_string_list: list[str] = None
        if DataTool.is_empty(data):
            self.new_line()
            self.write_line(empty_result_text)
        else:
            if not DataTool.is_empty(title):
                self.write_line(title)
            for index, data_item in enumerate(data):
                result_string_list = []
                if use_index and len(data) > 1:
                    result_string_list.append(f"{self.text_before}{str(index + 1)}:")
                if label_function is None:
                    for field_item in result.fields.list:
                        field: FieldItem = field_item
                        if not field.visible:
                            continue
                        item_data_value: str | None = None
                        if isinstance(data_item, dict):
                            item_data_value = data_item[field.name]
                        elif dataclasses.is_dataclass(data_item):
                            item_data_value = data_item.__getattribute__(field.name)
                        item_data_value = item_data_value if DataTool.is_empty(item_data_value) else PIH.DATA.FORMAT.by_formatter_name(field.data_formatter, item_data_value) or field.data_formatter.format(data=item_data_value) 
                        if DataTool.is_empty(item_data_value):
                            if data_label_function is None:
                                continue
                        default_value_label_function: Callable[[int, FieldItem, Result[T], Any], tuple[
                            bool, str]] = lambda _, field, __, data_value: (True, f"{self.bold(field.caption)}: {data_value}")
                        result_data_label_function: Callable[[int, FieldItem, T, Any], tuple[bool, str]] = data_label_function or default_value_label_function 
                        label_value_result: tuple[bool, str] = result_data_label_function(index, field, data_item, item_data_value)
                        label_value: str | None = None
                        if label_value_result[0] == True:
                            label_value = label_value_result[1]
                            if DataTool.is_none(label_value) and DataTool.is_not_none(field.default_value):
                                label_value = field_item.default_value
                        else:
                            label_value = default_value_label_function(None, field, None, item_data_value)[1]
                        if not DataTool.is_empty(label_value):
                            result_string_list.append(label_value)
                else:
                    result_string_list.append(label_function(data_item, index))
                if separated_result_item:
                    self.separated_line()
                self.write_line(item_separator.join(result_string_list))

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pih_title(self) -> None:
        self.cyan(self.text_color(Fore.WHITE, "███ ███ █┼█"))
        self.cyan(
            self.text_color(Fore.WHITE, "█▄█ ┼█┼ █▄█"))
        self.cyan(self.text_color(Fore.WHITE, "█┼┼ ▄█▄ █┼█") +
                         self.text_color(Fore.BLACK, f" {PIH.VERSION.value}"))
        self.new_line()

    def rpc_service_header(self, host: str, port: int, description: str) -> None:
        self.blue("PIH service")
        self.blue(f"Version: {PIH.VERSION.value}")
        self.green(f"Service host: {host}")
        self.green(f"Service port: {port}")
        self.green(f"Service name: {description}")

    def service_header(self, information: ServiceInformation) -> None:
        self.write_line("")
        self.pih_title()
        self.blue("Service starting...")
        self.write_line("")
        self.green(f"Service name: {information.name}")
        self.set_indent(1)
        if information.isolated:
            self.blue(f"[Isolate]")
        self.value("Host", PIH.DATA.FORMAT.donain(information.host))
        self.value("Port", information.port)
        self.value("PID process",  information.pid)
        self.set_indent(0)

    def free_marks(self, show_guest_marks: bool, use_index: bool = False, sort_by_tab_number: bool = True) -> None:
        def sort_function(item: Mark) -> Any:
            return item.TabNumber if sort_by_tab_number else item.GroupName
        self.table_with_caption_first_title_is_centered(ResultTool.sort(PIH.RESULT.MARK.free_list(show_guest_marks), sort_function), "Свободные карты доступа:", use_index)

    def guest_marks(self, use_index: bool = False) -> None:
        mark_list_result: Result[list[Mark]] = PIH.RESULT.MARK.free_list(True)
        mark_list_result.fields.visible(
            FIELD_NAME_COLLECTION.GROUP_NAME, False)
        def filter_function(item: Mark) -> bool:
            return EnumTool.get(MarkType, item.type) == MarkType.GUEST
        ResultTool.filter(mark_list_result, filter_function)
        self.table_with_caption_first_title_is_centered(
            mark_list_result, "Гостевые карты доступа:", use_index)

    def temporary_candidate_for_mark(self, mark: Mark) -> None:
        self.mark.result(
            Result(FIELD_COLLECTION.ORION.FREE_MARK, [mark]), "Временная карта")

    def free_marks_group_statistics(self, use_index: bool = False, show_guest_marks: bool | None = None) -> None:
        self.free_marks_group_statistics_for_result(
            PIH.RESULT.MARK.free_marks_group_statistics(show_guest_marks), use_index)

    def free_marks_by_group(self, group: dict, use_index: bool = False) -> None:
        self.free_marks_by_group_for_result(PIH.RESULT.MARK.free_marks_by_group_id(group), group, use_index)

    def free_marks_group_statistics_for_result(self, result: Result, use_index: bool) -> None:
        self.table_with_caption_last_title_is_centered(
            result, "Свободные карты доступа:", use_index)

    def free_marks_by_group_for_result(self, group: MarkGroup, result: Result, use_index: bool) -> None:
        group_name: str = group.GroupName
        self.table_with_caption_last_title_is_centered(
            result, f"Свободные карты доступа для группы доступа '{group_name}':", use_index)

    def temporary_marks(self, use_index: bool = False,) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[0]] = "c"
            table.align[caption_list[1]] = "c"
        self.table_with_caption(
            PIH.RESULT.MARK.temporary_list(), "Список временных карт:", use_index, modify_table)

    def containers_for_result(self, result: Result, use_index: bool = False) -> None:
        self.table_with_caption(result, "Подразделение:", use_index)

    def table_with_caption_first_title_is_centered(self, result: Result, caption: str, use_index: bool = False, label_function: Callable = None) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[int(use_index)]] = "c"
        self.table_with_caption(
            result, caption, use_index, modify_table, label_function)

    def table_with_caption_last_title_is_centered(self, result: Result, caption: str, use_index: bool = False, label_function: Callable = None) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[-1]] = "c"
        self.table_with_caption(
            result, caption, use_index, modify_table, label_function)

    def table_with_caption(self, result: Any, caption: str | None = None, use_index: bool = False, modify_table_function: Callable = None, label_function: Callable = None) -> None:
        if caption is not None:
            self.cyan(caption)
        is_result_type: bool = isinstance(result, Result)
        field_list = result.fields if is_result_type else ResultUnpack.unpack_fields(
            result)
        data: Any = result.data if is_result_type else ResultUnpack.unpack_data(result)
        if DataTool.is_empty(data):
            self.error("Не найдено!")
        else:
            if not isinstance(data, list):
                data = [data]
            if len(data) == 1:
                use_index = False
            if use_index:
                field_list.list.insert(0, FIELD_COLLECTION.INDEX)
            caption_list: list = field_list.get_caption_list()
            def create_table(caption_list: list[str]) -> PrettyTable:
                from prettytable.colortable import ColorTable, Themes
                table: ColorTable = ColorTable(
                    caption_list, theme=Themes.OCEAN)
                table.align = "l"
                if use_index:
                    table.align[caption_list[0]] = "c"
                return table
            table: PrettyTable = create_table(caption_list)
            if modify_table_function is not None:
                modify_table_function(table, caption_list)
            for index, item in enumerate(data):
                row_data: list = []
                for field_item_obj in field_list.get_list():
                    field_item: FieldItem = field_item_obj
                    if field_item.visible:
                        if field_item.name == FIELD_COLLECTION.INDEX.name:
                            row_data.append(str(index + 1))
                        elif not isinstance(item, dict):
                            if label_function is not None:
                                modified_item_data = label_function(
                                    field_item, item)
                                if modified_item_data is None:
                                    modified_item_data = getattr(
                                        item, field_item.name)
                                row_data.append(DataTool.check(
                                    modified_item_data, lambda: modified_item_data, "") if modified_item_data is None else modified_item_data)
                            else:
                                item_data = getattr(item, field_item.name)
                                row_data.append(DataTool.check(
                                    item_data, lambda: item_data, ""))
                        elif field_item.name in item:
                            item_data = item[field_item.name]
                            if label_function is not None:
                                modified_item_data = label_function(
                                    field_item, item)
                                row_data.append(
                                    item_data if modified_item_data is None else modified_item_data)
                            else:
                                row_data.append(item_data)
                table.add_row(row_data)
            print(table)
            table.clear()

    def template_users_for_result(self, data: dict, use_index: bool = False) -> None:
        def data_handler(field_item: FieldItem, item: User) -> Any:
            filed_name = field_item.name
            if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                return item.description
            return None
        self.table_with_caption(
            data, "Шаблоны для создания аккаунта пользователя:", use_index, None, data_handler)

class Input(InputBase):

    def __init__(self, user_input: UserInputBase, mark_input: MarkInputBase, output: OutputBase):
        self.output: OutputBase = output
        self.answer: str | None = None
        if user_input is not None:
            self.user: UserInputBase = user_input
            self.user.parent = self
        if mark_input is not None:
            self.mark: MarkInputBase = mark_input
            self.mark.parent = self

    def input(self, caption: str | None = None, new_line: bool = True, check_function: Callable[[str], str] | None = None) -> str:
        try:
            while True:
                if new_line and caption is not None:
                    self.output.input(caption)
                value: str = input(self.output.text_before) if new_line else input(self.output.text_before + caption)
                if check_function is not None: 
                    value_after: str = check_function(value)
                    if value_after is not None:
                        return value_after
                else:
                    return value
        except KeyboardInterrupt:
            raise KeyboardInterrupt()

    def telephone_number(self, format: bool = True, telephone_prefix: str = CONST.TELEPHONE_NUMBER_PREFIX) -> str:
        while True:
            self.output.input("Номер телефона")
            use_telephone_prefix: bool = telephone_prefix is not None
            telephone_number: str = self.input(
                telephone_prefix if use_telephone_prefix else "", False)
            if use_telephone_prefix:
                if not telephone_number.startswith(telephone_prefix):
                    telephone_number = telephone_prefix + telephone_number
            check: bool | None = None
            if format:
                telehone_number_after_fix = PIH.DATA.FORMAT.telephone_number(
                    telephone_number, telephone_prefix)
                check = PIH.CHECK.telephone_number(telehone_number_after_fix)
                if check and telehone_number_after_fix != telephone_number:
                    telephone_number = telehone_number_after_fix
                    self.output.value("Телефон отформатирован", telephone_number)
            if check or PIH.CHECK.telephone_number(telephone_number):
                return telephone_number
            else:
                self.output.error("Неверный формат номера телефона!")

    def email(self, title: str | None = None) -> str:
        email: str | None = None
        while True:
            email = self.input(title or "Адресс электронная почта")
            if PIH.CHECK.email(email):
                return email
            else:
                self.output.error("Неверный формат адресса электронной почты!")

    def polibase_person_card_registry_folder(self, value: str | None = None, title: str | None = None) -> str:
        while True:
            value = value or self.input(title or "Введите название папки с картами пациентов")
            if PIH.CHECK.POLIBASE.person_card_registry_folder(value):
                return PIH.DATA.FORMAT.polibase_person_card_registry_folder(value)
            else:
                self.output.error("Неверный формат названия папки с картами пациентов!")
                value = None

    def message(self, caption: str | None = None, prefix: str | None = None) -> str:
        caption = caption or "Введите сообщение"
        self.output.input(caption)
        return (prefix or "") + self.input(prefix, False)

    def description(self) -> str:
        self.output.input("Введите описание")
        return self.input()

    def login(self, check_on_exists: bool = False) -> str:
        login: str | None = None
        while True:
            login = self.input("Введите логин")
            if PIH.CHECK.login(login):
                if check_on_exists and PIH.CHECK.USER.exists_by_login(login):
                    self.output.error("Логин занят!")
                else:
                    return login
            else:
                self.output.error("Неверный формат логина!")

    def indexed_list(self, caption: str, name_list: list[Any], caption_list: list[str], by_index: bool = False) -> str:
        return self.item_by_index(caption, name_list, lambda item, index: caption_list[index if by_index else item])

    def indexed_field_list(self, caption: str, list: FieldItemList) -> str:
        name_list = list.get_name_list()
        return self.item_by_index(caption, name_list, lambda item, _: list.get_item_by_name(item).caption)

    def index(self, caption: str, data: list, label_function: Callable[[Any, int], str] = None, use_zero_index: bool = False) -> int:
        selected_index: int = -1
        length: int = len(data)
        has_error: bool = False
        while True:
            min_value: int = 1 - int(use_zero_index)
            max_value: int = length - int(use_zero_index)
            if not has_error and label_function is not None and length > 1:
                for index, item in enumerate(data):
                    self.output.index(
                            index + 1 - int(use_zero_index) if length > 1 else None, label_function(item, index), max_value)
            if length == 1:
                return 0
            selected_index = PIH.DATA.EXTRACT.decimal(self.input(
                caption + f" (от {min_value} до {max_value})"))
            if DataTool.is_empty(selected_index):
                selected_index = -1
            try:
                selected_index = int(selected_index) - min_value
                if selected_index >= 0 and selected_index < length:
                    return selected_index
            except ValueError:
                has_error = True
                continue

    def item_by_index(self, caption: str, data: list[Any], label_function: Callable[[Any, int], str] = None, use_zero_index: bool = False) -> Any:
        return data[self.index(caption, data, label_function, use_zero_index)]

    def tab_number(self, check: bool = True) -> str:
        tab_number: str | None = None
        while True:
            tab_number = self.input("Введите номер карты доступа")
            if check:
                if PIH.CHECK.MARK.tab_number(tab_number):
                    return tab_number
                else:
                    self.output.error(
                        "Неправильный формат номера карты доступа")
                    #return None
            else:
                return tab_number

    def password(self, secret: bool = True, check: bool = False, settings: PasswordSettings = None, is_new: bool = True) -> str:
        self.output.input(
            "Введите новый пароль" if is_new else "Введите пароль")
        while True:
            value = getpass("") if secret else self.input()
            if not check or PIH.CHECK.password(value, settings):
                return value
            else:
                self.output.error(
                    "Пароль не соответствует требованием безопасности")

    def same_if_empty(self, caption: str, src_value: str) -> str:
        value = self.input(caption)
        if value == "":
            value = src_value
        return value

    def name(self) -> str:
        return self.input("Введите часть имени")

    def full_name(self, one_line: bool = False) -> FullName:
        if one_line:
            while(True):
                value: str = self.input("Введите полное имя")
                if PIH.CHECK.full_name(value):
                    return FullNameTool.fullname_from_string(PIH.DATA.FORMAT.name(value))
                else:
                    pass
        else:
            def full_name_part(caption: str) -> str:
                while(True):
                    value: str = self.input(caption)
                    value = value.strip()
                    if PIH.CHECK.name(value):
                        return PIH.DATA.FORMAT.name(value)
                    else:
                        pass
            return FullName(full_name_part("Введите фамилию"), full_name_part("Введите имя"), full_name_part("Введите отчество"))

    def yes_no(self, text: str = " ", enter_for_yes: bool = False, yes_label: str | None = None, no_label: str | None = None, yes_checker: Callable[[str], bool] = None) -> bool:
        text = self.output.blue_str(self.output.text_color(Fore.WHITE, text))
        self.output.write_line(f"{text}? \n{self.output.green_str(self.output.text_black('Да (1 или Ввод)'))} / {self.output.red_str(self.output.text_black('Нет (Остальное)'), '')}" if enter_for_yes else
                               f"{text}? \n{self.output.red_str('Да (1)')} / {self.output.green_str(self.output.text_black('Нет (Остальное или Ввод)'), '')}")
        answer: str = self.input()
        answer = answer.lower()
        self.answer = answer
        return answer == "y" or answer == "yes" or answer == "1" or (answer == "" and enter_for_yes)

    def message_for_user_by_login(self, login: str) -> str:
        user: User = PIH.RESULT.USER.by_login(login).data
        if user is not None:
            head_string = f"Здравствуйте, {FullNameTool.to_given_name(user.name)}, "
            self.output.green(head_string)
            message = self.input("Введите сообщениеt: ")
            return head_string + message
        else:
            pass

    def polibase_person_any(self, title: str | None = None) -> str:
        return self.input(title or "Введите персональный номер или часть имени пациента")

class MarkInput(MarkInputBase):

    def __init__(self, input: Input = None):
        self.parent = input

    def free(self, group: MarkGroup = None) -> Mark:
        result: Result[list[Mark]] = None
        while True:
            if group is None:
                if self.parent.yes_no("Выбрать группы доступа для карты доступа, введя имени пользователя из этой группы"):
                    result = PIH.RESULT.MARK.by_name(self.parent.name())
                    mark_list: list[Mark] = result.data
                    length = len(mark_list)
                    if length > 0:
                        if length > 1:
                            self.parent.output.table_with_caption_first_title_is_centered(
                                result, "Найденные пользователи:", True)
                        group = self.parent.item_by_index(
                            "Выберите группу доступа", mark_list)
                    else:
                        self.parent.output.error(
                            "Пользователь с введенным именем не найден")
                else:
                    result = PIH.RESULT.MARK.free_marks_group_statistics(False)
                    data = result.data
                    length = len(data)
                    if length > 0:
                        if length > 1:
                            self.parent.output.free_marks_group_statistics_for_result(
                                result, True)
                        group = self.parent.item_by_index(
                            "Выберите группу доступа введя индекс", data)
                    else:
                        self.parent.output.error("Свободный карт доступа нет!")
                        return None
            else:
                result = PIH.RESULT.MARK.free_marks_by_group_id(group.GroupID)
                data = result.data
                length = len(data)
                if length > 0:
                    if length > 1:
                        self.parent.output.free_marks_by_group_for_result(
                            group, result, True)
                    return self.parent.item_by_index(
                        "Выберите карту доступа введя индекс", data)
                else:
                    self.parent.output.error(
                        f"Нет свободных карт для группы доступа '{group.GroupName}'!")
                    return self.free()

    def person_division(self) -> PersonDivision:
        division_list: list[PersonDivision] = PIH.RESULT.MARK.person_divisions().data
        division_list.insert(0, PersonDivision(0, "Без подразделения"))
        return self.parent.item_by_index("Выберите подразделение для персоны, которой принадлежит карта доступа", division_list, lambda item, _: item.name )

    def by_name(self) -> Mark:
        self.parent.output.head2("Введите имя персоны")
        result: Result[list[Mark]] = None
        while result is None:
            try:
                result = PIH.RESULT.MARK.by_name(
                    self.parent.name())
            except NotFound as error:
                self.parent.output.error(error.get_details())
        self.parent.output.mark.result(result, "Карты доступа", True)
        return self.parent.item_by_index("Выберите карточку, введя индекс", result.data)

    def by_any(self, value: str | None = None) -> Mark:
        result: Result[list[Mark]] = None
        while result is None:
            try:
                result = PIH.RESULT.MARK.by_any(value or self.any())
            except NotFound as error:
                self.parent.output.error(error.get_details())
        self.parent.output.mark.result(result, "Карты доступа", True)
        return self.parent.item_by_index("Выберите карточку, введя индекс", result.data)

    def any(self) -> str:
        return self.parent.input(
            "Введите часть имени или табельный номер держателя карты")


class UserInput(UserInputBase):

    def __init__(self, input: Input = None):
        self.parent = input

    def container(self) -> UserBase:
        result: Result[list[UserBase]] = PIH.RESULT.USER.containers()
        self.parent.output.containers_for_result(result, True)
        return self.parent.item_by_index("Выберите контейнер пользователя, введя индекс", result.data)

    def by_name(self) -> User:
        result: Result[list[User]] = PIH.RESULT.USER.by_name(
            self.parent.name())
        result.fields = FIELD_COLLECTION.AD.USER_NAME
        self.parent.output.table_with_caption(
            result, "Список пользователей", True)
        return self.parent.item_by_index("Выберите пользователя, введя индекс", result.data)

    def title_any(self, title: str | None = None) -> str:
        return self.parent.input(title or "Введите логин, часть имени или другой поисковый запрос")

    def by_any(self, value: str | None = None, active: bool | None = None, title: str | None = None, use_all: bool = False) -> list[User]:
        result: Result[list[User]] = PIH.RESULT.USER.by_any(value or self.title_any(title), active)
        label_function: Callable[[Any, int], str] = (lambda item, _: "Все" if item is None else item.name) if len(
            result.data) > 1 else None
        if use_all and len(result.data) > 1:
            result.data.append(None)
        result_data: User = self.parent.item_by_index("Выберите пользователя, введя индекс", result.data, label_function)
        return result.data if result_data is None else [result_data]

    def telephone_number(self, value: str | None = None, active: bool | None = None, title: str | None = None) -> User:
        try:
            return self.by_any(value, active, title)
        except NotFound:
            return None


    def template(self) -> User:
        result: Result[list[User]] = PIH.RESULT.USER.template_list()
        self.parent.output.template_users_for_result(result, True)
        return self.parent.item_by_index("Выберите шаблон пользователя, введя индекс", result.data)

    def search_attribute(self) -> str:
        return self.parent.indexed_field_list("Выберите по какому критерию искать, введя индекс",
                                             FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE)

    def search_value(self, search_attribute: str) -> str:
        field_item = FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE.get_item_by_name(
            search_attribute)
        return self.parent.input(f"Введите {field_item.caption.lower()}")

    def generate_password(self, once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT) -> str:
        def internal_generate_password(settings: PasswordSettings = None) -> str:
            return PasswordTools.generate_random_password(settings.length, settings.special_characters,
                                                          settings.order_list, settings.special_characters_count,
                                                          settings.alphabets_lowercase_count, settings.alphabets_uppercase_count,
                                                          settings.digits_count, settings.shuffled)
        while True:
            password = internal_generate_password(settings)
            if once or self.parent.yes_no(f"Использовать пароль {password}", True):
                return password
            else:
                pass

    def generate_login(self, full_name: FullName, ask_for_remove_inactive_user_if_login_is_exists: bool = True, ask_for_use: bool = True) -> str:
        login_list: list[str] = []
        inactive_user_list: list[User] = []
        login_is_exists: bool = False

        def show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string: str) -> User:
            user: User = PIH.RESULT.USER.by_login(login_string).data
            is_active: bool = PIH.CHECK.USER.active(user)
            self.parent.output.error(
                f"Логин '{login_string}' занят {'активным' if is_active else 'неактивным'} пользователем: {user.name}")
            self.parent.output.new_line()
            return user if not is_active else None
        login: FullName = NamePolicy.convert_to_login(full_name)
        login_string: str = FullNameTool.fullname_to_string(login, "")
        login_list.append(login_string)
        need_enter_login: bool = False

        def remove_inactive_user_action():
            login_string: str | None = None
            need_enter_login: bool = False
            if self.parent.yes_no("Удалить неактивных пользователей, чтобы освободить логин", True):
                user_for_remove: User = self.parent.item_by_index(
                    "Выберите пользователя для удаления, выбрав индекс", inactive_user_list, lambda user, _: f"{user.name} ({user.samAccountName})")
                self.parent.output.new_line()
                self.parent.output.value(f"Пользователь для удаления",
                                        user_for_remove.name)
                if self.parent.yes_no("Удалить неактивного пользователя", True):
                    if PIH.ACTION.USER.remove(user_for_remove):
                        self.parent.output.good("Удален")
                        login_string = user_for_remove.samAccountName
                        inactive_user_list.remove(user_for_remove)
                    else:
                        self.parent.output.error("Ошибка")
                else:
                    need_enter_login = True
            else:
                need_enter_login = True
            return need_enter_login, login_string
        if PIH.CHECK.USER.exists_by_login(login_string):
            user: User = show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
            if user is not None:
                inactive_user_list.append(user)
            login_alt: FullName = NamePolicy.convert_to_alternative_login(login)
            login_string = FullNameTool.fullname_to_string(login_alt, "")
            login_is_exists = login_string in login_list
            if not login_is_exists:
                login_list.append(login_string)
            if login_is_exists or PIH.CHECK.USER.exists_by_login(login_string):
                if not login_is_exists:
                    user = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                        login_string)
                    if user is not None:
                        inactive_user_list.append(user)
                login_reversed: FullName = NamePolicy.convert_to_reverse_login(login)
                login_is_exists = login_string in login_list
                login_string = FullNameTool.fullname_to_string(login_reversed, "")
                if not login_is_exists:
                    login_list.append(login_string)
                if login_is_exists or PIH.CHECK.USER.exists_by_login(login_string):
                    login_last: FullName = NamePolicy.convert_to_last_login(login)
                    login_string = FullNameTool.fullname_to_string(login_last, "")
                    if not login_is_exists:
                        user = show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
                        if user is not None:
                            inactive_user_list.append(user)
                    if ask_for_remove_inactive_user_if_login_is_exists and len(inactive_user_list) > 0:
                        need_enter_login, login_string = remove_inactive_user_action()
                    if need_enter_login:
                        while True:
                            login_string = self.parent.login()
                            if PIH.CHECK.USER.exists_by_login(login_string):
                                show_user_which_login_is_exists_and_return_user_if_it_inactive(
                                    login_string)
                            else:
                                break
        if not need_enter_login and ask_for_remove_inactive_user_if_login_is_exists and len(inactive_user_list) > 0:
            need_enter_login, login_string = remove_inactive_user_action()
            if need_enter_login:
                return self.generate_login(full_name, False)
        else:
            if ask_for_use and not self.parent.yes_no(f"Использовать логин '{login_string}' для аккаунта пользователя", True):
                login_string = self.parent.login(True)

        return login_string


def while_not_do(check_action: Callable[[None], bool] | None = None, attemp_count: int = None, success_handler: Callable[[None], None] = None, start_handler: Callable[[None], None] = None, sleep_time: int = None, action: Callable[[None], None] = None) -> None:
    while DataTool.is_empty(check_action) or not check_action():
        if start_handler is not None:
            start_handler()
            start_handler = None
        if action is not None:
            action()
        if attemp_count is not None:
            if attemp_count == 0:
                break
            attemp_count -= 1
        if sleep_time is not None:
            sleep(sleep_time)
    if success_handler is not None:
        success_handler()

class NamePolicy:

    @staticmethod
    def get_first_letter(name: str) -> str:
        letter = name[0]
        if letter.lower() == "ю":
            return "yu"
        return translit(letter, "ru", reversed=True).lower()

    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(
                full_name.last_name),
            NamePolicy.get_first_letter(
                full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name))

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.middle_name, login_list.last_name)

    @staticmethod
    def convert_to_last_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.last_name, login_list.middle_name)

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(login_list.middle_name, login_list.first_name, login_list.last_name)


class PIH:

    NAME: str = "pih"
    NAME_ALT: str = "пих"

    def __init__(self, input: InputBase = None, output: OutputBase = None, session: SessionBase = None): 
        if output is None:
            output = Output(UserOutput(), MarkOutput())
            PIH.output: Output = output
        else:
            self.output: Output = output
        if input is None:
            input = Input(
                UserInput(), MarkInput(), PIH.output)
            PIH.input: Input = input
        else:
            self.input: Input = input
        if session is None: 
            PIH.session: Session = Session(input, output)
        else:
            self.session: Session = session
        
    class MIO:
    
        ANSWER: dict[str, list[str]] = defaultdict(list)

        @staticmethod
        def create_output(recipient: str | Enum, greeting: bool = True) -> Output:
            from MobileHelperService.api import MobileOutput, MobileSession, Flags, format_given_name
            recipient = recipient if isinstance(recipient, str) else EnumTool.get(recipient)
            session: MobileSession = MobileSession(recipient, EnumTool.get(Flags.SILENCE))
            recipient_as_whatsapp_group: bool = recipient.endswith(CONST.MESSAGE.WHATSAPP.GROUP_SUFFIX)
            output: MobileOutput = MobileOutput(session)
            session.output = output
            if not recipient_as_whatsapp_group:
                output.user.get_formatted_given_name = lambda: format_given_name(session, output)
                session.say_hello(recipient, greeting)
            return output

        @staticmethod
        def waiting_for_input_from(recipient: str, handler: Callable[[str, Callable[[None], None]], None] | None = None) -> str | None:
            def internal_handler(message: str, close_handler: Callable[[None], None]) -> None:
                PIH.MIO.ANSWER[recipient].append(message)
                if DataTool.is_empty(handler):
                    close_handler()
                else:
                    handler(message, close_handler)  
            PIH.EVENT.waiting_for_mobile_helper_message_input(
                recipient, internal_handler)
            return PIH.MIO.ANSWER[recipient][-1] 

    class VERSION:

        value: str = "1.48059"

        @staticmethod
        def need_update() -> bool:
            return False
            #return importlib.util.find_spec(PIH.NAME) is not None and PIH.VERSION.value < PIH.VERSION.remote()
    
    class INPUT_WAIT:

        NAME: str = "RecipientWaitingForInput"

        @staticmethod
        def _get_name(group_name: str, recipient:str) -> str:
            return ":".join((group_name, recipient))

        @staticmethod
        def add(group_name: str, recipient: str, timeout: int) -> bool:
            return PIH.ACTION.DATA_STORAGE.value(RecipientWaitingForInput(group_name, timeout, recipient, PIH.DATA.now()), PIH.INPUT_WAIT._get_name(group_name, recipient), PIH.INPUT_WAIT.NAME)

        @staticmethod
        def remove(group_name: str, recipient: str) -> bool:
            return PIH.ACTION.DATA_STORAGE.value(None, PIH.INPUT_WAIT._get_name(group_name, recipient), PIH.INPUT_WAIT.NAME)
        
        @staticmethod
        def has(group_name: str, recipient: str) -> RecipientWaitingForInput:
            def extractor(data: Any | None) -> RecipientWaitingForInput | None:
                if DataTool.is_none(data):
                    return None
                result: RecipientWaitingForInput = DataTool.fill_data_from_source(RecipientWaitingForInput(), data)
                result.timestamp = DateTimeTool.datetime_from_string(result.timestamp)
                return result
            result: RecipientWaitingForInput | None = PIH.RESULT.DATA_STORAGE.value(PIH.INPUT_WAIT._get_name(group_name, recipient), extractor, PIH.INPUT_WAIT.NAME).data
            return DataTool.is_not_none(result) and (DataTool.is_none(result.timeout) or (DateTimeTool.now() - result.timestamp).seconds < result.timeout)

    class ERROR:

        notify_about_error: bool = True

        @staticmethod
        def service_host_is_unchanachable(host: str) -> None:
             PIH.output.error(
                f"Sorry, but service can't be start, cause service host is unchangeble.\n You are trying to start service on {PIH.DATA.FORMAT.donain(PIH.OS.host())}, but service must be started on {PIH.DATA.FORMAT.donain(host)}")


        @staticmethod
        def create_error_header(details: str) -> str:
            return f"\nВерсия: {PIH.VERSION.value}\nПользователь: {PIH.OS.get_login()}\nКомпьютер: {PIH.OS.host()}\n{details}"

        @contextmanager
        def detect() -> bool:
            try:
                yield True
            except Exception as error:
                PIH.ERROR.global_except_hook(type(error), error, error.__traceback__)

        @contextmanager
        def detect_interruption(message: str | None = None) -> bool:
            try:
                yield True
            except KeyboardInterrupt as _:
               DataTool.check_not_none(message, lambda: PIH.output.red(message))
        
        @staticmethod
        def rpc_error_handler(details: str, code: tuple, description: ServiceRoles, command: ServiceCommands) -> None:
            if isinstance(command, ServiceCommands):
                if code == StatusCode.UNAVAILABLE:
                    if PIH.ERROR.notify_about_error:
                        PIH.output.error(f"Error:")
                        PIH.output.set_indent(1)
                        for item in details.splitlines():
                            parts: list[str] = item.split(": ")
                            if len(parts) > 1:
                                PIH.output.value(parts[0], PIH.output.red_str(j(parts[1:], "; ")))  
                            else:
                                PIH.output.write_line(parts[0]) 
                        PIH.output.set_indent(0)    
                    return
                elif code == StatusCode.DEADLINE_EXCEEDED or details.lower().find("stream removed") != -1:
                    return
                else:
                    if PIH.ERROR.notify_about_error:
                        PIH.LOG.debug(
                            PIH.ERROR.create_error_header(details), LogMessageFlags.ERROR)
            raise Error(details, code) from None

        @staticmethod
        def global_except_hook(exctype, value, __traceback__):
            details_list: list[str] = []
            for item in value.args:
                if isinstance(item, str):
                    details_list.append(item)
            details: str = j(traceback.format_exception(value), nl())
            if PIH.ERROR.notify_about_error:
                PIH.LOG.debug(
                    PIH.ERROR.create_error_header(details), LogMessageFlags.ERROR)
            sys.__excepthook__(exctype, value, traceback)

        sys.excepthook = global_except_hook

        class POLIBASE:

            @staticmethod
            def create_not_found_error(title: str, value: str, start: str = "Пациент/Клиент") -> str:
                return NotFound(f"{start} с {title} '{value}' не найден", value)

        
        class USER:

            @staticmethod
            def get_not_found_error(title: str, active: bool, value: str) -> str:
                start: str | None = None
                if DataTool.is_none(active):
                    start = "Пользователь"
                elif active:
                    start = "Активный пользователь"
                else:
                    start = "Неактивный пользователь"
                return NotFound(f"{start} с {title} '{value}' не найден", value)

    class UPDATE:

        @staticmethod
        def for_service(role_or_information: ServiceRoles | ServiceDescription, modules: list[str] | None = None, pih_update: bool = False, modules_update: bool = True, show_output: bool = True) -> bool:
            if PIH.session.is_standalone:
                return True
            description: ServiceDescription = ServiceRoles.description(role_or_information)
            result: bool = True
            if pih_update:
                remote_executor_command_list: list[str] = PIH.EXECUTOR.create_command_for_start_service(description, True)
                command_list: list[str] = remote_executor_command_list + \
                    PIH.UPDATE.command_for_module(PIH.NAME, None)
                process_result: CompletedProcess = PIH.EXECUTOR.execute(
                    command_list, show_output)
                result = process_result.returncode == 0
            if not DataTool.is_empty(modules) and modules_update and result:
                installed_module_list: list[str] = {
                    pkg.key.lower() for pkg in pkg_resources.working_set}
                for module_name in [item.lower() for item in modules]:
                    if module_name not in installed_module_list:
                        result = result and PIH.UPDATE.install_module(
                            module_name, show_output=show_output)
                        if result:
                            pkg_resources.working_set.add_entry(module_name)
                        else:
                            break
            return result

        @staticmethod
        def command_for_module(module_name: str, version: str | None = None) -> list[str]:
            return [CONST.PYTHON.EXECUTOR, "-m", CONST.PYTHON.PYPI, CONST.PYTHON.COMMAND.INSTALL] + DataTool.check_not_none(version, lambda: [j((module_name, "==", version))], [module_name, "-U"])

        @staticmethod
        def localy(version: str | None = None, show_output: bool = False) -> bool:
            return PIH.UPDATE.install_module(PIH.NAME, version, show_output)

        @staticmethod
        def install_module(module_name: str, version: str | None = None, show_output: bool = False) -> bool:
            command_list = PIH.UPDATE.command_for_module(
                module_name, version)
            #command_list.pop(0)
            process_result: CompletedProcess = PIH.EXECUTOR.execute(
                command_list, show_output)
            returncode = process_result.returncode
            return returncode == 0

        @staticmethod
        def remotely(host: str, show_output: bool = False) -> bool:
            remote_executor_command_list: list[str] = PIH.EXECUTOR.create_command_for_psexec(
                host)
            command_list: list[str] = remote_executor_command_list + \
                PIH.UPDATE.command_for_module()
            process_result: CompletedProcess = PIH.EXECUTOR.execute(
                command_list, show_output)
            returncode = process_result.returncode
            return returncode == 0

        '''  
        @staticmethod
        def action(start_handler: Callable, update_start_handler: Callable, update_complete_handler: Callable) -> None:
            need_update: bool = PIH.VERSION.need_update()

            def internal_update_action(need_update: bool, start_handler: Callable, update_start_handler: Callable, update_complete_handler: Callable):
                if need_update:
                    update_start_handler()
                    if PIH.UPDATE.localy():
                        import importlib
                        importlib.reload(sys.modules[PIH.NAME])
                        importlib.reload(sys.modules[f"{PIH.NAME}.{PIH.NAME}"])
                        update_complete_handler()
                        start_handler()
                else:
                    start_handler()
            Thread(target=internal_update_action, args=(
                need_update, start_handler, update_start_handler, update_complete_handler,)).start()
        '''

    class SETTINGS:

        @staticmethod
        def to_datetime(value: SETTINGS) -> datetime:
            return PIH.DATA.CONVERT.settings_to_datetime(value)
        
        @staticmethod
        def to_datetime_list(value: SETTINGS) -> list[datetime]:
            return PIH.DATA.CONVERT.settings_to_datetime_list(value)

        @staticmethod
        def set(settings_item: SETTINGS | str, value: Any) -> bool:
            return PIH.ACTION.SETTINGS.set(settings_item, value)

        @staticmethod
        def set_default(settings_item: SETTINGS) -> bool:
            return PIH.ACTION.SETTINGS.set_default(settings_item)

        @staticmethod
        def get(settings_item: SETTINGS | str) -> Any:
            if isinstance(settings_item, str):
                return PIH.RESULT.SETTINGS.get_by_name(settings_item).data
            return PIH.RESULT.SETTINGS.get(settings_item).data

        @staticmethod
        def init() -> None:
            for setting_item in SETTINGS:
                if setting_item.value.auto_init:
                    PIH.SETTINGS.set_default(setting_item)

        @staticmethod
        def find(value: str | None) -> list[SETTINGS]:
            result: list[SETTINGS] = []
            for item in SETTINGS:
                if DataTool.is_none(value) or StringTool.contains(item.name, value) or StringTool.contains(item.value.key_name, value) or StringTool.contains(item.value.description, value):
                    result.append(item)
            return result

        class WORKSTATION:

            @staticmethod
            def shutdown_time() -> datetime:
                return PIH.DATA.CONVERT.settings_to_datetime(SETTINGS.WORKSTATION_SHUTDOWN_TIME)
            
            @staticmethod
            def reboot_time() -> datetime:
                return PIH.DATA.CONVERT.settings_to_datetime(SETTINGS.WORKSTATION_REBOOT_TIME)

        class USER:

            @staticmethod
            def use_cache() -> bool:
                return PIH.SETTINGS.get(SETTINGS.USER_USE_CACHE)
            
        class INDICATION:

            @staticmethod
            def ct_notification_start_time() -> list[datetime]:
                return PIH.DATA.CONVERT.settings_to_datetime(SETTINGS.INDICATION_CT_NOTIFICATION_START_TIME)
            
        class RESOURCE:
    
            @staticmethod
            def site_check_certificate_start_time() -> datetime:
                return PIH.DATA.CONVERT.settings_to_datetime(
                    SETTINGS.RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME)
            
            @staticmethod
            def site_check_free_spcae_perion_in_minutes() -> int:
                return PIH.SETTINGS.get(SETTINGS.RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES)


        class POLIBASE:

            @staticmethod
            def test_recipient(sender: Any) -> str | None:
                if sender == CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.CALL_CENTRE.value:
                    return PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_VISIT_NOTIFICATION_TEST_TELEPHONE_NUMBER)
                if sender == CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.MARKETER.value:
                    return PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_TEST_TELEPHONE_NUMBER)
                return None
            
            class REVIEW_NOTIFICATION:

                @staticmethod
                def start_time() -> datetime:
                    return PIH.DATA.CONVERT.settings_to_datetime(SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_START_TIME)

                @staticmethod
                def is_on() -> bool:
                    return PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_IS_ON)

                @staticmethod
                def day_delta() -> int:
                    return PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_DAY_DELTA)

                @staticmethod
                def notification_text(person: PolibasePerson, notification_confirmed: bool) -> str:
                    return str(PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION if notification_confirmed else SETTINGS.POLIBASE_PERSON_REVIEW_NOTIFICATION_TEXT)).format(name=FullNameTool.to_given_name(person))

            class VISIT:

                @staticmethod
                def offer_telegram_bot_url_text(person_full_name: str) -> str:
                    return str(PIH.SETTINGS.get(SETTINGS.POLIBASE_PERSON_TAKE_TELEGRAM_BOT_URL_TEXT)).format(name=FullNameTool.to_given_name(person_full_name)) 

    class EXECUTOR:

        @staticmethod
        def python_path(host: str | None = None) -> str:
            search_pattern: str = CONST.PYTHON.SEARCH_PATTERN
            if PIH.OS.host_is_local(host):
                host = None
            variable_list: list[str] = if_else(DataTool.is_none(host),
                lambda: PIH.OS.environment_variable(WINDOWS.ENVIROMENT_VARIABLES.PATH),
                lambda: PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
                        [CONST.POWERSHELL.NAME, j((WINDOWS.ENVIROMENT_COMMAND, WINDOWS.ENVIROMENT_VARIABLES.PATH), ":")], host, interactive=None), True, True).stdout).split(";")
            for variable_item in variable_list:
                index: int = variable_item.find(search_pattern)
                if index != -1 and len(variable_item) - (index + len(search_pattern)) <= 4:
                    return os.path.join(variable_item, PathTool.add_extension(CONST.PYTHON.EXECUTOR, FILE.EXTENSION.EXE))
            return None  

        @staticmethod
        def python_version(host: str | None = None) -> str:
            command: list[str] = [CONST.PYTHON.EXECUTOR_ALIAS, CONST.PYTHON.COMMAND.VERSION]
            if PIH.OS.host_is_local(host):
                host = None
            return j(str(PIH.EXECUTOR.execute(
                    if_else(DataTool.is_none(host), 
                            command,
                            lambda:PIH.EXECUTOR.create_command_for_psexec(command, host, interactive=True)), True, True).stdout).strip().split(" ")[1:]
                    )

        @staticmethod
        def get_disk_statistics_list(host: str) -> list[DiskStatistics]:
            output: str = PIH.EXECUTOR.execute(f"powershell Get-WmiObject -Class win32_logicalDisk -ComputerName {host}", True, True, as_shell=True).stdout
            result: list[DiskStatistics] = []
            delimiter: str = ": "
            delimiter_length: int = len(delimiter)
            disk_statistics: DiskStatistics | None = None
            for line in ListTool.not_empty_items(output.splitlines()):
                line: str = line
                if line.startswith("DeviceID"):
                    disk_statistics = DiskStatistics(line[line.find(delimiter) + delimiter_length: -1])
                    result.append(disk_statistics)
                if line.startswith("FreeSpace"):
                    disk_statistics.free_space = DataTool.if_not_empty(line[line.find(delimiter) + delimiter_length:], lambda item: int(item), 0)
                if line.startswith("Size"):
                    disk_statistics.size = DataTool.if_not_empty(line[line.find(delimiter) + delimiter_length:], lambda item: int(item), 0)
            return result

        @staticmethod
        def get_users_logged_on(host: str, active: bool | None = True) -> list[str]:
            def get_login_list(complete_process: CompletedProcess) -> set[str]:
                result: set[str] = set()
                output: str = complete_process.stdout.decode(WINDOWS.CHARSETS.ALTERNATIVE)
                #print(host, nl(), output)
                for line in output.splitlines()[1:]:
                    line = line.lower()
                    if DataTool.is_none(active) or (active and (line.find("active") != -1 or line.find("активно") != -1)) or (not active and (line.find("disc") != -1 or line.find("диск") != -1)):
                        result.add(line.split(" ")[1])
                #print(result)
                return result
            result: set[str] = set()
            result |= get_login_list(PIH.EXECUTOR.execute(
                ["query", "user", "/server:" + host], True, True, False))
            result |= get_login_list(PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
                ["query", "user", "/server"], host, interactive=None, run_from_system_account=True), True, True, False))
            return list(result)

        @staticmethod
        def stop_windows_service(name: str, workstation_name: str) -> bool:
            output: str = PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
                ["sc", "stop", name], workstation_name,  interactive=True, run_from_system_account=True), True, True).stdout
            return output.find("3  STOP_PENDING") != -1

        @staticmethod
        def start_windows_service(name: str, workstation_name: str) -> bool:
            output: str = PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
            ["sc", "start", name], workstation_name, interactive=True, run_from_system_account=True), True, True).stdout
            return output.find("2  START_PENDING") != -1 

        @staticmethod
        def check_for_windows_service_running(name: str, workstation_name: str) -> bool:
            output: str = PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
            ["sc", "query", name], workstation_name, interactive=True), True, True).stdout
            return output.find("4  RUNNING") != -1

        @staticmethod
        def ping(address_or_ip: str, host: str | None = None, count: int = 1, timeout: int = 100):
            command_list: list[str] = ["ping", "-4",  address_or_ip, "-n",
                                       str(count), "-w", str(timeout)]
            result: CompletedProcess = PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(command_list, host, interactive=True), True, True)
            output: str = result.stdout
            return result.returncode == 0 and output.count("(TTL)") < count
          
        @staticmethod
        def get_executor_path(executor_name: str) -> str:
            return PIH.PATH.adapt_if_windows(PIH.PATH.join(
                PATHS.WS.PATH, CONST.PSTOOLS.NAME, executor_name))

        @staticmethod
        def create_command_for_executor(executor_name: str, command: list[str], login: str | None = None, password: str | None = None) -> list[str]:
            login = if_else(DataTool.is_empty(login), None, lambda: "\\".join([AD.DOMAIN_NAME, login]))
            return [PIH.PATH.path(PIH.EXECUTOR.get_executor_path(executor_name)), CONST.PSTOOLS.NO_BANNER, CONST.PSTOOLS.ACCEPTEULA] + if_else(DataTool.is_empty(login), [], lambda: ["-u", login]) + if_else(DataTool.is_empty(password), [], lambda: ["-p", password]) + command
        
        @staticmethod
        def create_command_for_psexec(command: list[str], host: str | None = None, login: str | None = None, password: str | None = None, interactive: bool | None = False, run_from_system_account: bool = False, run_with_elevetion: bool = False) -> list[str]:
            command_prefix: list[str] = DataTool.check_not_none(interactive, lambda: [["-d", "-i"][interactive]], [])
            host_start: str = r"\\"
            local_host: bool = PIH.OS.host_is_local(host)
            if not local_host: 
                if not DataTool.is_empty(host):
                    command_prefix.append(("" if host.startswith(host_start) else host_start) + host)
                login = login or PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_LOGIN)
                password = password or PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_PASSOWORD)
            if run_from_system_account:
                command_prefix.append("-s")
            if run_with_elevetion:
                command_prefix.append("-h") 
            return PIH.EXECUTOR.create_command_for_executor(CONST.PSTOOLS.PS_EXECUTOR, command_prefix + command, login, password)
        
        @staticmethod
        def create_command_for_start_service(role_or_information: ServiceRoles | ServiceInformationBase, interactive: bool | None = False) -> list[str]:
            description: ServiceDescription = ServiceRoles.description(role_or_information)
            python_command: list[str] = [description.pyton_executor_path or CONST.PYTHON.EXECUTOR_ALIAS]
            local: bool = PIH.OS.host_is_local(description.host)
            local_action = lambda value: if_else(local, None, value)
            login: str | None = local_action(DataTool.check_not_none(description.login, lambda: PIH.DATA.FORMAT.variable(description.login)))
            password: str | None = local_action(DataTool.check_not_none(description.password, lambda: PIH.DATA.FORMAT.variable(description.password)))
            interactive = local_action(interactive)
            return PIH.EXECUTOR.create_command_for_psexec(python_command, local_action(PIH.SERVICE.get_host(role_or_information)), login, password, interactive, description.run_from_system_account, False)

        @staticmethod
        def execute(command: list[str] | str, show_output: bool, capture_output: bool = False, as_text: bool = True, as_shell: bool = False) -> CompletedProcess:
            if show_output:
                if capture_output:
                    process_result = subprocess.run(
                        command, capture_output=True, text=as_text, shell=as_shell)
                else:
                    process_result = subprocess.run(
                        command, text=as_text)
            else:
                process_result = subprocess.run(
                    command, stdout=DEVNULL, stderr=STDOUT, text=as_text)
            return process_result
        
        @staticmethod
        def execute_for_result(command: list[str] | str, show_output: bool, capture_output: bool = False, as_text: bool = True, as_shell: bool = False) -> CompletedProcess:
            return PIH.EXECUTOR.execute(command, show_output, capture_output, as_text, as_shell)

        @staticmethod
        def kill_process(name_or_pid: str | int, host: str | None = None, via_standart_tools: bool = True, show_output: bool = False) -> bool:
           local: bool = PIH.OS.host_is_local(host)
           if via_standart_tools:
                is_string: bool = isinstance(name_or_pid, str)
                command: list[str] = ["taskkill"]
                if not local:
                    command += ["/s", host]
                return PIH.EXECUTOR.execute(command + ["/t", "/f", "/im" if is_string else "/pid", PIH.PATH.add_extension(name_or_pid, FILE.EXTENSION.EXE) if is_string else str(name_or_pid)], show_output).returncode < 2
           return PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_executor(CONST.PSTOOLS.PS_KILL_EXECUTOR, [PIH.DATA.FORMAT.host(host), "-t", str(name_or_pid)]), show_output).returncode == 0

        @staticmethod
        def process_is_exists(pid: int, host: str | None = None, login: str | None = None, password: str | None = None) -> str:
            command_list: list[str] = ["tasklist", "/fi", f"pid eq {pid}", "/fo", "list"]
            login = "\\".join(
                [AD.DOMAIN_NAME, login or PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_LOGIN)])
            password = password or PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_PASSOWORD)
            if not DataTool.is_empty(host):
                command_list += ["/s", host]
                command_list += ["/u", login]
                command_list += ["/p", password]
            output: str = PIH.EXECUTOR.execute(
                command_list, True, True, as_text=False).stdout.decode(WINDOWS.CHARSETS.ALTERNATIVE).lower()
            return output.find("pid") != -1

        @staticmethod
        def kill_python_process(host: str, via_standart_tools: bool) -> bool:
            return PIH.EXECUTOR.kill_process(CONST.PYTHON.EXECUTOR, host, via_standart_tools)

        @staticmethod
        def _ws_action(value: str, host: str, show_output: bool = False) -> bool:
            return PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
                ["shutdown", value, "/t", "0"], host), show_output).returncode == 0

        @staticmethod
        def ws_reboot(host: str, show_output: bool = False) -> bool:
            return PIH.EXECUTOR._ws_action("/r", host, show_output)

        @staticmethod
        def ws_shutdown(host: str, show_output: bool = False) -> bool:
            return PIH.EXECUTOR._ws_action("/s", host, show_output)
        
    class EVENT:

        @staticmethod
        def send(value: Events, parameters: tuple[Any] | None = None) -> None:
            def internal_send_command(command_name: str, parameters: dict) -> None:
                try:
                    PIH.SERVICE.call_command(ServiceCommands.send_event,
                             (command_name, parameters))
                except Error as error:
                    PIH.output.error("Log send error")
            PIH.LOG.executor.submit(internal_send_command,
                                    value.name, PIH.EVENT.BUILDER.create_parameters_map(value, parameters))   

        @staticmethod
        def mri_filter_was_changed() -> None:
            PIH.EVENT.send(Events.MRI_CHILLER_FILTER_WAS_CHANGED, (PIH.DATA.MATERIALIZED_RESOURCES.get_count(MATERIALIZED_RESOURCES.TYPES.CHILLER_FILTER),))

        @staticmethod
        def computer_was_started(name: str) -> None:
            PIH.EVENT.send(
                Events.COMPUTER_WAS_STARTED, (name,))

        @staticmethod
        def server_was_started(name: str) -> None:
            PIH.EVENT.send(
                Events.SERVER_WAS_STARTED, (name,))

        @staticmethod
        def get_parameter(event: Events, parameters: dict[str, Any], parameter_name: str | None = None) -> Any | dict[str, Any]:
            parameters_map: dict[str, Any] = PIH.EVENT.BUILDER.create_parameters_map(event, parameters)
            return DataTool.check_not_none(parameter_name, lambda: parameters_map[parameter_name], parameters_map)

        class BUILDER:

            @staticmethod
            def create_parameters_map(event: Events, parameters: tuple[Any] | None = None, check_for_parameters_count: bool = True) -> dict:
                event_description: EventDescription = EnumTool.get(event)
                parameter_pattern_list: list = DataTool.as_list(
                    event_description.params)
                parameters = parameters or ()
                if check_for_parameters_count and len(parameter_pattern_list) > len(parameters):
                    raise Exception(
                        "Income parameter list length is less that parameter list length of command")
                result: dict[str, Any] = {}
                for index, parameter_pattern_item in enumerate(parameter_pattern_list):
                    if index < len(parameters):
                        parameter_pattern: ParamItem = parameter_pattern_item
                        value: Any | None = parameters[index]
                        if DataTool.is_not_none(value):
                            result[parameter_pattern.name] = value
                    else:
                        break
                return result

            @staticmethod
            def create_event(event: Events, paramters: Any | None = None, parameters_getter: Callable[[None], tuple[Any]] | None = None, default_value: tuple[Any] | Any | None = None, check_all: bool = False) -> Events | tuple[Events | tuple[Any]] | tuple[Any]:
                return DataTool.check_not_none(paramters, lambda: (event, parameters_getter()), event if DataTool.is_none(default_value) else (event, default_value), check_all)
            
            @staticmethod
            def polibase_person_with_inaccessable_email_was_detected(person: PolibasePerson | None = None, registrator_person: PolibasePerson | None = None, actual: bool = False) -> tuple[Events | tuple[Any]] | Events:
                def get_information() -> tuple[Any]:
                    workstation_name: str = "<не определён>"
                    workstation_description: str = "<не определён>"
                    if actual:
                        try:
                            user: User = PIH.RESULT.USER.by_polibase_pin(
                                registrator_person.pin).data
                            workstation: Workstation = PIH.RESULT.get_first_item(
                                PIH.RESULT.WORKSTATION.by_login(user.samAccountName)) or PIH.RESULT.WORKSTATION.by_name(CONST.TEST.WORKSTATION_MAME).data
                            if DataTool.is_not_none(workstation):
                                workstation_name = workstation.name
                                workstation_description = workstation.description
                        except NotFound:
                                pass
                    return (person.FullName, person.pin, person.email, registrator_person.FullName, workstation_name, workstation_description)
                event: Events = Events.POLIBASE_PERSON_WITH_INACCESSABLE_EMAIL_WAS_DETECTED
                return PIH.EVENT.BUILDER.create_event(event, registrator_person, get_information, DataTool.check_not_none(person, lambda: (None, person.pin)))

            @staticmethod
            def polibase_person_duplication_was_detected(person: PolibasePerson | None = None, duplicated_person: PolibasePerson | None = None, registrator_person: PolibasePerson | None = None) -> Events | tuple[Events, tuple[Any]]:
                event: Events = Events.POLIBASE_PERSON_DUPLICATION_WAS_DETECTED
                def get_information() -> tuple[Any]:
                    return (person.FullName, person.pin, duplicated_person.pin, duplicated_person.pin, registrator_person.FullName)
                return PIH.EVENT.BUILDER.create_event(event, person, get_information)

            @staticmethod
            def polibase_person_email_was_added(person: PolibasePerson | None = None, person_for_search: PolibasePerson | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.POLIBASE_PERSON_EMAIL_WAS_ADDED, person, lambda: (person.FullName, person.pin, person.email), DataTool.check_not_none(person_for_search, lambda: (None, person_for_search.pin)))
            
            @staticmethod
            def service_was_started(information: ServiceInformation | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.SERVICE_WAS_STARTED, information, lambda: (information.name,
                                                    information.host, information.port, information.pid,  information))

            @staticmethod
            def action_was_done(action: Actions | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.ACTION_WAS_DONE, action, lambda: (None, EnumTool.get(action).name,))

            @staticmethod
            def chiller_temperature_alert_was_fired() -> Events:
                return PIH.EVENT.BUILDER.create_event(Events.MRI_CHILLER_TEMPERATURE_ALERT_WAS_FIRED)

            @staticmethod
            def polibase_person_set_card_registry_folder(name: str | None = None, person_or_pin: PolibasePerson | int | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_WAS_SET_FOR_POLIBASE_PERSON, (name, person_or_pin), lambda: (DataTool.if_not_empty(person_or_pin, lambda person: PIH.RESULT.POLIBASE._person_pin(person)), name))
            
            @staticmethod
            def card_registry_folder_was_registered(name: str | None = None, place_a: int | None = None, place_b: int | None = None, place_c: int | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_WAS_REGISTERED, name, lambda: (name, place_a, place_b, place_c))
            
            @staticmethod
            def card_registry_folder_start_card_sorting(name: str | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_START_CARD_SORTING, name, lambda: (name, ))

            @staticmethod
            def card_registry_folder_complete_card_sorting(name: str | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_COMPLETE_CARD_SORTING, name, lambda: (PIH.DATA.FORMAT.polibase_person_card_registry_folder(name), ))

            staticmethod
            def chiller_was_turned_off() -> Events:
                return PIH.EVENT.BUILDER.create_event(Events.MRI_CHILLER_WAS_TURNED_OFF)
            
            @staticmethod
            def chiller_was_turned_on() -> Events:
                return PIH.EVENT.BUILDER.create_event(Events.MRI_CHILLER_WAS_TURNED_ON)

            @staticmethod
            def service_was_stopped(information: ServiceInformationBase | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.SERVICE_WAS_STOPPED, information, lambda: (information.name, information) )
            
            @staticmethod
            def polibase_persons_barcodes_old_format_were_detected(person_pin_list: list[int] | None = None) -> Events | tuple[Events, tuple[Any]]:
                return  PIH.EVENT.BUILDER.create_event(Events.POLIBASE_PERSONS_WITH_OLD_FORMAT_BARCODE_WAS_DETECTED, person_pin_list, lambda: (person_pin_list, ))
            
            @staticmethod
            def polibase_person_barcodes_new_format_were_created(person_pin_list: list[int] | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.POLIBASE_PERSON_BARCODES_WITH_OLD_FORMAT_WERE_CREATED, person_pin_list, lambda: (person_pin_list, ))

            @staticmethod
            def polibase_person_was_created(value: PolibasePerson | None = None) -> Events | tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.POLIBASE_PERSON_WAS_CREATED, value, lambda: (value.FullName, value.pin, value))
            
            @staticmethod
            def polibase_person_was_updated(value: PolibasePerson | None = None) -> tuple[Events, tuple[Any]]:
                return PIH.EVENT.BUILDER.create_event(Events.POLIBASE_PERSON_WAS_UPDATED, value, lambda: (value.FullName, value.pin, value)) 

        @staticmethod
        def polibase_person_visit_was_registered(value: PolibasePersonVisitDS) -> None:
            PIH.EVENT.send(Events.POLIBASE_PERSON_VISIT_WAS_REGISTERED, (
                value.FullName, "Предзапись" if value.pin == CONST.POLIBASE.PRERECORDING_PIN else value.pin, value))


        @staticmethod
        def resource_accessible(resource: ResourceStatus, at_first_time: bool) -> None:
            PIH.EVENT.send(Events.RESOURCE_ACCESSABLE,
                                (resource.name, resource, at_first_time))

        @staticmethod
        def resource_inaccessible(resource: ResourceStatus, at_first_time: bool, reason: RESOURCES.InaccessableReasons | None = None) -> None:
            reason_string: str = ""
            reason_name: str | None = None
            if not DataTool.is_empty(reason):
                reason_string = f"Причина: {reason.value}"
                reason_name = reason.name
            PIH.EVENT.send(Events.RESOURCE_INACCESSABLE, (resource.name,
                                resource, at_first_time, reason_string, reason_name))

        @staticmethod
        def polibase_person_visit_notification_was_registered(visit: PolibasePersonVisitDS, notification: PolibasePersonVisitNotificationDS) -> None:
            PIH.EVENT.send(Events.POLIBASE_PERSON_VISIT_NOTIFICATION_WAS_REGISTERED, (
                visit.FullName, "Предзапись" if visit.pin == CONST.POLIBASE.PRERECORDING_PIN else visit.pin, notification))

        @staticmethod
        def login() -> None:
            login: str = PIH.session.get_login()
            user: User = PIH.RESULT.USER.by_login(login).data
            PIH.EVENT.send(
                Events.LOG_IN, (user.name, login, PIH.OS.host()))

        @staticmethod
        def whatsapp_message_received(message: WhatsAppMessage) -> None:
            PIH.EVENT.send(
                Events.WHATSAPP_MESSAGE_RECEIVED, (message,))

        @staticmethod
        def new_file_detected(path: str) -> None:
            PIH.EVENT.send(
                Events.NEW_FILE_DETECTED, (PIH.PATH.path(path), ))

        @staticmethod
        def new_mail_message_was_received(value: NewMailMessage) -> None:
            PIH.EVENT.send(
                Events.NEW_EMAIL_MESSAGE_WAS_RECEIVED, (value.mailbox_address, value.subject, value.from_, value))

        @staticmethod
        def new_polibase_scanned_document_detected(value: PolibaseScannedDocument):
            PIH.EVENT.send(Events.NEW_POLIBASE_DOCUMENT_DETECTED,
                                (value.file_path, value.pin, value.document_name))

        @staticmethod
        def start_session() -> None:
            argv: list[str] = PIH.session.argv
            argv_str: str = ""
            if not DataTool.is_empty(argv):
                argv_str = " ".join(argv)
                argv_str = f"({argv_str})"
            login: str = PIH.session.get_login()
            user: User = PIH.RESULT.USER.by_login(login).data
            PIH.EVENT.send(Events.SESSION_STARTED, (user.name, login,
                                                        f"{PIH.session.file_name} {argv_str}", f"{PIH.VERSION.value}", PIH.OS.host()))

        @staticmethod
        def backup_robocopy_job_was_started(name: str, job_status: RobocopyJobStatus) -> None:
            PIH.EVENT.send(
                Events.BACKUP_ROBOCOPY_JOB_WAS_STARTED, (name, job_status.pid))

        @staticmethod
        def backup_robocopy_job_was_completed(name: str, job_status: RobocopyJobStatus) -> None:
            status: int = job_status.last_status
            is_live: bool = job_status.pid > 0
            status_string: str = "live job" if is_live else str(status)
            pid_string: str = str(job_status.pid) if is_live else "not live job"
            if status >= ROBOCOPY.ERROR_CODE_START:
                status_string += " (есть ошибки)"
            PIH.EVENT.send(
                Events.BACKUP_ROBOCOPY_JOB_WAS_COMPLETED, (name, status_string, status, pid_string))

        @staticmethod
        def service_is_inaccessable_and_will_be_restarted(information: ServiceInformationBase ) -> None:
            PIH.EVENT.send(Events.SERVICE_IS_INACCESIBLE_AND_WILL_BE_RESTARTED, (information.name, information))

        @staticmethod
        def service_was_not_started(information: ServiceInformation, error: str) -> None:
            PIH.EVENT.send(Events.SERVICE_WAS_NOT_STARTED, (information.name,
                                                            information.host, information.port, error, information))

        @staticmethod
        def hr_notify_about_new_employee(login: User) -> None:
            user: User = PIH.RESULT.USER.by_login(login).data
            hr_user: User = ResultTool.get_first_item(
                PIH.RESULT.USER.by_job_position(AD.JobPisitions.HR))
            PIH.EVENT.send(Events.HR_NOTIFY_ABOUT_NEW_EMPLOYEE, (FullNameTool.to_given_name(hr_user.name),
                                                                        user.name, user.mail))

        @staticmethod
        def it_notify_about_user_creation(login: str, password: str) -> None:
            it_user_list: list[User] = PIH.RESULT.USER.by_job_position(
                AD.JobPisitions.IT).data
            me_user_login: str = PIH.session.get_login()
            it_user_list = list(
                filter(lambda user: user.samAccountName != me_user_login, it_user_list))
            it_user: User = it_user_list[0]
            user: User = PIH.RESULT.USER.by_login(login).data
            PIH.EVENT.send(Events.IT_NOTIFY_ABOUT_CREATE_USER, (
                user.name, user.description, user.samAccountName, password, user.telephoneNumber, user.mail))
            PIH.EVENT.send(Events.IT_TASK_AFTER_CREATE_NEW_USER, (FullNameTool.to_given_name(
                it_user.name), user.name, user.mail, password))

        @staticmethod
        def it_notify_about_mark_creation(temporary: bool, full_name: Any, tab_number: str | None = None) -> None:
            name: str = FullNameTool.fullname_to_string(full_name) if isinstance(
                full_name, FullName) else full_name
            mark: Mark = PIH.RESULT.MARK.by_name(name, True).data
            telephone_number: str = PIH.DATA.FORMAT.telephone_number(
                mark.telephoneNumber)
            if temporary:
                PIH.EVENT.send(Events.IT_NOTIFY_ABOUT_CREATE_TEMPORARY_MARK,
                                    (name, tab_number, telephone_number))
            else:
                PIH.EVENT.send(Events.IT_NOTIFY_ABOUT_CREATE_NEW_MARK, (
                    name, telephone_number, mark.TabNumber, mark.GroupName))

        @staticmethod
        def it_notify_about_temporary_mark_return(mark: Mark, temporary_tab_number: int) -> None:
            PIH.EVENT.send(
                Events.IT_NOTIFY_ABOUT_TEMPORARY_MARK_RETURN, (mark.FullName, temporary_tab_number))

        @staticmethod
        def backup_notify_about_polibase_creation_db_dumb_start() -> None:
            PIH.EVENT.send(
                Events.POLIBASE_CREATION_DB_DUMP_START)

        @staticmethod
        def backup_notify_about_polibase_creation_db_dumb_complete() -> None:
            PIH.EVENT.send(
                Events.POLIBASE_CREATION_DB_DUMP_COMPLETE)

        @staticmethod
        def backup_notify_about_polibase_creation_archived_db_dumb_start() -> None:
            PIH.EVENT.send(
                Events.POLIBASE_CREATION_ARCHIVED_DB_DUMP_START)

        @staticmethod
        def backup_notify_about_polibase_creation_archived_db_dumb_complete() -> None:
            PIH.EVENT.send(
                Events.POLIBASE_CREATION_ARCHIVED_DB_DUMP_COMPLETE)

        @staticmethod
        def backup_notify_about_polibase_coping_archived_db_dumb_start(destination: str) -> None:
            PIH.EVENT.send(
                Events.POLIBASE_COPING_ARCHIVED_DB_DUMP_START, (destination,))

        @staticmethod
        def backup_notify_about_polibase_coping_archived_db_dumb_complete(destination: str) -> None:
            PIH.EVENT.send(
                Events.POLIBASE_COPING_ARCHIVED_DB_DUMP_COMPLETE, (destination,))

        @staticmethod
        def backup_notify_about_polibase_coping_db_dumb_start(destination: str) -> None:
            PIH.EVENT.send(
                Events.POLIBASE_COPING_DB_DUMP_START, (destination,))

        @staticmethod
        def backup_notify_about_polibase_coping_db_dumb_complete(destination: str) -> None:
            PIH.EVENT.send(
                Events.POLIBASE_COPING_DB_DUMP_COMPLETE, (destination,))

        @staticmethod
        def it_notify_about_mark_return(mark: Mark) -> None:
            PIH.EVENT.send(
                Events.IT_NOTIFY_ABOUT_MARK_RETURN, (mark.FullName, mark.TabNumber))

        @staticmethod
        def it_notify_about_create_new_mark(full_name: Any) -> None:
            PIH.EVENT.it_notify_about_mark_creation(
                False, full_name)

        @staticmethod
        def it_notify_about_create_temporary_mark(full_name: Any, tab_number: str) -> None:
            PIH.EVENT.it_notify_about_mark_creation(
                True, full_name, tab_number)

        @staticmethod
        def printer_report(name: str, location: str, report_text: str) -> bool:
            return PIH.EVENT.send(Events.PRINTER_REPORT, (name, location, report_text))

        @staticmethod
        def on_event(handler: Callable[[ParameterList, ServiceListener], None], block: bool = True) -> None:
            def thread_handler() -> None:
                ServiceListener().listen_for([ServiceCommands.send_event], lambda _, parameter_list, service_listener: handler(parameter_list, service_listener))
            if block:
                thread_handler()
            else:
                Thread(target=thread_handler).start()

        @staticmethod
        def wait_server_start(handler_or_server_name: Callable[[str, Callable[[None], None]], None] | str) -> None:
            def internal_handler(parameter_list: ParameterList, listener: ServiceListener) -> None:
                event, parameters = PIH.DATA.EXTRACT.EVENT.with_parameters(parameter_list)
                if event == Events.SERVER_WAS_STARTED:
                    server_name: str = parameters[0]
                    if callable(handler_or_server_name):
                        handler_or_server_name(server_name, listener.close)
                    else:
                        if handler_or_server_name.startswith(server_name):
                            listener.close()
            PIH.EVENT.on_event(internal_handler)


        @staticmethod
        def on_service_starts(handler_or_service_role_or_information: Callable[[str, Callable[[None], None]], None] | ServiceRoles | ServiceInformationBase) -> None:
            def internal_handler(parameter_list: ParameterList, listener: ServiceListener) -> None:
                event, parameters = PIH.DATA.EXTRACT.EVENT.with_parameters(parameter_list)
                if event == PIH.EVENT.BUILDER.service_was_started():
                    service_description_name: str = parameters[0]
                    if callable(handler_or_service_role_or_information):
                        handler_or_service_role_or_information(service_description_name, listener.close)
                    elif handler_or_service_role_or_information == service_description_name:
                        listener.close()
            PIH.EVENT.on_event(internal_handler)
        
        @staticmethod
        def on_robocopy_job_complete(handler_or_robocopy_job_name: Callable[[str, int, ServiceListener], None] | str) -> bool | None:
            class DATA_HOLDER:
                result: bool | None = None
            def internal_handler(parameter_list: ParameterList, listener: ServiceListener) -> None:
                event, parameters = PIH.DATA.EXTRACT.EVENT.with_parameters(parameter_list)
                if event == Events.BACKUP_ROBOCOPY_JOB_WAS_COMPLETED:
                    robocopy_job_status_name: str = parameters[0]
                    robocopy_job_status: int = parameters[-1]
                    DATA_HOLDER.result = robocopy_job_status < ROBOCOPY.ERROR_CODE_START
                    if callable(handler_or_robocopy_job_name):
                        handler_or_robocopy_job_name(
                            robocopy_job_status_name, robocopy_job_status, listener)
                    else:
                        if robocopy_job_status_name.startswith(handler_or_robocopy_job_name):
                            listener.close()
            PIH.EVENT.on_event(internal_handler)
            return DATA_HOLDER.result

        @staticmethod
        def waiting_for_mobile_helper_message_input(recipient: str, handler: Callable[[str, Callable[[None], None]], None]) -> None:
            def internal_handler(parameter_list: ParameterList, listener: ServiceListener) -> None:
                message: WhatsAppMessage = PIH.DATA.EXTRACT.EVENT.whatsapp_message(parameter_list)
                if not DataTool.is_empty(message) and PIH.DATA.FORMAT.telephone_number(message.sender) == PIH.DATA.FORMAT.telephone_number(recipient):
                    handler(message.message, listener.close)
            PIH.EVENT.on_event(internal_handler)

            
    class SERVICE:

        LONG_OPERATION_DURATION: int | None = None

        EVENT_LISTENER_NAME_PREFIX: str = "_@@EventListener@@_"
        SUPPORT_NAME_PREFIX: str = "_@@Support@@_"
        command_map: dict[str, ServiceDescription] | None = None

        class DATA_HOLDER:
            long_operation_listeners: list[Callable[[None], None]] = []

        @staticmethod
        def check_on_host_chanchable(role_or_information: ServiceRoles | ServiceInformationBase) -> bool:
            description: ServiceDescription = ServiceRoles.description(role_or_information)
            return description.host_changeable or StringTool.contains(PIH.OS.host(), description.host)

        @staticmethod
        def call_listeners_on_long_operation() -> None:
            for listener in PIH.SERVICE.DATA_HOLDER.long_operation_listeners:
                listener()

        @staticmethod
        def start_listen_for_long_operation(listener: Callable[[None], None]) -> None:
            PIH.SERVICE.DATA_HOLDER.long_operation_listeners.append(listener)

        @staticmethod
        def stop_listen_for_long_operation(listener: Callable[[None], None]) -> None:
            PIH.SERVICE.DATA_HOLDER.long_operation_listeners.remove(listener)

        @staticmethod
        def call(role_or_information: ServiceRoles | ServiceInformationBase | None, service_command: ServiceCommands, parameters: Any | None = None, timeout: int | None = None, blocked: bool = True, long_operation_duration: int | None = None) -> str | None:
            long_operation_duration = long_operation_duration or PIH.SERVICE.LONG_OPERATION_DURATION
            class DATA_HOLDER:
                stop_long_operation_action: bool = False
            def long_operation_action() -> None:
                time.sleep(long_operation_duration/1000)
                if not DATA_HOLDER.stop_long_operation_action:
                    PIH.SERVICE.call_listeners_on_long_operation()
            if not DataTool.is_empty(long_operation_duration):
                long_operation_thread: Thread = Thread(
                    target=long_operation_action)
                long_operation_thread.start()
            def action() -> str | None:
                result: str | None = RPC.call_service(role_or_information, service_command, parameters, timeout)
                DATA_HOLDER.stop_long_operation_action = True
                return result
            if blocked:
                return action()
            else:
                Thread(target=action).start()
                return None

        @staticmethod
        def call_command(value: ServiceCommands, parameters: dict[str, Any] | None = None, timeout: int | None = None, blocked: bool = True, long_operation_duration: int | None = None) -> str | None:
           return PIH.SERVICE.call(None, value, parameters, timeout, blocked, long_operation_duration)

        @staticmethod
        def get_support_host_list(role_or_information: ServiceRoles | ServiceInformationBase) -> list[str]:
            return list(filter(lambda item: item.name.startswith(f"{PIH.SERVICE.SUPPORT_NAME_PREFIX}{ServiceRoles.description(role_or_information).name}"), PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP))

        class ADMIN:

            SERVICE_INFORMATION_MAP: dict[ServiceInformationBase, ServiceInformation] = {}

            @staticmethod
            def check_on_startable(role_or_information: ServiceRoles | ServiceInformationBase) -> bool | None:
                service_description: ServiceDescription = if_else(isinstance(
                role_or_information, ServiceRoles), lambda: ServiceRoles.description(role_or_information), role_or_information)
                login_value: str | None = service_description.login
                login_variable_name_list: list[str] | None = PIH.DATA.EXTRACT.variables(login_value)
                if not DataTool.is_empty(login_variable_name_list):
                    if DataTool.is_empty(PIH.DATA.FORMAT.variable(login_value, True)):
                        raise Exception(f"Login for start service {service_description.host} ({login_variable_name_list[0]}) is not set")
                password_value: str | None = service_description.password
                password_variable_name_list: list[str] | None = PIH.DATA.EXTRACT.variables(password_value)
                if not DataTool.is_empty(PIH.DATA.EXTRACT.variables(password_value)):
                    if DataTool.is_empty(PIH.DATA.FORMAT.variable(password_value, True)):
                        raise Exception(f"Password for start service {service_description.host} ({password_variable_name_list[0]}) is not set")
                return True
            
            @staticmethod
            def change_host_on_local(role_or_information: ServiceRoles | ServiceInformationBase) -> None:
                ServiceRoles.description(role_or_information).host = PIH.OS.host()

            @staticmethod
            def service_information_list() -> list[ServiceInformation]:
                return DataTool.to_list(PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP)

            @staticmethod
            def kill_all(local: bool = True, via_standart_tools: bool = True, exclude_me: bool = False) -> bool:
                hosts: set[str] = set()
                for server_role in ServiceRoles:
                    host: str | None = ServiceRoles.description(server_role).host
                    if not DataTool.is_empty(host):
                        hosts.add(host)
                def kill(host: str, local: bool, via_standart_tools: bool) -> None:
                    if local:
                        PIH.EXECUTOR.kill_python_process(host, via_standart_tools)
                    else:
                        PIH.ACTION.WORKSTATION.kill_python_process(host, via_standart_tools)
                for host in hosts:
                    if host != PIH.OS.host():
                        kill(host, local, via_standart_tools)
                if not exclude_me:
                    for host in hosts:
                        if host == PIH.OS.host():
                            kill(host, local, via_standart_tools)

            @staticmethod
            def subscribe_on(service_command: ServiceCommands, type: int = SubscribtionTypes.ON_RESULT, name: str | None = None) -> bool:
                return RPC.service.subscribe_on(service_command, type, name)

            @staticmethod
            def unsubscribe(service_command: ServiceCommands, type: int) -> bool:
                return RPC.service.unsubscribe(service_command, type)

            @staticmethod
            def create_developer_service_description(port: int = None) -> ServiceDescription:
                if DataTool.is_none(port) or port == ServiceRoles.DEVELOPER.value.port:
                    return ServiceRoles.DEVELOPER.value
                return ServiceDescription(f"Developer_{port}", host=CONST.HOST.DEVELOPER.NAME, port=CONST.RPC.PORT(port))

            @staticmethod
            def create_support_service_or_master_service_description(master_service_desctiption: ServiceDescription, host: str | None = None) -> ServiceDescription:
                if PIH.SERVICE.check_on_accessibility(master_service_desctiption):
                    host = host or PIH.OS.host()
                    if master_service_desctiption.host != host:
                        port: int = PIH.SERVICE.create_port(master_service_desctiption)
                        return ServiceDescription(
                            name=":".join([f"{PIH.SERVICE.SUPPORT_NAME_PREFIX}{master_service_desctiption.name}", host]),
                            description=f"Support service for {master_service_desctiption.name} on {host}",
                            host=host,
                            port=port,
                            auto_restart=False)
                return master_service_desctiption
            
            @staticmethod
            def create_event_listener_service_description(host: str, port: int) -> ServiceDescription:
                return ServiceDescription(
                    name=":".join([PIH.SERVICE.EVENT_LISTENER_NAME_PREFIX, host, str(port)]),
                    description="Subscriber",
                    host=host,
                    port=port,
                    auto_start=False,
                    auto_restart=False)

            @staticmethod
            def as_developer(service_role: ServiceRoles, port: int = None) -> ServiceDescription:
                developer_service_description: ServiceDescription = PIH.SERVICE.ADMIN.create_developer_service_description(port)
                description: ServiceDescription = ServiceRoles.description(service_role)
                description.isolated = True
                description.host = developer_service_description.host
                description.port = developer_service_description.port
                return description

            @staticmethod
            def isolate(role_or_information: ServiceRoles | ServiceInformationBase) -> ServiceDescription:
                description: ServiceDescription = ServiceRoles.description(role_or_information)
                description.isolated = True
                description.auto_restart = False
                return description
            
            @staticmethod
            def restart(role_or_information: ServiceRoles | ServiceInformationBase, show_output: bool = True) -> bool | None:
                if PIH.SERVICE.ADMIN.check_on_startable(role_or_information):
                    PIH.SERVICE.ADMIN.stop(role_or_information, False)
                    return PIH.SERVICE.ADMIN.start(role_or_information, False, show_output)
                return None

            @staticmethod
            def start(role_or_information: ServiceRoles | ServiceInformationBase, check_if_started: bool = True, show_output: bool = True) -> bool | None:
                description: ServiceDescription = ServiceRoles.description(role_or_information, True)
                try:
                    PIH.SERVICE.ADMIN.check_on_startable(role_or_information)
                    if check_if_started:
                        if PIH.SERVICE.check_on_accessibility(description):
                            return None
                    command: list[str] = PIH.EXECUTOR.create_command_for_start_service(description)
                    service_file_path: str | None = None
                    service_file: str = PathTool.add_extension(CONST.SERVICE.NAME, FILE.EXTENSION.PYTHON)
                    if DataTool.is_empty(description.service_path):
                        service_file_path = PIH.PATH.join(
                            PATH_FACADE.VALUE, j((description.name, CONST.FACADE.SERVICE_FOLDER_SUFFIX)), service_file)
                    else:
                        service_file_path = PIH.PATH.join(description.service_path, service_file)
                    command.append(service_file_path)
                    command.append("--isolated")
                    command.append("0")
                    process_result: CompletedProcess = PIH.EXECUTOR.execute(command, show_output)
                    if process_result.returncode in [2, 2250, 2120]:
                        return False
                    return True
                except Exception as error:
                    A.O.error(error.args[0])
                    return None

            @staticmethod
            def kill(role_or_information: ServiceRoles | ServiceInformationBase, local: bool = True, via_standart_tools: bool = True) -> bool | None:
                information: ServiceInformation | None = PIH.SERVICE.get_information(role_or_information)
                if DataTool.is_empty(information):
                    return None
                pid: int = information.pid
                host: str = PIH.SERVICE.get_host(information)
                if local:
                    return PIH.EXECUTOR.kill_process(pid, host, via_standart_tools)
                return PIH.ACTION.WORKSTATION.kill_process(pid, host, via_standart_tools)
            
            @staticmethod
            def serve(role_or_information: ServiceRoles | ServiceInformationBase, 
                      call_handler: Callable[[ServiceCommands, ParameterList], Any] | None = None, 
                      starts_handler: Callable[[IService | None], None] | None = None, 
                      max_workers: int | None = None, 
                      stop_before: bool = True, 
                      depends_on_list: list[ServiceDescription | ServiceRoles] | None = None, 
                      isolate: bool = False,
                      show_output: bool = True) -> None:
                host: str = PIH.OS.host()
                service_description: ServiceInformationBase = ServiceRoles.description(role_or_information)
                if PIH.SERVICE.check_on_host_chanchable(service_description):
                    if isolate:
                        PIH.SERVICE.ADMIN.isolate(service_description)
                    else:
                        if not PIH.DATA.contains(host, service_description.host):
                            PIH.SERVICE.ADMIN.change_host_on_local(service_description)
                        if stop_before:
                            if PIH.SERVICE.check_on_accessibility(service_description):
                                PIH.SERVICE.ADMIN.stop(service_description)
                    def internal_start_handler(service: IService) -> None:
                        if PIH.OS.is_linux():
                            PIH.PATH.make_directory_if_not_exists(PATHS.FACADE.LINUX_MOUNT_POINT_PATH, host)
                            PIH.PATH.mount_facade_storage_on_linux_host(host)
                        if DataTool.is_not_none(starts_handler):
                            if starts_handler.__code__.co_argcount == 1:
                                starts_handler(service)
                            else:
                                starts_handler()
                    service: IService = RPC.create_service()
                    from inspect import signature, Signature
                    def internal_call_handler(command_name: str, parameter_list: ParameterList, context) -> Any | None:
                        if not DataTool.is_empty(call_handler):
                            sig: Signature = signature(call_handler)
                            arg_count: int = len(sig.parameters) - ("self" in sig.parameters)
                            if arg_count == 3:
                                if DataTool.is_in(sig.parameters, "context"):
                                    return call_handler(EnumTool.get(ServiceCommands, command_name), parameter_list, context) 
                                if DataTool.is_in(sig.parameters, "subscribtion_result"):
                                    return call_handler(EnumTool.get(ServiceCommands, command_name), parameter_list, PIH.DATA.EXTRACT.subscribtion_result(parameter_list))    
                            return call_handler(EnumTool.get(ServiceCommands, command_name), parameter_list) 
                        return None   
                    service.serve(service_description, internal_call_handler,
                                internal_start_handler, max_workers, depends_on_list, show_output)
                else:
                    PIH.ERROR.service_host_is_unchanachable(
                        service_description.host)

            @staticmethod
            def stop(role_or_information: ServiceRoles | ServiceInformationBase, check_if_started: bool = True, direct_call: bool = False) -> bool:
                description: ServiceDescription = ServiceRoles.description(role_or_information)
                if not check_if_started or PIH.SERVICE.check_on_accessibility(description):
                    if PIH.SERVICE.is_service_as_listener(description) or direct_call:
                        PIH.SERVICE.call(description, ServiceCommands.stop_service)
                        return True
                    service_information: ServiceInformationBase | None = DataTool.fill_data_from_source(
                            ServiceInformationBase(), PIH.SERVICE.get_information(description))
                    if DataTool.is_none(service_information):
                        return False
                    PIH.SERVICE.call(service_information,
                                    ServiceCommands.stop_service)
                    return True
                return False

            @staticmethod
            def update_service_information(list: list[ServiceInformation], add: bool = True, overwrite: bool = False) -> None:
                if overwrite:
                    PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP = {}    
                for item in list:
                    if add:
                        PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP[item] = item
                    else:
                        if item in PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP:
                            del PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP[item]

            @staticmethod
            def validate(cached: bool = False, include_isolated: bool = False) -> tuple[list, list]:
                if not cached:
                    PIH.SERVICE.ADMIN.request_for_service_information_list()
                service_information_list: list[ServiceInformation] = PIH.SERVICE.ADMIN.service_information_list()
                if not include_isolated:
                    service_information_list = list(filter(lambda item: not item.isolated, service_information_list)) 
                if not DataTool.is_empty(service_information_list):
                    length: int = len(service_information_list)
                    with ThreadPoolExecutor(max_workers=length) as executor:
                        future_to_bool = {executor.submit(
                            PIH.SERVICE.check_on_accessibility, service_descroption): service_descroption for service_descroption in service_information_list}
                        offline_service_list: list[ServiceInformation] = []
                        for value in futures.as_completed(future_to_bool):
                            if not value.result():
                                service_information: ServiceInformation = future_to_bool[value]
                                offline_service_list.append(service_information)
                                service_information_list.remove(service_information)
                                del PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP[service_information]
                        service_description_list: list[ServiceDescription] = list(filter(lambda item: item.visible_for_admin, map(lambda item: ServiceRoles.description(item), ServiceRoles)))
                        for service_description_item in service_description_list:
                            if service_description_item not in service_information_list and service_description_item not in offline_service_list:
                                offline_service_list.append(service_description_item)
                        return offline_service_list, service_information_list
                return [], []  

            @staticmethod
            def request_for_service_information_list() -> None:
                PIH.SERVICE.ADMIN.update_service_information(list(map(PIH.DATA.EXTRACT.service_information, DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.get_service_information_table, ((RPC.service_information or ServiceRoles.STUB).name), )) or [])), True, True)
                  
        @staticmethod
        def check_on_accessibility(role_or_information: ServiceRoles | ServiceInformationBase, cached: bool = False) -> bool:
            return not DataTool.is_empty(PIH.SERVICE.get_information(role_or_information, cached))
        
        @staticmethod
        def is_service_as_listener(information: ServiceInformationBase) -> bool:
            return information.name.find(PIH.SERVICE.EVENT_LISTENER_NAME_PREFIX) == 0
        
        @staticmethod
        def is_service_as_support(information: ServiceInformationBase) -> bool:
            return information.name.find(PIH.SERVICE.SUPPORT_NAME_PREFIX) == 0

        @staticmethod
        def get_information(role_or_information: ServiceRoles | ServiceInformationBase, cached: bool = True) -> ServiceInformation | None:
            service_information: ServiceInformationBase | None = ServiceRoles.description(
                role_or_information)
            #if PIH.SERVICE.is_service_as_listener(service_information):
            #    return RPC.ping(service_information)
            if DataTool.is_empty(PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP):
                PIH.SERVICE.ADMIN.request_for_service_information_list()    
            service_information = PIH.SERVICE.get_information_from_cache(
                service_information)
            if cached:
                return service_information
            if DataTool.is_empty(service_information):
                return None
            return RPC.ping(service_information)
        
        @staticmethod
        def get_information_or_description(role_or_information: ServiceRoles | ServiceInformationBase) -> ServiceInformation | ServiceDescription:
            return PIH.SERVICE.get_information(role_or_information) or ServiceRoles.description(role_or_information)
        
        @staticmethod
        def get_information_from_cache(role_or_information: ServiceRoles | ServiceInformationBase) -> ServiceInformation | None:
            description: ServiceDescription = ServiceRoles.description(role_or_information)
            return PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP[description] if description in PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP else None
        
        @staticmethod
        def description_by_command(value: ServiceCommands) -> ServiceDescription | None:
            if DataTool.is_empty(PIH.SERVICE.command_map):
                PIH.SERVICE.command_map = {}
                for service_role_item in ServiceRoles:
                    description: ServiceDescription = ServiceRoles.description(service_role_item)
                    for service_command_item in description.commands:
                        service_command_item: ServiceCommands = service_command_item
                        PIH.SERVICE.command_map[service_command_item.name] = description
            return PIH.SERVICE.command_map[value.name] if value.name in PIH.SERVICE.command_map else None

        @staticmethod
        def get_host(role_or_information: ServiceRoles | ServiceInformationBase) -> str:
            information: ServiceInformationBase | None = ServiceRoles.description(role_or_information)
            if isinstance(information, ServiceDescription):
                if not DataTool.is_empty(information.port):
                    return PIH.DATA.FORMAT.donain(information.host)
            return PIH.DATA.FORMAT.donain((PIH.SERVICE.get_information(role_or_information) or ServiceInformationBase()).host or information.host)

        @staticmethod
        def get_port(role_or_information: ServiceRoles | ServiceInformationBase) -> int | None:
            information: ServiceInformationBase | None = ServiceRoles.description(role_or_information)
            if isinstance(information, ServiceDescription):
                if not DataTool.is_empty(information.port):
                    return information.port
            return (PIH.SERVICE.get_information(role_or_information) or ServiceInformationBase()).port or information.port
        
        @staticmethod
        def create_port(role_or_information: ServiceRoles | ServiceInformationBase) -> int: 
            return ServiceRoles.description(role_or_information).port or NetworkTool.next_free_port()
        
        @staticmethod
        def create_host(role_or_information: ServiceRoles | ServiceInformationBase) -> int: 
            description: ServiceDescription = ServiceRoles.description(role_or_information)
            return PIH.OS.host() if description.isolated or DataTool.is_empty(description.host) else description.host

    class PATH(PATHS, PathTool):

        DIRECTORY_INFO_SECTION: str = "directory_info"

        @staticmethod
        def path(value: str) -> str:
            return value.replace("\\", "/").replace("\\\\", "//")

        @staticmethod
        def adapt_if_windows(value: str) -> str:
            return value.replace("/", "\\")

        @staticmethod
        def join(path: str, *paths) -> str:
            return PIH.PATH.path(os.path.join(path, *paths))

        @staticmethod
        def get_modification_time(path: str) -> str:
            return os.path.getmtime(PIH.PATH.adapt_if_linux(path))

        @staticmethod
        def get_creation_time(path: str) -> str:
            return os.path.getctime(PIH.PATH.adapt_if_linux(path))

        @staticmethod
        def adapt_if_linux(path: str) -> str:
            path = PIH.PATH.path(path)
            if PIH.OS.is_linux():
                alias: str = PATH_FACADE.VALUE
                if path.find(alias) == 0:
                    path = path[len(alias):]
                    path = PATHS.FACADE.LINUX_MOUNT_POINT_PATH + path
            return path

        @staticmethod
        def get_command_for_mount_storage_on_linux_host(storage_path: str, linux_mount_point: str, storage_host_user_login: str, storage_host_user_password: str) -> str:
            return f"mount -t cifs {PIH.PATH.convert_for_unix(storage_path)} {linux_mount_point} -o username={storage_host_user_login},password={storage_host_user_password}"

        @staticmethod
        def mount_storage_on_linux_host(linux_host: str, storage_path: str, linux_mount_point: str, storage_host_user_login: str, storage_host_user_password: str) -> None:
            PIH.RESULT.SSH.execute(PIH.PATH.get_command_for_mount_storage_on_linux_host(
                storage_path, linux_mount_point, storage_host_user_login, storage_host_user_password), linux_host, use_sudo=True)
            
        @staticmethod
        def mount_facade_storage_on_linux_host(linux_host: str | None = None) -> bool:
            if PIH.OS.is_linux():
                commnad: str = PIH.PATH.get_command_for_mount_facade_storage_on_linux_host()
                if_else(DataTool.is_none(linux_host),
                        lambda: PIH.EXECUTOR.execute(commnad, True, as_shell=True),
                    lambda: PIH.RESULT.SSH.execute(commnad, linux_host, use_sudo=True)
                )
                return True
            return False
                 
        @staticmethod
        def make_directory_if_not_exists(path: str, host: str | None = None) -> bool:
            command: str = f"mkdir {path}"
            if DataTool.is_none(host):
                return PathTool.make_directory_if_not_exists(path)
            else:
                PIH.RESULT.SSH.execute(command, host, use_sudo=True)
            return True

        @staticmethod
        def get_command_for_mount_facade_storage_on_linux_host() -> str:
            return PIH.PATH.get_command_for_mount_storage_on_linux_host(PATHS.FACADE.STORAGE_PATH(), 
                                                                        PATHS.FACADE.LINUX_MOUNT_POINT_PATH,
                                                                        PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_LOGIN),
                                                                        PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_PASSOWORD))
        @staticmethod
        def get_file_list_by_directory_info(path: str) -> list[str] | None:
            return PIH.PATH.get_file_list(path, DataTool.if_not_empty(PIH.RESULT.DATA_STORAGE.value(PIH.PATH.get_directory_info_name(
                None, PIH.PATH.path(path)), DirectoryInfo(), PIH.PATH.DIRECTORY_INFO_SECTION).data, lambda info: info.last_created_file_timestamp))

        @staticmethod
        def get_directory_info_name(file_path: str | None, directory_path: str | None = None) -> str:
            return j((PIH.PATH.DIRECTORY_INFO_SECTION, (directory_path or PIH.PATH.get_file_directory(file_path))), "_")

        @staticmethod
        def save_timestamp_for_directory_info(path: str) -> None:
            path = PIH.PATH.path(path)
            PIH.ACTION.DATA_STORAGE.value(DirectoryInfo(path, DateTimeTool.now().timestamp()),
                        PIH.PATH.get_directory_info_name(path), PIH.PATH.DIRECTORY_INFO_SECTION)

        @staticmethod
        def get_directory_info(path: str) -> DirectoryInfo | None:
            return PIH.RESULT.DATA_STORAGE.value(PIH.PATH.get_directory_info_name(None, PIH.PATH.path(path)), DirectoryInfo(), PIH.PATH.DIRECTORY_INFO_SECTION).data

        @staticmethod
        def get_host(value: str) -> str:
            return PIH.DATA.FORMAT.host(value, reverse=True)

        @staticmethod
        def resolve(value: str) -> str:
            if value[0] == "{" and value[-1] == "}":
                value = value[1: -1]
            return PathTool.resolve(value, PIH.OS.host())
        
        class QR_CODE:

            @staticmethod
            def polibase_person_card_registry_folder(name: str) -> str:
                name = name.upper()
                return PIH.PATH.join(PATHS.POLIBASE_APP_DATA.PERSON_CARD_REGISTRY_FOLDER, PathTool.replace_prohibited_symbols_from_path_with_symbol(PathTool.add_extension(name, FILE.EXTENSION.PNG)))

            @staticmethod
            def mobile_helper_command(name: str) -> str:
                name = PIH.DATA.FORMAT.mobile_helper_command(name)
                return PIH.PATH.join(PATHS.MOBILE_HELPER.QR_CODE_FOLDER, PathTool.replace_prohibited_symbols_from_path_with_symbol(PathTool.add_extension(name, FILE.EXTENSION.PNG)))

    class DATA(DataTool, StringTool, ListTool, DateTimeTool, EnumTool, FullNameTool):

        @staticmethod
        def translit(value, language_code=None, reversed=False, strict=False):
            return translit(value, language_code, reversed, strict)
        
        class VARIABLE:

            NAME: str = "variable"

            @staticmethod
            def set(name: str, value: Any) -> None:
                PIH.ACTION.DATA_STORAGE.value(value, name, section=PIH.DATA.VARIABLE.NAME)

            @staticmethod
            def find(name: str | None) -> list[StorageValue]:
                return PIH.DATA.MATERIALIZED_RESOURCES.find(name) + PIH.SETTINGS.find(name)

            @staticmethod
            def value(variable_name: str, from_environment: bool = False) -> Any | None:
                variable_handler: Callable[[str], Any] = PIH.OS.environment_variable
                if from_environment:
                    return variable_handler(variable_name)
                return variable_handler(variable_name) or PIH.RESULT.DATA_STORAGE.value(variable_name, None, PIH.DATA.VARIABLE.NAME).data or PIH.DATA.MATERIALIZED_RESOURCES.get_count(variable_name) or PIH.SETTINGS.get(variable_name)

        class ACTIONS:

            @staticmethod
            def get(action_or_name: str | Actions) -> Actions | None:
                action: Actions | None = None if isinstance(action_or_name, str) else action_or_name
                if DataTool.is_none(action):
                    for item in Actions:
                        if item.name == action_or_name or item.value.name == action_or_name or action_or_name in item.value.alias:
                            action = item
                            break
                return action

        class MATERIALIZED_RESOURCES:

            @staticmethod
            def find(value: str | None) -> list[MATERIALIZED_RESOURCES.TYPES]:
                result: list[SETTINGS] = []
                for item in MATERIALIZED_RESOURCES.TYPES:
                    if DataTool.is_none(value) or StringTool.contains(item.name, value) or StringTool.contains(item.value.key_name, value) or StringTool.contains(item.value.description, value):
                        result.append(item)
                return result

            @staticmethod
            def get_count(type: MATERIALIZED_RESOURCES.TYPES | str) -> int:
                return PIH.RESULT.DATA_STORAGE.value(if_else(isinstance(type, str), type, lambda: type.name), None, MATERIALIZED_RESOURCES.NAME).data

            @staticmethod
            def set_count(type: MATERIALIZED_RESOURCES.TYPES, value: int) -> bool:
                return PIH.ACTION.DATA_STORAGE.value(value, type.name, MATERIALIZED_RESOURCES.NAME)

            @staticmethod
            def add_count(type: MATERIALIZED_RESOURCES.TYPES, value: int) -> bool:
                return PIH.ACTION.DATA_STORAGE.value(PIH.DATA.MATERIALIZED_RESOURCES.get_count(type) + value, type.name, MATERIALIZED_RESOURCES.NAME)

        @staticmethod
        def save_base64_as_image(path: str, content: str) -> bool:
            with open(path, "wb") as file:
                file.write(base64.decodebytes(bytes(content, "utf-8")))
                return True 
            return False

        @staticmethod
        def uuid() -> str:
            return str(uuid.uuid4().hex)

        class USER:

            @staticmethod
            def by_login(value: str, active: bool | None = None, cached: bool | None = None) -> User:
                return PIH.RESULT.USER.by_login(value, active, cached).data

            @staticmethod
            def by_name(value: str) -> User:
                return PIH.RESULT.USER.by_name(value).data

        class MARK:

            @staticmethod
            def by_tab_number(value: str) -> User:
                return PIH.RESULT.MARK.by_tab_number(value).data

        class SETTINGS:

            @staticmethod
            def get(value: SETTINGS) -> Any:
                return PIH.RESULT.SETTINGS.get(value).data

        class FILTER:

            @staticmethod
            def symbols_only_in(value: str, check_value: str) -> str:
                return "".join(c for c in value if c in check_value)

            @staticmethod
            def users_by_dn(data: list[User], dn: str) -> list:
                return list(filter(lambda x: x.distinguishedName.find(dn) != -1, data))

        class EXTRACT:

            @staticmethod
            def command_menu(value: str) -> tuple[str, list[CommandMenuItem]]:
                result: list[CommandMenuItem] = []
                fields: list[str] = [name for _, name, _, _ in Formatter().parse(value) if name]
                for field_item in fields:
                    index_start: int = field_item.find("\"menu\"")
                    if index_start != -1:
                        index_start = value.find("\"menu\":")
                        index_end: int = value.find("]}") + 2
                        index_start -= 1
                        manu_text: str = value[index_start: index_end]
                        value = value[0: index_start] + value[index_end: len(value) - 1]
                        menu_json = json.loads(manu_text)
                        for menu_json_item in menu_json["menu"]:
                            result.append(CommandMenuItem(menu_json_item["command"], menu_json_item["label"]))
                return value, result

            @staticmethod
            def new_mail_message(value: dict) -> NewMailMessage:
                return DataTool.fill_data_from_source(NewMailMessage(), value)

            @staticmethod
            def mailbox_info(value: dict | None) -> MailboxInfo | None:
                if DataTool.is_none(value):
                    return None
                result: MailboxInfo = DataTool.fill_data_from_source(MailboxInfo(), value)
                result.timestamp = DateTimeTool.datetime_from_string(result.timestamp)
                return result

            @staticmethod
            def polibase_person(value: dict) -> PolibasePerson:
                polibase_person: PolibasePerson = DataTool.fill_data_from_source(PolibasePerson(), value)
                polibase_person.Birth = DateTimeTool.datetime_from_string(polibase_person.Birth)
                polibase_person.registrationDate = DateTimeTool.datetime_from_string(polibase_person.registrationDate )
                return polibase_person

            @staticmethod
            def datetime(value: str | None, format: str) -> datetime | None:
                if DataTool.is_empty(value):
                    return None
                result: datetime | None = None
                try:
                    result = DateTimeTool.datetime_from_string(value, format)
                except ValueError as error:
                    date_extract_pattern: str = "[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}"
                    date_list: list[str] = re.findall(date_extract_pattern, value)
                    if not DataTool.is_empty(date_list):
                        result = PIH.DATA.EXTRACT.datetime(date_list[0], format)
                return result
            
            @staticmethod
            def boolean(value: int | str | None) -> bool | None:
                if DataTool.is_empty(value):
                    return False
                if isinstance(value, str):
                    value =  value.lower()
                    if value in ["1", "yes", "да"]:
                        return True
                    if value in ["0", "no", "нет"]:
                        return True
                if isinstance(value, int):
                    if value == 1:
                        return True
                    if value == 0:
                        return False
                return None
            
            @staticmethod
            def service_information(value: dict | ServiceInformation) -> ServiceInformation:
                service_information: ServiceInformation = DataTool.fill_data_from_source(ServiceInformation(), value) if isinstance(value, dict) else value
                if not DataTool.is_empty(service_information.subscribtions):
                    service_information.subscribtions = DataTool.fill_data_from_list_source(Subscribtion, service_information.subscribtions)   
                return service_information

            @staticmethod
            def wappi_telephone_number(value: Any) -> str:
                if isinstance(value, str):
                    return PIH.DATA.FORMAT.telephone_number(value.split(CONST.MESSAGE.WHATSAPP.WAPPI.CONTACT_SUFFIX)[0])
                if isinstance(value, dict):
                    return PIH.DATA.FORMAT.telephone_number(value["user"])
                
            class EVENT:

                @staticmethod
                def parameter(event_ds: EventDS | None, param_item: ParamItem) -> Any | None:
                    if DataTool.is_none(event_ds):
                        return None
                    event: Events = EnumTool.get(Events, event_ds.name)
                    event_description: EventDescription = EnumTool.get(event)
                    param_index: int = event_description.params.index(param_item)
                    if param_index == -1 or param_index >= len(event_ds.parameters):
                        return None
                    for index, name in enumerate(event_ds.parameters):
                        if index == param_index:
                            return event_ds.parameters[name]

                @staticmethod
                def whatsapp_message(parameter_list: ParameterList) -> WhatsAppMessage | None:
                    allow: bool = PIH.DATA.EXTRACT.subscribtion_result(parameter_list).result
                    message: WhatsAppMessage | None = None
                    if allow:
                        event, parameters = PIH.DATA.EXTRACT.EVENT.with_parameters(parameter_list)
                        if event == Events.WHATSAPP_MESSAGE_RECEIVED:
                            message = DataTool.fill_data_from_source(WhatsAppMessage(), parameters[0])
                            if not DataTool.is_empty(message.message):
                                message.message = urllib.parse.unquote(message.message)
                    return message
                
                @staticmethod
                def action(parameters: dict[str, Any]) -> ActionWasDone:
                    action: ActionWasDone = DataTool.fill_data_from_source(ActionWasDone(), PIH.EVENT.get_parameter(Events.ACTION_WAS_DONE, parameters), copy_by_index=True)
                    action.action = EnumTool.get(Actions, action.action)
                    return action
                
                @staticmethod
                def get(parameter_list: ParameterList) -> Events:
                    event_content: Any | list[Any] = parameter_list.list[0] if PIH.DATA.CHECK.has_subscribtion_result(parameter_list) else parameter_list.list
                    return EnumTool.get(Events, event_content[0])
                
                @staticmethod
                def with_parameters(parameter_list: ParameterList) -> tuple[Events, list[Any]]:
                    event_data: Any | list[Any] = parameter_list.list[0] if PIH.DATA.CHECK.has_subscribtion_result(parameter_list) else parameter_list.list
                    event: Events = EnumTool.get(Events, event_data[0])
                    in_parameters: dict[str, Any] = event_data[1]
                    out_parameters: list[Any] = []
                    if not DataTool.is_empty(event.value.params):
                        for event_parameters_description in event.value.params:
                            event_parameters_description: ParamItem = event_parameters_description
                            if event_parameters_description.optional:
                                if DataTool.is_in(in_parameters, event_parameters_description.name):
                                    out_parameters.append(in_parameters[event_parameters_description.name])
                                else:
                                    out_parameters.append(None)
                            else:
                                out_parameters.append(in_parameters[event_parameters_description.name])
                    return event, out_parameters
                
            @staticmethod
            def subscribtion_result(parameter_list: ParameterList) -> SubscribtionResult | None:
                def extractor() -> SubscriberInformation:
                    result: SubscribtionResult = DataTool.fill_data_from_source(SubscribtionResult(), parameter_list.list[-1])
                    if isinstance(result.result, str):
                        try:
                            result.result = DataTool.rpc_unrepresent(result.result)
                        except Exception as error:
                            pass
                    return result                                               
                return None if DataTool.is_empty(parameter_list.list) or not PIH.DATA.CHECK.has_subscribtion_result(parameter_list) else extractor()
            
            @staticmethod
            def parameter_list(parameter_list: ParameterList) -> ParameterList:
                return ParameterList(parameter_list.get()) if PIH.DATA.CHECK.has_subscribtion_result(parameter_list) else parameter_list

            @staticmethod
            def email(value: str) -> str | None:
                emails: list[str] = re.findall(
                    r"[A-Za-z0-9_%+-.]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}", value)
                if len(emails) > 0:
                    return emails[0]
                return None
            
            @staticmethod
            def float(value: str) -> float:
                if not DataTool.is_empty(value):
                    floats: list[str] = re.findall(
                        r"\d+[\.\,]*\d+", value)
                    if len(floats) > 0:
                        return float(floats[0].replace(",", "."))
                return None

            @staticmethod
            def decimal(value: str, min: int = None, max: int = None) -> int | None:
                value = value.strip()
                result: int | None = None
                numbers: list[str] = re.findall(r"\d+", value)
                if len(numbers) > 0:
                    result = int(numbers[0])
                    if min is not None and max is not None and (result < min or result > max):
                        result = None
                return result

            @staticmethod
            def variables(value: str | None) -> list[str] | None:
                if DataTool.is_none(value):
                    return None
                fields: list[str] | None = [name for _, name, _, _ in Formatter().parse(value) if name]
                if DataTool.is_empty(fields):
                    return None
                return fields

            @staticmethod
            def parameter(object: dict, name: str) -> str:
                return object[name] if name in object else ""

            @staticmethod
            def tab_number(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.TAB_NUMBER)

            @staticmethod
            def telephone(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.TELEPHONE_NUMBER)

            @staticmethod
            def login(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.LOGIN)

            @staticmethod
            def name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.NAME)

            @staticmethod
            def dn(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def group_name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_NAME)

            @staticmethod
            def group_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_ID)

            @staticmethod
            def as_full_name(mark_object: dict) -> FullName:
                return FullNameTool.fullname_from_string(PIH.DATA.EXTRACT.full_name(mark_object))

            @staticmethod
            def full_name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.FULL_NAME)

            @staticmethod
            def person_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.PERSON_ID)

            @staticmethod
            def mark_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.MARK_ID)

            @staticmethod
            def description(object: dict) -> str:
                result = PIH.DATA.EXTRACT.parameter(
                    object, FIELD_NAME_COLLECTION.DESCRIPTION)
                if isinstance(result, tuple) or isinstance(result, list):
                    return result[0]

            @staticmethod
            def container_dn(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.container_dn_from_dn(PIH.DATA.EXTRACT.dn(user_object))

            @staticmethod
            def container_dn_from_dn(dn: str) -> str:
                return ",".join(dn.split(",")[1:])
            
        class CONVERT:

            @staticmethod
            def settings_to_datetime(item: SETTINGS, format: str = CONST.SECONDLESS_TIME_FORMAT) -> datetime | list[datetime]:
                settings_value: str | list[str] = PIH.SETTINGS.get(item)
                return  PIH.DATA.CONVERT.settings_to_datetime_list(item, format) if isinstance(settings_value, list) else DateTimeTool.datetime_from_string(settings_value, format)
            
            @staticmethod
            def settings_to_datetime_list(item: SETTINGS, format: str = CONST.SECONDLESS_TIME_FORMAT) -> list[datetime]:
                return list(map(lambda item: DateTimeTool.datetime_from_string(item, format), PIH.SETTINGS.get(item)))

            @staticmethod
            def file_to_base64(path: str) -> str | None:
                path = PIH.PATH.adapt_if_linux(path)
                while True:
                    try:
                        with open(path, "rb") as file:
                            return PIH.DATA.CONVERT.bytes_to_base64(file.read())
                    except Exception:
                        pass
                return None
                
            @staticmethod
            def bytes_to_base64(value: bytes) -> str:
                return PIH.DATA.CONVERT.bytes_to_string(PIH.DATA.CONVERT.to_base64(value))
            
            @staticmethod
            def to_base64(value: Any) -> str:
                return base64.b64encode(value)

            @staticmethod 
            def bytes_to_string(value: bytes) -> str:
                return value.decode("utf-8")
            
        class STATISTICS:

            NAME: str = "statistics"

            @staticmethod
            def by_name(value: str) -> TimeSeriesStatistics | None:
                def is_equal(value: MATERIALIZED_RESOURCES.TYPES, name: str) -> bool:
                    return EnumTool.get(value).key_name == name or value.name == name
                if is_equal(MATERIALIZED_RESOURCES.TYPES.CHILLER_FILTER, value):
                    return PIH.DATA.STATISTICS.for_chiller_filter()
                return None

            @staticmethod
            def for_chiller_filter() -> TimeSeriesStatistics | None:
                events_result: Result[list[EventDS]] = PIH.RESULT.EVENTS.get(*PIH.EVENT.BUILDER.action_was_done(Actions.CHILLER_FILTER_CHANGING))
                if ResultTool.is_empty(events_result):
                    return None
                datetime_list: list[datetime] = ResultTool.map(events_result, lambda event: event.timestamp).data
                distance: list[timedelta] = []
                for index, _ in enumerate(datetime_list):
                    if index == len(datetime_list) - 1:
                        break
                    value: timedelta = datetime_list[index + 1] - datetime_list[index]
                    distance.append(int(value.total_seconds()))
                return TimeSeriesStatistics(len(events_result), datetime_list, distance, min(distance), max(distance), int(sum(distance) / len(distance)))
            
        class CHECK:

            @staticmethod
            def polibase_person_has_new_barcode_format(polibase_person: PolibasePerson) -> bool:
                return not (DataTool.is_empty(polibase_person.barcode) or polibase_person.barcode.find(CONST.POLIBASE.BARCODE.NEW_PREFIX) == -1)

            @staticmethod
            def polibase_person_barcode(value: BarcodeInformation) -> bool:
                data: int | None = None
                try:
                    data = int(value.data)
                except ValueError:
                    return False
                return value.type in CONST.POLIBASE.BARCODE.SUPPORT_FORMATS and PIH.CHECK.POLIBASE.person_pin(data)

            @staticmethod
            def has_subscribtion_result(parameter_list: ParameterList) -> bool:
                return len(parameter_list.list) == 2 and DataTool.fill_data_from_source(SubscribtionResult(), parameter_list.list[-1]).checker
            
            @staticmethod
            def by_secondless_time(value_datetime: datetime, value_str: str | None) -> bool:
                return False if DataTool.is_empty(value_str) else DateTimeTool.is_equal_by_time(value_datetime, DateTimeTool.datetime_from_string(value_str, CONST.SECONDLESS_TIME_FORMAT)) 
            
            @staticmethod
            def empty(value) -> bool:
                return DataTool.is_empty(value)

            @staticmethod
            def decimal(value: int | str | None)-> bool:
                return DataTool.is_not_none(value) and (isinstance(value, int) or (isinstance(value, str) and value.isdecimal()))

            class INDICATIONS:

                @staticmethod
                def chiller_value_actual(value_container: ChillerIndicationsValueContainer) -> bool:
                    return (DateTimeTool.now() - DateTimeTool.datetime_from_string(value_container.timestamp, CONST.ISO_DATETIME_FORMAT)).total_seconds() // 60 <= INDICATIONS.CHILLER.ACTUAL_VALUES_TIME_DELTA_IN_MINUTES

                @staticmethod
                def chiller_value_valid(value: ChillerIndicationsValue) -> bool:
                    return not DataTool.is_empty(value.temperature)

        class FORMAT:

            class BACKUP:
    
                SPLITTER: str = "::"

                @staticmethod
                def job_full_name(name: str, source: str, destination: str) -> str:
                    return PIH.DATA.FORMAT.BACKUP.SPLITTER.join([source, destination, name])
                
                @staticmethod
                def job_status_name(name: str, source: str, destination: str) -> str:
                    return PIH.DATA.FORMAT.BACKUP.SPLITTER.join(["robocopy_job_status", PIH.DATA.FORMAT.BACKUP.job_full_name(name, source, destination)])


            @staticmethod
            def donain(value: str) -> str:
                return if_else(value.endswith(AD.DOMAIN_DNS), value, lambda: j((value, AD.DOMAIN_DNS), "."))

            @staticmethod
            def variable(value: str | None, from_environment: bool = False) -> str | None:
                if DataTool.is_none(value):
                    return value
                variable_name_list: list[str] | None = PIH.DATA.EXTRACT.variables(value)
                if DataTool.is_empty(variable_name_list):
                    return None
                variable_name: str = variable_name_list[0]
                return PIH.DATA.VARIABLE.value(variable_name, from_environment)

            @staticmethod
            def statistics(type: MATERIALIZED_RESOURCES.TYPES) -> str | None:
                statistics: TimeSeriesStatistics | None = PIH.DATA.STATISTICS.by_name(type.name)
                if DataTool.is_none(statistics):
                    return None
                count: int = PIH.DATA.MATERIALIZED_RESOURCES.get_count(type)
                def to_days(value: int) -> int:
                    return int(DateTimeTool.seconds_to_days(value))
                return j(
                    (
                        "Остаток по времени (дней):",
                        f" {CONST.VISUAL.BULLET} Максимально: {count * to_days(statistics.max)}",
                        f" {CONST.VISUAL.BULLET} Минимально: {count * to_days(statistics.min)}",
                        f" {CONST.VISUAL.BULLET} В среднем: {count * to_days(statistics.avg)}",
                    ),
                    "\n"
                )

            @staticmethod
            def yes_no(value: bool, symbolic: bool = False) -> str:
                c: Callable[[bool, Callable[[None], Any | None] | Any, Callable[[None], Any | None] | Any], Any] = DataTool.check
                return c(value, c(symbolic, CONST.VISUAL.YES, "Да"), c(symbolic, CONST.VISUAL.NO, "Нет"))

            @staticmethod
            def size(value: int) -> str:
                return str(int(value / 1024 / 1024 / 1024 )) + " Гб"


            @staticmethod
            def format(value: str) -> str:
                fields: list[str] = [name for _, name, _, _ in Formatter().parse(value) if name]
                #my_fields: list[str] = DataTool.to_list(DATA.FORMATTER)
                formatter: dict[str, str] = {}
                for field_item in fields:
                    #if field_item in my_fields:
                    formatter[field_item] = PIH.DATA.FORMAT.by_formatter_name(field_item, None)
                if DataTool.is_empty(formatter):
                    return value
                return value.format(**formatter)

            @staticmethod
            def index(value: int) -> str:
                return str(value + 1) if value > 0 else ""
                      
            @staticmethod
            def user_principal_name(login: str) -> str:
                return "@".join((login, AD.DOMAIN_MAIN))

            @staticmethod
            def as_string(value: Any, escaped_string: bool = False, mapper: Callable[[Any], str] | None = None) -> str:
                result: str | None = None
                if isinstance(value, Enum):
                    result = value.name
                else:
                    result = str(value)
                if escaped_string:
                    if isinstance(value, (str, datetime, Enum)):
                        result = f"'{result}'"
                    if isinstance(value, dict):
                        result = f"'{DataTool.rpc_represent(value, False)}'"
                return DataTool.check_not_none(mapper, lambda: mapper(result), result)
                
            @staticmethod
            def host(value: str, reverse: bool = False) -> str:
                host_start: str = r"\\"
                if reverse:
                    return ListTool.not_empty_items(j(j(value.replace("\\", ":")).replace("/", ":")).split(":"))[0]
                return ("" if value.startswith(host_start) else host_start) + value 

            @staticmethod
            def get_chiller_indications_value_image_name(datetime: datetime | str) -> str:
                if isinstance(datetime, str):
                    datetime = PIH.DATA.datetime_from_string(datetime, CONST.ISO_DATETIME_FORMAT)
                return PIH.PATH.replace_prohibited_symbols_from_path_with_symbol(PIH.DATA.datetime_to_string(datetime, CONST.DATETIME_FORMAT))

            @staticmethod
            def by_formatter_name(value: Enum | str, data: Any | None) -> str | None:
                if isinstance(value, str):
                    value = EnumTool.get_by_value(DATA.FORMATTER, value) or value
                if isinstance(value, str):
                    name: str = j((PIH.DATA.STATISTICS.NAME, "_"))
                    index: int = value.lower().find(name)
                    if index != -1:
                        index += len(name)
                        type: MATERIALIZED_RESOURCES.TYPES | None = EnumTool.get_by_value_or_key(MATERIALIZED_RESOURCES.TYPES, value[index: ].upper())
                        if DataTool.is_none(type):
                            return None
                        return PIH.DATA.FORMAT.statistics(type)
                if isinstance(value, str):
                    return PIH.DATA.VARIABLE.value(value)
                if value == DATA.FORMATTER.MY_DATETIME:
                    return PIH.DATA.FORMAT.datetime(data)
                if value == DATA.FORMATTER.MY_DATE:
                    return PIH.DATA.FORMAT.date(data)
                if value == DATA.FORMATTER.CHILLER_FILTER_COUNT:
                    return str(PIH.DATA.MATERIALIZED_RESOURCES.get_count(MATERIALIZED_RESOURCES.TYPES.CHILLER_FILTER))
                if value == DATA.FORMATTER.CHILLER_INDICATIONS_VALUE_INDICATORS:
                    result_list: list[str] = [] 
                    for index in range(len(INDICATIONS.CHILLER.INDICATOR_NAME)):
                        if BM.has_index(data, index):
                            result_list.append(f"{CONST.VISUAL.BULLET} {INDICATIONS.CHILLER.INDICATOR_NAME[index]}")
                    return "\n".join(("\n", "\n".join(result_list), ""))
                return None

            @staticmethod
            def polibase_person_card_registry_folder(value: str) -> str:         
                return value.upper()

            @staticmethod
            def mobile_helper_command(value: str) -> str:
                return value.lower()

            @staticmethod
            def mobile_helper_qr_code_text(value: str) -> str:
                return PIH.DATA.FORMAT.whatsapp_send_message_to(PIH.DATA.FORMAT.telephone_number_international(PIH.DATA.TELEPHONE_NUMBER.it_administrator()), f"{PIH.NAME} {value}".replace(" ", "+"))
            
            @staticmethod
            def whatsapp_send_message_to(telephone_number: str, message: str) -> str:
                return CONST.MESSAGE.WHATSAPP.SEND_MESSAGE_TO_TEMPLATE.format(telephone_number, message)

            @staticmethod
            def string(value: str | None) -> str:
                return ("" or value).lower().replace('"', '')
            
            @staticmethod
            def telephone_number(value: str, prefix: str = CONST.TELEPHONE_NUMBER_PREFIX) -> str:
                if DataTool.is_empty(value) or value.endswith(CONST.MESSAGE.WHATSAPP.GROUP_SUFFIX):
                    return value
                if prefix != CONST.TELEPHONE_NUMBER_PREFIX:
                    value = value[value.find(prefix):]
                src_value: str = value
                if not DataTool.is_empty(value):
                    value = re.sub("[\-\(\) ]", "", value)
                    if value.startswith(prefix):
                        value = value[len(prefix):]
                    if len(value) == 0:
                        return src_value
                    value = prefix + \
                        (value[1:] if (value[0] ==
                         "8" or value[0] == CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX) else value)
                    pattern: str = ("^\\" if prefix[0] == "+" else "^") + prefix + "[0-9]{10}"
                    matcher: re.Match = re.match(pattern, value)
                    if matcher is not None:
                        return matcher.group(0)
                    else:
                        return src_value
                else:
                    return src_value

            @staticmethod
            def telephone_number_international(value: str) -> str:
                return PIH.DATA.FORMAT.telephone_number(value, CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX)

            @staticmethod
            def email(value: str, add_default_domain: bool = False, remove_restricted_symbols: bool = False) -> str:
                if add_default_domain and value.find("@") == -1:
                    return PIH.DATA.FORMAT.email("@".join((value, CONST.SITE_ADDRESS)))
                if remove_restricted_symbols:
                    for char in "\"(),:;<>[\\] ":
                        value = value.replace(char, "")
                return value#.lower()

            @staticmethod
            def name(value: str, remove_non_alpha: bool = False, name_part_minimal_length: int | None = None) -> str:
                name_part_list: list[str] = list(
                    filter(lambda item: len(item) > (0 if name_part_minimal_length is None else name_part_minimal_length - 1), value.split(" ")))
                if len(name_part_list) == 1:
                    value = value.lower()
                    value = re.sub("[^а-я]+", "",
                                   value) if remove_non_alpha else value
                    if len(value) > 1:
                        value = StringTool.capitalize(value)
                    return value
                return " ".join(list(map(lambda item: PIH.DATA.FORMAT.name(item, remove_non_alpha), name_part_list)))

            @staticmethod
            def location_list(value: str, remove_first: bool = True, reversed: bool = True) -> list[str]:
                location_list: list[str] = value.split(
                    ",")[1 if remove_first else 0:]
                if reversed:
                    location_list.reverse()
                return list(map(
                    lambda item: item.split("=")[-1], location_list))

            @staticmethod
            def get_user_account_control_values(uac: int) -> list[str]:
                result: list[str] = []
                for count, item in enumerate(AD.USER_ACCOUNT_CONTROL):
                    if (pow(2, count) & uac) != 0:
                        result.append(item)
                return result
            
            @staticmethod
            def description(value: str) -> str:
                return (value.split("|")[0]).rstrip()
             
            @staticmethod
            def to_date(value: str) -> str:
                value = value.strip()
                value = value.replace("/", CONST.DATE_PART_DELIMITER)
                value = value.replace(",", CONST.DATE_PART_DELIMITER)
                value = value.replace(" ", CONST.DATE_PART_DELIMITER)
                return value

            @staticmethod
            def date(iso_datetime_value: str | datetime) -> str:
                return DateTimeTool.datetime_to_string(datetime.fromisoformat(iso_datetime_value) if isinstance(iso_datetime_value, str) else iso_datetime_value, CONST.DATE_FORMAT)

            @staticmethod
            def datetime(iso_datetime_value: str | datetime) -> str:
                return DateTimeTool.datetime_to_string(iso_datetime_value if isinstance(iso_datetime_value, datetime) else datetime.fromisoformat(iso_datetime_value), CONST.DATETIME_FORMAT)
          

        class TELEPHONE_NUMBER:

            wappi_profile_to_telephone_number_map: dict = None

            @staticmethod
            def all(active: bool = True) -> list[str]:
                def filter_function(user: User) -> str:
                    return user.telephoneNumber is not None
                def map_function(user: User) -> str:
                    return PIH.DATA.FORMAT.telephone_number(user.telephoneNumber)
                return ResultTool.map(ResultTool.filter(PIH.RESULT.USER.by_name(AD.SEARCH_ALL_PATTERN, active=active), filter_function), map_function).data

            @staticmethod
            def it_administrator() -> str:
                return PIH.DATA.TELEPHONE_NUMBER.by_login(PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_LOGIN))

            @staticmethod
            def call_centre_administrator() -> str:
                return PIH.DATA.TELEPHONE_NUMBER.by_login(AD.USER.CALL_CENTRE_ADMINISTRATOR)

            @staticmethod
            def marketer() -> str:
                return PIH.DATA.TELEPHONE_NUMBER.by_login(AD.USER.MARKETER)

            @staticmethod
            def for_wappi(value: Any) -> str | None:
                WP = CONST.MESSAGE.WHATSAPP.WAPPI.Profiles
                value = EnumTool.get_by_value_or_key(WP, value)
                map: dict = PIH.DATA.TELEPHONE_NUMBER.wappi_profile_to_telephone_number_map
                if DataTool.is_none(map):
                    map = {
                        WP.CALL_CENTRE: PIH.DATA.TELEPHONE_NUMBER.call_centre_administrator(),
                        WP.IT: PIH.DATA.TELEPHONE_NUMBER.it_administrator(),
                        WP.MARKETER: PIH.DATA.TELEPHONE_NUMBER.marketer(),
                    }
                    PIH.DATA.TELEPHONE_NUMBER.wappi_profile_to_telephone_number_map = map
                return DataTool.if_is_in(map, value)

            @staticmethod
            def by_login(value: str, format: bool = True, active: bool = True, cached: bool = True) -> str:
                result: str = PIH.DATA.USER.by_login(value, active, cached).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            @staticmethod
            def by_workstation_name(value: str) -> str:
                workstation: Workstation = PIH.RESULT.WORKSTATION.by_name(value).data
                return PIH.DATA.TELEPHONE_NUMBER.by_login(workstation.samAccountName)

            @staticmethod
            def by_mark_tab_number(value: str, format: bool = True) -> str:
                result: str = PIH.DATA.MARK.by_tab_number(
                    value).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            @staticmethod
            def by_polibase_person_pin(value: int, format: bool = True) -> bool:
                result: str = PIH.DATA.POLIBASE.person_by_pin(
                    value).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            @staticmethod
            def by_full_name(value: Any, format: bool = True) -> str:
                value_string: str | None = None
                if isinstance(value, str):
                    value_string = value
                    value = FullNameTool.fullname_from_string(value)
                else:
                    value_string = FullNameTool.fullname_to_string(value)
                telephone_number: str = PIH.RESULT.MARK.by_full_name(
                    value_string, True).data.telephoneNumber
                if PIH.CHECK.telephone_number(telephone_number):
                    return PIH.DATA.FORMAT.telephone_number(telephone_number) if format else telephone_number
                telephone_number = PIH.RESULT.USER.by_full_name(
                    value_string, True).data.telephoneNumber
                if PIH.CHECK.telephone_number(telephone_number):
                    return PIH.DATA.FORMAT.telephone_number(telephone_number) if format else telephone_number
                details: str = f"Телефон для {value_string} не найден"
                raise NotFound(details)

        class POLIBASE:

            @staticmethod
            def person_by_pin(value: int, test: bool | None = None) -> PolibasePerson:
                return PIH.RESULT.POLIBASE.person_by_pin(value, test).data

            @staticmethod
            def duplicate_persons_by_person(person: PolibasePerson, check_for_birth: bool = True) -> list[PolibasePerson]:
                def check_function(check_person: PolibasePerson) -> bool:
                    return check_person.pin != person.pin and (not check_for_birth or check_person.Birth == person.Birth)
                return ResultTool.get_first_item(ResultTool.filter(PIH.RESULT.POLIBASE.persons_by_full_name(person.FullName), lambda item: check_function(item)))
            
            @staticmethod
            def unique_by_telephone(value: str) -> PolibasePerson:
                value = PIH.DATA.FORMAT.telephone_number(value)
                def check_function(check_person: PolibasePerson) -> bool:
                    return PIH.DATA.FORMAT.telephone_number(check_person.telephoneNumber) == value
                return ResultTool.get_first_item(ResultTool.filter(PIH.RESULT.POLIBASE.person_by_telephone_number(value), lambda item: check_function(item)))

            @staticmethod
            def duplicate_persons_by_person_pin(value: int, check_birth: bool = True) -> list[PolibasePerson]:
                try:
                    return PIH.DATA.POLIBASE.duplicate_persons_by_person(PIH.RESULT.POLIBASE.person_by_pin(value).data, check_birth)
                except NotFound as error:
                    return None

            @staticmethod
            def sort_person_list_by_pin(value: list[PolibasePerson] | PolibasePerson | None = None) -> list[PolibasePerson] | int | Callable[[PolibasePerson], int]:
                def sort_function(person: PolibasePerson) -> int:
                    return person.pin
                if isinstance(value, PolibasePerson):
                    return sort_function(value)
                if DataTool.is_empty(value):
                    return sort_function
                value.sort(key=sort_function)
                return value

    class OS:

        @staticmethod
        def stop_windows_service(name: str, workstation_name: str) -> bool | None:
            accessable: bool | None = PIH.CHECK.WORKSTATION.accessibility(workstation_name)
            if DataTool.is_none(accessable):
                return None
            return PIH.EXECUTOR.stop_windows_service(name, workstation_name)      
        
        @staticmethod
        def start_windows_service(name: str, workstation_name: str) -> bool | None:
            accessable: bool | None = PIH.CHECK.WORKSTATION.accessibility(workstation_name)
            if DataTool.is_none(accessable):
                return None
            return PIH.EXECUTOR.start_windows_service(name, workstation_name)      
        
        @staticmethod
        def start_windows_service_if_stopped(name: str, workstation_name: str) -> bool | None:
            windows_service_information = name, workstation_name
            if not PIH.CHECK.WORKSTATION.windows_service_running(*windows_service_information):
                return PIH.OS.start_windows_service(*windows_service_information)
            return None

        @staticmethod
        def host_is_local(value: str | None) -> bool:
            return DataTool.is_empty(value) or socket.gethostbyname(
                socket.gethostname()) == socket.gethostbyname(value)

        @staticmethod
        def make_sudo(command: str, password: str) -> str:
            return f"echo -e '{password}\n' | sudo -S " + command

        @staticmethod
        def python_path(host: str | None = None) -> str | None:
            return PIH.EXECUTOR.python_path(host)

        @staticmethod
        def python_version(host: str | None = None) -> str:
            return PIH.EXECUTOR.python_version(host)

        @staticmethod
        def name() -> str:
            return platform.system()

        @staticmethod
        def is_linux() -> bool:
            return PIH.OS.name() == "Linux"

        @staticmethod
        def get_login() -> str:
            return os.getlogin()

        @staticmethod
        def host() -> str:
            return platform.node()

        @staticmethod
        def pid() -> int:
            return os.getppid()

        @staticmethod
        def environment_variable(name: str) -> str:
            return os.getenv(name)
        
        @staticmethod
        def os_name() -> str:
            return PIH.OS.environment_variable("OS")

        @staticmethod
        def domain_dns() -> str:
            return PIH.OS.environment_variable("USERDNSDOMAIN")
        
        @staticmethod
        def domain() -> str:
            return PIH.OS.environment_variable("USERDOMAIN")

        @staticmethod
        def kill_process(name_or_pid: str | int, via_standart_tools: bool = True, show_output: bool = False) -> bool:
            return PIH.EXECUTOR.kill_process(name_or_pid, None, via_standart_tools, show_output)


    class RESULT(ResultTool):

        class EVENTS:

           @staticmethod
           def get(value: Events, parameters: tuple[Any] | None = None) -> Result[list[EventDS]]:
                def extractor(data: Any) -> EventDS:
                    result: EventDS = DataTool.fill_data_from_source(EventDS(), data)
                    #from json string to python object
                    result.parameters = DataTool.rpc_unrepresent(result.parameters)
                    if isinstance(result.timestamp, str):
                        result.timestamp = DateTimeTool.datetime_from_string(result.timestamp)
                    return result
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_event, EventDS(value.name, PIH.EVENT.BUILDER.create_parameters_map(value, parameters, check_for_parameters_count = False))), extractor)

        class NOTES:
    
            @staticmethod
            def by_name(name: str) -> Result[Note]:
                id: str = DataTool.rpc_unrepresent(PIH.SERVICE.call_command(
                    ServiceCommands.get_gkeep_item_id, (name, )))
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_note, id), Note)

        class SSH:

            @staticmethod
            def execute(command: str, host: str, username: str | None = None, password: str | None = None, use_sudo: bool = False) -> Result[list[str]]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.execute_ssh_command, (command, host, username, password, use_sudo)))

            @staticmethod
            def get_certificate_information(host: str, username: str | None = None, password: str | None = None) -> Result[str | None]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_certificate_information, (host, username, password)))
            
            @staticmethod
            def get_unix_free_space_information_by_drive_name(drive_name: str, host: str, username: str | None = None, password: str | None = None) -> Result[str | None]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_unix_free_space_information_by_drive_name, (drive_name, host, username, password)))

        class DATA_STORAGE:

            @staticmethod
            def value(name: str, class_type_holder: T | Callable[[Any], T] | None, section: str | None = None) -> Result[T]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_storage_value, (name, section)), class_type_holder)
            
            @staticmethod
            def ogrn(code: str) -> Result[OGRN]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_ogrn_value, (code, )), OGRN)
            
            @staticmethod
            def fms_unit_name(code: str) -> Result[str]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_fms_unit_name, (code, )))

        class MESSAGE:

            class DELAYED:

                @staticmethod
                def get(search_condition: MessageSearchCritery | None = None, take_to_work: bool = False) -> Result[list[DelayedMessageDS]]:
                    return DataTool.to_result(
                        PIH.SERVICE.call_command(ServiceCommands.search_delayed_messages, (search_condition, take_to_work)), DelayedMessageDS)

        class RECOGNIZE:

            @staticmethod
            def recognize_document(file_path: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(
                    ServiceCommands.recognize_document, (file_path, )))

            @staticmethod
            def barcodes_information(file_path: str, get_only_first_barcode: bool = False, log_level: int = 0) -> Result[list[list[BarcodeInformation]]]:
                def extractor(data: list[dict[str, Any]]) -> list[BarcodeInformation]:
                    return list(map(lambda item: DataTool.fill_data_from_source(BarcodeInformation(), item), data))
                return DataTool.to_result(
                        PIH.SERVICE.call_command(ServiceCommands.get_barcode_list_information, (file_path, get_only_first_barcode, log_level)), extractor)

        class RESOURCES:

            @staticmethod
            def get_status_list(checkable_section_list: list[CheckableSections] | None = None, force_update: bool = False, all: bool = False) -> Result[list[ResourceStatus]]:
                def fill_data(data: dict) -> ResourceStatus:
                    return DataTool.fill_data_from_source(SiteResourceStatus() if "check_certificate_status" in data else ResourceStatus(), data)
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_resource_status_list, (None if DataTool.is_empty(checkable_section_list) else list(map(lambda item: item.name, checkable_section_list)), force_update, all)), fill_data)

            @staticmethod
            def get_resource_status_list(force_update: bool = False, all: bool = False) -> Result[list[ResourceStatus]]:
                return PIH.RESULT.RESOURCES.get_status_list([CheckableSections.RESOURCES], force_update, all)

            @staticmethod
            def get_status(checkable_section_list: list[CheckableSections], resource_desription_or_address: Any, force: bool = False) -> ResourceStatus:
                address: str | None = None
                if isinstance(resource_desription_or_address, ResourceDescription):
                    address = resource_desription_or_address.address
                elif isinstance(resource_desription_or_address, str):
                    address = resource_desription_or_address
                if not DataTool.is_empty(address):
                    resource_list: list[ResourceStatus] = PIH.RESULT.RESOURCES.get_status_list(checkable_section_list, force).data
                    for item in resource_list:
                        if item.address == address:
                            return item
                return None
            
            @staticmethod
            def get_resource_status(resource_desription_or_address: Any, force: bool = False) -> ResourceStatus:
                return PIH.RESULT.RESOURCES.get_status([CheckableSections.RESOURCES], resource_desription_or_address, force)
            
        class INDICATIONS:

            @staticmethod
            def last_ct_value_containers(cached: bool, count: int = 1) -> Result[list[CTIndicationsValueContainer]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_last_ct_indications_value_container_list, (cached, count)), CTIndicationsValueContainer)

            @staticmethod
            def last_chiller_value_containers(cached: bool, count: int = 1, valid_values: bool = True) -> Result[list[ChillerIndicationsValueContainer]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_last_сhiller_indications_value_container_list, (cached, count, valid_values)), ChillerIndicationsValueContainer)

        class BACKUP:

            @staticmethod
            def robocopy_job_status_list() -> Result[list[RobocopyJobStatus]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.robocopy_get_job_status_list), RobocopyJobStatus)

        class SETTINGS:

            @staticmethod
            def key(key: str, default_value: Any | None = None) -> Result[Any]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_settings_value, (key, default_value)))

            @staticmethod
            def get(settings_item: SETTINGS) -> Result[Any]:
                settings_value: StorageValue = EnumTool.get(settings_item)
                return PIH.RESULT.SETTINGS.get_by_name(settings_value.key_name or settings_item.name, settings_value.default_value)
            
            @staticmethod
            def get_by_name(value: str, default_value: Any | None = None) -> Result[Any]:
                return PIH.RESULT.SETTINGS.key(value, default_value)

        class SERVERS:

            @staticmethod
            def all_description() -> Result[list[WorkstationDescription]]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_all_workstation_description, (AD.SERVERS_CONTAINER_DN,)), WorkstationDescription)

        class WORKSTATION:

            @staticmethod
            def all_description() -> Result[list[WorkstationDescription]]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_all_workstation_description), WorkstationDescription)

            @staticmethod
            def all_with_prooperty(value: AD.WSProperies) -> Result[list[Workstation]]:
                def filter_function(workstation: Workstation) -> bool:
                    return BM.has(workstation.properties, value.value)
                return ResultTool.filter(PIH.RESULT.WORKSTATION.all(), filter_function)

            @staticmethod
            def by_login(value: str) -> Result[list[Workstation]]:
                value = PIH.DATA.FORMAT.string(value)
                if PIH.CHECK.USER.exists_by_login(value):
                    return DataTool.to_result(
                        PIH.SERVICE.call_command(ServiceCommands.get_workstation_list_by_user_login, value), Workstation)
                else:
                    raise NotFound(f"Пользователь с логином {value} не найден")

            @staticmethod
            def by_internal_telephone_number(value: int) -> Result[Workstation]:
                result: Result[list[Workstation]] = PIH.RESULT.WORKSTATION.all()
                workstation_list: list[Workstation] = result.data
                result_worksation: Workstation | None = None
                for workstation in workstation_list:
                    if not DataTool.is_empty(workstation.description):
                        index: int = workstation.description.find(CONST.INTERNAL_TELEPHONE_NUMBER_PREFIX)
                        if index != -1:
                            internal_telephone_number_text: str = workstation.description[index:]
                            internal_telephone_number: int = PIH.DATA.EXTRACT.decimal(internal_telephone_number_text)
                            if internal_telephone_number == value:
                                result_worksation = workstation
                                break
                if result_worksation is not None:#and result_worksation.accessable and not DataTool.is_empty(result_worksation.samAccountName):
                    return Result(result.fields, workstation)
                else:
                    raise PIH.ERROR.USER.get_not_found_error(
                        "внутренним номером телефона", True, str(value))

            @staticmethod
            def by_any(value: int | str) -> Result[list[Workstation]]:
                if PIH.DATA.CHECK.decimal(value):
                    try:
                        return ResultTool.as_list(PIH.RESULT.WORKSTATION.by_internal_telephone_number(int(value)))
                    except NotFound:
                        return PIH.RESULT.WORKSTATION.by_login(PIH.RESULT.USER.by_tab_number(value).data.samAccountName)
                if PIH.CHECK.WORKSTATION.name(value):
                    return ResultTool.as_list(PIH.RESULT.WORKSTATION.by_name(value))
                try:
                    return PIH.RESULT.WORKSTATION.by_login(value)
                except NotFound:
                    detail: str = f"Компьютер с параметром поиска {value} не найден"
                    raise NotFound(detail)

            @staticmethod
            def by_name(value: str) -> Result[Workstation]:
                value = PIH.DATA.FORMAT.string(value).lower()
                result: Result[Workstation] = ResultTool.with_first_item(ResultTool.filter(
                    PIH.RESULT.WORKSTATION.all(), lambda item: item.name.lower() == value))
                if ResultTool.is_empty(result):
                    raise NotFound(f"Компьютер с именем {value} не найден")
                return result

            @staticmethod
            def all() -> Result[list[Workstation]]:
                def every_action(workstation: Workstation) -> None:
                    workstation.name = workstation.name.lower()
                return ResultTool.every(DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_all_workstations), Workstation), every_action)

        class INVENTORY:

            @staticmethod
            def report(report_file_path: str, open_for_edit: bool = False) -> Result[list[InventoryReportItem]]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_inventory_report, (report_file_path, open_for_edit)), InventoryReportItem)

        class TIME_TRACKING:

            @staticmethod
            def today(tab_number_list: list[str] | None = None) -> Result[list[TimeTrackingResultByPerson]]:
                return PIH.RESULT.TIME_TRACKING.create(tab_number_list=tab_number_list)

            def yesterday(tab_number_list: list[str] | None = None) -> Result[list[TimeTrackingResultByPerson]]:
                yesterday: datetime = DateTimeTool.yesterday()
                return PIH.RESULT.TIME_TRACKING.create(DateTimeTool.start_date(yesterday), DateTimeTool.start_date(yesterday), tab_number_list)

            @staticmethod
            def in_period(day_start: int = 1, day_end: int | None = None, month: int | None  = None, tab_number: list[str] | None = None) -> Result[list[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now()
                if month is not None:
                    now = now.replace(month=month)
                start_date: datetime = DateTimeTool.start_date(now)
                end_date: datetime = DateTimeTool.end_date(now)
                if day_start < 0:
                    start_date -= timedelta(days=abs(day_start))
                else:
                    start_date = start_date.replace(day=day_start)
                if day_end is not None:
                    if day_end < 0:
                        day_end -= timedelta(days=abs(day_start))
                    else:
                        day_end = start_date.replace(day=day_start)
                return PIH.RESULT.TIME_TRACKING.create(start_date, end_date, tab_number)

            @staticmethod
            def create(start_date: datetime | None = None, end_date: datetime | None = None, tab_number_list: list[str] | None = None) -> Result[list[TimeTrackingResultByPerson]]:
                now: datetime | None = DataTool.check(DataTool.is_empty(start_date) or DataTool.is_empty(end_date), datetime.now())
                start_date = DateTimeTool.start_date(start_date or now)
                end_date = DateTimeTool.end_date(end_date or now)

                def get_date_or_time(entity: TimeTrackingEntity, date: bool) -> str :
                    return DataTool.check_not_none(entity, lambda: entity.TimeVal.split(CONST.DATETIME_SPLITTER)[not date])
                result_data: dict = {}
                full_name_by_tab_number_map: dict = {}
                result_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
                data: list[TimeTrackingEntity] = DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_time_tracking, (start_date, end_date, tab_number_list)), TimeTrackingEntity).data
                for time_tracking_entity in data:
                    tab_number: str = time_tracking_entity.TabNumber
                    full_name_by_tab_number_map[tab_number] = time_tracking_entity.FullName
                    result_data[time_tracking_entity.DivisionName][tab_number][get_date_or_time(time_tracking_entity, True)].append(
                        time_tracking_entity)
                result: list[TimeTrackingResultByDivision] = []
                for division_name in result_data:
                    if division_name is None:
                        continue
                    result_division_item: TimeTrackingResultByDivision = TimeTrackingResultByDivision(
                        division_name)
                    result.append(result_division_item)
                    for tab_number in result_data[division_name]:
                        result_person_item: TimeTrackingResultByPerson = TimeTrackingResultByPerson(
                            tab_number, full_name_by_tab_number_map[tab_number])
                        result_division_item.list.append(result_person_item)
                        for date in result_data[division_name][tab_number]:
                            time_tracking_entity_list: list[TimeTrackingEntity] = result_data[division_name][tab_number][date]
                            time_tracking_enter_entity: TimeTrackingEntity = None
                            time_tracking_exit_entity: TimeTrackingEntity = None
                            for time_tracking_entity_list_item in time_tracking_entity_list:
                                if time_tracking_entity_list_item.Mode == 1:
                                    time_tracking_enter_entity = time_tracking_entity_list_item
                                if time_tracking_entity_list_item.Mode == 2:
                                    time_tracking_exit_entity = time_tracking_entity_list_item
                            duration: int = 0
                            if time_tracking_enter_entity is not None:
                                if time_tracking_exit_entity is not None:
                                    enter_time: datetime = datetime.fromisoformat(
                                        time_tracking_enter_entity.TimeVal).timestamp()
                                    exit_time: datetime = datetime.fromisoformat(
                                        time_tracking_exit_entity.TimeVal).timestamp()
                                    if enter_time < exit_time:
                                        #    enter_time, exit_time = exit_time, enter_time
                                        #    time_tracking_enter_entity, time_tracking_exit_entity = time_tracking_exit_entity, time_tracking_enter_entity
                                        duration = int(exit_time - enter_time)
                                    result_person_item.duration += duration
                            result_person_item.list.append(
                                TimeTrackingResultByDate(date, get_date_or_time(time_tracking_enter_entity, False),
                                                         get_date_or_time(time_tracking_exit_entity, False), duration))
                for division in result:
                    for person in division.list:
                        index: int = 0
                        length: int = len(person.list)
                        for _ in range(length):
                            item: TimeTrackingResultByDate = person.list[index]
                            if item.duration == 0:
                                # if item.enter_time is None and item.exit_time is not None:
                                if index < length - 1:
                                    item_next: TimeTrackingResultByDate = person.list[index + 1]
                                    if item.exit_time is not None:
                                        if item_next.enter_time is not None:
                                            duration = int(datetime.fromisoformat(item.date + CONST.DATETIME_SPLITTER + item.exit_time).timestamp(
                                            ) - datetime.fromisoformat(item_next.date + CONST.DATETIME_SPLITTER + item_next.enter_time).timestamp())
                                            item.duration = duration
                                            person.duration += duration
                                            if item_next.exit_time is None:
                                                index += 1
                            index += 1
                            if index >= length - 1:
                                break

                return Result(FIELD_COLLECTION.ORION.TIME_TRACKING_RESULT, result)

        class PRINTER:

            @staticmethod
            def all() -> Result[list[PrinterADInformation]]:
                def filter_by_server_name(printer_list: list[PrinterADInformation]) -> list[PrinterADInformation]:
                    return list(filter(lambda item: item.serverName == CONST.HOST.PRINTER_SERVER.NAME, printer_list))
                result: Result[list[PrinterADInformation]] = DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_printers), PrinterADInformation)
                return Result(result.fields, filter_by_server_name(result.data))

            @staticmethod
            def report() -> Result[list[PrinterReport]]:
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.printers_report), PrinterReport)

        class MARK:

            @staticmethod
            def by_tab_number(value: str) -> Result[Mark]:
                result: Result[Mark] = DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_mark_by_tab_number, value), Mark)
                if ResultTool.is_empty(result):
                    details: str = f"Карта доступа с номером '{value}' не найдена"
                    raise NotFound(details)
                return result

            @staticmethod
            def by_division(division_or_id: PersonDivision | int) -> Result[list[Mark]]:
                division_id: int = DataTool.check(isinstance(
                    division_or_id, PersonDivision), lambda: division_or_id.id, division_or_id)
                return DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_mark_list_by_division_id, division_id), Mark)

            @staticmethod
            def person_divisions() -> Result[list[PersonDivision]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_mark_person_division_list), PersonDivision)

            @staticmethod
            def by_name(value: str, first_item: bool = False) -> Result[list[Mark]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_mark_by_person_name, value), Mark, first_item)

            @staticmethod
            def by_full_name(value: FullName, first_item: bool = False) -> Result[list[Mark]]:
                return PIH.RESULT.MARK.by_name(FullNameTool.fullname_from_string(value), first_item)

            @staticmethod
            def temporary_list() -> Result[list[TemporaryMark]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_temporary_mark_list), TemporaryMark)

            @staticmethod
            def by_any(value: str) -> Result[list[Mark]]:
                if PIH.CHECK.MARK.tab_number(value):
                    return ResultTool.as_list(PIH.RESULT.MARK.by_tab_number(value))
                elif PIH.CHECK.name(value, True):
                    return PIH.RESULT.MARK.by_name(value)
                return Result()

            @staticmethod
            def free_list(show_with_guest_marks: bool = False) -> Result[list[Mark]]:
                result: Result[list[Mark]] = DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_free_mark_list), Mark)

                def filter_function(item: Mark) -> bool:
                    return EnumTool.get(MarkType, item.type) != MarkType.GUEST
                return result if show_with_guest_marks else ResultTool.filter(result, filter_function)

            @staticmethod
            def free_marks_by_group_id(value: int) -> Result[list[Mark]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_free_mark_list_by_group_id, value), Mark)

            @staticmethod
            def free_marks_group_statistics(show_guest_marks: bool | None = None) -> Result[list[MarkGroupStatistics]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_free_mark_group_statistics_list, show_guest_marks), MarkGroupStatistics)

            @staticmethod
            def all() -> Result[list[Mark]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_mark_list), Mark)

            @staticmethod
            def temporary_mark_owner(mark: Mark) -> Result[Mark]:
                return DataTool.check(mark is not None and EnumTool.get(MarkType, mark.type) == MarkType.TEMPORARY, lambda: DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_owner_mark_for_temporary_mark, mark.TabNumber), Mark), None)

            @staticmethod
            def temporary_mark_owner_by_tab_number(value: str) -> Result[Mark]:
                return PIH.RESULT.MARK.temporary_mark_owner(PIH.RESULT.MARK.by_tab_number(value).data)

        class POLIBASE:

            @staticmethod
            def _person_pin(person_or_pin: PolibasePerson | int) -> int:
                return person_or_pin.pin if isinstance(person_or_pin, PolibasePerson) else person_or_pin

            class NOTIFICATION:

                @staticmethod
                def by(value: PolibasePersonVisitNotification) -> Result[list[PolibasePersonVisitNotification]]:
                    return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_visit_notifications, value), PolibasePersonVisitNotification)

                @staticmethod
                def by_message_id(value: int) -> Result[PolibasePersonVisitNotification]:
                    return ResultTool.with_first_item(PIH.RESULT.POLIBASE.NOTIFICATION.by(PolibasePersonVisitNotification(messageID=value)))

                class CONFIRMATION:
                    
                    @staticmethod
                    def by(recipient: str, sender: str) -> Result[PolibasePersonNotificationConfirmation]:
                        return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_notification_confirmation, PolibasePersonNotificationConfirmation(recipient, sender)), PolibasePersonNotificationConfirmation)

            class INFORMATION_QUEST:

                @staticmethod
                def get(search_critery: PolibasePersonInformationQuest) -> Result[list[PolibasePersonInformationQuest]]:
                    return DataTool.to_result(
                        PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_information_quests, search_critery), PolibasePersonInformationQuest)

            class VISIT:

                @staticmethod
                def after_id(value: int, test: bool | None = None) -> Result[list[PolibasePersonVisitDS]]:
                    return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_visits, (PolibasePersonVisitSearchCritery(vis_no=f">{value}"), test)), PolibasePersonVisitDS)

                @staticmethod
                def by_id(value: int, test: bool | None = None) -> Result[PolibasePersonVisitDS]:
                    return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_visits, (PolibasePersonVisitSearchCritery(vis_no=value), test)), PolibasePersonVisitDS, True)

                @staticmethod
                def last_id(test: bool | None = None) -> Result[int]:
                    return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_person_visits_last_id, test))

                @staticmethod
                def today(test: bool | None = None) -> Result[list[PolibasePersonVisitDS]]:
                    return PIH.RESULT.POLIBASE.VISIT.by_registration_date(DateTimeTool.today(as_datetime=True), test)

                @staticmethod
                def prerecording_today(test: bool | None = None) -> Result[list[PolibasePersonVisitDS]]:
                    return PIH.RESULT.POLIBASE.VISIT.prerecording_by_registration_date(DateTimeTool.today(as_datetime=True), test)

                @staticmethod
                def by_registration_date(value: datetime, test: bool | None = None) -> Result[list[PolibasePersonVisitDS]]:
                    return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_visits, (PolibasePersonVisitSearchCritery(vis_reg_date=DateTimeTool.date_to_string(value, CONST.POLIBASE.DATE_FORMAT)), test)), PolibasePersonVisitDS)

                @staticmethod
                def prerecording_by_registration_date(value: datetime = None, test: bool | None = None) -> Result[list[PolibasePersonVisitDS]]:
                    def filter_function(value: PolibasePersonVisitDS) -> bool:
                        return value.pin == CONST.POLIBASE.PRERECORDING_PIN
                    return ResultTool.filter(PIH.RESULT.POLIBASE.VISIT.by_registration_date(value, test), filter_function)

                class DATA_STORAGE:

                    @staticmethod
                    def search(value: PolibasePersonVisitDS) -> Result[PolibasePersonVisitDS]:
                        return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.search_polibase_person_visits_in_data_storage, (value, )), PolibasePersonVisitDS, True)

                    @staticmethod
                    def last() -> Result[PolibasePersonVisitDS]:
                        return PIH.RESULT.POLIBASE.VISIT.DATA_STORAGE.search(PolibasePersonVisitDS(id=-1))


            @staticmethod
            def person_by_telephone_number(value: str, test: bool | None = None) -> Result[list[PolibasePerson]]:
                value = PIH.DATA.FORMAT.telephone_number_international(value)
                result: Result[PolibasePerson] = DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_polibase_persons_by_telephone_number, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error("идентификационным номером", value)
                return result

            @staticmethod
            def person_by_pin(value: int, test: bool | None = None) -> Result[PolibasePerson]:
                result: Result[PolibasePerson] = DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_polibase_person_by_pin, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error("идентификационным номером", value)
                return result

            @staticmethod
            def person_by_email(value: str, test: bool | None = None) -> Result[PolibasePerson]:
                result: Result[PolibasePerson] = DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_polibase_person_by_email, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error("адресом электронной почты", value)
                return result

            @staticmethod
            def persons_pin_by_visit_date(date: datetime, test: bool | None = None) -> Result[list[int]]:
                if test:
                    return Result(None, [CONST.TEST.PIN])
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_persons_pin_by_visit_date, (date.strftime(CONST.DATE_FORMAT), test)))

            @staticmethod
            def person_registrator_by_pin(value: int, test: bool | None = None) -> Result[PolibasePerson]:
                result: Result[list[PolibasePerson]] = DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_person_registrator_by_pin, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error(
                        "идентификационным номером", value)
                return result

            @staticmethod
            def person_operator_by_pin(value: int, test: bool | None = None) -> Result[PolibasePerson]:
                result: Result[list[PolibasePerson]] = DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_person_operator_by_pin, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error(
                        "идентификационным номером", value)
                return result

            @staticmethod
            def persons_by_full_name(value: str, test: bool | None = None) -> Result[list[PolibasePerson]]:
                value = FullNameTool.format(value)
                result: Result[list[PolibasePerson]] = DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_persons_by_full_name, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error("именем", value)
                return result
            


            @staticmethod
            def persons_by_pin(value: list[int], test: bool | None = None) -> Result[list[PolibasePerson]]:
                result: Result[list[PolibasePerson]] = DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_persons_by_pin, (value, test)), PIH.DATA.EXTRACT.polibase_person)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.POLIBASE.create_not_found_error("идентификационным номером", value)
                return result

            @staticmethod
            def persons_by_card_registry_folder(name: str, test: bool | None = None) -> Result[list[PolibasePerson]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_persons_by_card_registry_folder_name, (name, test)), PIH.DATA.EXTRACT.polibase_person)

            @staticmethod
            def person_pin_list_with_old_format_barcode(test: bool | None = None) -> Result[list[int]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_polibase_person_pin_list_with_old_format_barcode, (test, )))

            @staticmethod
            def persons_by_any(value: str, test: bool | None = None) -> Result[list[PolibasePerson]]:
                if value == CONST.POLIBASE.BARCODE.NOT_FOUND:
                    raise BarcodeNotFound()
                if PIH.CHECK.telephone_number(value) or PIH.CHECK.telephone_number_international(value):
                    return ResultTool.as_list(PIH.RESULT.POLIBASE.person_by_telephone_number(value, test))
                if PIH.CHECK.POLIBASE.person_pin(value):
                    return ResultTool.as_list(PIH.RESULT.POLIBASE.person_by_pin(int(value), test))
                if PIH.CHECK.POLIBASE.person_card_registry_folder(value):
                    return PIH.RESULT.POLIBASE.persons_by_card_registry_folder(value, test)
                return ResultTool.as_list(PIH.RESULT.POLIBASE.persons_by_full_name(value))

        class USER:

            @staticmethod
            def by_login(value: str, active: bool | None = None, cached: bool | None = None) -> Result[User]:
                result: Result[User] = DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_user_by_login, (value, active, cached)), User)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.USER.get_not_found_error("логином", active, value)
                return result

            @staticmethod
            def by_telephone_number(value: str, active: bool | None = None) -> Result[User]:
                result: Result[User] = DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_user_by_telephone_number, (value, active)), User, True)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.USER.get_not_found_error("номером телефона", active, value)
                return result

            @staticmethod
            def by_internal_telephone_number(value: int) -> Result[User]:
                workstation_list: list[Workstation] = PIH.RESULT.WORKSTATION.all().data
                result_worksation: Workstation = None
                for workstation in workstation_list:
                    if not DataTool.is_empty(workstation.description):
                        index: int = workstation.description.find(CONST.INTERNAL_TELEPHONE_NUMBER_PREFIX)
                        if index != -1:
                            internal_telephone_number_text: str = workstation.description[index:]
                            internal_telephone_number: int = PIH.DATA.EXTRACT.decimal(internal_telephone_number_text)
                            if internal_telephone_number == value:
                                result_worksation = workstation
                                break
                if result_worksation is not None and result_worksation.accessable and not DataTool.is_empty(result_worksation.samAccountName):
                    return PIH.RESULT.USER.by_login(workstation.samAccountName)
                else:
                    raise PIH.ERROR.USER.get_not_found_error(
                        "внутренним номером телефона", True, str(value))

            @staticmethod
            def by_polibase_pin(value: int) -> Result[User]:
                return ResultTool.with_first_item(PIH.RESULT.USER.by_name(PIH.RESULT.POLIBASE.person_by_pin(value).data.FullName))

            @staticmethod
            def by_workstation_name(name: str) -> Result[User]:
                name = name.lower()
                user_workstation: Workstation = DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_user_by_workstation, name), Workstation, True).data
                if DataTool.is_empty(user_workstation):
                    details: str = f"Компьютер с именем '{name}' не найден!"
                    raise NotFound(details)
                if DataTool.is_empty(user_workstation.samAccountName):
                    raise NotFound(f"За компьютером {name} нет залогиненного пользователя", name)
                return PIH.RESULT.USER.by_login(user_workstation.samAccountName)

            @staticmethod
            def by_any(value: Any, active: bool | None = None) -> Result[list[User]]:
                def by_number(value: int) -> Result[list[User]]:
                    try:
                        return ResultTool.as_list(PIH.RESULT.USER.by_tab_number(value))
                    except NotFound:
                        try:
                            return ResultTool.as_list(PIH.RESULT.USER.by_login(PIH.RESULT.WORKSTATION.by_internal_telephone_number(value).data.samAccountName))
                        except:
                            return ResultTool.as_list(PIH.RESULT.USER.by_polibase_pin(value))
                if isinstance(value, Mark):
                    return PIH.RESULT.USER.by_name(value.FullName)
                elif isinstance(value, FullName):
                    return PIH.RESULT.USER.by_full_name(value, False, active)
                elif isinstance(value, (WorkstationDescription, Workstation)):
                    return PIH.RESULT.USER.by_any(value.name, active)
                elif isinstance(value, str):
                    if value.lower().startswith(CONST.GROUP_PREFIX):
                        value = str(value[len(CONST.GROUP_PREFIX):])
                        return PIH.RESULT.USER.by_group_name(value)
                    try:
                        value_as_telephone_number: str = PIH.DATA.FORMAT.telephone_number(value)
                        if PIH.CHECK.telephone_number(value_as_telephone_number):
                            return ResultTool.as_list(PIH.RESULT.USER.by_telephone_number(value_as_telephone_number, active))
                    except Exception:
                        pass
                    if PIH.DATA.CHECK.decimal(value):
                       return by_number(value)
                    if PIH.CHECK.WORKSTATION.name(value):
                        return ResultTool.as_list(PIH.RESULT.USER.by_workstation_name(value))
                    if PIH.CHECK.login(value):
                        return ResultTool.as_list(PIH.RESULT.USER.by_login(value, active))
                    if value == "" or PIH.CHECK.name(value):
                        return PIH.RESULT.USER.by_name(value, active)
                elif isinstance(value, int):
                    return by_number(value)
                raise PIH.ERROR.USER.get_not_found_error("поисковым значением", active, value)

            @staticmethod
            def by_job_position(value: AD.JobPisitions) -> Result[list[User]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_users_by_job_position, value.name), User)

            @staticmethod
            def by_group(value: AD.Groups) -> Result[list[User]]:
                return PIH.RESULT.USER.by_group_name(value.name)

            @staticmethod
            def by_group_name(value: str) -> Result[list[User]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_users_by_group, value), User)


            @staticmethod
            def template_list() -> Result[list[User]]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_template_users), User)

            @staticmethod
            def containers() -> Result[list[UserBase]]:
                return DataTool.to_result(PIH.SERVICE.call_command(
                    ServiceCommands.get_containers), UserBase)

            @staticmethod
            def by_full_name(value: FullName, get_first: bool = False, active: bool | None = None) -> Result[list[User] | User]:
                return DataTool.to_result(PIH.SERVICE.call_command(ServiceCommands.get_user_by_full_name, (value, active)), User, get_first)

            @staticmethod
            def by_name(value: str, active: bool | None = None, cached: bool | None = None) -> Result[list[User]]:
                result: Result[list[User]] = DataTool.to_result(
                    PIH.SERVICE.call_command(ServiceCommands.get_users_by_name, (value, active, cached)), User)
                if ResultTool.is_empty(result):
                    raise PIH.ERROR.USER.get_not_found_error("именем", active, value)
                return result

            @staticmethod
            def all(active: bool | None = None) -> Result[list[User]]:
                return PIH.RESULT.USER.by_name(AD.SEARCH_ALL_PATTERN, active)

            @staticmethod
            def list_with_telephone_number(active: bool | None = None) -> Result[list[User]]:
                def user_with_telephone_number(user: User) -> bool:
                    return PIH.CHECK.telephone_number(user.telephoneNumber)
                return ResultTool.filter(PIH.RESULT.USER.all(active), lambda user: user_with_telephone_number(user))

            @staticmethod
            def by_tab_number(value: str) -> Result[User]:
                result: Result[Mark] = PIH.RESULT.MARK.by_tab_number(value)
                if ResultTool.is_empty(result):
                    details: str = f"Карта доступа с номером {value} не найдена"
                    raise NotFound(details)
                return PIH.RESULT.USER.by_mark(result.data)

            @staticmethod
            def by_mark(value: Mark) -> Result[User]:
                return Result(FIELD_COLLECTION.AD.USER, DataTool.check(value, lambda: DataTool.get_first_item(PIH.RESULT.USER.by_full_name(FullNameTool.fullname_from_string(value.FullName)).data)))

    class CHECK:

        class EVENTS:

            @staticmethod
            def has(value: Events | None, parameters: tuple[Any] | None = None) -> bool:
                return not ResultTool.is_empty(PIH.RESULT.EVENTS.get(value, parameters))

            @staticmethod
            def timeouted(event: Events, parameters: dict | None, timeout_in_seconds: int) -> bool:
                event_ds: EventDS | None = PIH.RESULT.get_first_item(
                    PIH.RESULT.sort(PIH.RESULT.EVENTS.get(event, parameters), lambda item: item.timestamp, reserve=True))
                return DataTool.is_none(event_ds) or (
                    DateTimeTool.now() - event_ds.timestamp).total_seconds() > timeout_in_seconds

        class SETTINGS:
    
            @staticmethod
            def by_time(current: datetime, settings: SETTINGS) -> bool:
                return DateTimeTool.is_equal_by_time(current, PIH.SETTINGS.to_datetime(settings))

        class INDICATION:

            @staticmethod
            def ct_notification_start_time(current: datetime) -> bool:
                start_time_list: list[datetime] = PIH.SETTINGS.INDICATION.ct_notification_start_time()
                for start_time in start_time_list:
                    if DateTimeTool.is_equal_by_time(current, start_time):
                        return True
                return False
            
        class RECOGNIZE:

            @staticmethod
            def document_type_exists(file_path: str, value: DocumentTypes, log_level: int | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.document_type_exists, (file_path, value.name, log_level)))

        class NOTES:

            @staticmethod
            def exists(name: str) -> bool:
                return not DataTool.is_empty(DataTool.rpc_unrepresent(
                    PIH.SERVICE.call_command(ServiceCommands.get_gkeep_item_id, (name, ))))

        class RESOURCE:

            @staticmethod
            def accessibility_by_ping_with_port(address_or_ip: str, port:int, host: str | None = None, count: int | None = None, check_for_all: bool = True) -> bool:
                return PIH.CHECK.RESOURCE.accessibility_by_ping(":".join((address_or_ip, str(port))), host, count, check_for_all)

            @staticmethod
            def accessibility_by_smb_port(address_or_ip: str, host: str | None = None, count: int | None = None, check_for_all: bool = True) -> bool:
                return PIH.CHECK.RESOURCE.accessibility_by_ping_with_port(address_or_ip, WINDOWS.PORTS.SMB, host, count, check_for_all)
            
            @staticmethod
            def accessibility_by_ping(address_or_ip: str, host: str | None = None, count: int | None = None, check_for_all: bool = True) -> bool:
                count = count or 4
                ping_command: list[str] = [PIH.EXECUTOR.get_executor_path(
                    CONST.PSTOOLS.PS_PING), CONST.PSTOOLS.ACCEPTEULA, "-4", "-n", str(count), address_or_ip]
                process_result: CompletedProcess = PIH.EXECUTOR.execute(DataTool.check_not_none(host,
                    lambda: PIH.EXECUTOR.create_command_for_psexec(ping_command, host,  
                    PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_LOGIN),
                    PIH.DATA.VARIABLE.value(LINK.ADMINISTRATOR_PASSOWORD), True), ping_command), True, True)
                if process_result.returncode == 0:
                    result: str = process_result.stdout
                    lost_marker: str = "Lost = "
                    index: int = result.find(lost_marker)
                    if index != -1:
                        lost_count: int = int(result[index +
                                                len(lost_marker): result.find(" (", index)])
                        if check_for_all:
                            return lost_count == 0
                        return lost_count < count
                return False

            @staticmethod
            def accessibility(resource_status_or_address: Any) -> bool:
                resource_status: ResourceStatus = None
                if isinstance(resource_status_or_address, ResourceDescription):
                    resource_status = resource_status_or_address
                else:
                    resource_status = PIH.RESULT.RESOURCES.get_resource_status(
                        resource_status_or_address)
                return None if resource_status is None else resource_status.inaccessibility_counter < resource_status.inaccessibility_check_values[0]
                
            @staticmethod
            def vpn_pacs_accessibility(count: int = 2) -> bool:
                return PIH.EXECUTOR.ping(RESOURCES.DESCRIPTIONS.VPN_PACS_SPB.address, CONST.HOST.WS255.NAME, count)
            
            @staticmethod
            def pacs_accessibility(count: int = 2) -> bool:
                return PIH.CHECK.RESOURCE.accessibility_by_ping(RESOURCES.DESCRIPTIONS.PACS_SPB.address, CONST.HOST.WS255.NAME, count)
           
            @staticmethod
            def wappi_profile_accessibility(value: Any, cached: bool = False) -> bool:
                return PIH.CHECK.RESOURCE.accessibility(PIH.RESULT.RESOURCES.get_resource_status(EnumTool.get_value(value, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value))) if cached else PIH.CHECK.MESSAGE.WHATSAPP.WAPPI.accessibility(value, False)

            @staticmethod
            def ws_accessibility(name: str) -> bool:
                result: Result[Workstation] = PIH.RESULT.WORKSTATION.by_name(name)
                return not ResultTool.is_empty(result) and result.data.accessable
            
            @staticmethod
            def polibase_accessibility(cached: bool = False) -> bool:
                try:
                    if cached:
                        return PIH.RESULT.RESOURCES.get_resource_status(RESOURCES.DESCRIPTIONS.POLIBASE).accessable
                    result_by_ping: bool = PIH.SERVICE.check_on_accessibility(ServiceRoles.POLIBASE)    
                    result_by_pin : bool = PIH.CHECK.POLIBASE.person_exists_by_pin(CONST.POLIBASE.PRERECORDING_PIN)
                    return result_by_ping and result_by_pin
                except NotFound:
                    pass
                return False

        class EMAIL:

            @staticmethod
            def accessability(value: str) -> bool:
                def internal_accessability(value: str, verification_method: EmailVerificationMethods.DEFAULT) -> bool:
                     return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.check_email_accessibility, (value, verification_method)))
                if not internal_accessability(value, EmailVerificationMethods.DEFAULT):
                    return internal_accessability(value, EmailVerificationMethods.ABSTRACT_API)   
                return True
               

        class FILE:

            @staticmethod
            def excel_file(path: str) -> bool:
                return os.path.isfile(path) and PathTool.get_extension(path) in [FILE.EXTENSION.EXCEL_OLD, FILE.EXTENSION.EXCEL_NEW]

        class ACCESS:

            @staticmethod
            def by_group(group: AD.Groups, exit_on_access_denied: bool = False, session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                session = session or PIH.session
                user: User = session.get_user()
                result: bool = False
                notify: bool = notify_on_success or notify_on_fail
                if group in session.allowed_groups:
                    result = True
                    notify = False
                else:
                    result = PIH.CHECK.USER.by_group(user, group)
                    if result:
                        session.add_allowed_group(group)
                if notify:
                    PIH.LOG.it(
                        f"Запрос на доступа к группе: {group.name} от пользователя {user.name} ({user.samAccountName}). Доступ {'разрешен' if result else 'отклонен'}.", LogMessageFlags.NORMAL if result else LogMessageFlags.ERROR)
                if not result and exit_on_access_denied:
                    session.exit(5, "Функционал недоступен...")
                return result

            @staticmethod
            def admin(exit_on_access_denied: bool = False, session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.Admin, exit_on_access_denied, session, notify_on_fail, notify_on_success)

            @staticmethod
            def service_admin(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.ServiceAdmin, False, session, notify_on_fail, notify_on_success)

            @staticmethod
            def inventory(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.Inventory, False, session, notify_on_fail, notify_on_success)

            @staticmethod
            def polibase(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.Polibase, False, session, notify_on_fail, notify_on_success)

            @staticmethod
            def card_registry(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.CardRegistry, False, session, notify_on_fail, notify_on_success)

        class USER:

            @staticmethod
            def by_group(user: User, group: AD.Groups) -> bool:
                return not DataTool.is_empty(ResultTool.do_while(PIH.RESULT.USER.by_group(group), lambda check_user: check_user.samAccountName == user.samAccountName))

            @staticmethod
            def exists_by_login(value: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.check_user_exists_by_login, value))

            @staticmethod
            def user(user: User) -> bool:
                return PIH.CHECK.full_name(user.name)

            @staticmethod
            def active(user: User) -> bool:
                return user.distinguishedName.find(AD.ACTIVE_USERS_CONTAINER_DN) != -1

            @staticmethod
            def exists_by_full_name(full_name: FullName) -> bool:
                return not ResultTool.is_empty(PIH.RESULT.USER.by_full_name(full_name))

            @staticmethod
            def search_attribute(value: str) -> bool:
                return value in AD.SEARCH_ATTRIBUTES

            @staticmethod
            def property(value: str | None, default_value: str = USER_PROPERTIES.PASSWORD) -> str:
                return value or default_value

            @staticmethod
            def accessibility() -> bool:
                return PIH.SERVICE.check_on_accessibility(ServiceRoles.AD)

        class MESSAGE:

            class WHATSAPP:

                class WAPPI:

                    @staticmethod
                    def from_me(value: str) -> bool:
                        value = PIH.DATA.FORMAT.telephone_number(value)
                        return value in [PIH.DATA.TELEPHONE_NUMBER.it_administrator(), PIH.DATA.TELEPHONE_NUMBER.call_centre_administrator(), PIH.DATA.TELEPHONE_NUMBER.marketer()]

                    @staticmethod
                    def accessibility(profile: Any, cached: bool = True) -> bool:
                        def internal_accessibility(profile: Any | None = None) -> bool:
                            profile = EnumTool.get_value(profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                            url: str = f"{CONST.MESSAGE.WHATSAPP.WAPPI.URL_GET_STATUS}{profile}"
                            headers: dict = {
                                "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION,
                                "Content-Type": "application/json"
                            }
                            response_result: dict = None
                            try:
                                response: Response = requests.get(url, headers=headers)
                                response_result = json.loads(response.text)
                            except Exception:
                                return False
                            if "status" in response_result:
                                if response_result["status"] == "error":
                                    return False
                            return response_result["app_status"] == "open"
                        return PIH.CHECK.RESOURCE.wappi_profile_accessibility(profile, True) if cached else internal_accessibility(profile)

        class MARK:

            @staticmethod
            def free(tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.check_mark_free, tab_number))

            @staticmethod
            def exists_by_full_name(full_name: FullName) -> bool:
                result: Result[list[Mark]] = PIH.RESULT.MARK.by_name(
                    FullNameTool.fullname_to_string(full_name))
                return ResultTool.is_empty(result)

            @staticmethod
            def accessibility() -> bool:
                return PIH.SERVICE.check_on_accessibility(ServiceRoles.MARK)

            @staticmethod
            def tab_number(value: str) -> bool:
                return value.isdecimal()

        class TIME_TRACKING:

            @staticmethod
            def accessibility() -> bool:
                return PIH.CHECK.ACCESS.by_group(AD.Groups.TimeTrackingReport)

        class INVENTORY:

            @staticmethod
            def is_report_file(file_path: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.check_inventory_report, file_path))

            @staticmethod
            def accessibility() -> bool:
                return PIH.SERVICE.check_on_accessibility(ServiceRoles.DOCS) and PIH.CHECK.ACCESS.inventory()

        class POLIBASE:

            @staticmethod
            def accessibility() -> bool:
                return PIH.SERVICE.check_on_accessibility(ServiceRoles.POLIBASE) and PIH.CHECK.ACCESS.polibase()

            @staticmethod
            def person_card_registry_folder(value: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.check_polibase_person_card_registry_folder_name, value))

            @staticmethod
            def person_exists_by_pin(pin: int) -> bool:
                try:
                    return not ResultTool.is_empty(PIH.RESULT.POLIBASE.person_by_pin(pin))
                except NotFound:
                    return False

            @staticmethod
            def person_pin(value: str | int) -> bool:
                is_numeric: bool = value.isnumeric() if isinstance(value, str) else True if isinstance(value, int) else False 
                return is_numeric and int(value) > CONST.POLIBASE.PERSON_MINIMAL_PIN

            class NOTIFICATION:

                @staticmethod
                def exists(value: PolibasePersonVisitNotification) -> bool:
                    return not ResultTool.is_empty(PIH.RESULT.POLIBASE.NOTIFICATION.by(value))

                class CONFIRMATION:

                    @staticmethod
                    def exists(recipient: str, sender: str, state: int = None) -> bool:
                        result: Result[PolibasePersonNotificationConfirmation] = PIH.RESULT.POLIBASE.NOTIFICATION.CONFIRMATION.by(
                            recipient, sender)
                        return not ResultTool.is_empty(result) and (True if state is None else result.data.status == state)
            
            class DATABASE:

                def creation_start_time(value: datetime) -> bool:
                    return DateTimeTool.is_equal_by_time(value, PIH.SETTINGS.to_datetime(SETTINGS.POLIBASE_CREATION_DB_DUMP_START_TIME))

        @staticmethod
        def login(value: str) -> bool:
            pattern: str = r"^[a-z]+[a-z_0-9]{"+str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH - 1) + ",}"
            return re.fullmatch(pattern, value, re.IGNORECASE) is not None

        class WORKSTATION:

            @staticmethod
            def accessibility(name: str) -> bool | None:
                try:
                    return PIH.RESULT.WORKSTATION.by_name(name).data.accessable
                except NotFound as _:
                    return None

            @staticmethod
            def windows_service_running(name: str, host: str) -> bool | None:
                accessable: bool | None = PIH.CHECK.WORKSTATION.accessibility(host)
                if DataTool.is_none(accessable):
                    return None
                return PIH.EXECUTOR.check_for_windows_service_running(name, host)

            @staticmethod
            def name(value: str) -> bool:
                value = PIH.DATA.FORMAT.string(value)
                for prefix in AD.WORKSTATION_PREFIX_LIST:
                    if value.startswith(prefix):
                        return True
                return False

            @staticmethod
            def exists(name: str) -> bool:
                name = name.lower()
                return not ResultTool.is_empty(ResultTool.filter(PIH.RESULT.WORKSTATION.all_description(), lambda workstation: name == workstation.name.lower()))

            @staticmethod
            def has_property(workstation: WorkstationDescription, property: AD.WSProperies) -> bool:
                return BM.has(workstation.properties, property)

            @staticmethod
            def watchable(workstation: WorkstationDescription) -> bool:
                return PIH.CHECK.WORKSTATION.has_property(workstation, AD.WSProperies.Watchable)

            @staticmethod
            def shutdownable(workstation: WorkstationDescription) -> bool:
                return PIH.CHECK.WORKSTATION.has_property(workstation, AD.WSProperies.Shutdownable)

            @staticmethod
            def rebootable(workstation: WorkstationDescription) -> bool:
                return PIH.CHECK.WORKSTATION.has_property(workstation, AD.WSProperies.Rebootable)

        @staticmethod
        def telephone_number(value: str, international: bool = False) -> bool:
            return not DataTool.is_empty(value) and re.fullmatch(("" if international else r"^\+") + "[0-9]{11,13}$", value) is not None

        @staticmethod
        def telephone_number_international(value: str) -> bool:
            return PIH.CHECK.telephone_number(value, True)

        @staticmethod
        def email(value: str, check_accesability: bool = False) -> bool:
            return not DataTool.is_empty(re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", value))  and (not check_accesability or PIH.CHECK.EMAIL.accessability(value))
        
        @staticmethod
        def name(value: str, use_space: bool = False) -> bool:
            pattern = r"[а-яА-ЯёЁ" + (" " if use_space else "") + \
                "]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def full_name(value: str) -> bool:
            pattern = r"[а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(
                CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def password(value: str, settings: PasswordSettings = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(value, settings.length, settings.special_characters)


    class LOG:

        executor = ThreadPoolExecutor(max_workers=1)

        @staticmethod
        def send(value: str, channel: LogMessageChannels = LogMessageChannels.DEFAULT, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            level = level or LogMessageFlags.DEFAULT
            def internal_send_message(message: str, channel_name: str, level_value: int) -> None:
                with PIH.ERROR.detect():
                    try:
                        PIH.SERVICE.call_command(ServiceCommands.send_log_message,
                                (message, channel_name, level_value))
                    except Error as error:
                        PIH.output.error("Log send error")
            PIH.LOG.executor.submit(internal_send_message, value,
                                        channel.name, DataTool.as_bitmask_value(level))
            return value

        @staticmethod
        def debug_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.DEBUG_BOT, level)

        @staticmethod
        def debug(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.DEBUG, level)

        @staticmethod
        def new_email_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.NEW_EMAIL_BOT, level)

        @staticmethod
        def new_email(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.NEW_EMAIL, level)

        @staticmethod
        def services(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.SERVICES, level)

        @staticmethod
        def resources(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.RESOURCES, level)
        
        @staticmethod
        def printers(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.PRINTER, level)

        @staticmethod
        def services_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.SERVICES_BOT, level)

        @staticmethod
        def backup(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.BACKUP, level)

        @staticmethod
        def polibase(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.POLIBASE, level)

        @staticmethod
        def polibase_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.POLIBASE_BOT, level)

        @staticmethod
        def card_registry(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.CARD_REGISTRY, level)

        @staticmethod
        def card_registry_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.CARD_REGISTRY_BOT, level)

        @staticmethod
        def polibase_error(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.POLIBASE_ERROR, level)

        @staticmethod
        def polibase_error_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.POLIBASE_ERROR_BOT, level)

        @staticmethod
        def it(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.IT, level)

        @staticmethod
        def it_bot(message: str, level: int | tuple[Enum] | Enum | list[Enum] | list[int] | None = None) -> str:
            return PIH.LOG.send(message, LogMessageChannels.IT_BOT, level)


    class MESSAGE:

        class POLIBASE:

            @staticmethod
            def notify(message: str, test: bool = True) -> None:
                PIH.MESSAGE.WORKSTATION.to_all_workstations(message, AD.Groups.PolibaseUsers, [CONST.HOST.WS255.NAME], None, test, 180)

            @staticmethod
            def notify_about_polibase_closing(message: str | None = None, test: bool = True) -> None:
                PIH.MESSAGE.POLIBASE.notify(message or PIH.SETTINGS.get(
                    SETTINGS.POLIBASE_WAS_EMERGENCY_CLOSED_NOTIFICATION_TEXT), test)
                
            @staticmethod
            def notify_about_polibase_restarted(test: bool = True) -> None:
                PIH.MESSAGE.POLIBASE.notify(PIH.SETTINGS.get(
                    SETTINGS.POLIBASE_WAS_RESTARTED_NOTIFICATION_TEXT), test)


        class WORKSTATION:
              
            executor = ThreadPoolExecutor(max_workers=10)

            @staticmethod
            def to_all_workstations(message: str, filter_group: AD.Groups | None = None, to_all_user_workstation_name_list: list[str] | None = None, session: Session = None, test: bool = True, timeout: int = 60) -> None:
                session = session or PIH.session
                filter_user_login_list: list[str] = None if filter_group is None else ResultTool.map(PIH.RESULT.USER.by_group(filter_group), lambda item: item.samAccountName.lower()).data
                filter_user_login_list_is_empty: bool = DataTool.is_empty(filter_user_login_list)
                to_all_user_workstation_name_list_is_empty: bool = DataTool.is_empty(
                    to_all_user_workstation_name_list)
                def filter_function(workstation: Workstation) -> bool:
                    workstation_name: str = workstation.name.lower()
                    if test:
                        return workstation_name == CONST.TEST.WORKSTATION_MAME
                    return workstation.accessable and ((filter_user_login_list_is_empty or workstation.samAccountName in filter_user_login_list) or (to_all_user_workstation_name_list_is_empty or workstation_name in to_all_user_workstation_name_list))
                def every_action(workstation: Workstation) -> None:
                    def internal_send_message(user_login: str | None, workstation_name: str, message: str) -> None:
                        if not DataTool.is_empty(to_all_user_workstation_name_list) and workstation_name in to_all_user_workstation_name_list:
                            if not test:
                                PIH.MESSAGE.WORKSTATION.to_user_or_workstation(None, workstation_name, message, timeout)
                        else:
                            if DataTool.is_empty(user_login):
                                if test:
                                    PIH.MESSAGE.WORKSTATION.to_user_or_workstation(user_login, workstation_name, message, timeout)
                                else:
                                    pass
                                #dont send message - cause workstation is on but no one user is logged
                            else:
                                if test:
                                    if workstation_name == CONST.TEST.WORKSTATION_MAME:
                                        PIH.MESSAGE.WORKSTATION.to_user_or_workstation(user_login, workstation_name, message, timeout)
                                else:
                                    PIH.MESSAGE.WORKSTATION.to_user_or_workstation(user_login, workstation_name, message, timeout)
                    result_message: str = f"Сообщение от {session.user_given_name} ({PIH.DATA.FORMAT.description(session.get_user().description)}):"
                    result_message += f" День добрый, "
                    user: User | None = None if DataTool.is_empty(workstation.samAccountName) else PIH.RESULT.USER.by_login(workstation.samAccountName, True, True).data
                    result_message += DataTool.if_not_empty(user, lambda user: f"{FullNameTool.to_given_name(user)}, ", "")
                    result_message += message
                    PIH.MESSAGE.WORKSTATION.executor.submit(
                        internal_send_message, workstation.samAccountName, workstation.name.lower(), result_message)
                ResultTool.every(ResultTool.filter(PIH.RESULT.WORKSTATION.all(), filter_function), every_action)

            @staticmethod
            def to_user(value: User | str, message: str, timeout: int = 60, method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.WORKSTATION.to_user_or_workstation(value.samAccountName if isinstance(value, User) else value, None, message, timeout, method_type)

            @staticmethod
            def to_workstation(value: WorkstationDescription | str, message: str, timeout: int = 60, method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.WORKSTATION.by_workstation_name(value.name if isinstance(value, WorkstationDescription) else value, message, timeout, method_type)

            @staticmethod
            def by_workstation_name(value: str, message: str, timeout: int = 60, method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE) -> bool:
                user: User = None
                try:
                    user = PIH.RESULT.USER.by_workstation_name(value).data
                except NotFound as error:
                    pass
                return PIH.MESSAGE.WORKSTATION.to_user_or_workstation(user.samAccountName if user is not None else None, value, message, timeout, method_type)

            @staticmethod
            def to_user_or_workstation(user_login: str, workstation_name: str, message: str, timeout: int = 60, method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE) -> bool:
                if method_type == WorkstationMessageMethodTypes.REMOTE:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.send_message_to_user_or_workstation, (user_login, workstation_name, message, timeout)))
                def internal_send_by_login_and_workstation_name(login: str, workstation_name: str) -> None:
                    if method_type == WorkstationMessageMethodTypes.LOCAL_PSTOOL_MSG:
                        PIH.EXECUTOR.execute(PIH.EXECUTOR.create_command_for_psexec(
                            [CONST.MSG.EXECUTOR, f"/time:{timeout}", login, message], workstation_name), False)
                    if method_type == WorkstationMessageMethodTypes.LOCAL_MSG:
                        PIH.EXECUTOR.execute(
                            [CONST.MSG.EXECUTOR, f"/time:{timeout}", login, f"/server:{workstation_name}", message], False)
                if workstation_name is None:
                    result: Result[list[Workstation]] = PIH.RESULT.WORKSTATION.by_login(
                        user_login)
                    ResultTool.every(result, lambda workstation: internal_send_by_login_and_workstation_name(user_login, workstation.name))
                else:
                    if user_login is None:
                        internal_send_by_login_and_workstation_name(
                            "*", workstation_name)
                    else:
                        internal_send_by_login_and_workstation_name(
                            user_login, workstation_name)
                return True

            @staticmethod
            def by_login(login: str, message: str, timeout: int = 60, method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.WORKSTATION.to_user_or_workstation(login, None, message, timeout, method_type)

        class WHATSAPP:

            class WAPPI:

                class QUEUE:
    
                    @staticmethod
                    def add(message: Message, recipient: str, sender: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles, high_priority: bool = False) -> bool:
                        return PIH.MESSAGE.WHATSAPP.WAPPI.QUEUE.add_message(Message(message, recipient, sender.value), high_priority)
                    
                    @staticmethod
                    def add_message(message: Message, high_priority: bool = False) -> bool:
                        return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.add_message_to_queue, (message, high_priority)))


                WAPPI_PROFILE_MAP: dict | None = None 

                @staticmethod
                def get_wappi_collection() -> dict:
                    WP = CONST.MESSAGE.WHATSAPP.WAPPI
                    result: dict = PIH.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP or {
                        WP.Profiles.IT: PIH.DATA.TELEPHONE_NUMBER.it_administrator(),
                        WP.Profiles.CALL_CENTRE: PIH.DATA.TELEPHONE_NUMBER.call_centre_administrator(),
                        WP.Profiles.MARKETER: PIH.DATA.TELEPHONE_NUMBER.marketer()
                    }
                    if PIH.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP is None:
                        PIH.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP = result
                    return result

                @staticmethod
                def send_to_group(group: CONST.MESSAGE.WHATSAPP.GROUP, message: str, profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles = CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.IT) -> bool:
                    return PIH.MESSAGE.WHATSAPP.WAPPI.send(group.value, message, profile)

                @staticmethod
                def get_profile_id(telephone_number: str) -> CONST.MESSAGE.WHATSAPP.WAPPI.Profiles:
                    if PIH.CHECK.telephone_number_international(telephone_number):
                        telephone_number = PIH.DATA.FORMAT.telephone_number(telephone_number)
                    profile_id_collection = PIH.MESSAGE.WHATSAPP.WAPPI.get_wappi_collection()
                    for item in profile_id_collection:
                        if profile_id_collection[item] == telephone_number:
                            return item
                    return None

                @staticmethod
                def get_message_list(telephone_number: str, profile: Any | None = None) -> list[WhatsAppMessage]:
                    profile = EnumTool.get_value(profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                    url: str = f"{CONST.MESSAGE.WHATSAPP.WAPPI.URL_GET_MESSAGES}{profile}&chat_id={telephone_number}{CONST.MESSAGE.WHATSAPP.WAPPI.CONTACT_SUFFIX}"
                    headers: dict = {
                        "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION,
                        "Content-Type": "application/json"
                    }
                    result: list[WhatsAppMessage] = []
                    try:
                        response: Response = requests.get(url, headers=headers)
                    except Exception:
                        return result
                    response_result: dict = json.loads(response.text)
                    has_error: bool = response_result["status"] == "error" or ("detail" in response_result and response_result["detail"] == "Messages not found")
                    if not has_error:
                        for message_item in response_result["messages"]:
                            if message_item["type"] == "chat":
                                result.append(WhatsAppMessage(message_item["body"], message_item["fromMe"], str(message_item["from"]).split("@")[0], 
                                   str(message_item["to"]).split("@")[0], profile, message_item["time"]))
                    return result 
                
                @staticmethod
                def send(telephone_number: str, message: Any, profile: Any | None = None) -> bool:
                    profile = EnumTool.get_value(profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                    url: str | None = None
                    payload: dict = {"recipient": telephone_number}
                    if isinstance(message, str):
                        payload["body"] = message
                        url: str = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_MESSAGE
                    elif isinstance(message, (WhatsAppMessageListPayload, WhatsAppMessageButtonsPayload)):
                        for item_name in message.__dataclass_fields__:
                            item_value: Any = message.__getattribute__(item_name)
                            if not DataTool.is_empty(item_value):
                                if item_name == "buttons":
                                    payload[item_name] = list(map(lambda button: button.__dict__, item_value))
                                else:
                                    payload[item_name] = item_value
                        if isinstance(message, WhatsAppMessageListPayload):
                            url = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_LIST_MESSAGE
                        else:
                            url = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_BUTTONS_MESSAGE
                    url += profile
                    headers: dict = {"accept": "application/json",
                                     "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION, "Content-Type": "application/json"}
                    try:
                        response: Response = requests.post(
                            url, data=json.dumps(payload), headers=headers)
                    except ConnectTimeout:
                        return False
                    if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                        PIH.LOG.resources(
                            "Аккаунт Wappi (сервис для отправики сообщений через WhatsApp) не оплачен", LogMessageFlags.ERROR)
                    status_code: int = response.status_code
                    return status_code == 200

                @staticmethod
                def send_base64_file(url: str, telephone_number: str, caption: str, file_name: str | None, base64_content: str,  profile: Any | None = None) -> bool:
                    profile = EnumTool.get_value(
                        profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                    payload: dict = {"recipient": telephone_number,
                                     "caption": caption,
                                     "b64_file": base64_content}
                    if not DataTool.is_empty(file_name):
                        payload["file_name"] = file_name   
                    headers: dict = {"accept": "application/json",
                                     "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION, "Content-Type": "application/json"}
                    url = url + profile
                    try:
                        response: Response = requests.post(
                            url, data=json.dumps(payload), headers=headers)
                    except ConnectTimeout:
                        return False
                    if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                        PIH.LOG.resources(
                            "Аккаунт Wappi (сервис для отправики сообщений через WhatsApp) не оплачен", LogMessageFlags.ERROR)
                    return response.status_code == 200

                @staticmethod
                def send_video(telephone_number: str, caption: str, base64_content: str, profile: Any | None = None) -> bool:
                    return PIH.MESSAGE.WHATSAPP.WAPPI.send_base64_file(CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_VIDEO, telephone_number, caption, None, base64_content, profile)

                @staticmethod
                def send_image(telephone_number: str, caption: str, base64_content: str, profile: Any | None = None) -> bool:
                    return PIH.MESSAGE.WHATSAPP.WAPPI.send_base64_file(CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_IMAGE, telephone_number, caption, None, base64_content, profile)

                @staticmethod
                def send_document(telephone_number: str, caption: str, file_name: str, base64_content: str, profile: Any | None = None) -> bool:
                    return PIH.MESSAGE.WHATSAPP.WAPPI.send_base64_file(CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_DOCUMENT, telephone_number, caption, file_name, base64_content, profile)

            
            @staticmethod
            def send_via_browser(telephone_number: str, message: str) -> bool:
                pywhatkit_is_exists: bool = importlib.util.find_spec(
                    "pywhatkit") is not None
                if not pywhatkit_is_exists:
                    PIH.output.green(
                        "Установка библиотеки для отправки сообщения. Ожидайте...")
                    if not PIH.UPDATE.install_module("pywhatkit"):
                        PIH.output.error(
                            "Ошибка при установке библиотеки для отправки сообщений!")
                try:
                    import pywhatkit as pwk
                    pwk.sendwhatmsg_instantly(telephone_number, message)
                except Exception as уrror:
                    PIH.output.error("Ошибка при отправке сообщения!")

            @staticmethod
            def send(telephone_number: str, message: Any, via_wappi: bool = True, use_alternative: bool = True, wappi_profile: Any | None = None) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                result: bool = False
                telephone_number = PIH.DATA.FORMAT.telephone_number(
                    telephone_number)
                if via_wappi:
                    result = PIH.MESSAGE.WHATSAPP.WAPPI.send(
                        telephone_number, message, wappi_profile)
                if result:
                    return result
                if use_alternative or not via_wappi:
                    return PIH.MESSAGE.WHATSAPP.send_via_browser(telephone_number, message)
                return False

            @staticmethod
            def send_video(telephone_number: str, caption: str, base64_value: str, wappi_profile: Any | None = None) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                telephone_number = PIH.DATA.FORMAT.telephone_number(telephone_number)
                return PIH.MESSAGE.WHATSAPP.WAPPI.send_video(telephone_number, caption, base64_value, wappi_profile)

            @staticmethod
            def send_image(telephone_number: str, caption: str, base64_value: str, wappi_profile: Any | None = None) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                telephone_number = PIH.DATA.FORMAT.telephone_number(
                    telephone_number)
                return PIH.MESSAGE.WHATSAPP.WAPPI.send_image(telephone_number, caption, base64_value, wappi_profile)
        
            @staticmethod
            def send_document(telephone_number: str, caption: str, base64_value: str, wappi_profile: Any | None = None) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value)
                telephone_number = PIH.DATA.FORMAT.telephone_number(
                    telephone_number)
                return PIH.MESSAGE.WHATSAPP.WAPPI.send_document(telephone_number, caption, base64_value, wappi_profile)

            @staticmethod
            def send_to_user(user: User, message: Any, via_wappi: bool = True, use_alternative: bool = True, wappi_profile: Any | None = None) -> bool:
                return PIH.MESSAGE.WHATSAPP.send(user.telephoneNumber, message, via_wappi, use_alternative, EnumTool.get_value(
                    wappi_profile, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT.value))

        class DELAYED:

            @staticmethod
            def register(message: DelayedMessage) -> int:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.register_delayed_message, PIH.ACTION.MESSAGE.DELAYED.prepeare_message(message)))

            @staticmethod
            def send(message: DelayedMessage, high_priority: bool = True) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.send_delayed_message, (PIH.ACTION.MESSAGE.DELAYED.prepeare_message(message), high_priority)))

    class CARD_REGISTRY:

        @staticmethod
        def set_folder_for_person(folder_name: str | None, person_or_pin: PolibasePerson | int, already_set: bool = False) -> bool:
            result: bool = already_set or PIH.ACTION.POLIBASE.set_card_registry_folder(folder_name, person_or_pin)
            event_builder = PIH.EVENT.BUILDER.polibase_person_set_card_registry_folder
            if result:
                if DataTool.is_empty(folder_name):
                    PIH.ACTION.EVENTS.remove(*event_builder(None, person_or_pin))
                    result = True
                else:
                    event_ds: EventDS | None = ResultTool.get_first_item(PIH.RESULT.EVENTS.get(
                        *event_builder(None, person_or_pin)))
                    allow_to_add: bool = False
                    if DataTool.is_not_none(event_ds):
                        card_registry_folder: str = event_ds.parameters[FIELD_NAME_COLLECTION.CARD_REGISTRY_FOLDER]
                        allow_to_add = card_registry_folder != folder_name
                        if allow_to_add:
                            PIH.ACTION.EVENTS.remove(
                                *event_builder(card_registry_folder, person_or_pin))
                    else:
                        PIH.EVENT.send(
                            *event_builder(folder_name, person_or_pin))
            return result

        @staticmethod
        def start_card_sorting_for(folder_name: str) -> None:
            event_builder_function: Callable[[None], Events | tuple[Events, tuple[Any]]] = PIH.EVENT.BUILDER.card_registry_folder_start_card_sorting
            PIH.ACTION.EVENTS.remove(
                *event_builder_function(folder_name))
            PIH.ACTION.EVENTS.remove(
                    *PIH.EVENT.BUILDER.card_registry_folder_complete_card_sorting(folder_name))
            PIH.EVENT.send(*event_builder_function(folder_name))

        @staticmethod
        def complete_card_sorting_for(folder_name: str) -> None:
            event_builder_function: Callable[[None], Events | tuple[Events, tuple[Any]]
                                   ] = PIH.EVENT.BUILDER.card_registry_folder_complete_card_sorting
            PIH.ACTION.EVENTS.remove(*event_builder_function(folder_name))
            PIH.EVENT.send(*event_builder_function(folder_name))

        @staticmethod
        def folder_is_sorted(folder_name: str | None) -> bool:
            if DataTool.is_empty(folder_name):
                return False
            return not ResultTool.is_empty(PIH.RESULT.EVENTS.get(*PIH.EVENT.BUILDER.card_registry_folder_complete_card_sorting(folder_name)))
        
        @staticmethod
        def persons_by_folder(folder_name: str, polibase_person_list_result: Result[list[PolibasePerson]] | None = None) -> Result[list[PolibasePerson]]:
            folder_is_sorted: bool = PIH.CARD_REGISTRY.folder_is_sorted(folder_name)
            polibase_person_list_result = polibase_person_list_result or PIH.RESULT.POLIBASE.persons_by_card_registry_folder(folder_name)
            if folder_is_sorted:
                ResultTool.sort(polibase_person_list_result, PIH.DATA.POLIBASE.sort_person_list_by_pin)
            else:
                polibase_person_list_map: dict[int, PolibasePerson] = {person.pin : person for person in polibase_person_list_result.data}
                polibase_person_list: list[PolibasePerson] = []
                polibase_person_pin_list: list[int] = PIH.CARD_REGISTRY.persons_pin_by_folder(folder_name)
                for pin in polibase_person_pin_list:
                    if DataTool.is_in(polibase_person_list_map, pin):
                        polibase_person_list.append(polibase_person_list_map[pin])
                polibase_person_list_result.data = polibase_person_list
            return polibase_person_list_result

        @staticmethod
        def persons_pin_by_folder(folder_name: str) -> list[int]:
            def map_function(value: EventDS | PolibasePerson) -> int:
                if isinstance(value, PolibasePerson):
                    return value.pin
                return value.parameters[FIELD_NAME_COLLECTION.PERSON_PIN]
            folder_is_sorted: bool = PIH.CARD_REGISTRY.folder_is_sorted(folder_name)
            if folder_is_sorted:
                return list(map(map_function, PIH.DATA.POLIBASE.sort_person_list_by_pin(PIH.RESULT.POLIBASE.persons_by_card_registry_folder(folder_name).data)))
            def sort_function(event: EventDS) -> datetime:
                return event.timestamp
            return ResultTool.map(ResultTool.sort(PIH.RESULT.EVENTS.get(*PIH.EVENT.BUILDER.polibase_person_set_card_registry_folder(folder_name)), sort_function), map_function).data

    class ACTION:

        class PATH:

            @staticmethod
            def listen(value: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.listen_for_new_files, (value, )))   

        class ACTIONS:

            @staticmethod
            def was_done(action: Actions | str, user_login_or_user: str | User | None = None, parameters: list = []) -> bool | None:
                user: User | None = None
                if isinstance(user_login_or_user, User):
                    user = user_login_or_user
                if DataTool.is_empty(user_login_or_user) or isinstance(user_login_or_user, str):
                    user = PIH.RESULT.USER.by_login(user_login_or_user or AD.USER.ADMINISTRATOR, True, True).data
                _action: Actions | None = PIH.DATA.ACTIONS.get(action)
                if DataTool.is_none(_action):
                    return None
                PIH.EVENT.send(Events.ACTION_WAS_DONE, (EnumTool.get(
                    _action).description, _action.name, user.name, user.samAccountName, parameters))
                return True

            @staticmethod
            def have_to_be_done(action: Actions | str) -> bool | None:
                _action: Actions | None = PIH.DATA.ACTIONS.get(action)
                if DataTool.is_none(_action):
                    return None
                PIH.EVENT.send(Events.ACTION_HAVE_TO_BE_DONE, (_action.name, EnumTool.get(_action).description))
                return True

        class EVENTS:
    
            @staticmethod
            def register(value: Events, parameters: dict[str, Any] | None = None, remove_before: bool = False) -> bool:
                if remove_before:
                    PIH.ACTION.EVENTS.remove(value, parameters)
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.register_event, (EventDS(value.name, parameters, DateTimeTool.now()), )))

            @staticmethod
            def update(value: Events, parameter_for_search: tuple[Any], parameters_for_set: tuple[Any]) -> bool:
                return PIH.ACTION.EVENTS.remove(value, parameter_for_search) and PIH.ACTION.EVENTS.register(value, PIH.EVENT.BUILDER.create_parameters_map(value, parameters_for_set))

            @staticmethod
            def remove(value: Events, parameters: tuple[Any] | dict[str, Any] | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.remove_event, EventDS(value.name, DataTool.check(isinstance(parameters, dict), parameters, lambda: PIH.EVENT.BUILDER.create_parameters_map(value, parameters, check_for_parameters_count=False)))))

        class NOTES:
        
            @staticmethod
            def create(name: str, note: Note) -> bool:
                id: str | None = DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_note, (note, )))
                if DataTool.is_empty(id):
                    return False
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.add_gkeep_map_item, (name, id)))

        class QR_CODE:

            @staticmethod
            def titled(data: str, title, path: str, font_size: int | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_qr_code, (data, title, path, font_size)))

            @staticmethod
            def print(path: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.print_image, (path, )))

            @staticmethod
            def for_mobile_helper_command(value: str, title: str, path: str, font_size: int | None = None) -> bool:
                return PIH.ACTION.QR_CODE.titled(PIH.DATA.FORMAT.mobile_helper_qr_code_text(PIH.DATA.FORMAT.mobile_helper_command(value)), title, path, font_size)
            
            @staticmethod
            def for_polibase_person_card_registry_folder(name: str) -> bool:
                name = PIH.DATA.FORMAT.polibase_person_card_registry_folder(name)
                return PIH.ACTION.QR_CODE.for_mobile_helper_command(" ".join(["card", "registry", urllib.parse.quote(name)]), name, PIH.PATH.QR_CODE.polibase_person_card_registry_folder(name), 80)

        class INDICATION:

            class CT:

                @staticmethod
                def register(value: CTIndicationsValue, forced: bool = False) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.register_ct_indications_value, (value, forced)))

            class CHILLER:
                    
                @staticmethod
                def register(value: ChillerIndicationsValue, forced: bool = False) -> bool:
                    data: dict = PIH.SERVICE.call_command(ServiceCommands.register_chiller_indications_value, (value, forced))
                    return not DataTool.is_empty(data)

        class MOBILE_HELPER:

            @staticmethod
            def send_message(value: str, recipient: str | Enum, flags: int | None = None) -> bool:    
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.send_mobile_helper_message, (value, recipient if isinstance(recipient, str) else EnumTool.get(recipient), flags)))

        class BACKUP:

            @staticmethod
            def attach_shared_disks(name: str | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.attach_shared_disks, (name, )))

            @staticmethod
            def start_robocopy_job(name: str | None = None, source: str | None = None, destination: str | None = None, force: bool = False) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.robocopy_start_job, (name, source, destination, force)))

            @staticmethod
            def start_robocopy_job_by_name(value: str, force: bool = False) -> bool:
                return PIH.ACTION.BACKUP.start_robocopy_job(value, force=force)

        class DATA_STORAGE:

            @staticmethod
            def value(value: Any, name: str | None = None, section: str | None = None) -> bool:
                try:
                    name = name or value.__getattribute__("name")
                except AttributeError as error:
                    pass
                else:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_storage_value, (name, value, section)))

        class MESSAGE:

            class DELAYED:

                @staticmethod
                def update(value: DelayedMessageDS, search_critery: MessageSearchCritery) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.update_delayed_message, (value, search_critery)))

                @staticmethod
                def update_status(value: DelayedMessageDS, status: MessageStatuses) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update(DelayedMessageDS(status=status.value), MessageSearchCritery(id=value.id))

                @staticmethod
                def complete(value: DelayedMessageDS) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update_status(value, MessageStatuses.COMPLETE)

                @staticmethod
                def abort(value: DelayedMessageDS) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update_status(value, MessageStatuses.ABORT)

                @staticmethod
                def prepeare_message(message: DelayedMessage) -> DelayedMessage:
                    if message.type is None:
                        message.type = MessageTypes.WHATSAPP.value
                    if message.date is not None:
                        if isinstance(message.date, datetime):
                            message.date = DateTimeTool.datetime_to_string(
                                message.date, CONST.DATA_STORAGE.DATETIME_FORMAT)
                    if message.sender is not None:
                        message.sender = EnumTool.get_value(message.sender)
                    if  message.type == MessageTypes.WHATSAPP.value and not DataTool.is_empty(message.recipient):
                        if PIH.CHECK.telephone_number(message.recipient):
                            #+7 -> 7
                            message.recipient = PIH.DATA.FORMAT.telephone_number(message.recipient, CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX)
                    return message
        
        class SETTINGS:

            @staticmethod
            def key(key: str, value: Any) -> bool:
                return DataTool.rpc_unrepresent(
                    PIH.SERVICE.call_command(ServiceCommands.set_settings_value, (key, value)))

            @staticmethod
            def set(settings_item: SETTINGS | str, value: Any) -> bool:
                return PIH.ACTION.SETTINGS.key(if_else(isinstance(settings_item, str), settings_item, lambda: settings_item.value.key_name or settings_item.name), value)

            @staticmethod
            def set_default(settings_item: SETTINGS) -> bool:
                return PIH.ACTION.SETTINGS.set(settings_item, settings_item.value.default_value)

        class USER:

            @staticmethod
            def drop_user_cache() -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.drop_user_cache))

            @staticmethod
            def create_from_template(container_dn: str,
                                     full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_user_by_template, (container_dn, full_name, login, password, description, telephone, email)))

            @staticmethod
            def create_in_container(container_dn: str,
                                    full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_user_in_container, (container_dn, full_name, login, password, description, telephone, email)))

            @staticmethod
            def set_telephone_number(user: User, telephone: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_user_telephone_number, (user.distinguishedName, telephone)))

            @staticmethod
            def set_password(user: User, password: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_user_password, (user.distinguishedName, password)))

            @staticmethod
            def set_status(user: User, status: str, container: UserBase) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_user_status, (user.distinguishedName, status, DataTool.check(container, lambda: container.distinguishedName))))

            @staticmethod
            def remove(user: User) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.remove_user, user.distinguishedName))

        class TIME_TRACKING:

            @staticmethod
            def save_report(path: str, start_date: datetime, end_date: datetime, tab_number_list: list[str] | None = None, plain_format: bool = False) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.save_time_tracking_report, (path, DateTimeTool.start_date(start_date), DateTimeTool.end_date(end_date), tab_number_list, plain_format)))

        class INVENTORY:

            @staticmethod
            def create_barcodes(report_file_path: str, result_directory: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_barcodes_for_inventory, (report_file_path, result_directory)))

            @staticmethod
            def save_report_item(report_file_path: str, item: InventoryReportItem) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.save_inventory_report_item, (report_file_path, item)))

            @staticmethod
            def close_report(report_file_path: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.close_inventory_report, report_file_path))

        class PRINTER:

            @staticmethod
            def report() -> bool:
                return not ResultTool.is_empty(PIH.RESULT.PRINTER.report())

            @staticmethod
            def status() -> bool:
                return not ResultTool.is_empty(PIH.RESULT.PRINTER.status())

        class POLIBASE:

            executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=10)

            @staticmethod
            def client_program_close_for_all(notify: bool = True, notification_message: str | None = None, test: bool = True) -> None:
                def close_action(workstation: Workstation) -> None:
                    PIH.ACTION.POLIBASE.client_program_close_for_workstation(workstation)
                def filter_function(workstation: Workstation) -> bool:
                    return workstation.name == CONST.TEST.WORKSTATION_MAME if test else workstation.accessable 
                def every_action(workstation: Workstation) -> None:
                    PIH.ACTION.POLIBASE.executor.submit(close_action, workstation)
                if notify:
                    PIH.MESSAGE.POLIBASE.notify_about_polibase_closing(notification_message, test)
                ResultTool.every(ResultTool.filter(PIH.RESULT.WORKSTATION.all(), filter_function), every_action)

            @staticmethod
            def client_program_close_for_workstation(workstation: Workstation) -> bool:
                return PIH.ACTION.WORKSTATION.kill_process(
                    CONST.POLIBASE.PROCESS_NAME, workstation.name)

            def restart(test: bool = True) -> None:
                PIH.EXECUTOR.ws_reboot(HOSTS.POLIBASE_TEST.NAME if test else HOSTS.POLIBASE.NAME)

            class NOTIFICATION:

                @staticmethod
                def register(value: PolibasePersonVisitNotificationDS) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.register_polibase_person_visit_notification, value))

                class CONFIRMATION:

                    @staticmethod
                    def update(recepient: str, sender: str, status: int) -> bool:
                        return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.update_polibase_person_notification_confirmation, PolibasePersonNotificationConfirmation(recepient, sender, status)))

            class INFORMATION_QUEST:

                @staticmethod
                def register(person: PolibasePerson) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.register_polibase_person_information_quest, PolibasePersonInformationQuest(person.pin, person.FullName, person.telephoneNumber)))
                
                @staticmethod
                def start(person_or_pin: PolibasePerson | int) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.start_polibase_person_information_quest, (person_or_pin if isinstance(person_or_pin, int) else person_or_pin.pin, )))

                @staticmethod
                def update(value: PolibasePersonInformationQuest, search_critery: PolibasePersonInformationQuest) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.update_polibase_person_information_quest, (value, search_critery)))

            @staticmethod
            def create_barcode_for_person(person_or_pin: PolibasePerson | int, test: bool | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_barcode_for_polibase_person, (PIH.RESULT.POLIBASE._person_pin(person_or_pin), test)))

            @staticmethod
            def set_card_registry_folder(value: str | None, person_or_pin: PolibasePerson | int, test: bool | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_polibase_person_card_folder_name, (value, PIH.RESULT.POLIBASE._person_pin(person_or_pin), test)))

            @staticmethod
            def set_email(value: str, person: PolibasePerson, test: bool | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_polibase_person_email, (value, person.pin, test)))
            
            @staticmethod
            def set_telephone_number(index: int, value: str, person: PolibasePerson, test: bool | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_polibase_person_telephone_number, (index, value, person.pin, test)))

            @staticmethod
            def set_barcode(value: str, person: PolibasePerson, test: bool | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_barcode_for_polibase_person, (value, person.pin, test)))

            class DB:

                @staticmethod
                def backup(dump_file_name: str | None = None, test: bool | None = None) -> bool:
                    return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_polibase_database_backup, (dump_file_name, test)))

            class VISIT:

                class DATA_STORAGE:

                    @staticmethod
                    def update(value: PolibasePersonVisitDS) -> bool:
                        return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.update_polibase_person_visit_to_data_stogare, value))

        class MARK:

            @staticmethod
            def create(full_name: FullName, person_division_id: int,  tab_number: str, telephone: str | None = None) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_mark, (full_name, person_division_id, tab_number, telephone)))

            @staticmethod
            def set_full_name_by_tab_number(full_name: FullName, tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_full_name_by_tab_number, (full_name, tab_number)))

            @staticmethod
            def set_telephone_by_tab_number(telephone: str, tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.set_telephone_by_tab_number, (telephone, tab_number)))

            @staticmethod
            def make_as_free_by_tab_number(tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.make_mark_as_free_by_tab_number, tab_number))

            @staticmethod
            def make_as_temporary(temporary_mark: Mark, owner_mark: Mark) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.make_mark_as_temporary, (temporary_mark.TabNumber, owner_mark.TabNumber)))

            @staticmethod
            def remove(mark: Mark) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.remove_mark_by_tab_number, mark.TabNumber))

        class DOCUMENTS:

            @staticmethod
            def create_statistics_chart(type: STATISTICS.Types) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_statistics_chart, (type.name, )))

            @staticmethod 
            def save_base64_as_image(path: str, content: str) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.save_base64_as_image, (path, content)))

            @staticmethod
            def create_for_user(path: str, full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> bool:
                locale.setlocale(locale.LC_ALL, 'ru_RU')
                date_now = datetime.now().date()
                date_now_string = f"{date_now.day} {calendar.month_name[date_now.month]} {date_now.year}"
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.create_user_document, (path, date_now_string, CONST.SITE_ADDRESS, CONST.SITE_PROTOCOL + CONST.SITE_ADDRESS, CONST.EMAIL_SERVER_ADDRESS, full_name, tab_number, pc, polibase, email)))

        class WORKSTATION:
    
            @staticmethod
            def reboot(host: str | None = None, force: bool = False) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.reboot, (host, force)))

            @staticmethod
            def shutdown(host: str | None = None, force: bool = False) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.shutdown, (host, force)))
            
            @staticmethod
            def kill_process(name_or_pid: str | int, host: str, via_standart_tools: bool = True) -> bool:
                return DataTool.rpc_unrepresent(PIH.SERVICE.call_command(ServiceCommands.kill_process, (name_or_pid, host, via_standart_tools)))
            
            @staticmethod
            def kill_python_process(host: str, via_standart_tools: bool = False) -> bool:
                return PIH.ACTION.WORKSTATION.kill_process(CONST.PYTHON.EXECUTOR, host, via_standart_tools)   

class ActionStack(list):

    def __init__(self, caption: str = "", *argv: Callable[[], ActionValue], input: InputBase = None, output: OutputBase = None):
        self.input = input or PIH.input
        self.output = output or PIH.output
        self.acion_value_list: list[ActionValue] = []
        self.caption = caption
        for arg in argv:
            self.append(arg)
        self.start()

    def call_actions_by_index(self, index: int = 0, change: bool = False):
        previous_change: bool = False
        while True:
            try:
                action_value: ActionValue = self[index]()
                if action_value:
                    if change or previous_change:
                        previous_change = False
                        if index < len(self.acion_value_list):
                            self.acion_value_list[index] = action_value
                        else:
                            self.acion_value_list.append(action_value)
                    else:
                        self.acion_value_list.append(action_value)
                index = index + 1
                if index == len(self) or change:
                    break
            except KeyboardInterrupt:
                self.output.new_line()
                self.output.error("Повтор предыдущих действия")
                self.output.new_line()
                if index > 0:
                    previous_change = True
                    #self.show_action_values()
                    #index = index - 1
                else:
                    continue

    def show_action_values(self) -> None:
        def label(item: ActionValue, _):
            return item.caption
        self.call_actions_by_index(self.input.index(
            "Выберите свойство для изменения, введя индекс", self.acion_value_list, label), True)

    def start(self):
        self.call_actions_by_index()
        while True:
            self.output.new_line()
            self.output.head2(self.caption)
            for action_value in self.acion_value_list:
                self.output.value(action_value.caption, action_value.value)
            if self.input.yes_no("Данные верны", True):
                break
            else:
                self.show_action_values()

class A:

    root = PIH()

    MIO = root.MIO

    IW = root.INPUT_WAIT

    R = root.RESULT
    D = root.DATA
    D_V = D.VARIABLE
    D_TN = D.TELEPHONE_NUMBER
    D_MR = D.MATERIALIZED_RESOURCES
    D_FL = D.FILTER
    D_Ex = D.EXTRACT
    D_Ex_E = D_Ex.EVENT
    D_M = D.MARK
    D_C = D.CHECK
    D_STAT = D.STATISTICS
    A = root.ACTION
    
    A_D = A.DOCUMENTS
    A_QR = A.QR_CODE
    A_I = A.INDICATION
    A_I_CT = A_I.CT
    A_I_CH = A_I.CHILLER
    ME = root.MESSAGE
    ME_P = ME.POLIBASE
    A_WS = A.WORKSTATION
    R_ME = R.MESSAGE
    R_R = R.RESOURCES
    R_RCG = R.RECOGNIZE
    R_SSH = R.SSH
    R_I = R.INDICATIONS
    R_N = R.NOTES
    R_E = R.EVENTS
    #
    A_ME = A.MESSAGE
    A_ACT = A.ACTIONS
    A_TT = A.TIME_TRACKING
    A_MIO = A.MOBILE_HELPER
    R_ME_D = R_ME.DELAYED
    A_ME_D = A_ME.DELAYED
    A_N = A.NOTES
    A_E = A.EVENTS
    
    #
    ME_WS = ME.WORKSTATION
    ME_P = ME.POLIBASE
    ME_WH = ME.WHATSAPP
    ME_D = ME.DELAYED
    ME_WH_W = ME_WH.WAPPI
    ME_WH_W_Q = ME_WH_W.QUEUE
    A_ME_WH_W_Q = ME_WH_W.QUEUE
    #
    S = root.SETTINGS
    S_U = S.USER
    S_P = S.POLIBASE
    S_R = S.RESOURCE
    S_WS = S.WORKSTATION
    S_P_V = S_P.VISIT
    S_P_RN = S_P.REVIEW_NOTIFICATION
    #
    C = root.CHECK
    D_ACT = D.ACTIONS
    C_R = C.RESOURCE
    C_I = C.INDICATION
    C_M = C.MARK
    C_TT = C.TIME_TRACKING
    C_A = C.ACCESS
    C_S = C.SETTINGS
    C_WS = C.WORKSTATION
    C_ME = C.MESSAGE
    C_ME_WH = C_ME.WHATSAPP
    C_ME_WH_W = C_ME_WH.WAPPI
    C_N = C.NOTES
    C_RCG = C.RECOGNIZE
    #
    A_M = A.MARK
    R_M = R.MARK
    R_U = R.USER
    R_TT = R.TIME_TRACKING
    A_U = A.USER
    C_U = C.USER
    D_F = D.FORMAT
    D_F_B = D_F.BACKUP
    D_CO = D.CONVERT
    A_P = A.POLIBASE
    C_E = C.EVENTS
    C_P = C.POLIBASE
    C_P_DB = C_P.DATABASE
    D_P = D.POLIBASE
    R_P = R.POLIBASE
    R_PR = R.PRINTER
    R_SRVS = R.SERVERS
    #
    A_PTH = A.PATH
    A_P_V = A_P.VISIT
    A_P_V_DS = A_P_V.DATA_STORAGE
    R_P_V = R_P.VISIT
    R_P_V_DS = R_P_V.DATA_STORAGE
    A_P_N = A_P.NOTIFICATION
    A_P_N_C = A_P_N.CONFIRMATION
    R_P_N = R_P.NOTIFICATION
    R_P_N_C = R_P_N.CONFIRMATION
    C_P_N = C_P.NOTIFICATION
    C_P_N_С = C_P_N.CONFIRMATION
    R_WS = R.WORKSTATION
    C_WS = C.WORKSTATION
    A_P_IQ = A_P.INFORMATION_QUEST
    R_P_IQ = R_P.INFORMATION_QUEST
    SRV = root.SERVICE
    SRV_A = SRV.ADMIN
    I = root.input
    I_U = I.user
    A_B = A.BACKUP
    R_B = R.BACKUP
    O = root.output
    SE = root.session
    A_DS = A.DATA_STORAGE
    R_DS = R.DATA_STORAGE
    V = root.VERSION
    OS = root.OS
    U = root.UPDATE
    EXC = root.EXECUTOR
    ER = root.ERROR
    E = root.EVENT
    E_B = E.BUILDER
    PTH = root.PATH
    PTH_DS = PTH.DATA_STORAGE
    PTH_U = PTH.USER
    PTH_P = PTH.POLIBASE
    PTH_QR = PTH.QR_CODE
    PTH_FNT = PTH.FONTS
    PTH_I = PTH.INDICATIONS
    L = root.LOG

    CT = CONST
    CT_LNK = LINK
    CT_EMAIL = EMAIL
    CT_MR = MATERIALIZED_RESOURCES
    CT_WINDOWS = WINDOWS
    CT_SCN = SCAN
    CT_EVM = EmailVerificationMethods
    CT_D = DATA
    CT_DT = DocumentTypes
    CT_RBK = ROBOCOPY
    CT_H = HOSTS
    CT_FNT = FONT
    CT_SR = ServiceRoles
    CT_SC = ServiceCommands
    CT_SubT = SubscribtionTypes
    CT_F = FILE
    CT_R = RESOURCES
    CT_R_D = CT_R.DESCRIPTIONS
    CT_R_IR = CT_R.InaccessableReasons
    CT_STATISTICS = STATISTICS
    CT_F_E = CT_F.EXTENSION
    CT_P = CT.POLIBASE
    CT_P_DD = CT_P.DocumentDescriptions
    CT_FC = FIELD_COLLECTION
    CT_S = SETTINGS
    CT_ME = CT.MESSAGE
    CT_ME_WH = CT_ME.WHATSAPP
    CT_ME_WH_W = CT_ME_WH.WAPPI
    CT_L_ME_F = LogMessageFlags
    CT_L_ME_CH = LogMessageChannels
    CT_V = CT.VISUAL
    CT_E = Events
    CT_ACT = Actions
    CT_MD = MEDICAL_DOCUMENT
    CT_MD_DT = CT_MD.DirectionTypes
    CT_DS = CT.DATA_STORAGE
    CT_FNC = FIELD_NAME_COLLECTION
    CT_FCA = FieldCollectionAliases
    CT_UP = USER_PROPERTIES
    CT_AD = AD
    CT_AD_U = AD.USER
    CT_I = INDICATIONS
    C_P_DB = C_P.DATABASE
    D_P = D.POLIBASE
    R_P = R.POLIBASE
    R_PR = R.PRINTER

    CR = root.CARD_REGISTRY
    #