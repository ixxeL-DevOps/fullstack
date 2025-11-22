#!/usr/bin/env bash

set -euo pipefail

# shellcheck disable=SC2155
export ROOT_DIR="$(git rev-parse --show-toplevel)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

# Talos requires the nodes to be 'Ready=False' before applying resources
function wait_for_nodes() {
    log debug "Waiting for nodes to be available"

    # Skip waiting if all nodes are 'Ready=True'
    if kubectl wait nodes --for=condition=Ready=True --all --timeout=10s &>/dev/null; then
        log info "Nodes are available and ready, skipping wait for nodes"
        return
    fi

    # Wait for all nodes to be 'Ready=False'
    until kubectl wait nodes --for=condition=Ready=False --all --timeout=10s &>/dev/null; do
        log info "Nodes are not available, waiting for nodes to be available"
        sleep 10
    done
}

# Applications in the helmfile require Prometheus custom resources (e.g. servicemonitors)
function apply_prometheus_crds() {
    log debug "Applying Prometheus CRDs"

    # renovate: datasource=github-releases depName=prometheus-operator/prometheus-operator
    local -r version=v0.87.0
    local resources crds

    # Fetch resources using kustomize build
    if ! resources=$(kustomize build "https://github.com/prometheus-operator/prometheus-operator/?ref=${version}" 2>/dev/null) || [[ -z "${resources}" ]]; then
        log error "Failed to fetch Prometheus CRDs, check the version or the repository URL"
    fi

    # Extract only CustomResourceDefinitions
    if ! crds=$(echo "${resources}" | yq '. | select(.kind == "CustomResourceDefinition")' 2>/dev/null) || [[ -z "${crds}" ]]; then
        log error "No CustomResourceDefinitions found in the fetched resources"
    fi

    # Check if the CRDs are up-to-date
    if echo "${crds}" | kubectl diff --filename - &>/dev/null; then
        log info "Prometheus CRDs are up-to-date"
        return
    fi

    # Apply the CRDs
    if echo "${crds}" | kubectl apply --server-side --filename - &>/dev/null; then
        log info "Prometheus CRDs applied successfully"
    else
        log error "Failed to apply Prometheus CRDs"
    fi
}

# The application namespaces are created before applying the resources
function apply_namespaces() {
    log debug "Applying namespaces"

    local -r namespaces="argocd external-secrets"

    for ns in ${namespaces}; do

        # Check if the namespace resources are up-to-date
        if  kubectl get namespace "${ns}" &>/dev/null; then
            log info "Namespace resource is up-to-date" resource "${ns}"
            continue
        fi

        # Apply the namespace resources
        if kubectl create namespace "${ns}" --dry-run=client --output=yaml \
            | kubectl apply --server-side --filename - &>/dev/null;
        then
            log info "Namespace resource applied" resource "${ns}"
        else
            log error "Failed to apply namespace resource" resource "${ns}"
        fi
    done
}

# Secrets to be applied before the helmfile charts are installed
function apply_secrets() {
    log debug "Applying secrets"

   declare -A secrets_paths=(
        ["admin/github/gh-app/ixxel-devops/argocd"]="argocd"
        ["admin/wildcard/root-ca"]="external-secrets"
    )

    for path in "${!secrets_paths[@]}"; do
        local namespace="${secrets_paths[$path]}"
        log debug "Retrieving secret from Vault: ${path} (Namespace: ${namespace})"

        local secret
        secret="$(vault kv get -field=kube-secret -tls-skip-verify -address="${VAULT_ENDPOINT}" "${path}")"

        if [[ -z "${secret}" ]]; then
            log error "Secret is empty for ${path} (Namespace: ${namespace})"
            continue
        fi

        # Vérifier si le secret est à jour avant de l'appliquer
        if echo "${secret}" | kubectl diff -n "${namespace}" -f - &>/dev/null; then
            log info "Secret from ${path} is already up-to-date in ${namespace}"
            continue
        fi

        # Appliquer le secret dans le namespace correspondant
        if echo "${secret}" | kubectl apply -n "${namespace}" -f - &>/dev/null; then
            log info "Secret from ${path} successfully applied in ${namespace}"
        else
            log error "Failed to apply secret from ${path} in ${namespace}"
        fi
    done
}


function main() {
    # Verifications before bootstrapping the cluster
    check_env KUBECONFIG TALOSCONFIG
    check_cli jq kubectl kustomize vault talosctl yq

    wait_for_nodes
    apply_prometheus_crds
    apply_namespaces
    apply_secrets
}

main "$@"
