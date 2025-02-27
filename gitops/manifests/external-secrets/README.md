
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ed7fb38105a83279e6a3108b62f15a600f649de0
helm template . --name-template external-secrets-k0s --include-crds
```