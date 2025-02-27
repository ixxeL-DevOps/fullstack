
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a0003ed981ecea6f099cb7ff353435f2846ae91e
helm template . --name-template external-secrets-k0s --include-crds
```