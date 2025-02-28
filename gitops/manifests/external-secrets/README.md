
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 2f30f81b0877a61615fc8f9633f4e5acfaa774cd
helm template . --name-template external-secrets-k0s --include-crds
```