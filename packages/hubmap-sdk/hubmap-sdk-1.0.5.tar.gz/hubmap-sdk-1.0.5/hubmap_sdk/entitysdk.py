from hubmap_sdk import Sample, Collection, Dataset, sdk_helper
import requests

"""
The entity-api class is the mechanism by which functions of the entity api are interacted. 
Create an instance of the class and give it the optional arguments 'token' and 'service_url'. Token is a Globus
 authentication token, and service_url is the base url to the entity webservice you would like to use. These are
 "https://entity.api.hubmapconsortium.org" for the production sever, "https://entity-api.dev.hubmapconsortium.org" for 
 the DEV server, "https://entity-api.test.hubmapconsortium.org" for the TEST server, 
 "https://entity-api.stage.hubmapconsortium.org" for the STAGE server or use a localhost. If no token is given, only 
 functionality designated for public access will be usable. If no service_url is given, all requests will be made 
 against the production server
"""


class EntitySdk:
    def __init__(self, token=None, service_url='https://entity.api.hubmapconsortium.org/'):
        self.header = {}
        self.token = token
        if service_url.endswith('/'):
            self.entity_url = service_url
        else:
            self.entity_url = service_url + '/'
        if token is not None:
            self.header['Authorization'] = f'Bearer {self.token}'

    # Using an instance of the EntitySdk class with appropriate authentication token, service_url as well as the
    # entity_type ('donor', 'sample', etc) and a dictionary containing the data for the new entity, an entity will be
    # created via the entity-api. If the entity is created successfully, a new instance of the class corresponding to
    # the desired entity_type will be returned. If creation fails, an exception will be raised with the error message
    # from entity-api.
    def create_entity(self, entity_type, data):
        # If an entity_type given is not one of the accepted entity types, an exception will be raised.
        self.header['X-Hubmap-Application'] = 'ingest-api'
        if entity_type.lower() not in ['donor', 'sample', 'dataset', 'upload', 'collection']:
            error_message = "Accepted entity types are (case-insensitive): 'donor', 'sample', 'dataset', 'upload', or " \
                            "'collection'"
            raise sdk_helper.HTTPException(error_message, 400)
        # If the request to entity-api fails, an exception will be raised.
        url = f"{self.entity_url}entities/{entity_type}"
        output = sdk_helper.make_request('post', self, url, data=data)
        # If the request to entity-api is successfully made, but a >299 response code is returned an exception is raised
        # Upon a satisfactory response from entity-api, a new instance of the desired class will be created and returned
        new_instance = sdk_helper.make_entity(output)
        return new_instance

    # returns the version, build, and neo4j_connection status and prints the same information out.
    def get_status(self):
        try:
            r = requests.get(self.entity_url + 'status')
        # if the request fails, in this case an error is not raised. The error message is instead returned since this
        # may be a desired outcome.
        except Exception as e:
            print(e)
            return e
        output = r.json()
        if r.status_code < 300:
            print(f"version: {output['version']}, build: {output['build']}, neo4j_connection: "
                  f"{output['neo4j_connection']}")
        return output

    # Takes an id (HuBMAP id or UUID) for a sample or dataset and will return a list of organs that are ancestors to
    # the given sample or Dataset. This method does not require authorization, however if a token is given, it must be
    # valid, and if no token is given or if the token does not belong to HuBMAP-Read group, ancestor organ info will
    # only be returned for public entities.
    def get_ancestor_organs(self, identifier):
        url = f"{self.entity_url}entities/{identifier}/ancestor-organs"
        output = sdk_helper.make_request('get', self, url)
        organs_list = []
        for item in output:
            organ = Sample(item)
            organs_list.append(organ)
        return organs_list

    # takes the id of an entity (HuBMAP ID or UUID) and returns an instance of the entity corresponding to the ID given
    # This method requires a token.
    def get_entity_by_id(self, identifier):
        url = f"{self.entity_url}entities/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        new_instance = sdk_helper.make_entity(output)
        return new_instance

    # Takes in an id (HuBMAP ID or UUID) and returns a dictionary with the provenance tree above the given ID.
    # Optionally accepts an integer "depth" which will limit the size of the returned tree. This method requires a
    # token
    def get_entity_provenance(self, identifier, depth=None):
        url = f"{self.entity_url}entities/{identifier}/provenance"
        if depth is not None:
            depth = f"?depth={depth}"
        output = sdk_helper.make_request('get', self, url, depth)
        return output

    # returns a list of all available entity types as defined in the schema yaml
    # https://raw.githubusercontent.com/hubmapconsortium/entity-api/test-release/entity-api-spec.yaml
    # A token is not required, but if one if given, it must be valid.
    def get_entity_types(self):
        url = f"{self.entity_url}entity-types"
        output = sdk_helper.make_request('get', self, url)
        return output

    # Takes an id (HuBMAP ID or UUID) for a collection. Returns the details of the collection in the form of a
    # dictionary with the attached datasets. If no token, or a valid token with no HuBMAP-Read group membership, then
    # only a public collection will be returned, as well as only public datasets.
    def get_collection(self, identifier):
        url = f"{self.entity_url}collections/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        new_instance = Collection(output)
        return new_instance

    # Returns a list of all public collections. No token is required, however if one is provided, it must be valid.
    def get_collections(self):
        url = f"{self.entity_url}collections"
        output = sdk_helper.make_request('get', self, url)
        list_of_collections = []
        for item in output:
            new_collection = Collection(item)
            list_of_collections.append(new_collection)
        return list_of_collections

    # Creates multiple samples from the same source. Accepts a dictionary containing the information of the source
    # entity and an integer designating how many samples to create. Returns a list of the newly created sample objects.
    # 'direct_ancestor_uuid' is a required field in the dictionary. An example of a valid call would be:
    # create_multiple_samples(5, data) where data is the dictionary containing the information about the new entities.
    # A token is required.
    def create_multiple_samples(self, count, data):
        result = []
        url = f"{self.entity_url}entities/multiple-samples/{count}"
        output = sdk_helper.make_request('post', self, url, data=data)
        for item in output:
            sample_instance = Sample(item)
            result.append(sample_instance)
        return result

    # Updates the properties of a given entity. Accepts the id (HuBMAP ID or UUID) for the target entity to update, as
    # well as a dictionary with the new/updated properties for the entity. A token is required to update an entity. An
    # object is returned to show a simple message in the format: {'message': f"{normalized_entity_type} of {id} has been updated"}.
    def update_entity(self, identifier, data):
        url = f"{self.entity_url}entities/{identifier}"
        result = sdk_helper.make_request('put', self, url, data=data)
        return result

    # Returns a list of all the ancestors of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # No token is required, however if a token is given, it must be valid. If no token is given or token is not for a
    # user in the Hubmap-Read group, ancestors will only be returned for public entities
    def get_ancestors(self, identifier):
        list_of_ancestors = []
        url = f"{self.entity_url}ancestors/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_ancestors.append(new_instance)
        return list_of_ancestors

    # Returns a list of all the descendants of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # No token is required, however if a token is given, it must be valid. If no token is given or token is not for a
    # user in the Hubmap-Read group, descendants will only be returned for public entities
    def get_descendants(self, identifier):
        list_of_descendants = []
        url = f"{self.entity_url}descendants/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_descendants.append(new_instance)
        return list_of_descendants

    # Returns a list of all the parents of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # No token is required, however if a token is given, it must be valid. If no token is given or token is not for a
    # user in the Hubmap-Read group, parents will only be returned for public entities
    def get_parents(self, identifier):
        list_of_parents = []
        url = f"{self.entity_url}parents/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_parents.append(new_instance)
        return list_of_parents

    # Returns a list of all the parents of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # No token is required, however if a token is given, it must be valid. If no token is given or token is not for a
    # user in the Hubmap-Read group, parents will only be returned for public entities
    def get_children(self, identifier):
        list_of_children = []
        url = f"{self.entity_url}children/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_children.append(new_instance)
        return list_of_children

    # Returns a list of the previous revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. No token is required, however if a token is given, it must be valid. If no token is given or token is not
    # for a user in the Hubmap-Read group, previous revisions will only be returned for public entities
    def get_previous_revisions(self, identifier):
        list_of_previous_revisions = []
        url = f"{self.entity_url}previous_revisions/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_previous_revisions.append(new_instance)
        return list_of_previous_revisions

    # Returns a list of the next revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. No token is required, however if a token is given, it must be valid. If no token is given or token is not
    # for a user in the Hubmap-Read group, next revisions will only be returned for public entities
    def get_next_revisions(self, identifier):
        list_of_next_revisions = []
        url = f"{self.entity_url}next_revisions/{identifier}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_next_revisions.append(new_instance)
        return list_of_next_revisions

    # Accepts an id (HuBMAP ID or UUID) for a collection and a list of datasets. Links each dataset in the list to the
    # target collection. Requires a valid Token. Returns a string "Successfully added all the specified datasets to the
    # target collection" if successful.
    def add_datasets_to_collection(self, identifier, list_of_datasets):
        dataset_dictionary = {'dataset_uuids': list_of_datasets}
        url = f"{self.entity_url}collections/{identifier}/add-datasets"
        sdk_helper.make_request('put', self, url, data=dataset_dictionary)
        return "Successfully added all the specified datasets to the target collection"

    # Returns the globus url for an entity given by an id (HuBMAP ID or UUID). A token is not required, but if one is
    # given it must be valid. If a token is not given, or if the user does not have HuBMAP-Read group access, a globus
    # url will only be returned for public entities
    def get_globus_url(self, identifier):
        url = f"{self.entity_url}entities/{identifier}/globus-url"
        r = sdk_helper.make_request('get', self, url)
        return r

    # Returns a dataset object corresponding to the most recent revision of the dataset given by the id (HuBMAP ID or
    # UUID). A token is not required, but if one is provided, it must be valid. If a token is not given, or if the user
    # does not have HuBMAP-Read group access, then the last published dataset will be returned.
    def get_dataset_latest_revision(self, identifier):
        url = f"{self.entity_url}datasets/{identifier}/latest-revision"
        output = sdk_helper.make_request('get', self, url)
        new_dataset = Dataset(output)
        return new_dataset

    # Takes an id to a dataset (HuBMAP ID or UUID) and returns the revision number as an integer. If the dataset of the
    # given id is not a revision of any other dataset, it will return 1. If it is the first revision of an original
    # dataset, it will return 2, and so on. A token is not required, however if a token is provided it must be valid.
    # If there is no token or the user does not have HuBMAP-Read group access, and the ID is for an unpublished dataset,
    # an error will be raised.
    def get_dataset_revision_number(self, identifier):
        url = f"{self.entity_url}datasets/{identifier}/revision"
        output = sdk_helper.make_request('get', self, url)
        return output

    # Retracts a published dataset. Accepts an id (HuBMAP ID or UUID) and a string retraction_reason. A token is
    # required and the user must have HuBMAP-Data-Admin access. Adds retraction reason as a property to the dataset, and
    # ads a property sub_status which is set to "retracted". Returns an dataset object for the given id with the new
    # properties.
    def retract_dataset(self, identifier, retraction_reason):
        retract_json = {'retraction_reason': retraction_reason}
        url = f"{self.entity_url}datasets/{identifier}/retract"
        output = sdk_helper.make_request('put', self, url, data=retract_json)
        new_dataset = Dataset(output)
        return new_dataset

    # Returns a list of all revisions from a given id (HuBMAP ID or UUID). The id can be for any revision in the chain.
    # For example, if a given is for the third revision out of 7, it will return revisions 1 through 7. The list will be
    # ordered from most recent to oldest revision. An optional boolean parameter include_dataset allows the entire
    # dataset for each revision to be included in the list. By default this is false. No token is required, however if a
    # token is given it must be valid. If no token is given, or if the user does not have HuBMAP-Read group access, only
    # public datasets will be returned. If the id given itself is not public, and a token with read access is not given,
    # an error will be raised.
    def get_revisions_list(self, identifier, include_dataset=False):
        list_of_revisions = []
        if include_dataset != True:
            include_dataset = False
        url = f"{self.entity_url}datasets/{identifier}/revisions"
        dataset_include = ''
        if include_dataset:
            dataset_include = '?include_dataset=True'
        output = sdk_helper.make_request('get', self, url, dataset_include)
        if not include_dataset:
            return output
        else:
            for item in output:
                dict_with_dataset_object = {}
                new_dataset = Dataset(item['dataset'])
                dict_with_dataset_object['revision_number'] = item['revision_number']
                dict_with_dataset_object['dataset_uuid'] = item['uuid']
                dict_with_dataset_object['dataset'] = new_dataset
                list_of_revisions.append(dict_with_dataset_object)
            return list_of_revisions


    # Returns a list of all associated organs from a given id (HuBMAP ID or UUID). Does not require a token, however if
    # a token is given, it must be valid. If no token is given, or no HuBMAP-Read group access, only public datasets
    # will be accepted, and only public organs will be returned
    def get_associated_organs_from_dataset(self, identifier):
        list_or_organs = []
        url = f"{self.entity_url}datasets/{identifier}/organs"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = Sample(item)
            list_or_organs.append(new_instance)
        return list_or_organs

    # Returns provenance information for every dataset. Output is a list of dictionaries, where each dictionary contains
    # information on a given dataset. Optional parameters are has_rui_info (acceptable values are 'true' or 'false' and
    # are case-insensitive), organ (accepts an organ code for a given organ, case-insensitive), group_uuid (accepts a
    # uuid for a given group), and dataset status (acceptable values are 'published', 'qa', and 'new' and is case-
    # insensitive.
    def get_prov_info(self, has_rui_info=None, organ=None, group_uuid=None, dataset_status=None):
        url = f"{self.entity_url}datasets/prov-info"
        arguments = "?format=json"
        if has_rui_info is not None:
            arguments = arguments + "&has_rui_info=" + str(has_rui_info)
        if organ is not None:
            arguments = arguments + "&organ=" + organ
        if group_uuid is not None:
            arguments = arguments + "&group_uuid=" + group_uuid
        if dataset_status is not None:
            arguments = arguments + "&dataset_status=" + dataset_status
        output = sdk_helper.make_request('get', self, url, arguments)
        return output

    # Returns the provenance information in the form of a dictionary for a given dataset given by its id (HuBMAP ID, or
    # uuid).
    def get_prov_info_by_id(self, identifier):
        url = f"{self.entity_url}datasets/{identifier}/prov-info"
        arguments = "?format=json"
        output = sdk_helper.make_request('get', self, url, arguments)
        return output

    # empty the entity cache for the given entity
    def clear_cache(self, identifier):
        url = f"{self.entity_url}flush-cache/{identifier}"
        output = sdk_helper.make_request('delete', self, url)
        return output

    # empty the entire entity cache
    def clear_all_cache(self):
        url = f"{self.entity_url}flush-all-cache"
        output = sdk_helper.make_request('delete', self, url)
        return output
