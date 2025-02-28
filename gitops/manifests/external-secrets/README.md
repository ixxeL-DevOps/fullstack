
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3679499af71947e857811be6f59157a288e587e2
helm template . --name-template external-secrets-k0s --include-crds
```