
import jmespath

from convisoappsec.flow.graphql_api.beta.models.issues.sast import CreateSastFindingInput
from convisoappsec.flow.graphql_api.beta.schemas import mutations


class IssuesAPI(object):
    """ To operations on Issues's (aka, findings and vulnerabilities)) in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_sast(self, sast_issue_model: CreateSastFindingInput):
        graphql_variables = {
            "input": sast_issue_model.to_graphql_dict()
        }
        
        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_SAST_FINDING_INPUT,
            graphql_variables
        )

        expected_path = 'createSastFinding.issue'

        issue = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return issue
