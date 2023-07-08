from datetime import datetime
from datetime import datetime
from typing import Any
from typing import List
from uuid import UUID

from ..authenticate import AuthenticationResult
from ..consts import ENDPOINT
from ..helpers import from_str, from_datetime, from_none, from_int, from_list, from_float, from_bool


# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome3_from_dict(json.loads(json_string))


class House:
    house_id: UUID
    electricity_local_id: str
    name: str
    address: str
    postal_code: str
    city: str
    district: str
    country: str
    timezone: str
    creation_date: datetime
    client_id: UUID
    house_profile: str
    service_provider: str
    gas_local_id: None
    classification: str
    status: str
    is_settlement_active: int
    settlement_valid_from: datetime
    billing_date: datetime
    billing_period: str
    readings_date: datetime
    product_type: str
    latitude: float
    longitude: float
    id_meteo: int
    plan: str
    permission_role: str

    def __init__(self, house_id: UUID, electricity_local_id: str, name: str, address: str, postal_code: str, city: str,
                 district: str, country: str, timezone: str, creation_date: datetime, client_id: UUID,
                 house_profile: str, service_provider: str, gas_local_id: None, classification: str, status: str,
                 is_settlement_active: int, settlement_valid_from: datetime, billing_date: datetime,
                 billing_period: str, readings_date: datetime, product_type: str, latitude: float, longitude: float,
                 id_meteo: int, plan: str, permission_role: str) -> None:
        self.house_id = house_id
        self.electricity_local_id = electricity_local_id
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.district = district
        self.country = country
        self.timezone = timezone
        self.creation_date = creation_date
        self.client_id = client_id
        self.house_profile = house_profile
        self.service_provider = service_provider
        self.gas_local_id = gas_local_id
        self.classification = classification
        self.status = status
        self.is_settlement_active = is_settlement_active
        self.settlement_valid_from = settlement_valid_from
        self.billing_date = billing_date
        self.billing_period = billing_period
        self.readings_date = readings_date
        self.product_type = product_type
        self.latitude = latitude
        self.longitude = longitude
        self.id_meteo = id_meteo
        self.plan = plan
        self.permission_role = permission_role

    @staticmethod
    def from_dict(obj: Any) -> 'House':
        assert isinstance(obj, dict)
        house_id = UUID(obj.get("houseId"))
        electricity_local_id = from_str(obj.get("electricityLocalId"))
        name = from_str(obj.get("name"))
        address = from_str(obj.get("address"))
        postal_code = from_str(obj.get("postalCode"))
        city = from_str(obj.get("city"))
        district = from_str(obj.get("district"))
        country = from_str(obj.get("country"))
        timezone = from_str(obj.get("timezone"))
        creation_date = from_datetime(obj.get("creationDate"))
        client_id = UUID(obj.get("clientId"))
        house_profile = from_str(obj.get("houseProfile"))
        service_provider = from_str(obj.get("serviceProvider"))
        gas_local_id = from_none(obj.get("gasLocalId"))
        classification = from_str(obj.get("classification"))
        status = from_str(obj.get("status"))
        is_settlement_active = from_int(obj.get("isSettlementActive"))
        settlement_valid_from = from_datetime(obj.get("settlementValidFrom"))
        billing_date = from_datetime(obj.get("billingDate"))
        billing_period = from_str(obj.get("billingPeriod"))
        readings_date = from_datetime(obj.get("readingsDate"))
        product_type = from_str(obj.get("productType"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        id_meteo = from_int(obj.get("idMeteo"))
        plan = from_str(obj.get("plan"))
        permission_role = from_str(obj.get("permissionRole"))
        return House(house_id, electricity_local_id, name, address, postal_code, city, district, country, timezone,
                     creation_date, client_id, house_profile, service_provider, gas_local_id, classification, status,
                     is_settlement_active, settlement_valid_from, billing_date, billing_period, readings_date,
                     product_type, latitude, longitude, id_meteo, plan, permission_role)


class Device:
    connection_state: bool
    creation_date: datetime
    device_id: UUID
    device_local_id: str
    firmware_version: str
    house_id: UUID
    last_communication: datetime
    model: str
    type: str

    def __init__(self, connection_state: bool, creation_date: datetime, device_id: UUID, device_local_id: str,
                 firmware_version: str, house_id: UUID, last_communication: datetime, model: str, type: str) -> None:
        self.connection_state = connection_state
        self.creation_date = creation_date
        self.device_id = device_id
        self.device_local_id = device_local_id
        self.firmware_version = firmware_version
        self.house_id = house_id
        self.last_communication = last_communication
        self.model = model
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Device':
        assert isinstance(obj, dict)
        connection_state = from_bool(obj.get("connectionState"))
        creation_date = from_datetime(obj.get("creationDate"))
        device_id = UUID(obj.get("deviceId"))
        device_local_id = from_str(obj.get("deviceLocalId"))
        firmware_version = from_str(obj.get("firmwareVersion"))
        house_id = UUID(obj.get("houseId"))
        last_communication = from_datetime(obj.get("lastCommunication"))
        model = from_str(obj.get("model"))
        type = from_str(obj.get("type"))
        return Device(connection_state, creation_date, device_id, device_local_id, firmware_version, house_id,
                      last_communication, model, type)


class HousesResponse:
    houses: List[House]

    def __init__(self, houses: List[House]) -> None:
        self.houses = houses

    @staticmethod
    def from_dict(obj: Any) -> 'HousesResponse':
        assert isinstance(obj, dict)
        houses = from_list(House.from_dict, obj.get("houses"))
        return HousesResponse(houses)


class Equipment:
    authentication: AuthenticationResult = None
    endpoint = ENDPOINT + "/equipment"

    def __init__(self, authentication: AuthenticationResult):
        self.authentication = authentication

    def houses(self) -> List[House]:
        response = self.authentication.get(f"{self.endpoint}/houses")
        houses_response = HousesResponse.from_dict(response.json())
        return houses_response.houses

    def device(self, house: House) -> List[Device]:
        response = self.authentication.get(f"{self.endpoint}/houses/{house.house_id}/device")
        devices = from_list(Device.from_dict, response.json())
        return devices
