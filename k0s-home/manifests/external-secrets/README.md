
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 692d63725ba753f1642618ce6557f016f8b1ac94
helm template . --name-template external-secrets-k0s --include-crds
```