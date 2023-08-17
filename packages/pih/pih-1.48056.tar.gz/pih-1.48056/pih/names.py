import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")

from pih.collection import FieldItem, FieldItemList, ParamItem
from enum import Enum


class DATA:
    # deprecated
    class EXTRACTOR:
        USER_NAME_FULL: str = "user_name_full"
        USER_NAME: str = "user_name"
        AS_IS: str = "as_is"

    class FORMATTER(Enum):
        MY_DATETIME: str = "my_datetime"
        MY_DATE: str = "my_date"
        CHILLER_INDICATIONS_VALUE_INDICATORS: str = (
            "chiller_indications_value_indicators"
        )
        CHILLER_FILTER_COUNT: str = "chiller_filter_count"


class USER_PROPERTIES:
    TELEPHONE_NUMBER: str = "telephoneNumber"
    EMAIL: str = "mail"
    DN: str = "distinguishedName"
    USER_ACCOUNT_CONTROL: str = "userAccountControl"
    LOGIN: str = "samAccountName"
    DESCRIPTION: str = "description"
    PASSWORD: str = "password"
    USER_STATUS: str = "userStatus"
    NAME: str = "name"


class FIELD_NAME_COLLECTION:
    ACTION_NAME: str = "action_name"
    ACTION_DESCRIPTION: str = "action_description"
    FULL_NAME: str = "FullName"
    TYPE: str = "type"
    GROUP_NAME: str = "GroupName"
    GROUP_ID: str = "GroupID"
    COMMENT: str = "Comment"
    CARD_REGISTRY_FOLDER: str = "ChartFolder"
    DESTINATION: str = "destination"
    BIRTH: str = "Birth"
    TAB_NUMBER: str = "TabNumber"
    OWNER_TAB_NUMBER: str = "OwnerTabNumber"
    NAME: str = USER_PROPERTIES.NAME
    MIDNAME: str = "MidName"
    PERSON_ID: str = "pID"
    MARK_ID: str = "mID"
    ID: str = "id"
    PIN: str = "pin"
    PID: str = "pid"
    VISIT_ID: str = "visitID"
    MESSAGE_ID: str = "messageID"
    VALUE: str = "value"
    FILE: str = "file"
    DIVISION_NAME: str = "DivisionName"
    DIVISION_ID: str = "DivisionID"
    BARCODE: str = "barcode"
    PROPERTIES: str = "properties"
    PARAMETERS: str = "parameters"
    MESSAGE: str = "message"
    STATUS: str = "status"
    FEEDBACK_CALL_STATUS: str = "feedbackCallStatus"
    REGISTRATION_DATE: str = "registrationDate"
    TYPE: str = "type"
    CABINET_ID: str = "cabinetID"
    DOCTOR_ID: str = "doctorID"
    DOCTOR_FULL_NAME: str = "doctorFullName"
    SERVICE_GROUP_ID: str = "serviceGroupID"
    PORT_NAME: str = "portName"
    TEMPERATURE: str = "temperature"
    HUMIDITY: str = "humidity"
    INDICATORS: str = "indicators"
    DATA: str = "data"
    COUNT: str = "count"

    SEARCH_ATTRIBUTE_LOGIN: str = USER_PROPERTIES.LOGIN
    SEARCH_ATTRIBUTE_NAME: str = USER_PROPERTIES.NAME

    TELEPHONE_NUMBER: str = USER_PROPERTIES.TELEPHONE_NUMBER
    EMAIL: str = f"e{USER_PROPERTIES.EMAIL}"
    DN: str = USER_PROPERTIES.DN
    LOGIN: str = USER_PROPERTIES.LOGIN
    ACTIVE_USERS_LOGIN: str = "active_" + USER_PROPERTIES.LOGIN
    DESCRIPTION: str = USER_PROPERTIES.DESCRIPTION
    PASSWORD: str = USER_PROPERTIES.PASSWORD
    ACCESSABLE: str = "accessable"
    STEP: str = "step"
    STEP_CONFIRMED: str = "stepConfirmed"
    GRADE: str = "grade"
    INFORMATION_WAY: str = "informationWay"
    TIME: str = "time"

    TIMESTAMP: str = "timestamp"
    DATE: str = "date"
    BEGIN_DATE: str = "beginDate"
    COMPLETE_DATE: str = "completeDate"
    RECIPIENT: str = "recipient"
    SENDER: str = "sender"
    TYPE: str = "type"
    ANSWER: str = "answer"
    STATE: str = "state"

    INVENTORY_NUMBER: str = "inventory_number"
    QUANTITY: str = "quantity"
    ROW: str = "row"
    NAME_COLUMN: str = "name_column"
    INVENTORY_NUMBER_COLUMN: str = "inventory_number_column"
    QUANTITY_COLUMN: str = "quantity_column"

    TEMPLATE_USER_CONTAINER: str = "templated_user"
    CONTAINER: str = "container"

    REMOVE: str = "remove"
    AS_FREE: str = "as_free"
    CANCEL: str = "cancel"

    WORKSTATION_NAME: str = "workstation_name"
    WORKSTATION_DESCRIPTION: str = "workstation_description"
    PERSON_NAME: str = "person_name"
    PERSON_PIN: str = "person_pin"
    REGISTRATOR_PERSON_NAME: str = "registrator_person_name"
    REGISTRATOR_PERSON_PIN: str = "registrator_person_pin"


