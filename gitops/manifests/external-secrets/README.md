
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout beae06bb2424f465334502575558c34d3836676e
helm template . --name-template external-secrets-k0s --include-crds
```