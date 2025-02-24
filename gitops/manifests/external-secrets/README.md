
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8b15ab2ccdf400589afd526a1c5b0088851d9373
helm template . --name-template external-secrets-k0s --include-crds
```