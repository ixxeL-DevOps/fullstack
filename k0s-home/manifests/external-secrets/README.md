
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8ecd4114f5903437f5cd49cb4c4fe3e93225af53
helm template . --name-template external-secrets-k0s --include-crds
```