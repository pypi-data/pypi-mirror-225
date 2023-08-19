from datetime import datetime, date

from pymasmovil.client import Client
from pymasmovil.models.contract import Contract
from pymasmovil.errors.exceptions import (
    WrongFormattedDate,
    UnknownMMError,
    InvalidTargetConsumption,
)


class Asset(Contract):
    _route = "/v2/assets"

    maxNumTariff = ""
    numTariff = ""
    assetType = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, session, asset_id):
        contract = super().get(session, asset_id)

        return cls(**contract["asset"])

    @classmethod
    def get_by_phone(cls, session, phone):
        """
        Retrieve the asset associated to a given phone number from the MM sytem.

        :param:
            phone (str): Phone number of the contract we expect
        :return: dict containing the asset from the MM response
        """
        params = {"rowsPerPage": 1, "actualPage": 1, "phone": phone}

        response = Client(session).get(cls._route, **params)

        return cls(**response["rows"][0])

    @classmethod
    def update_product(
        cls,
        session,
        asset_id,
        transaction_id,
        product_id="",
        execute_date="",
        additional_bonds=[],
        bonds_to_remove=[],
        promotions=[],
        promotions_to_remove=[],
        shared_bond_product_id=None,
        shared_bond_id=None,
    ):
        """
        Modify asset request:
            - change tariff
            - add one-shot bonds

        :param:
            asset_id (str): MM Asset ID
            transaction_id (str): Unique and correlative 18-length numeric code
            productId (str): ID from the new tariff we want to apply
                            [only for change tariff]
            execute_date (str): request date [only for change tariff]
            additional_bonds (list): additional bonds to add
            bonds_to_remove (list): additional bonds to delete
            promotions (list): promotions to add
            bonds_to_remove (list): promotions to delete
            shared_bond_product_id (str): MM product ID from the shared bond
                                        [only for change tariff]
            shared_bond_id (str): MM ID for an existing instance of a shared bond
                                to which we want to add another mobile line sharing
                                its data [only for change tariff]

        :return: modified asset
        """

        route = "{}/{}/change-asset".format(cls._route.replace("v2", "v1"), asset_id)

        active_change = {
            "transactionId": transaction_id,
            "assetInfo": {
                "executeDate": execute_date,
                "productId": product_id,
                "additionalBonds": additional_bonds,
                "removeBonds": [{"assetId": bond_id} for bond_id in bonds_to_remove],
                "promotions": promotions,
                "removePromotions": [
                    {"assetId": bond_id} for bond_id in promotions_to_remove
                ],
            },
        }

        shared_bond_data = {
            "percentConsumption": "100",
            "productRelation": "",
        }
        if shared_bond_product_id:
            # New shared bond to create
            shared_bond_data["productId"] = shared_bond_product_id
            active_change["sharedBond"] = shared_bond_data

        elif shared_bond_id:
            # Existing shared bond to add a line to
            shared_bond_data["productRelation"] = shared_bond_id
            active_change["sharedBond"] = shared_bond_data

        response = Client(session).patch(route, (), active_change)

        if response == "Petición aceptada":
            return response
        else:
            raise UnknownMMError(response)

    @classmethod
    def get_consumption(cls, session, asset_id, init_date="", end_date=""):
        """
        Retrieve the asset consumption from current month

        :param:
            asset_id (str): MM Asset ID
            init_date (str): [YYYY-MM-DD] Date from which we want to consult the consumption.
                            Default value: first day of current month
            end_date (str): [YYYY-MM-DD] Date up to which we want to consult the consumption
                            Default value: today

        :return: dict containing the consumption (voice and data) from the MM response
        """

        route = "{}/{}/consumption".format(cls._route, asset_id)
        expected_format = "%Y-%m-%d"  # (ex: 2022-06-05)
        today = date.today()

        if init_date and cls._check_date(init_date, expected_format):
            init_date = init_date
        else:
            init_date = datetime(today.year, today.month, 1).strftime(expected_format)

        if end_date and cls._check_date(end_date, expected_format):
            end_date = end_date
        else:
            end_date = today.strftime(expected_format)

        params = {"iniDate": init_date, "endDate": end_date}

        response = Client(session).get(route, **params)
        bonds = response[0]["listBonos"]
        key_list_consumption = [
            "vozNacionalTotal",
            "vozNacional",
            "volumenTotal",
            "volumen",
        ]
        key_list_bond = ["nombreProducto", "idBono"]
        consumptions = []
        for bond in bonds:
            bond_consumption = bond["listConsumos"][0]
            consumptions.append(
                {
                    **dict((key, bond[key]) for key in key_list_bond if key in bond),
                    **dict(
                        (key, bond_consumption[key])
                        for key in key_list_consumption
                        if key in bond_consumption
                    ),
                }
            )

        return consumptions

    @classmethod
    def change_shared_bond_consumption_limit(cls, session, asset_id, consumption_limit):
        """
        Change the shared bond to which an asset is belonging, so
        it shares data with other mobiles

        :param:
            asset_id (str): MM Asset ID
            consumption_limit (int): percentage (10/25/50/75/100)

        :return: OK MM response
        """
        route = "{}/{}/consumption-profile".format(
            cls._route.replace("v2", "v1"), asset_id
        )

        if str(consumption_limit) not in ["10", "25", "50", "75", "100"]:
            raise InvalidTargetConsumption(consumption_limit)

        params = {"newConsum": consumption_limit}

        response = Client(session).patch(route, params, {})

        if response == "Petición aceptada":
            return response
        else:
            raise UnknownMMError(response)

    @classmethod
    def change_shared_bond(cls, session, asset_id, shared_bond_id, limit_percentage):
        """
        Change the shared bond to which an asset is belonging, so
        it shares data with other mobiles

        :param:
            asset_id (str): MM Asset ID
            shared_bond_id (str): Shared bond ID from MM (Producto)
            limit_percentage (int): percentage (10/25/50/75/100)

        :return: OK MM response
        """
        route = "{}/{}/switch-bonus".format(
            cls._route.replace("v2", "v1"), asset_id
        )

        if str(limit_percentage) not in ["10", "25", "50", "75", "100"]:
            raise InvalidTargetConsumption(limit_percentage)

        params = {"targetConsumption": limit_percentage, "idBond": shared_bond_id}

        response = Client(session).patch(route, params, {})

        if response == "Petición aceptada":
            return response
        else:
            raise UnknownMMError(response)

    def _check_date(str_date, expected_format):
        """
        Checks if string date matches the expected format
        If it does not, a custom WrongFormattedDate exception is raised

        :param:
            str_date (str): input string formatted date
            expected_format (str): expected date format code
        """
        try:
            datetime.strptime(str_date, expected_format)
        except ValueError:
            raise WrongFormattedDate(str_date, expected_format)
        return True
