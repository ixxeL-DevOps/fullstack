
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8112aaa8ed74f4678d7cc5bb3747ae90b7ba45a5
helm template . --name-template external-secrets-k0s --include-crds
```