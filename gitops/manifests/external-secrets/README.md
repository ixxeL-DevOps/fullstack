
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b29d54a7b25cd1b564394788597fd18bb24c599c
helm template . --name-template external-secrets-k0s --include-crds
```