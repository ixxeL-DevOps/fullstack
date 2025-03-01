
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9ebbc1e235d30316e0e5852ce5f0214599f50e3e
helm template . --name-template external-secrets-k0s --include-crds
```