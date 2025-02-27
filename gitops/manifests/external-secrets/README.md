
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 58479cd4cb478ae265ad53c7cb5822c9acb7cf9e
helm template . --name-template external-secrets-k0s --include-crds
```