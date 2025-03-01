
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a66759d7f1e70b222804c9e29b212e277e4d94df
helm template . --name-template external-secrets-k0s --include-crds
```