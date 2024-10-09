from gql import gql
from lib.types.severity import Severity
from lib.settings import settings

from lib.types.finding_type import FindingType


class GhostwriterFinding:

    def __init__(
        self,
        title=None,
        cvss_score=0.0,
        cvss_vector="",
        description="",
        mitigation="",
        affected_entities=[],
        replication_steps="",
        report_id=settings.ghostwriter.report_id,
        finding_type=FindingType.NETWORK,
        assigned_to_id=settings.ghostwriter.assigned_to_id,
        references="",
        impact="",
        added_as_blank=False,
    ):

        assert title, "Title is required"
        assert report_id, "Report ID is required"
        assert assigned_to_id, "Assigned To Username is required"

        self.report_id = report_id
        self.finding_type = finding_type
        self.severity = Severity.from_cvss(cvss_score, cvss_vector)
        self.assigned_to_id = assigned_to_id
        self.references = references
        self.affected_entities = affected_entities
        self.mitigation = mitigation
        self.replication_steps = replication_steps
        self.impact = impact
        self.added_as_blank = added_as_blank

        self.title = title
        self.description = description

    @property
    def query(self):

        return gql(
            """
            mutation MyMutation ($added_as_blank: Boolean!, $affected_entities: String!, $cvss_score: float8!, $cvss_vector: String!, $description: String!, $mitigation: String!, $replication_steps: String!, $title: String!, $report_id: bigint!, $finding_type_id: bigint!, $severity_id: bigint!, $assigned_to_id: bigint!) {
                insert_reportedFinding_one(object: {
                    addedAsBlank: $added_as_blank,
                    affectedEntities: $affected_entities,
                    cvssScore: $cvss_score,
                    cvssVector: $cvss_vector,
                    description: $description,
                    mitigation: $mitigation,
                    replication_steps:  $replication_steps,
                    title: $title,
                    reportId: $report_id,
                    findingTypeId: $finding_type_id,
                    severityId: $severity_id,
                    assignedToId: $assigned_to_id
                }) {
                id
                }
            }
            """
        )

    @property
    def variable_values(self):
        return {
            "added_as_blank": self.added_as_blank,
            "affected_entities": self.affected_entities,
            "cvss_score": self.severity.cvss_score,
            "cvss_vector": f"{self.severity.cvss_vector}",
            "description": f"{self.description}",
            "mitigation": f"{self.mitigation}",
            "replication_steps": f"{self.replication_steps}",
            "title": f"{self.title}",
            "report_id": int(self.report_id),
            "finding_type_id": self.finding_type.value,
            "severity_id": int(self.severity.value),
            "assigned_to_id": int(self.assigned_to_id),
        }
