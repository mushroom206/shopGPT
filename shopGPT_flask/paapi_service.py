from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def search_items(item_query):

    """ Following are your credentials """
    """ Please add your access key here """
    access_key = os.getenv('PAAPI_ACCESS_KEY')

    """ Please add your secret key here """
    secret_key = os.getenv('PAAPI_SECRET_KEY')

    """ Please add your partner tag (store/tracking id) here """
    partner_tag = "rei042-20"

    """ PAAPI host and region to which you want to send request """
    """ For more details refer: https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region"""
    host = "webservices.amazon.com"
    region = "us-east-1"

    """ API declaration """
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    """ Request initialization"""

    """ Specify keywords """
    keywords = item_query

    """ Specify the category in which search request is to be made """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/use-cases/organization-of-items-on-amazon/search-index.html """
    search_index = "All"

    """ Specify item count to be returned in search result """
    item_count = 3

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.IMAGES_VARIANTS_LARGE
    ]

    """ Forming request """
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
            merchant='Amazon'
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    try:
        """ Sending request """
        response = default_api.search_items(search_items_request)

        print("API called Successfully")
        print("Complete Response:", response)
        return response

        """ Parse response """
        # if response.search_result is not None:
        #     print("Printing first item information in SearchResult:")
        #     item_0 = response.search_result.items[0]
        #     if item_0 is not None:
        #         if item_0.asin is not None:
        #             print("ASIN: ", item_0.asin)
        #         if item_0.detail_page_url is not None:
        #             print("DetailPageURL: ", item_0.detail_page_url)
        #         if (
        #             item_0.item_info is not None
        #             and item_0.item_info.title is not None
        #             and item_0.item_info.title.display_value is not None
        #         ):
        #             print("Title: ", item_0.item_info.title.display_value)
        #         if (
        #             item_0.offers is not None
        #             and item_0.offers.listings is not None
        #             and item_0.offers.listings[0].price is not None
        #             and item_0.offers.listings[0].price.display_amount is not None
        #         ):
        #             print(
        #                 "Buying Price: ", item_0.offers.listings[0].price.display_amount
        #             )
        # if response.errors is not None:
        #     print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
        #     print("Error code", response.errors[0].code)
        #     print("Error message", response.errors[0].message)

    except ApiException as exception:
        print("Error calling PA-API 5.0!")
        print("Status code:", exception.status)
        print("Errors :", exception.body)
        print("Request ID:", exception.headers["x-amzn-RequestId"])

    except TypeError as exception:
        print("TypeError :", exception)

    except ValueError as exception:
        print("ValueError :", exception)

    except Exception as exception:
        print("Exception :", exception)