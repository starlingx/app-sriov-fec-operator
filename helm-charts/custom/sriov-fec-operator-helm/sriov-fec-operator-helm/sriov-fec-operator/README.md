# Sriov Fec Operator Helm Chart

This Helm chart deploys the Sriov Fec Operator on Kubernetes clusters.
Application images that are used here are prepared specifically for Starlingx.

## Source

Charts are based on
<https://github.com/smart-edge-open/sriov-fec-operator/releases/tag/sriov-fec-operator-23.41>.
Upstream deployment is based on OLM
[Operator Lifecycle Manager](<https://olm.operatorframework.io/>).
Manifests used here are close representation of what can be found in
[config](<https://github.com/smart-edge-open/sriov-fec-operator/tree/sriov-fec-operator-23.41/config>).
Resources from that directory are organized into usual helm templates structure.
CRDs found here are located in
[api](<https://github.com/smart-edge-open/sriov-fec-operator/tree/sriov-fec-operator-23.41/api>)
directory, in OLM deployment they are built from that directory into yamls.

## Installation

```bash
$ helm install sriov-fec-operator sriov-fec-operator
```

Will install application in sriov-fec-operator namespace. Operator
dependencies are not included in this chart.
