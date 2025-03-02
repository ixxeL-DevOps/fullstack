
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ac5281449bb77a9d540a8bf9beafdefe9ae93a15
helm template . --name-template external-secrets-k0s --include-crds
```