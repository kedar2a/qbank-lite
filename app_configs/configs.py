import os
import sys

try:
    from django.conf import settings
except ImportError:
    from ..dlkit_runtime_project import settings

from dlkit.primordium.type.primitives import Type

from dlkit_runtime.utilities import impl_key_dict

if getattr(sys, 'frozen', False):
    ABS_PATH = os.path.dirname(sys.executable)
else:
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    ABS_PATH = '{0}'.format(os.path.abspath(os.path.join(PROJECT_PATH, os.pardir)))
    TEST_ABS_PATH = '{0}'.format(os.path.abspath(os.path.join(PROJECT_PATH, os.pardir)))


#MEDIA_PATH = '/data/media'
MEDIA_PATH = ABS_PATH
DATA_STORE_PATH = 'webapps/CLIx/datastore'
STUDENT_RESPONSE_DATA_STORE_PATH = 'webapps/CLIx/datastore/studentResponseFiles'

TEST_DATA_STORE_PATH = '/data/media'
TEST_STUDENT_RESPONSE_DATA_STORE_PATH = 'test_datastore/studentResponseFiles'

FILESYSTEM_ASSET_CONTENT_TYPE = Type(**
                                     {
                                         'authority': 'odl.mit.edu',
                                         'namespace': 'asset_content_record_type',
                                         'identifier': 'filesystem'
                                     })

###################################################
# PRODUCTION SETTINGS
###################################################

FILESYSTEM_ADAPTER_1 = {
    'id': 'filesystem_adapter_configuration_1',
    'displayName': 'Filesystem Adapter Configuration',
    'description': 'Configuration for Filesystem Adapter',
    'parameters': {
        'implKey': impl_key_dict('filesystem_adapter'),
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'dataStorePath': {
            'syntax': 'STRING',
            'displayName': 'Path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': DATA_STORE_PATH, 'priority': 1}  # Mac
            ]
        },
        #'secondaryDataStorePath': {
        #    'syntax': 'STRING',
        #    'displayName': 'Path to local filesystem datastore',
        #    'description': 'Filesystem path for setting the MongoClient host.',
        #    'values': [
        #        {'value': STUDENT_RESPONSE_DATA_STORE_PATH, 'priority': 1}  # Mac
        #    ]
        #},
    }
}

FILESYSTEM_1 = {
    'id': 'filesystem_configuration_1',
    'displayName': 'Filesystem Configuration',
    'description': 'Configuration for Filesystem Implementation',
    'parameters': {
        'implKey': impl_key_dict('filesystem'),
        'recordsRegistry': {
            'syntax': 'STRING',
            'displayName': 'Python path to the extension records registry file',
            'description': 'dot-separated path to the extension records registry file',
            'values': [
                {'value': 'records.registry', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
#        'assetContentRecordTypeForFiles': {
#            'syntax': 'TYPE',
#            'displayName': 'Asset Content Type for Files',
#            'description': 'Asset Content Type for Records that store Files on local disk',
#            'values': [
#                {'value': FILESYSTEM_ASSET_CONTENT_TYPE, 'priority': 1}
#            ]
#        },
        'dataStorePath': {
            'syntax': 'STRING',
            'displayName': 'Path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': DATA_STORE_PATH, 'priority': 1}
            ]
        },
        'dataStoreFullPath': {
            'syntax': 'STRING',
            'displayName': 'Full path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': MEDIA_PATH, 'priority': 1}
            ]
        },
        'magicItemLookupSessions': {
            'syntax': 'STRING',
            'displayName': 'Which magic item lookup sessions to try',
            'description': 'To handle magic IDs.',
            'values': [
                {'value': 'records.assessment.clix.magic_item_lookup_sessions.CLIxMagicItemLookupSession', 'priority': 1}
            ]
        },
    },

}

AUTHZ_ADAPTER_1 = {
    'id': 'authz_adapter_configuration_1',
    'displayName': 'AuthZ Adapter Configuration',
    'description': 'Configuration for AuthZ Adapter',
    'parameters': {
        'implKey': impl_key_dict('authz_adapter'),
        'authzAuthorityImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'assessmentProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Assessment Provider Implementation',
            'description': 'Implementation for assessment service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'authorizationProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Authorization Provider Implementation',
            'description': 'Implementation for authorization service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'learningProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Learning Provider Implementation',
            'description': 'Implementation for learning service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'hierarchyProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Hierarchy Provider Implementation',
            'description': 'Implementation for hierarchy service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'FILESYSTEM_ADAPTER_1', 'priority': 1}
            ]
        },
        'loggingProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Logging Provider Implementation',
            'description': 'Implementation for logging provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
    }
}