class FIELD_ITEM_COLLECTION:
    TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TAB_NUMBER, "Табельный номер"
    )
    OWNER_TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.OWNER_TAB_NUMBER, "Табельный номер владельца"
    )
    FULL_NAME: FieldItem = FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "Полное имя")
    TEMPERATURE: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TEMPERATURE, "Температура", data_formatter="{data}°C"
    )
    INDICATORS: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.INDICATORS,
        "Индикаторы",
        data_formatter=DATA.FORMATTER.CHILLER_INDICATIONS_VALUE_INDICATORS.value,
    )
    INDICATION_TIMESTAMP: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TIMESTAMP,
        "Время снятия показаний",
        data_formatter=DATA.FORMATTER.MY_DATETIME.value,
    )


class FIELD_COLLECTION:
    INDEX: FieldItem = FieldItem("__Index__", "Индекс", True)
    POSITION: FieldItem = FieldItem(
        "position", "Расположение", True, default_value="Нет в реестре карт"
    )

    VALUE: FieldItem = FieldItem("", "Значение", True)
    VALUE_LIST: FieldItem = FieldItem("", "Список значений", True)

    class ORION:
        MARK_ACTION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.REMOVE, "Удалить"),
            FieldItem(FIELD_NAME_COLLECTION.AS_FREE, "Сделать свободной"),
            FieldItem(FIELD_NAME_COLLECTION.CANCEL, "Оставить"),
        )

        GROUP_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.GROUP_NAME, "Группа доступа"),
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Описание", False),
        )

        TAB_NUMBER_BASE: FieldItemList = FieldItemList(FIELD_ITEM_COLLECTION.TAB_NUMBER)

        FREE_MARK: FieldItemList = FieldItemList(TAB_NUMBER_BASE, GROUP_BASE)

        TAB_NUMBER: FieldItemList = FieldItemList(
            TAB_NUMBER_BASE,
            FieldItem(
                FIELD_NAME_COLLECTION.DIVISION_NAME,
                "Подразделение",
                default_value="Без подразделения",
            ),
            GROUP_BASE,
        ).position(FIELD_NAME_COLLECTION.DIVISION_NAME, 2)

        TEMPORARY_MARK: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FIELD_ITEM_COLLECTION.OWNER_TAB_NUMBER,
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False),
        )

        PERSON: FieldItemList = (
            FieldItemList(
                TAB_NUMBER,
                FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон", True),
                FIELD_ITEM_COLLECTION.FULL_NAME,
            )
            .position(FIELD_NAME_COLLECTION.FULL_NAME, 1)
            .position(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, 2)
        )

        PERSON_DIVISION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.ID, "ID", False),
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название подразделения"),
        )

        PERSON_EXTENDED: FieldItemList = FieldItemList(
            PERSON,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False),
        )

        GROUP: FieldItemList = FieldItemList(
            GROUP_BASE, FieldItem(FIELD_NAME_COLLECTION.GROUP_ID, "Group id", False)
        ).visible(FIELD_NAME_COLLECTION.COMMENT, True)

        GROUP_STATISTICS: FieldItemList = FieldItemList(
            GROUP,
            FieldItem("Count", "Количество"),
        ).visible(FIELD_NAME_COLLECTION.COMMENT, False)

        TIME_TRACKING: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FieldItem("TimeVal", "Время"),
            FieldItem("Remark", "Remark"),
            FieldItem("Mode", "Mode"),
        )

        TIME_TRACKING_RESULT: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FieldItem("Date", "Дата"),
            FieldItem("EnterTime", "Время прихода"),
            FieldItem("ExitTime", "Время ухода"),
            FieldItem("Duration", "Продолжительность"),
        )

    class INRENTORY:
        ITEM: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название инвентарного объекта"),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER, "Инвентарный номер"),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY, "Количество"),
            FieldItem(FIELD_NAME_COLLECTION.NAME_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY_COLUMN, None, False),
        )

    class AD:
        WORKSTATION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Имя компьютера"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание"),
            FieldItem(FIELD_NAME_COLLECTION.PROPERTIES, "Свойства", visible=False),
        )

        USER_ACTION: FieldItemList = FieldItemList(
            FieldItem(USER_PROPERTIES.TELEPHONE_NUMBER, "Изменить номер телефона"),
            FieldItem(USER_PROPERTIES.PASSWORD, "Изменить пароль"),
            FieldItem(USER_PROPERTIES.USER_STATUS, "Активировать или деактивировать"),
        )

        USER_WORKSTATION: FieldItemList = FieldItemList(
            WORKSTATION,
            FieldItem(FIELD_NAME_COLLECTION.ACCESSABLE, "Доступен"),
            FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Имя залогированного пользователя"),
        )

        SEARCH_ATTRIBUTE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_LOGIN, "Логин"),
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_NAME, "Имя"),
        )

        CONTAINER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание"),
        )

        USER_NAME: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Полное имя пользователя")
        )

        TEMPLATED_USER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание")
        )

        USER: FieldItemList = (
            FieldItemList(
                CONTAINER,
                FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Логин"),
                FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"),
                FieldItem(USER_PROPERTIES.EMAIL, "Электронная почта"),
                FieldItem(FIELD_NAME_COLLECTION.DN, "Размещение"),
                FieldItem("userAccountControl", "Свойства аккаунта", False),
            )
            .position(FIELD_NAME_COLLECTION.DESCRIPTION, 4)
            .caption(
                FIELD_NAME_COLLECTION.NAME,
                USER_NAME.get_item_by_name(FIELD_NAME_COLLECTION.NAME).caption,
            )
        )

        CONTAINER_TYPE: FieldItemList = FieldItemList(
            FieldItem(
                FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER, "Шаблонный пользователь"
            ),
            FieldItem(FIELD_NAME_COLLECTION.CONTAINER, "Контейнер"),
        )

    class POLIBASE:
        CARD_REGISTRY_FOLDER: FieldItem = FieldItem(
            FIELD_NAME_COLLECTION.CARD_REGISTRY_FOLDER,
            "Папка карты пациента",
            default_value="Не зарегистрирована в реестре карт пациентов",
        )

        PERSON_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.PIN, "Идентификационный номер пациента"),
            FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "ФИО пациента"),
            FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"),
        )

        PERSON_VISIT: FieldItemList = FieldItemList(
            PERSON_BASE,
            FieldItem(FIELD_NAME_COLLECTION.REGISTRATION_DATE, "Дата регистрации"),
            FieldItem(FIELD_NAME_COLLECTION.DOCTOR_FULL_NAME, "Имя доктора"),
        )

        PERSON: FieldItemList = FieldItemList(
            PERSON_BASE,
            FieldItem(
                FIELD_NAME_COLLECTION.BIRTH,
                "День рождения",
                True,
                "datetime",
                data_formatter=f"{DATA.FORMATTER.MY_DATE.value}",
            ),
            FieldItem(
                FIELD_NAME_COLLECTION.EMAIL,
                "Электронная почта",
                default_value="Нет электронной почты",
            ),
            CARD_REGISTRY_FOLDER,
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Комментарий"),
        )

    class POLICY:
        PASSWORD_TYPE: FieldItemList = FieldItemList(
            # FieldItem("EMAIL", "Для почты"),
            # FieldItem("SIMPLE", "Простой"),
            FieldItem("NORMAL", "Стандартный"),
            FieldItem("STRONG", "Сложный"),
        )

    class PRINTER:
        ITEM: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem("serverName", "Server name"),
            FieldItem(FIELD_NAME_COLLECTION.PORT_NAME, "Host name"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"),
            FieldItem("adminDescription", "Admin description", False),
            FieldItem("driverName", "Driver name"),
        )

    class INDICATIONS:
        CT_VALUE: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TEMPERATURE,
            FieldItem(
                FIELD_NAME_COLLECTION.HUMIDITY, "Влажность", data_formatter="{data}%"
            ),
        )

        CHILLER_VALUE: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TEMPERATURE, FIELD_ITEM_COLLECTION.INDICATORS
        )

        CT_VALUE_CONTAINER: FieldItemList = FieldItemList(
            CT_VALUE, FIELD_ITEM_COLLECTION.INDICATION_TIMESTAMP
        )

        CHILLER_VALUE_CONTAINER: FieldItemList = FieldItemList(
            CHILLER_VALUE, FIELD_ITEM_COLLECTION.INDICATION_TIMESTAMP
        )


