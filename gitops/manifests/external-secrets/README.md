
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout c48538cd3215e947605ba206894fa5cc3d4b7462
helm template . --name-template external-secrets-k0s --include-crds
```