from urllib.parse import urlparse

import jmespath

from convisoappsec.flow.graphql_api.v1.models.asset import CreateAssetInput
from convisoappsec.flow.graphql_api.v1.schemas import mutations, resolvers


class AssetsAPI(object):
    """ To operations on Asset's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_asset(self, asset_input: CreateAssetInput):
        graphql_variables = asset_input.to_graphql_dict()

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_ASSET,
            graphql_variables
        )

        expected_path = 'createAsset.asset'

        asset = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return asset

    def get_by_company_id(self, comapany_id, page=1, limit=32):
        graphql_variables = {
            "id": comapany_id,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ASSETS,
            graphql_variables
        )

        expected_path = 'assets.collection'

        assets_by_company = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return assets_by_company

    def get_asset_url(self, company_id, asset_id):
        parsed_url = urlparse(self.__conviso_graphql_client.url)

        asset_path = '/scopes/{}/assets/{}'.format(
            company_id,
            asset_id
        )

        parsed_url = parsed_url._replace(path=asset_path)

        return parsed_url.geturl()
