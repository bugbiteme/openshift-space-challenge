#!/bin/bash

# Check if a namespace was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <namespace>"
  exit 1
fi

NAMESPACE=$1

# Check if the namespace exists
if ! oc get namespace "$NAMESPACE" >/dev/null 2>&1; then
  echo "Namespace $NAMESPACE does not exist."
  exit 1
fi

# List and delete resources in the namespace, excluding specific kinds
oc get "$(oc api-resources --namespaced=true --verbs=list -o name | awk '{printf "%s%s", sep, $0; sep=","}')" \
  --ignore-not-found -n "$NAMESPACE" --no-headers \
  -o=custom-columns=KIND:.kind,NAME:.metadata.name,NAMESPACE:.metadata.namespace --sort-by='kind' 2>/dev/null | \
  awk '!/^PackageManifest|^LimitRange|^EndpointSlice|^Persistant/ {system("oc delete --ignore-not-found "$1" "$2" -n "$3)}'

echo "Cleaned up resources in namespace $NAMESPACE."
