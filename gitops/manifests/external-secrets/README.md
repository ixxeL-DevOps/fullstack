
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 58380b229cb9873ee7c4f09deb525ba6e8c1af09
helm template . --name-template external-secrets-k0s --include-crds
```