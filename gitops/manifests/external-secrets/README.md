
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3403eafdc077382850cba1f18d59edd83483c0cf
helm template . --name-template external-secrets-k0s --include-crds
```