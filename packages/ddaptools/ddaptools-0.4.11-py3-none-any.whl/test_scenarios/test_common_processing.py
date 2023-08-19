from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *




# def common_processor_using_mock():

#     publisher_credentials = {}
#     publisher_settings = {}

#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials=publisher_credentials, settings=publisher_settings)
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "387a26ff-ceed-5015-a6c9-a2cad90329c0" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated

#     return processor

# # def test_picks_chrome_enhancement_instantiation(common_processor_using_mock):
# #     processor = common_processor_using_mock
# #     processor.runJobs() # Should also post at the Mock Database

def test_salesforce():
    """
    1. Salesforce event.
    2. Publishes in database should result in updated start and updated endtime.
    """
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }

    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)

    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)

    # Salesforce Sample:  588e876e-31e6-91d4-863f-e0986fd90dad
    processor = PostgresS3ConnectorBasedCommonProcessor(
        job_parameters={"guid": "123e4567-e89b-12d3-a456-gog12og11asd"},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database


def xtest_joining_chrome():
    """
    Two tasks:
    1. same span guid
    2. Clear sequence continuity
    3. Both uses chrome as the data producer.
    4. Publishes in database should result in updated start and updated endtime.
    """
    
    # organizationDBProvider.initialization(ORGANIZATION_GUID) # At this version only initiated here, as organization guid is known.

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }


    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)

    # Raw Sample: e297909e-dcc4-ebf6-04e7-4e37946f50e5
    # Demo Sample: 387a26ff-ceed-5015-a6c9-afa
    # First part sample: aaad64e8-672f-3fa3-a94f-53c3cfe3d789
    # Second part sample: aaad64e8-672f-3fa3-a94-second-part


    """Examples
    [
        {
            "activity":"tab-focus","domain":"github.com",
            "duration":49.48,"endTime":"2023-06-15T19:20:49.532Z",
            "guid":"8460b54f-bfb9-d9e1-2a12-4e83329afde3", "incognito":false,"interactions":{}, "spanGuid": "AAAAAAAAAA", "isEventComplete":false,
            "params":{},"spanGUID":"0c4b4c8b-d00a-88ed-0f1e-24e045becaeb","spanSequence":0,
            "spanStartTime":"2023-06-15T19:20:00.044Z","timestamp":"2023-06-15T19:20:00.044Z",
            "title":"GitHub: Let’s build from here · GitHub","url":"https://github.com/"
        }, 
        {
            "activity":"tab-focus","domain":"github.com",
            "duration":10,"endTime":"2023-06-15T19:21:59.532Z","spanGuid": "AAAAAAAAAA",
            "guid":"8460b54f-bfb9-d9e1-2a12-second-part","incognito":false,"interactions":{},"isEventComplete":false,
            "params":{},"spanGUID":"0c4b4c8b-d00a-88ed-0f1e-24e045becaeb","spanSequence":1,
            "spanStartTime":"2023-06-15T19:20:00.044Z","timestamp":"2023-06-15T19:21:49.532Z",
            "title":"GitHub: Let’s build from here · GitHub","url":"https://github.com/"
        }
    ]

    """
    
    processor = PostgresConnectorBasedCommonProcessor(
        job_parameters={"guid": "aaad64e8-672f-3fa3-a94f-53c3cfe3d789"},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database

    
    processor = PostgresConnectorBasedCommonProcessor(
        job_parameters={"guid": "aaad64e8-672f-3fa3-a94-second-part"},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database













