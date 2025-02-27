
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 13b8a631cb5cb66bef1b3b185516da25e824961c
helm template . --name-template external-secrets-k0s --include-crds
```