GSTUDIO_1 = {
    'id': 'gstudio_configuration_1',
    'displayName': 'Gstudio Configuration',
    'description': 'Configuration for Gstudio Implementation',
    'parameters': {
        'implKey': impl_key_dict('gstudio'),
        'mongoDBNamePrefix': {
            'syntax': 'STRING',
            'displayName': 'Mongo DB Name Prefix',
            'description': 'Prefix for naming mongo databases.',
            'values': [
                {'value': '', 'priority': 1}
            ]
        },
        'recordsRegistry': {
            'syntax': 'STRING',
            'displayName': 'Python path to the extension records registry file',
            'description': 'dot-separated path to the extension records registry file',
            'values': [
                {'value': 'records.registry', 'priority': 1}
            ]
        },
        'authority': {
            'syntax': 'STRING',
            'displayName': 'Mongo Authority',
            'description': 'Authority.',
            'values': [
                {'value': 'GSTUDIO', 'priority': 1}
            ]
        },
        'indexes': {
            'syntax': 'OBJECT',
            'displayName': 'Mongo DB Indexes',
            'description': 'Indexes to set in MongoDB',
            'values': [
                {'value': {}, 'priority': 1}
            ]
        },
        'mongoHostURI': {
            'syntax': 'STRING',
            'displayName': 'Mongo Host URI',
            'description': 'URI for setting the MongoClient host.',
            'values': [
                {'value': 'mongodb://localhost:27017', 'priority': 1}
            ]
        },
        'keywordFields': {
            'syntax': 'OBJECT',
            'displayName': 'Keyword Fields',
            'description': 'Text fields to include in keyword queries',
            'values': [
                {'value': {}, 'priority': 1}
            ]
        },
        'localImpl': {
            'syntax': 'STRING',
            'displayName': 'Implementation identifier for local service provider',
            'description': 'Implementation identifier for local service provider.  Typically the same identifier as the Mongo configuration',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
    }
}


GSTUDIO_AUTHZ_ADAPTER_1 = {
    'id': 'gstudio_authz_adapter_configuration_1',
    'displayName': 'GStudio AuthZ Adapter Configuration',
    'description': 'Configuration for GStudio AuthZ Adapter',
    'parameters': {
        'implKey': impl_key_dict('gstudio'),
        'authorizationProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Authorization Provider Implementation',
            'description': 'Implementation for authorization service provider',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
	}
}


SERVICE = {
    'id': 'dlkit_runtime_bootstrap_configuration',
    'displayName': 'DLKit Runtime Bootstrap Configuration',
    'description': 'Bootstrap Configuration for DLKit Runtime',
    'parameters': {
        'implKey': impl_key_dict('service'),
        'assessmentProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Assessment Provider Implementation',
            'description': 'Implementation for assessment service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'loggingProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Logging Provider Implementation',
            'description': 'Implementation for logging service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                # {'value': 'FILESYSTEM_ADAPTER_1', 'priority': 1}
                {'value': 'GSTUDIO_AUTHZ_ADAPTER_1', 'priority': 1}
            ]
        },
        'learningProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Learning Provider Implementation',
            'description': 'Implementation for learning service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
        'hierarchyProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Hierarchy Provider Implementation',
            'description': 'Implementation for hierarchy service provider',
            'values': [
                {'value': 'FILESYSTEM_1', 'priority': 1}
            ]
        },
    }
}

BOOTSTRAP = {
    'id': 'bootstrap_configuration',
    'displayName': 'BootStrap Configuration',
    'description': 'Configuration for Bootstrapping',
    'parameters': {
        'implKey': impl_key_dict('service'),
    }
}


###################################################
# TEST SETTINGS
###################################################

