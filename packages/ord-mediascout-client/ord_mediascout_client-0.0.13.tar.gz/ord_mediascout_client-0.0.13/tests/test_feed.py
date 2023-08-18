import pytest

from ord_mediascout_client import (
    ORDMediascoutClient,
    ORDMediascoutConfig,
    CreativeType,
    CreativeForm,
)
from ord_mediascout_client.feed_models import (
    CreateFeedElementsWebApiDto,
    FeedElementWebApiDto,
    FeedElementTextDataItem,
    CreateContainerWebApiDto,
    ResponseContainerWebApiDto,
    GetFeedElementsWebApiDto,
)


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


# Test is temporarily disabled
# def test_create_feed_element(client: ORDMediascoutClient) -> None:
#     request_data = CreateFeedElementsWebApiDto(
#         feedName='test_feed_lighter_one',
#         feedElements=[
#             FeedElementWebApiDto(
#                 nativeCustomerId='1',
#                 description='first of test_feed_lighter_one',
#                 advertiserUrls=['http://lighter_one.kz'],
#                 textData=[
#                     FeedElementTextDataItem(
#                         textData='sampletext',
#                     )
#                 ]
#             )
#         ],
#         feedNativeCustomerId='15',
#     )

#     response_data = client.create_feed_elements(request_data)

#     assert response_data[0].id is not None


# Test is temporarily disabled
# def test_get_feed_elements(client: ORDMediascoutClient) -> None:
#     request_data = GetFeedElementsWebApiDto(
#         feedNativeCustomerId='15',
#     )

#     response_data = client.get_feed_elements(request_data)

#     assert response_data[0].id is not None


# Test is temporarily disabled
# def test_create_container(client: ORDMediascoutClient) -> None:
#     request_data = CreateContainerWebApiDto(
#         type=CreativeType.CPM,
#         form=CreativeForm.Other,
#         description='test container description',
#         name='test container name',
#         feedId='FD4DHlrdcfpk2fe540VFBjvQ',
#         finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
#         okvedCodes=[],
#         isNative=False,
#         isSocial=False,
#     )

#     response_data = client.create_container(request_data)

#     assert response_data.id is not None