class FieldCollectionAliases(Enum):
    TIME_TRACKING: FieldItem = FIELD_COLLECTION.ORION.TIME_TRACKING
    PERSON: FieldItem = FIELD_COLLECTION.ORION.PERSON
    TEMPORARY_MARK: FieldItem = FIELD_COLLECTION.ORION.TEMPORARY_MARK
    POLIBASE_PERSON: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON
    POLIBASE_PERSON_VISIT: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON_VISIT
    PERSON_DIVISION: FieldItem = FIELD_COLLECTION.ORION.PERSON_DIVISION
    PERSON_EXTENDED: FieldItem = FIELD_COLLECTION.ORION.PERSON_EXTENDED
    WORKSTATION: FieldItem = FIELD_COLLECTION.AD.WORKSTATION
    USER_WORKSTATION: FieldItem = FIELD_COLLECTION.AD.USER_WORKSTATION
    VALUE: FieldItem = FIELD_COLLECTION.VALUE
    VALUE_LIST: FieldItem = FIELD_COLLECTION.VALUE_LIST


class PARAM_ITEMS:

    NAME: ParamItem = ParamItem(FIELD_NAME_COLLECTION.NAME, "")
    PID: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PID, "")
    STATUS: ParamItem = ParamItem(FIELD_NAME_COLLECTION.STATUS, "")
    PERSON_PIN: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PERSON_PIN, "")
    PERSON_NAME: ParamItem = ParamItem(FIELD_NAME_COLLECTION.PERSON_NAME, "")
    REGISTRATOR_PERSON_NAME: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.REGISTRATOR_PERSON_NAME, "")
    REGISTRATOR_PERSON_PIN: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.REGISTRATOR_PERSON_PIN, "")
    CARD_REGISTRY_FOLDER: ParamItem = ParamItem(
        FIELD_NAME_COLLECTION.CARD_REGISTRY_FOLDER, "")
    DESTINATION: ParamItem = ParamItem(FIELD_NAME_COLLECTION.DESTINATION, "")
    COUNT: ParamItem = ParamItem(FIELD_NAME_COLLECTION.COUNT, "Количество")
