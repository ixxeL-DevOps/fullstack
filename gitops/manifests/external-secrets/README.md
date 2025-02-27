
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5dac8e1153958c08a7030d2e475dda81d8aa21cf
helm template . --name-template external-secrets-k0s --include-crds
```