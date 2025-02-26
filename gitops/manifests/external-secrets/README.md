
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5715525abbe3261096997ac128274b4d5dfcdbf6
helm template . --name-template external-secrets-k0s --include-crds
```