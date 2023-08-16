class CreateSastFindingInput:
    def __init__(
        self,
        asset_id,
        code_snippet,
        file_name,
        vulnerable_line,
        first_line,
        title,
        description,
        severity,
        commit_ref,
        deploy_id,
        fingerprint,
        reference,
    ):
        self.asset_id = asset_id
        self.severity = CreateSastFindingInput.normalize_severity(severity)
        self.title = title
        self.description = description
        self.code_snippet = code_snippet
        self.file_name = file_name
        self.vulnerable_line = int(vulnerable_line)
        self.first_line = int(first_line)
        self.fingerprint = fingerprint
        self.reference = reference

        self.commit_ref = commit_ref
        self.deploy_id = deploy_id

        self.commit_ref = commit_ref
        self.deploy_id = deploy_id

    def to_graphql_dict(self):
        """
        This function returns a dictionary containing various attributes of an
        asset in a GraphQL format.
        """
        return {
            "assetId": self.asset_id,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "codeSnippet": self.code_snippet,
            "fileName": self.file_name,
            "vulnerableLine": self.vulnerable_line,
            "firstLine": self.first_line,
            "fingerprint": self.fingerprint,
            "reference": self.reference,
            "commitRef": self.commit_ref,
            "deployId": self.deploy_id,
        }

    @staticmethod
    def normalize_severity(severity):
        """
        The function normalizes severity by validating and returning a standardized severity level.
        """

        validate_severity = ["LOW", "MEDIUM", "HIGH", "CRITICAL", "NOTIFICATION"]
        if severity.upper() in validate_severity:
            return severity.upper()
        else:
            return validate_severity[0]
