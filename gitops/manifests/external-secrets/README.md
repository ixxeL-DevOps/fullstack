
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9bd31a72fd1440d365943b6759f52b2600c5a80a
helm template . --name-template external-secrets-k0s --include-crds
```