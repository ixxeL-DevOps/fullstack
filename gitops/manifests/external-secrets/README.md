
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout afd3946d97e720a35630e443e6c17a544f16dc5c
helm template . --name-template external-secrets-k0s --include-crds
```