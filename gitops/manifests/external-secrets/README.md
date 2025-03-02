
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7f41b6a4ecbe91fd6c978530a85e65c27fbcd30f
helm template . --name-template external-secrets-k0s --include-crds
```