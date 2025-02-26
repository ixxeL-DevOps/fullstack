
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8e13473a267b23a092f51327f4376fc74f97c2c6
helm template . --name-template external-secrets-k0s --include-crds
```