
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 99e487f5e285c8f01e9dcdd3b1ddba2e7de0eeb0
helm template . --name-template external-secrets-k0s --include-crds
```