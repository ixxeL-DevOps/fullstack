
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9d6dd456e97a633b6925c4e62fadeecf4880fb73
helm template . --name-template external-secrets-k0s --include-crds
```