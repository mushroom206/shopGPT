from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException
from paapi5_python_sdk.models.get_variations_request import GetVariationsRequest
from paapi5_python_sdk.models.get_variations_resource import GetVariationsResource


from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()


def search_items(item_query):
    MAX_RETRIES = 3
    retries = 0

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
    item_count = 5

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.IMAGES_VARIANTS_LARGE,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
        SearchItemsResource.PARENTASIN
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
            merchant='All',
            min_reviews_rating=4,
            availability='Available',
            sort_by= 'Relevance' 
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    while retries < MAX_RETRIES:
        try:
            """ Sending request """
            response = default_api.search_items(search_items_request)

            print("API called Successfully")
            # print("Complete Response:", response)
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

        retries += 1
        time.sleep(1)    

def search_items_with_price(item_query, minPrice, maxPrice):
    MAX_RETRIES = 3
    retries = 0

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

    """ Add Price """
    minPrice = add_zeros_after_dot(minPrice)
    maxPrice = add_zeros_after_dot(maxPrice)

    if minPrice.isdigit():
        minPrice = int(minPrice)
    else:
        minPrice = None

    if maxPrice.isdigit():
        maxPrice = int(maxPrice)
    else:
        maxPrice = None        

    """ Specify the category in which search request is to be made """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/use-cases/organization-of-items-on-amazon/search-index.html """
    search_index = "All"

    """ Specify item count to be returned in search result """
    item_count = 5

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.IMAGES_VARIANTS_LARGE,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
        SearchItemsResource.PARENTASIN
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
            merchant='All',
            max_price=maxPrice,
            min_price=minPrice,
            min_reviews_rating=4,
            min_saving_percent=20,
            availability='Available',
            sort_by= 'Relevance'
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    while retries < MAX_RETRIES:
        try:
            """ Sending request """
            response = default_api.search_items(search_items_request)

            print("API called Successfully")
            # print("Complete Response:", response)
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

        retries += 1
        time.sleep(1)
        
def get_variations(asin, variation_page):
    MAX_RETRIES = 3
    retries = 0

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
    

    """ Specify language of preference """
    """ For more details, refer https://webservices.amazon.com/paapi5/documentation/locale-reference.html"""
    # languages_of_preference = ["es_US"]

    """ Choose resources you want from GetVariationsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#resources-parameter """
    get_variations_resources = [
        GetVariationsResource.ITEMINFO_TITLE,
        GetVariationsResource.OFFERS_LISTINGS_PRICE,
        GetVariationsResource.VARIATIONSUMMARY_VARIATIONDIMENSION,
        GetVariationsResource.IMAGES_PRIMARY_LARGE,
        GetVariationsResource.IMAGES_VARIANTS_LARGE,
        GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
        GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
        GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    ]

    """ Forming request """
    try:
        get_variations_request = GetVariationsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            marketplace="www.amazon.com",
            # languages_of_preference=languages_of_preference,
            asin=asin,
            resources=get_variations_resources,
            variation_page=variation_page
        )
    except ValueError as exception:
        print("Error in forming GetVariationsRequest: ", exception)
        return

    while retries < MAX_RETRIES:
        try:
            """ Sending request """
            response = default_api.get_variations(get_variations_request)

            print("API called Successfully")
            print("Complete Response:", response)

            return response
            """ Parse response """
            # if response.variations_result is not None:
            #     print("Printing VariationSummary:")
            #     if (
            #         response.variations_result.variation_summary is not None
            #         and response.variations_result.variation_summary.variation_count
            #         is not None
            #     ):
            #         print(
            #             "VariationCount: ",
            #             response.variations_result.variation_summary.variation_count,
            #         )

            #     print("Printing first item information in VariationsResult:")
            #     item_0 = response.variations_result.items[0]
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

        retries += 1
        time.sleep(1)              

def add_zeros_after_dot(string):
    result = string
    if not string:
        # print(result)
        return result
    if "." not in string:
        result = string + ".00"
    else:
        decimal_part = string.split(".")[1]
        if len(decimal_part) == 0:
            result = string + "00"
        elif len(decimal_part) == 1:
            result = string + "0"
        elif len(decimal_part) >= 2:
            result = string[:string.index('.')+3]
    result = result.replace("[^0-9]", "")
    result = result.replace(".", "")
    return result

        