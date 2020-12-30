"""

This file houses functions and classes that pertain to Roblox authenticated user account information.

"""

from datetime import datetime
from ro_py.gender import RobloxGender

endpoint = "https://accountinformation.roblox.com/"


class AccountInformationMetadata:
    """
    Represents account information metadata.
    """
    def __init__(self, metadata_raw):
        self.is_allowed_notifications_endpoint_disabled = metadata_raw["isAllowedNotificationsEndpointDisabled"]
        self.is_account_settings_policy_enabled = metadata_raw["isAccountSettingsPolicyEnabled"]
        self.is_phone_number_enabled = metadata_raw["isPhoneNumberEnabled"]
        self.max_user_description_length = metadata_raw["MaxUserDescriptionLength"]
        self.is_user_description_enabled = metadata_raw["isUserDescriptionEnabled"]
        self.is_user_block_endpoints_updated = metadata_raw["isUserBlockEndpointsUpdated"]


class PromotionChannels:
    """
    Represents account information promotion channels.
    """
    def __init__(self, promotion_raw):
        self.promotion_channels_visibility_privacy = promotion_raw["promotionChannelsVisibilityPrivacy"]
        self.facebook = promotion_raw["facebook"]
        self.twitter = promotion_raw["twitter"]
        self.youtube = promotion_raw["youtube"]
        self.twitch = promotion_raw["twitch"]


class AccountInformation:
    """
    Represents authenticated client account information (https://accountinformation.roblox.com/)
    This is only available for authenticated clients as it cannot be accessed otherwise.
    """
    def __init__(self, requests):
        self.requests = requests
        self.account_information_metadata = None
        self.promotion_channels = None

    async def update(self):
        """
        Updates the account information.
        """
        account_information_req = await self.requests.get(
            url="https://accountinformation.roblox.com/v1/metadata"
        )
        self.account_information_metadata = AccountInformationMetadata(account_information_req.json())
        promotion_channels_req = await self.requests.get(
            url="https://accountinformation.roblox.com/v1/promotion-channels"
        )
        self.promotion_channels = PromotionChannels(promotion_channels_req.json())

    async def get_gender(self):
        """
        Gets the user's gender.

        Returns
        -------
        RobloxGender
        """
        gender_req = await self.requests.get(endpoint + "v1/gender")
        return RobloxGender(gender_req.json()["gender"])

    async def set_gender(self, gender):
        """
        Sets the user's gender.

        Parameters
        ----------
        gender : RobloxGender
        """
        await self.requests.post(
            url=endpoint + "v1/gender",
            data={
                "gender": str(gender.value)
            }
        )

    async def get_birthdate(self):
        """
        Grabs the user's birthdate.

        Returns
        -------
        datetime.datetime
        """
        birthdate_req = await self.requests.get(endpoint + "v1/birthdate")
        birthdate_raw = birthdate_req.json()
        birthdate = datetime(
            year=birthdate_raw["birthYear"],
            month=birthdate_raw["birthMonth"],
            day=birthdate_raw["birthDay"]
        )
        return birthdate

    async def set_birthdate(self, birthdate):
        """
        Sets the user's birthdate.

        Parameters
        ----------
        birthdate : datetime.datetime
        """
        await self.requests.post(
            url=endpoint + "v1/birthdate",
            data={
              "birthMonth": birthdate.month,
              "birthDay": birthdate.day,
              "birthYear": birthdate.year
            }
        )
