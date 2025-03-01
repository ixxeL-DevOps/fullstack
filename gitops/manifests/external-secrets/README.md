
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3c90365fa082112182a4d654df085ce77206a056
helm template . --name-template external-secrets-k0s --include-crds
```