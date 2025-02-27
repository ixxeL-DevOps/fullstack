
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a5e95e0a6e39ad3abe67a46c8cbd22e48e7fc424
helm template . --name-template external-secrets-k0s --include-crds
```