TEST_FILESYSTEM_ADAPTER_1 = {
    'id': 'filesystem_adapter_configuration_1',
    'displayName': 'Filesystem Adapter Configuration',
    'description': 'Configuration for Filesystem Adapter',
    'parameters': {
        'implKey': impl_key_dict('filesystem_adapter'),
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'dataStorePath': {
            'syntax': 'STRING',
            'displayName': 'Path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': TEST_DATA_STORE_PATH, 'priority': 1}  # Mac
            ]
        },
        'secondaryDataStorePath': {
            'syntax': 'STRING',
            'displayName': 'Path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': TEST_STUDENT_RESPONSE_DATA_STORE_PATH, 'priority': 1}  # Mac
            ]
        },
    }
}

TEST_FILESYSTEM_1 = {
    'id': 'filesystem_configuration_1',
    'displayName': 'Filesystem Configuration',
    'description': 'Configuration for Filesystem Implementation',
    'parameters': {
        'implKey': impl_key_dict('filesystem'),
        'recordsRegistry': {
            'syntax': 'STRING',
            'displayName': 'Python path to the extension records registry file',
            'description': 'dot-separated path to the extension records registry file',
            'values': [
                {'value': 'records.registry', 'priority': 1}
            ]
        },
        'hierarchyProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Hierarchy Provider Implementation',
            'description': 'Implementation for hierarchy service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'relationshipProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Relationship Provider Implementation',
            'description': 'Implementation for relationship service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
#        'assetContentRecordTypeForFiles': {
#            'syntax': 'TYPE',
#            'displayName': 'Asset Content Type for Files',
#            'description': 'Asset Content Type for Records that store Files on local disk',
#            'values': [
#                {'value': FILESYSTEM_ASSET_CONTENT_TYPE, 'priority': 1}
#            ]
#        },
        'dataStorePath': {
            'syntax': 'STRING',
            'displayName': 'Path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': TEST_DATA_STORE_PATH, 'priority': 1}
            ]
        },
        'dataStoreFullPath': {
            'syntax': 'STRING',
            'displayName': 'Full path to local filesystem datastore',
            'description': 'Filesystem path for setting the MongoClient host.',
            'values': [
                {'value': TEST_ABS_PATH, 'priority': 1}
            ]
        },
        'magicItemLookupSessions': {
            'syntax': 'STRING',
            'displayName': 'Which magic item lookup sessions to try',
            'description': 'To handle magic IDs.',
            'values': [
                {'value': 'records.assessment.clix.magic_item_lookup_sessions.CLIxMagicItemLookupSession', 'priority': 1}
            ]
        },
    },

}

TEST_AUTHZ_ADAPTER_1 = {
    'id': 'authz_adapter_configuration_1',
    'displayName': 'AuthZ Adapter Configuration',
    'description': 'Configuration for AuthZ Adapter',
    'parameters': {
        'implKey': impl_key_dict('authz_adapter'),
        'authzAuthorityImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'assessmentProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Assessment Provider Implementation',
            'description': 'Implementation for assessment service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'authorizationProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Authorization Provider Implementation',
            'description': 'Implementation for authorization service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'learningProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Learning Provider Implementation',
            'description': 'Implementation for learning service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'hierarchyProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Hierarchy Provider Implementation',
            'description': 'Implementation for hierarchy service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_ADAPTER_1', 'priority': 1}
            ]
        },
        'loggingProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Logging Provider Implementation',
            'description': 'Implementation for logging provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
    }
}

TEST_SERVICE = {
    'id': 'dlkit_runtime_bootstrap_configuration',
    'displayName': 'DLKit Runtime Bootstrap Configuration',
    'description': 'Bootstrap Configuration for DLKit Runtime',
    'parameters': {
        'implKey': impl_key_dict('service'),
        'assessmentProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Assessment Provider Implementation',
            'description': 'Implementation for assessment service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'loggingProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Logging Provider Implementation',
            'description': 'Implementation for logging service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'repositoryProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Repository Provider Implementation',
            'description': 'Implementation for repository service provider',
            'values': [
                {'value': 'GSTUDIO_1', 'priority': 1}
            ]
        },
        'learningProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Learning Provider Implementation',
            'description': 'Implementation for learning service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'hierarchyProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Hierarchy Provider Implementation',
            'description': 'Implementation for hierarchy service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
        'authorizationProviderImpl': {
            'syntax': 'STRING',
            'displayName': 'Authorization Provider Implementation',
            'description': 'Implementation for authorization service provider',
            'values': [
                {'value': 'TEST_FILESYSTEM_1', 'priority': 1}
            ]
        },
    }
}
