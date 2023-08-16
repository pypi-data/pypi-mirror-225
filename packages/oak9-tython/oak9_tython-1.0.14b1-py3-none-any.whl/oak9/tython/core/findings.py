from models.shared.shared_pb2 import Finding
from models.shared.shared_pb2 import FindingType
from models.shared.shared_pb2 import ResourceMetadata
from models.shared.shared_pb2 import Severity


def create_design_gap(
        *,
        resource_metadata: ResourceMetadata,
        config_id: str,
        description: str,
        current_value: str,
        capability_id: str = None,
        preferred_value: str = None,
        fix: str = None,
        documentation_url: str = None,
        severity: Severity = None
) -> Finding:
    """ Use this function to create findings of type 'design gap' """

    return Finding(
        resource_metadata=resource_metadata,
        config_id=config_id,
        description=description,
        current_value=str(current_value),
        preferred_value=preferred_value or '',
        finding_type=FindingType.DESIGN_GAP,
        fix=fix or '',
        documentation_url=documentation_url or '',
        severity=severity or Severity.MODERATE,
        capability_id=capability_id or ''
    )
