from typing import List

from kubernetes.config import KUBE_CONFIG_DEFAULT_LOCATION

from vessl.util.constant import VESSL_HELM_CHART_NAME
from vessl.util.exception import VesslRuntimeException


class ClusterInstallCommandBuilder:
    def __init__(self) -> None:
        self.default_arguments = [
            "helm",
            "install",
            "vessl",
            f"vessl/{VESSL_HELM_CHART_NAME}",
            "--create-namespace",
        ]
        self.namespace = "vessl"
        self.kubeconfig = KUBE_CONFIG_DEFAULT_LOCATION
        self.cluster_name = ""
        self.access_token = ""
        self.provider_type = "on-premise"
        self.local_path_provisioner_enabled = True

        # optional) As these overrides default values.yaml, should check if this is empty
        # and skip when empty
        self.helm_values = []
        self.agent_local_storage_class_name = ""
        self.pod_resource_path = ""

    def with_namespace(self, namespace: str) -> "ClusterInstallCommandBuilder":
        self.namespace = namespace
        return self

    def with_kubeconfig(self, kubeconfig_path: str) -> "ClusterInstallCommandBuilder":
        self.kubeconfig = kubeconfig_path
        return self

    def with_cluster_name(self, cluster_name: str) -> "ClusterInstallCommandBuilder":
        self.cluster_name = cluster_name
        return self

    def with_access_token(self, access_token: str) -> "ClusterInstallCommandBuilder":
        self.access_token = access_token
        return self

    def with_provider_type(self, provider_type: str) -> "ClusterInstallCommandBuilder":
        self.provider_type = provider_type
        return self

    def with_agent_local_storage_class_name(self, name: str) -> "ClusterInstallCommandBuilder":
        """
        - agent.localStorageClassName={name}
        """
        self.agent_local_storage_class_name = name
        return self

    def set_local_path_provisioner_enabled(self, enabled) -> "ClusterInstallCommandBuilder":
        """
        - local-path-provisioner.enabled={enabled}
        """
        self.local_path_provisioner_enabled = enabled
        return self

    def with_helm_values(self, helm_values: List[str]) -> "ClusterInstallCommandBuilder":
        self.helm_values = helm_values
        return self

    # @XXX(seokju) rough assumption: k0s user will install k0s nodes
    # if this becomes a problem, patch chart and cli.
    def set_pod_resource_path(self, path: str) -> "ClusterInstallCommandBuilder":
        """
        - dcgm-exporter.kubeletPath={path}
        """
        self.pod_resource_path = path
        return self

    def build(self) -> List[str]:
        if not self.cluster_name:
            raise VesslRuntimeException("cluster_name is required to build install command")
        if not self.access_token:
            raise VesslRuntimeException("access_token is required to build install command")
        self.default_arguments.extend(["--namespace", self.namespace])
        self.default_arguments.extend(["--kubeconfig", self.kubeconfig])
        self.default_arguments.extend(["--set", f"agent.clusterName={self.cluster_name}"])
        self.default_arguments.extend(["--set", f"agent.accessToken={self.access_token}"])
        self.default_arguments.extend(["--set", f"agent.providerType={self.provider_type}"])
        self.default_arguments.extend(
            [
                "--set",
                f"local-path-provisioner.enabled={'true' if self.local_path_provisioner_enabled else 'false'}",
            ]
        )

        # check optionals
        if self.agent_local_storage_class_name:
            self.default_arguments.extend(
                [
                    "--set",
                    f"agent.localStorageClassName={self.agent_local_storage_class_name}",
                ]
            )
        for helm_value in self.helm_values:
            if helm_value:
                self.default_arguments.extend(["--set", helm_value])

        if self.pod_resource_path:
            self.default_arguments.extend(
                [
                    "--set",
                    f"dcgm-exporter.kubeletPath={self.pod_resource_path}",
                ]
            )
        return self.default_arguments
