from typing import Any, Callable
import importlib.util
import sys
from subprocess import CompletedProcess
from typing import Any
from datetime import datetime
import os
import re

pih_exists = importlib.util.find_spec("pih.pih") is not None
if not pih_exists:
    sys.path.append("//pih/facade")
from pih.const import (MarkType, 
                       PASSWORD, 
                       PasswordSettings, 
                       CheckableSections, 
                       FILE)
from pih import (PIH,
                A, 
                ActionValue, 
                ActionStack, 
                Input,
                Output, 
                Session, 
                while_not_do)
from pih.errors import NotFound
from pih.collection import (Mark, 
                            User, 
                            FullName, 
                            PersonDivision,
                            UserBase, 
                            LoginPasswordPair, 
                            MarkGroup, 
                            Result, 
                            FieldItemList,
                            WorkstationDescription, 
                            ResourceStatus, 
                            SiteResourceStatus,
                            CTIndicationsValue, 
                            Workstation, 
                            RobocopyJobStatus, 
                            ChillerIndicationsValueContainer, 
                            PrinterReport, 
                            DiskStatistics)
from pih.tools import j, nl

class ConsoleAppsApi:

    LINE: str = "........................................................"

    def __init__(self, pih: PIH | None = None):
        self.pih = pih or PIH
        self.full_name: FullName | None = None
        self.tab_number: str | None = None
        self.telephone_number: str | None = None
        self.division_id: int | None = None
        self.user_is_exists: bool = False
        self.login: str | None = None
        self.password: str | None = None
        self.internal_email: str | None = None
        self.external_email: str | None = None
        self.email_password: str | None = None
        self.polibase_login: str | None = None
        self.polibase_password: str | None = None
        self.user_container: UserBase
        self.description: str | None = None
        self.use_template_user: bool
        self.need_to_create_mark: bool | None = None

    def create_qr_code_for_mobile_helper_command(self, command: str | None = None, title: str | None = None, show_result: bool = True) -> str | None:
        command = command or self.input.input("Введите название команды")
        title = title or self.input.input("Введите заголовок")
        result: bool = A.A_QR.for_mobile_helper_command(command, title, os.path.join(A.PTH.MOBILE_HELPER.QR_CODE_FOLDER, A.PTH.replace_prohibited_symbols_from_path_with_symbol(A.PTH.add_extension(command, FILE.EXTENSION.PNG))), 56)
        qr_code_image_path: str = A.PTH_QR.mobile_helper_command(command)
        if show_result:
            if result:
                self.output.good(
                    j((nl(f"Файл qr кода {self.bold(title)} создан."), nl("Путь к файлу:"), nl(self.bold(qr_code_image_path)))))
            else:
                self.output.error("qr код не был создан")
        return qr_code_image_path

    def create_qr_code_for_card_registry_folder(self, card_registry_folder_name: str | None = None, show_result: bool = True) -> list[str]:
        if A.D_C.empty(card_registry_folder_name):
            card_registry_folder_name = self.input.input(f"Введите название папки (или несколько значений названий папок разделенной запятой или пробелом)")
        card_registry_folder_name_list: list[str] = re.split("\W+", card_registry_folder_name)
        card_registry_folder_name_list = list(map(lambda item: str(item).strip(), card_registry_folder_name_list))
        result_path_list: list[str] = []
        for card_registry_folder_name_item in card_registry_folder_name_list:
            card_registry_folder_name_item = A.D_F.polibase_person_card_registry_folder(card_registry_folder_name_item)
            result: bool = A.A_QR.for_polibase_person_card_registry_folder(card_registry_folder_name_item)
            qr_code_image_path: str = PIH.PATH.QR_CODE.polibase_person_card_registry_folder(card_registry_folder_name_item)
            if show_result and len(card_registry_folder_name_list) == 1:
                if not result:
                    self.output.error("qr код не был создан")
            if result:
                result_path_list.append(qr_code_image_path)
        return result_path_list
    
    def disks_information(self, host: str | None = None) -> None:
        host = host or self.input.input("Введите название хоста (компьютера или сервера)")
        with self.output.make_indent(2, True):
            if A.C_R.accessibility_by_ping(host):
                disk_statistics_list: list[DiskStatistics] = list(filter(lambda item: item.size > 0, A.EXC.get_disk_statistics_list(host)))
                if A.D_C.empty(disk_statistics_list):
                    self.output.error("Хост не имеет дисков")
                else:
                    self.output.write_line(nl("Информация о дисках:"))
                    for disk_statistics in disk_statistics_list:
                        self.output.write_line(f"{A.CT_V.BULLET} {self.bold(disk_statistics.name)}: {A.D_F.size(disk_statistics.free_space)} из {A.D_F.size(disk_statistics.size)}")
            else:
                self.output.error("Хост не доступен или не найден")

    @property
    def is_mobile(self) -> bool:
        return self.session.name == "mobile"

    def resources_and_indications_check(self, checkable_section_list: list[CheckableSections], ask_for_update_before: bool = False, force_update: bool = False, all: bool = False) -> None:
        with self.output.make_indent(2):
            if CheckableSections.RESOURCES in checkable_section_list or (
                CheckableSections.WS in checkable_section_list\
                or CheckableSections.SERVERS in checkable_section_list):
                def label_function(resource: ResourceStatus, index: int) -> str:
                    result: list[str] = [] 
                    accessable: bool = resource.accessable
                    status: str = A.D_F.yes_no(accessable, True)
                    result.append(" ".join((status, self.bold(self.output.blue_str(
                        resource.name)))))
                    if isinstance(resource, SiteResourceStatus):
                        if resource.check_free_space_status:
                            free_space_result_list: str = resource.free_space_status.split(" ")
                            result.append(f"      Cвободное место: {free_space_result_list[0]} ({free_space_result_list[1]})")
                        if resource.check_certificate_status:
                            result.append(f"      Сертификат доступен до: {resource.certificate_status}")
                    return A.CT.NEW_LINE.join(result)
                force_update = force_update or (ask_for_update_before and self.input.yes_no(
                    "Обновить перед получением"))
                if force_update:
                    self.output.write_line(
                        self.italic(f"{self.get_formatted_given_name()}, ожидайте получение результата..."))
                for checkable_section in [CheckableSections.RESOURCES, CheckableSections.WS, CheckableSections.SERVERS]:
                    if checkable_section in checkable_section_list:
                        if self.is_mobile:
                            self.output.new_line()
                        if all:
                            self.output.write_line(" ".join((A.CT_V.BULLET, self.bold(A.D.check(checkable_section == CheckableSections.RESOURCES, "Основные ресурсы", A.D.check(checkable_section == CheckableSections.WS, "Наблюдаемые компьютеры", "Сервера"))))))
                        with self.output.make_indent(2, True):
                            self.output.write_result(A.R_R.get_status_list([checkable_section], force_update, all if len(checkable_section_list) == 1 and CheckableSections.WS in checkable_section_list else False), False, label_function=label_function, separated_result_item=self.is_mobile)
            if CheckableSections.INDICATIONS in checkable_section_list:
                with A.ER.detect():
                    if self.is_mobile:
                        self.output.new_line()
                    self.output.write_line(self.bold(f"{A.CT_V.BULLET} Показания в помещении КТ"))
                    with self.output.make_indent(2, True):
                        self.output.write_result(A.R_I.last_ct_value_containers(True))
                        path: str = A.PTH.STATISTICS.get_file_path(A.D.get(A.CT_STATISTICS.Types.CT))
                        self.output.write_image(j(("   ", A.CT_V.BULLET, " ", self.output.bold("График показаний"))), A.D_CO.file_to_base64(path))
                    self.output.separated_line()
                    self.output.write_line(self.bold(f"{A.CT_V.BULLET} Показания в техническом помещении МРТ"))
                    chiller_indications_value_container_result: Result[list[ChillerIndicationsValueContainer]] = A.R_I.last_chiller_value_containers(True)
                    chiller_indications_value_container: ChillerIndicationsValueContainer = A.R.get_first_item(chiller_indications_value_container_result)
                    path: str = A.PTH_I.CHILLER_DATA_IMAGE_LAST
                    modification_timstamp: float = A.PTH.get_modification_time(path)
                    file_creating_datetime: datetime | None = datetime.fromtimestamp(modification_timstamp if modification_timstamp > 0 else A.PTH.get_creation_time(path))
                    with self.output.make_indent(2, True):
                        if A.C_E.has(A.E_B.chiller_was_turned_off()):
                            self.output.write_line(j((A.CT_V.WARNING, "Чиллер выключен!", A.CT_V.WARNING)))
                        else:
                            self.output.write_result(chiller_indications_value_container_result, title="Показания чиллера\n" if A.D_C.INDICATIONS.chiller_value_actual(chiller_indications_value_container) else f"{self.bold('Внимание!')}: Показания чиллера неактуальны\n", separated_result_item=False)
                            self.output.write_image(f"    Изображение дисплея чиллера\nВремя снятия: {A.D_F.datetime(file_creating_datetime)}", A.D_CO.file_to_base64(A.PTH_I.CHILLER_DATA_IMAGE_LAST_RESULT))
            if CheckableSections.MATERIALIZED_RESOURCES in checkable_section_list:
                if self.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(f"{A.CT_V.BULLET} Материальные ресурсы"))
                with self.output.make_indent(2, True):
                    for resource_type in A.CT_MR.TYPES:
                        self.output.write_line(f"{A.CT_V.BULLET} {self.bold(A.D.get(resource_type).description)}")
                        with self.output.make_indent(2, True):
                            self.output.write_line(nl(j((nl(), self.output.bold("Количество"), ": ", str(A.D_MR.get_count(resource_type)), " штук"))))
                            self.output.write_line(A.D_F.statistics(resource_type))
                            self.output.write_image(f"   {A.CT_V.BULLET} График выработки фильтров чиллера МРТ", A.D_CO.file_to_base64(
                                A.PTH.STATISTICS.get_file_path(resource_type.name)))
            if CheckableSections.VALENTA in checkable_section_list:
                scanned_file_path_list: list[str] = A.PTH.get_file_list_by_directory_info(
                    A.PTH.WS_816_SCAN.VALUE)
                count: int = len(scanned_file_path_list)
                if self.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(f"{A.CT_V.BULLET} Новые исследования в Валенте: " + ("Нет" if count == 0 else f"Да ({count})")))    
                if count > 0:
                    if self.input.yes_no("Показать отсканированные изображения"):
                        for scanned_file_path in scanned_file_path_list:
                            self.output.write_image(j(("Дата создания файла: ", A.D_F.datetime(datetime.fromtimestamp(A.PTH.get_creation_time(scanned_file_path))))),
                                A.D_CO.file_to_base64(scanned_file_path))
                    if self.input.yes_no("Синхронизировать Валенту"):
                        A.A_ACT.was_done(A.CT_ACT.VALENTA_SYNCHRONIZATION, self.session.user)
            if CheckableSections.PRINTERS in checkable_section_list:
                def printer_report(printer_report: PrinterReport) -> str:
                    report_list: list[str] = []
                    admin_description_list: list[str] = ("" or printer_report.adminDescription).split(",")
                    name: str = printer_report.ip.split('.')[0]
                    report_list.append(f"{self.bold('Модель')}: {printer_report.model}\n{self.bold('Название')}: {name}\n{self.bold('Описание')}: {printer_report.description}")
                    if printer_report.name != -401 and "infoless" not in admin_description_list:   
                        for item in (("Тонер", printer_report.get_toner), None if "drumless" in admin_description_list else ("Драм-юнит", printer_report.get_drum)):
                            if A.D.is_not_none(item):
                                report_list.append(f" {A.CT_V.BULLET} {self.bold(item[0])}")
                                def get_value(function: Callable[[str], int], color: str) -> str:
                                    value: int = function(color)
                                    result: str = str(value)
                                    if value < 5:
                                        result += j((" ", A.CT_V.WARNING))
                                    return result
                                report_list += [f"   {self.bold(color.upper())}: {get_value(item[1], color)}" for color in (
                                    ["k"] if "bw" in admin_description_list else ["c", "m", "y", "k"])]
                    else:
                        report_list.append(f"Принтер {A.D.check(printer_report.accessable, '', 'не ')}доступен")
                    return nl().join(report_list)
                if self.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(f"{A.CT_V.BULLET} Отчет по принтерам"))
                printer_report_list: list[PrinterReport] = A.R_PR.report().data
                for printer_report_item in printer_report_list:
                    self.output.separated_line()
                    with self.output.make_indent(2, True):
                        self.output.write_line(printer_report(printer_report_item))
            if not all:
                if CheckableSections.BACKUPS in checkable_section_list:
                    robocopy_job_status_list: Result[list[RobocopyJobStatus]] = A.R_B.robocopy_job_status_list()
                    sort_by_status: bool = self.input.yes_no("Сортировать по статусу", no_label=f"{self.bold(f'Сортировать по дате выполнения - {A.CT_V.NUMBER_SYMBOLS[0]}')}")
                    A.R.sort(robocopy_job_status_list, (lambda item: item.last_status or max(A.CT_RBK.STATUS_CODE.keys())) if sort_by_status else lambda item: datetime.fromtimestamp(0) if A.D_C.empty(item.last_created) else A.D.datetime_from_string(item.last_created), sort_by_status)
                    def job_status_item_label_function(job_status: RobocopyJobStatus, index: int) -> str:
                        name: str = job_status.name
                        source: str = job_status.source
                        destination: str = job_status.destination 
                        status: int | None = None
                        date: str | None = None
                        if job_status.active:
                            date = "выполняется"
                        else:
                            if job_status.last_created is not None:
                                date = f"{A.D_F.datetime(job_status.last_created)}"
                            status = job_status.last_status
                        variants: list[str] = ["--" if status is None else self.bold(str(status)), "--" if A.D_C.empty(date) else self.bold(date)]
                        return j((f" {A.CT_V.BULLET} ", variants[not sort_by_status], ": ", variants[sort_by_status], j((nl(), "   ", name, ": ", source, A.CT_V.ARROW, destination))))
                    variants: list[str] = [self.bold("Статус"), self.bold("Дата выполнения")]
                    self.output.write_result(
                        robocopy_job_status_list, False, label_function=job_status_item_label_function, separated_result_item=False, title=j((f" {A.CT_V.BULLET} ", variants[not sort_by_status], ": ", variants[sort_by_status], nl(), "   Название Robocopy-задания", nl(), ConsoleAppsApi.LINE)))

    def polibase_restart(self) -> None:
        if self.input.yes_no("Перезапустить сервер Polibase"):
            check_word: str = A.CT_P.NAME
            test: bool = not (check_word == self.input.input(
                f"Введите контрольное слово: {self.bold(check_word)}"))
            notify: bool = test or self.input.yes_no("Уведомить пользователей", True)
            title: str = f"Перезапуск Polibase{' test' if test else ''}"
            polibase_host: str = A.CT_H.POLIBASE_TEST.NAME if test else A.CT_H.POLIBASE.NAME
            self.output.write_line(A.L.it(
                f"{title}: Начат процесс закрытия программы Polibase на компьютерах."))
            A.A_P.client_program_close_for_all(notify, None, test)
            self.output.new_line()
            self.output.write_line(A.L.it(
                f"{title}: Начат процесс перезагрузки сервера Polibase."))
            A.A_P.restart(test)
            while_not_do(lambda: not A.C_R.accessibility_by_ping(
                polibase_host), sleep_time=5)
            self.output.new_line()
            self.output.write_line(A.L.it(
                    f"{title}: Начат процесс загрузки сервера Polibase."))
            while_not_do(lambda: A.C_R.accessibility_by_ping(polibase_host), sleep_time=5)
            self.output.new_line()
            A.E.wait_server_start(polibase_host)
            self.output.write_line(A.L.it(f"{title}: Завершен процесс загрузки сервера Polibase."))
            A.ME_P.notify_about_polibase_restarted(test)

    def polibase_client_program_close(self, search_value: str | None = None, for_all: bool = False) -> None:
        if for_all:
            check_word: str = A.CT_P.NAME
            test: bool = not (check_word == (search_value or self.input.input(
            f"Введите контрольное слово - {self.bold(check_word)}")))
            A.A_P.client_program_close_for_all(True, self.input.input("Введите сообщение для пользователей Polibase"), test) 
        else:
            try:
                workstation_list: Result[list[Workstation]] = A.R_WS.by_any(search_value or self.input.input("Введите запрос для поиска компьютера"))
                def every_action(workstation: Workstation) -> None:
                    if A.A_P.client_program_close_for_workstation(workstation):
                        self.output.good(f"Программа Polibase закрыта на компьютере {workstation.name}")
                A.R.every(workstation_list, every_action)
            except NotFound as error:
                self.output.error(error.get_details())
                search_value = None

    def process_kill(self, host_name: str | None, process_name: str | None) -> None:
        try:
            workstation_list: Result[list[Workstation]] = A.R_WS.by_any(host_name or self.input.input("Введите запрос для поиска компьютера"))
            def every_action(workstation: Workstation, process_name: str) -> None:
                process_value: int | str = process_name
                try:
                    process_value = int(process_value)
                except ValueError:
                    pass
                if A.A_WS.kill_process(process_value, workstation.name):
                    self.output.good(A.D.check(isinstance(process_value, str), f"Процесс с именем \"{process_value}\"", f"Программа с идентификационным номером {process_value}") + f" закрыта на компьютере {workstation.name}")
                else:
                    self.output.error("Процесс не найден")
            A.R.every(workstation_list, lambda workstation: every_action(workstation, process_name or self.input.input("Введите название процесса или его PID")))
        except NotFound as error:
            self.output.error(error.get_details())
            host_name = None

       
    @property
    def output(self) -> Output:
        return self.pih.output

    @property
    def input(self) -> Input:
        return self.pih.input

    def send_whatsapp_message(self, telephone_number: str, message: str) -> bool:
        return A.ME_WH_W.send(telephone_number, message, A.CT_ME_WH_W.Profiles.IT)

    def mark_find(self, value: str | None = None) -> None:
        self.output.mark.by_any(value or self.input.mark.any())

    def arg(self, index: int = 0, default_value: Any | None = None) -> Any:
        return self.session.arg(index, default_value)

    def register_ct_indications(self) -> None:
        text: str = f"число, которое может содержать дробную часть разделенную {self.bold('точкой')} или {self.bold('запятой')}"
        number_format_notification_text: str = f"- {self.italic(text)}"
        def float_check_function(value: str | None, show_error: bool = True) -> str | None:
            result: float | None = None
            if value is not None:
                result = A.D_Ex.float(value)
            if show_error and result is None:
                self.output.error(
                    f"Введите {self.bold('число')} {number_format_notification_text}")
            return None if result is None else str(result)
        temperature: float = float_check_function(self.arg(), False) or self.input.input(
            f"Введите значение {self.bold('температуры')} {number_format_notification_text}", check_function=float_check_function)
        humidity: float = float_check_function(self.arg(1), False) or self.input.input(
            f"Введите значение {self.bold('влажности')} {number_format_notification_text}", check_function=float_check_function)
        indications_value: CTIndicationsValue = CTIndicationsValue(temperature, humidity)
        if A.A_I_CT.register(indications_value):
            with self.output.send_to_group(A.CT_ME_WH.GROUP.CT_INDICATIONS):
                self.output.write_result(
                    Result(A.CT_FC.INDICATIONS.CT_VALUE, indications_value), title=f"{self.get_formatted_given_name()}, отправил следующие показания в помещение КТ:")
            self.output.good("Спасибо, показания отправлены")

    def find_free_mark(self, value: str | None = None) -> None:
        self.output.mark.result(A.R_M.by_any(
            value or self.input.mark.any()), "Список свободных карт доступа:")

    def find_user(self, value: str | None = None) -> None:
        try:
            result: Result[list[User]] = A.R_U.by_any(
                value or self.input.user.title_any())
        except NotFound as error:
            self.output.error(error.get_details())
        else:
            self.output.user.result(result, "Пользователи:")

    def create_password(self) -> str:
        password: str | None = None
        password_settings: PasswordSettings = PASSWORD.get(self.input.indexed_field_list(
            "Выберите тип пароля", A.CT_FC.POLICY.PASSWORD_TYPE))
        while True:
            password = self.input.user.generate_password(
                True, password_settings)
            self.output.value("Пароль", password)
            if self.input.yes_no("Использовать", True):
                break
        if self.input.yes_no("Отправить в ИТ отдел"):
            A.L.it(f"Сгенерированный пароль:")
            A.L.it(password)
        return password

    def make_mark_as_free(self, value: str | None = None) -> None:
        mark: Mark = self.input.mark.by_any(value)
        mark_type: int = A.D.get(MarkType, mark.type)
        if mark_type == MarkType.FREE:
            self.output.error(
                "Карта доступа с введенным номером уже свободная")
        else:
            if self.input.yes_no("Сделать карту свободной"):
                if mark_type == MarkType.TEMPORARY:
                    temporary_tab_number: int = mark.TabNumber
                    mark = A.R_M.temporary_mark_owner(
                        mark).data
                if A.A_M.make_as_free_by_tab_number(mark.TabNumber):
                    if mark_type == MarkType.TEMPORARY:
                        A.E.it_notify_about_temporary_mark_return(
                            mark, temporary_tab_number)
                    else:
                        A.E.it_notify_about_mark_return(mark)
                    self.output.good(
                        f"Карта доступа с номером {mark.TabNumber} стала свободной")
                else:
                    self.output.error("Ошибка")
            else:
                self.output.error("Отмена")

    def who_lost_the_mark(self, tab_number: str | None = None):
        try:
            tab_number = tab_number or self.input.tab_number()
            if tab_number is not None:
                try:
                    mark: Mark = A.R_M.by_tab_number(
                        tab_number).data
                    mark_type: MarkType = A.D.get(MarkType, mark.type)
                    if mark_type == MarkType.FREE:
                        self.output.good("Это свободная карта доступа")
                    elif mark_type == MarkType.GUEST:
                        self.output.good("Это гостевая карта доступа")
                    else:
                        if mark_type == MarkType.TEMPORARY:
                            mark = A.R_M.temporary_mark_owner(
                                mark).data
                            tab_number = mark.TabNumber
                            self.output.good("Это временная карта доступа")
                        if mark is not None:
                            telephone_number: str = mark.telephoneNumber
                            self.output.value("Персона", mark.FullName)
                            if not A.C.telephone_number(telephone_number):
                                user: User = A.R_U.by_tab_number(
                                    tab_number).data
                                if user is not None:
                                    telephone_number = user.telephoneNumber
                            if not A.C.telephone_number(telephone_number):
                                self.output.error(f"Телефон не указан")
                            else:
                                self.output.value(
                                    "Телефон", telephone_number)
                                if self.input.yes_no("Отправить сообщение", True):
                                    details: str = self.input.input(
                                        f"{self.get_formatted_given_name()}, уточните, где забрать найденную карту")
                                    if self.send_whatsapp_message(
                                            telephone_number, f"День добрый, {A.D.to_given_name(mark.FullName)}, вашу карту доступа ({tab_number}) нашли, заберите ее {details}"):
                                        self.output.good(
                                            "Сообщение отправлено")
                                    else:
                                        self.output.error(
                                            "Ошибка при отправке сообщения")
                        else:
                            self.output.error("Телефон не указан")
                except NotFound:
                    self.output.error(
                        "Карта доступа, с введенным номером не найдена")
        except KeyboardInterrupt:
            pass

    def bold(self, value: str) -> str:
        return self.output.bold(value)

    def italic(self, value: str) -> str:
        return self.output.italic(value)

    def run_command(self, command_list: list[str] | None = None) -> None:
        default_host: str = A.CT_H.DC2.NAME
        host: str | None = None
        def get_command_list() -> list[str]:
            command_list: tuple[list[str], list[str]] = A.D.dequotes(
                self.pih.input.input("Введите команду"))
            return list(filter(lambda item: not A.D_C.empty(item), command_list[0] + command_list[1]))
        command_list = command_list or get_command_list()
        use_psexec: bool = A.D_C.empty([value for value in list(map(
            lambda item: item.lower(), command_list)) if value in A.CT.PSTOOLS.COMMAND_LIST])
        result: CompletedProcess | None = None
        if use_psexec:
            if A.D_C.empty(host):
                if self.input.yes_no(f"Использовать хост {self.bold(default_host)}, для выполнения команды", no_label=f"{self.bold('Или введите название хоста')}"):
                    host = default_host
                else:
                    host = self.input.answer
            while True:
                host = host.lower()
                if A.C_R.accessibility_by_ping(host, count=1):
                    self.output.write_line(
                        nl(f"Команда будет запущена на хосте {self.bold(host)}"))
                    break
                else:
                    self.output.error(f"Хост {self.bold(host)} не доступен")
                    host = self.input.input(
                        "Введите имя хоста, на котором будет выполнена команда")
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.EXC.execute(A.EXC.create_command_for_psexec(
                command_list, host, interactive=True, run_from_system_account=True, run_with_elevetion=True), True, True)
        else:
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.EXC.execute(
                A.EXC.create_command_for_psexec(command_list[0], command_list[1:]), True, True)
        result_out: str = result.stdout
        if not A.D_C.empty(result_out):
            self.output.write_line(result_out)
        if result.returncode != 0:
            error: str = result.stderr
            self.output.write_line(error)

    def create_new_mark(self):

        self.full_name: str | None = None
        self.tab_number: str | None = None
        self.telephone_number: str | None = None
        self.division_id: int | None = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполните ФИО персоны")
            self.full_name = self.input.full_name(True)
            user_exists: bool = not A.C.MARK.exists_by_full_name(
                self.full_name)
            if user_exists:
                self.output.error(
                    "Персона с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО персоны", A.D.fullname_to_string(self.full_name))

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполните номер телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_tab_number() -> ActionValue:
            self.output.header("Выбор группы и номера для карты доступа")
            free_mark: Mark = self.input.mark.free()
            group_name: str = free_mark.GroupName
            self.tab_number = free_mark.TabNumber
            self.output.value("Группа карты доступа", group_name)
            return self.output.get_action_value("Номер карты пропуска", self.tab_number)

        def get_division() -> ActionValue:
            self.output.header("Выбор подразделения")
            person_division: PersonDivision = self.input.mark.person_division()
            self.division_id = person_division.id
            return self.output.get_action_value("Подразделение, к которому прикреплена персона", person_division.name)

        ActionStack("Данные пользователя",
                    get_full_name,
                    get_division,
                    get_telephone_number,
                    get_tab_number,
                    input=self.input,
                    output=self.output
                    )
        if self.input.yes_no("Создать карту доступа для персоны", True):
            if A.A_M.create(self.full_name, self.division_id, self.tab_number, self.telephone_number):
                self.output.good("Карты доступа создана!")
                A.E.it_notify_about_create_new_mark(
                    self.full_name)
                if self.input.yes_no("Уведомить персону", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, Вам выдана карта доступа с номером {self.tab_number}")
            else:
                self.output.error("Карта доступа не создана!")

    def send_workstation_message_to_all(self) -> None:
        message: str = self.input.message(
            f"{self.get_formatted_given_name()}, введите сообщение для всех пользователей")
        A.ME_WS.to_all_workstations(
            message, None, [A.CT_H.WS255], self.session)

    @property
    def user(self) -> User:
        return self.session.user

    @property
    def user_description(self) -> str:
        return A.D_F.description(self.user.description)

    def send_workstation_message(self, recipient_name: str | None = None, message: str | None = None, ask_for_use_dialog: bool = True) -> None:
        recipient: User | WorkstationDescription | None = None
        while True:
            try:
                recipient = A.D.get_first_item(
                    self.input.user.by_any(recipient_name, True))
                if recipient is not None:
                    break
            except NotFound as error:
                value: str = error.get_value()
                if A.C_WS.name(value):
                    if A.C_WS.exists(value):
                        recipient = A.R_WS.by_name(value).data
                        break
                if recipient is None:
                    recipient_name = None
                    self.output.error(error.get_details())
        if isinstance(recipient, User) and A.R.is_empty(A.R_WS.by_login(recipient.samAccountName)):
            self.output.error(
                f"Пользователь {recipient.name} ({recipient.samAccountName}) не залогинен ни за одним компьютером.")
        else:
            try:
                use_dialog: bool = False
                if ask_for_use_dialog:
                    use_dialog = A.D_C.empty(message) and self.input.yes_no("Начать диалог")
                else:
                    use_dialog = True
                while True:
                    user_given_name: str = self.get_formatted_given_name(self.user_given_name)
                    if isinstance(recipient, User):
                        message = message or self.input.message(
                            f"{user_given_name}, введите сообщение для пользователя {self.get_formatted_given_name(A.D.to_given_name(recipient))}", f"Сообщение от {self.user_given_name} ({self.user_description}): {A.D.to_given_name(recipient)}, ")
                        if A.ME_WS.to_user(recipient, message):
                            self.output.good("Сообщение отправлено")
                    else:
                        message =  message or self.input.message(
                            f"{user_given_name}, введите сообщение для компьютера {recipient.name}", f"Сообщение от {self.user_given_name} ({self.user_description}): ")
                        if A.ME_WS.to_workstation(recipient, message):
                            self.output.good("Сообщение отправлено")
                            message = None
                    if use_dialog:
                        self.output.separated_line()
                    else:
                        break
            except KeyboardInterrupt:
                if use_dialog:
                    self.output.error("Выход из диалога...")
                else:
                    self.output.error("Отмена...")

    @property
    def user_given_name(self) -> str:
        return self.session.user_given_name
    
    def get_formatted_given_name(self, value: str | None = None) -> str:
        return self.output.user.get_formatted_given_name(value or self.user_given_name)

    def create_temporary_mark(self, owner_mark: Mark | None = None) -> None:
        owner_mark = owner_mark or self.input.mark.by_any()
        mark_group: MarkGroup | None = None
        if self.input.yes_no("Выдать временную карту доступа из той же группы доступа"):
            mark_group = owner_mark
        temporary_mark: Mark = self.input.mark.free(mark_group)
        self.output.temporary_candidate_for_mark(temporary_mark)
        full_name: str = owner_mark.FullName
        tab_number: str = temporary_mark.TabNumber
        if self.input.yes_no(f"Создать временную карту для {full_name} с табельным номеров {tab_number}", True):
            if A.A_M.make_as_temporary(temporary_mark, owner_mark):
                self.output.good("Временная карта создана")
                telephone_number: str = owner_mark.telephoneNumber
                A.E.it_notify_about_create_temporary_mark(
                    full_name, tab_number)
                if not A.C.telephone_number(telephone_number):
                    user: User = A.R.get_first_item(A.R_U.by_any(
                        owner_mark))
                    if user is not None:
                        telephone_number = user.telephoneNumber
                if A.C.telephone_number(telephone_number):
                    if self.input.yes_no("Уведомить персону", True):
                        self.send_whatsapp_message(
                            telephone_number, f"Сообщение от ИТ отдела: День добрый, {self.get_formatted_given_name(full_name)}, Вам выдана временная карта доступа с номером {tab_number}")
            else:
                self.output.error("Ошибка при создании временной карты")
        else:
            self.output.error("Отмена")

    def telephone_number_fix_action(self, user: User) -> None:
        try:
            telephone: str = self.input.telephone_number()
            if A.A_U.set_telephone_number(user, telephone):
                self.output.good("Сохранен")
                self.output.line()
            else:
                self.output.error("Ошибка")
        except KeyboardInterrupt:
            self.output.new_line()
            self.output.error("Отмена")
            self.output.new_line()

    def start_user_telephone_number_editor(self) -> None:
        only_empty_telephone_number_edit: bool = self.input.yes_no(
            "Редактировать только телефоны, которые не заданы", True)
        result: Result[list[User]] = A.R_U.all(True)
        for user in result.data:
            user: User = user
            if A.C_U.user(user):
                if user.telephoneNumber is None:
                    self.output.error(f"{user.name}: нет телефона")
                    self.telephone_number_fix_action(user)
                elif not A.C.telephone_number(user.telephoneNumber):
                    fixed_telephone: str = A.D_F.telephone_number(
                        user.telephoneNumber)
                    if A.C.telephone_number(fixed_telephone):
                        self.output.good(f"{user.name} телефон исправлен")
                        A.A_U.set_telephone_number(
                            user, fixed_telephone)
                    else:
                        self.output.yellow(
                            f"{user.name}: неправильный формат телефона ({user.telephoneNumber})")
                else:
                    if not only_empty_telephone_number_edit:
                        self.output.good(
                            f"{user.name}: телефон присутствует")
                        self.telephone_number_fix_action(user)
            else:
                self.output.notify(
                    f"{user.name}, похоже не пользователь, у которого должен быть номер телефона")

    def start_user_property_setter(self, property_name: str, search_value: str | None = None, choose_user: bool = False) -> None:
        try:
            user_list: list[User] | None = None
            fields: FieldItemList = A.CT_FC.AD.USER
            active: bool | None = True if (
                property_name == A.CT_UP.PASSWORD or property_name == A.CT_UP.TELEPHONE_NUMBER) else None
            if choose_user:
                user_list = self.input.user.by_any(search_value, active)
            else:
                result: Result[list[User]] = A.R_U.by_any(
                    self.input.user.title_any(), active)
                user_list = result.data
            if property_name == A.CT_UP.USER_STATUS:
                for status in [A.CT_AD.ACTIVE_USERS_CONTAINER_DN, A.CT_AD.INACTIVE_USERS_CONTAINER_DN]:
                    work_user_list: list[User] = A.D_F.users_by_dn(
                        user_list, A.CT_AD.INACTIVE_USERS_CONTAINER_DN if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN else A.CT_AD.ACTIVE_USERS_CONTAINER_DN)
                    for index, user in enumerate(work_user_list):
                        try:
                            self.output.user.result(Result(fields, [user]))
                            if self.input.yes_no(f"{'Активировать' if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN else 'Деактивировать' } пользователя"):
                                if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN:
                                    if self.input.yes_no("Использовать шаблон для пользователя", True):
                                        user_container = self.input.user.template()
                                    else:
                                        user_container = self.input.user.container()
                                else:
                                    user_container = UserBase(
                                        distinguishedName=A.CT_AD.INACTIVE_USERS_CONTAINER_DN)
                                if A.A_U.set_status(user, status, user_container):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.new_line()
                                self.output.error("Отмена")
                        except KeyboardInterrupt:
                            self.output.new_line()
                            if index == len(user_list) - 1:
                                self.output.error("Отмена")
                            else:
                                self.output.error("Отмена - следующий")
                            self.output.new_line()
            else:
                for index, user in enumerate(user_list):
                    try:
                        if property_name == A.CT_UP.TELEPHONE_NUMBER:
                            self.output.user.result(
                                Result(fields, [user]), None)
                            telephone = self.input.telephone_number()
                            if A.C.telephone_number(telephone) and self.input.yes_no("Установить", True):
                                if A.A_U.set_telephone_number(user, telephone):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                        elif property_name == A.CT_UP.PASSWORD:
                            self.output.user.result(
                                Result(fields, [user]), "Пользователи:")
                            password: str | None = None
                            while True:
                                password = self.input.user.generate_password(True, PASSWORD.get(
                                    self.input.indexed_field_list("Выберите тип пароля", A.CT_FC.POLICY.PASSWORD_TYPE)))
                                self.output.value("Пароль", password)
                                if self.input.yes_no("Использовать", True):
                                    break
                            if self.input.yes_no("Установить", True):
                                if A.A_U.set_password(user, password):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                    except KeyboardInterrupt:
                        self.output.new_line()
                        self.output.error(
                            "Отмена" + (" - следующий" if index != len(user_list) - 1 else ""))
                        self.output.new_line()
        except NotFound as error:
            self.output.error(error.get_details())

    @property
    def session(self) -> Session:
        return self.pih.session

    def create_new_user(self) -> None:

        self.full_name: FullName | None = None
        self.tab_number: str | None = None
        self.telephone_number: str | None = None
        self.division_id: int | None = None
        self.user_is_exists: bool = False
        self.login: str | None = None
        self.password: str | None = None
        self.internal_email: str | None = None
        self.external_email: str | None = None
        self.email_password: str | None = None
        self.polibase_login: str | None = None
        self.polibase_password: str | None = None
        self.user_container: User | None = None
        self.description: str | None = None
        self.use_template_user: bool | None = None
        self.need_to_create_mark: bool | None = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполнение ФИО пользователя")
            self.full_name = self.input.full_name(True)
            self.user_is_exists = A.C.USER.exists_by_full_name(
                self.full_name)
            if self.user_is_exists:
                self.output.error(
                    "Пользователем с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО пользователя", A.D.fullname_to_string(self.full_name))

        def get_login() -> ActionValue:
            self.output.header("Создание логина для аккаунта пользователя")
            self.login = self.input.user.generate_login(self.full_name)
            return self.output.get_action_value("Логин пользователя", self.login)

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполнение номера телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_description() -> ActionValue:
            self.output.header("Заполнение описания пользователя")
            self.description = self.input.description()
            return self.output.get_action_value("Описание", self.description, False)

        def get_template_user_container_or_user_container() -> ActionValue:
            self.output.header("Выбор контейнера для пользователя")
            if self.input.yes_no("Использовать шаблон для создания аккаунта пользователя", True):
                self.user_container, self.use_template_user = (
                    self.input.user.template(), True)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.description)
            else:
                self.user_container, self.use_template_user = (
                    self.input.user.container(), False)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.distinguishedName)

        def get_pc_password() -> ActionValue:
            self.output.header("Создание пароля для аккаунта пользователя")
            self.password = self.input.user.generate_password(
                settings=PASSWORD.SETTINGS.PC)
            return self.output.get_action_value("Пароль", self.password, False)

        def get_internal_email() -> ActionValue:
            self.output.header("Создание корпоративной электронной почты")
            if self.input.yes_no("Создать", True):
                self.internal_email = A.D_F.email(self.login, add_default_domain = True)
            return self.output.get_action_value("Адресс корпоративной электронной почты пользователя", self.internal_email)

        def get_email_password() -> ActionValue:
            if self.internal_email:
                self.output.header(
                    "Создание пароля для корпоротивной электронной почты")
                if self.input.yes_no("Использовать пароль от аккаунта пользователя", True):
                    self.email_password = self.password
                else:
                    self.email_password = self.input.user.generate_password(
                        settings=PASSWORD.SETTINGS.EMAIL)
                return self.output.get_action_value("Пароль электронной почты",  self.email_password, False)
            return None

        def get_external_email() -> ActionValue:
            self.output.header("Добавление внешней почты")
            if self.input.yes_no("Добавить"):
                self.external_email = self.input.email()
            return self.output.get_action_value("Адресс внешней электронной почты пользователя", self.external_email if self.external_email else "Нет", False)

        def get_division() -> ActionValue:
            full_name_string: str = A.D.fullname_to_string(self.full_name)
            mark: Mark = A.R_M.by_name(
                full_name_string, True).data
            if mark is not None:
                if self.input.yes_no(
                        f"Найдена карта доступа для персоны {full_name_string} с номером {mark.TabNumber}. Использовать", True):
                    self.need_to_create_mark = False
                    self.tab_number = mark.TabNumber
                    return None
            self.need_to_create_mark = self.input.yes_no(
                f"Создать карту доступа для персоны '{full_name_string}'", True)
            if self.need_to_create_mark:
                self.output.header("Выбор подразделения")
                person_division: PersonDivision = self.input.mark.person_division()
                self.division_id = person_division.id
                return self.output.get_action_value("Подразделение персоны, которой принадлежит карта доступа", person_division.name)
            return None

        def get_tab_number() -> ActionValue:
            if self.need_to_create_mark:
                self.output.header("Создание карты доступа")
                free_mark: Mark = self.input.mark.free()
                group_name: str = free_mark.GroupName
                self.tab_number = free_mark.TabNumber
                self.output.value("Группа карты доступа", group_name)
                return self.output.get_action_value("Номер карты доступа", self.tab_number)
            return None

        ActionStack(
            "Данные пользователя",
            get_full_name,
            get_login,
            get_telephone_number,
            get_description,
            get_template_user_container_or_user_container,
            get_pc_password,
            get_internal_email,
            get_email_password,
            get_external_email,
            get_division,
            get_tab_number,
            input=self.input,
            output=self.output
        )
        polibase_login: str = self.login
        polibase_password: str = self.password
        if self.input.yes_no("Создать аккаунт для пользователя", True):
            if self.use_template_user:
                A.A_U.create_from_template(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            else:
                A.A_U.create_in_container(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            if self.need_to_create_mark:
                self.tab_number = self.tab_number or A.R_M.by_name(
                    A.D.fullname_to_string(self.full_name), True).data.TabNumber
                A.A_M.create(
                    self.full_name, self.division_id, self.tab_number, self.telephone_number)
            user_account_document_path: str = A.PTH_U.get_document_name(
                A.D.fullname_to_string(self.full_name), self.login if self.user_is_exists else None)
            if A.A_D.create_for_user(user_account_document_path, self.full_name, self.tab_number, LoginPasswordPair(self.login, self.password), LoginPasswordPair(
                    polibase_login, polibase_password), LoginPasswordPair(self.internal_email, self.email_password)):
                A.E.hr_notify_about_new_employee(self.login)
                A.E.it_notify_about_user_creation(
                    self.login, self.password)
                if self.need_to_create_mark:
                    A.E.it_notify_about_create_new_mark(
                        self.full_name)
                if self.input.yes_no("Сообщить пользователю о создании документов", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, Вас ожидает документы и карта доступа с номером {self.tab_number} в отделе")
                if self.input.yes_no("Отправить пользователю данные об аккаунте", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, данные Вашего аккаунта:\nЛогин: {self.login}\nПароль: {self.password}\nЭлектронная почта: {self.internal_email}")
