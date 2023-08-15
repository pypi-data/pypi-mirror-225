from typing import List

from openapi_client import (
    ModelServiceGatewayUpdateAPIInput,
    ModelserviceModelServiceListResponse,
    ModelserviceModelServiceRevisionListResponse,
)
from openapi_client import OrmModelServiceGatewayTrafficSplitEntry as TrafficSplitEntry
from openapi_client import (
    ResponseModelServiceGatewayInfo,
    ResponseModelServiceInfo,
    ResponseModelServiceRevision,
    ResponseSimpleModelServiceRevision,
    ServingGatewayYamlImportAPIInput,
    ServingRevisionYamlImportAPIInput,
)
from vessl import vessl_api


def list_servings(organization: str) -> ModelserviceModelServiceListResponse:
    return vessl_api.model_service_list_api(organization_name=organization)


def create_revision_from_yaml(
    organization: str, serving_name: str, yaml_body: str
) -> ResponseModelServiceRevision:
    payload = ServingRevisionYamlImportAPIInput(yaml_body)

    return vessl_api.serving_revision_yaml_import_api(
        organization_name=organization,
        model_service_name=serving_name,
        serving_revision_yaml_import_api_input=payload,
    )


def read_revision(
    organization: str, serving_name: str, revision_number: int
) -> ResponseModelServiceRevision:
    return vessl_api.model_service_revision_read_api(
        organization_name=organization,
        model_service_name=serving_name,
        revision_number=revision_number,
    )


def list_revisions(
    organization: str, serving_name: str
) -> List[ResponseSimpleModelServiceRevision]:
    resp: ModelserviceModelServiceRevisionListResponse = vessl_api.model_service_revision_list_api(
        organization_name=organization,
        model_service_name=serving_name,
    )
    return resp.results


def read_gateway(organization: str, serving_name: str) -> ResponseModelServiceGatewayInfo:
    model_service: ResponseModelServiceInfo = vessl_api.model_service_read_api(
        model_service_name=serving_name,
        organization_name=organization,
    )
    return model_service.gateway_config


def update_gateway(
    organization: str, serving_name: str, gateway: ModelServiceGatewayUpdateAPIInput
) -> ResponseModelServiceGatewayInfo:
    return vessl_api.model_service_gateway_update_api(
        model_service_name=serving_name,
        organization_name=organization,
        model_service_gateway_update_api_input=gateway,
    )


def _get_updated_traffic_split_rule(
    rules_current: List[TrafficSplitEntry], revision_number: int, weight: int, port: int
) -> List[TrafficSplitEntry]:
    """
    Combines the previous traffic split rule with new rule.
    When filling the remaining weight, this function uses the one with higher revision number.

    For example, with the current rule of:
    - revision #2 (port 2222) 70%
    - revision #3 (port 3333) 30%

    with a call to this function with:
    - revision #4 (port 4444) 50%

    yields a new rule of:
    - revision #4 (port 4444) 50%
    - revision #3 (port 3333) 30%
    - revision #2 (port 2222) 20%

    Revision #3 takes priority over #2, because it has the higher number (3 > 2).
    """
    # Sort from latest revision (with highest number) to oldest
    rules_current = sorted(rules_current, key=lambda x: x.revision_number, reverse=True)

    rules_new: List[TrafficSplitEntry] = [
        TrafficSplitEntry(revision_number=revision_number, port=port, traffic_weight=weight)
    ]

    weight_remaining = 100 - weight

    # Iterate through current traffic rules and add them if possible
    for rule in rules_current:
        if weight_remaining <= 0:
            break
        new_weight = min(weight_remaining, rule.traffic_weight)
        rules_new.append(
            TrafficSplitEntry(
                revision_number=rule.revision_number, port=rule.port, traffic_weight=new_weight
            )
        )
        weight_remaining -= new_weight
        if weight_remaining <= 0:
            break

    if weight_remaining > 0:
        # This can happen if rules_current's weight do not sum up to 100
        # (this is possible for disabled gateways).
        # Handle this case safely by delegating all remaining weights to our target rule.
        rules_new[0].traffic_weight += weight_remaining

    return rules_new


def update_gateway_for_revision(
    organization: str,
    serving_name: str,
    revision_number: int,
    port: int,
    weight: int,
) -> ResponseModelServiceGatewayInfo:
    gateway_current = read_gateway(organization=organization, serving_name=serving_name)

    rules_new = _get_updated_traffic_split_rule(
        rules_current=gateway_current.rules or [],
        revision_number=revision_number,
        port=port,
        weight=weight,
    )

    gateway_updated = vessl_api.model_service_gateway_update_api(
        organization_name=organization,
        model_service_name=serving_name,
        model_service_gateway_update_api_input=ModelServiceGatewayUpdateAPIInput(
            enabled=True,
            endpoint=gateway_current.endpoint,
            ingress_class=gateway_current.ingress_class,
            annotations=gateway_current.annotations,
            traffic_split=rules_new,
        ),
    )
    return gateway_updated


def update_gateway_from_yaml(
    organization: str, serving_name: str, yaml_body: str
) -> ResponseModelServiceGatewayInfo:
    payload = ServingGatewayYamlImportAPIInput(yaml_body)

    return vessl_api.serving_gateway_yaml_import_api(
        organization_name=organization,
        model_service_name=serving_name,
        serving_gateway_yaml_import_api_input=payload,
    )
