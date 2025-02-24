
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 80dcf95e5bf3a0fec99e0cb9a1ad389e220c768f
helm template . --name-template external-secrets-k0s --include-crds
```