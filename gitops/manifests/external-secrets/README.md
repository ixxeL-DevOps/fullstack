
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1b65ab93216059a32c0b8e28f36da2e2bd8730ac
helm template . --name-template external-secrets-k0s --include-crds
```