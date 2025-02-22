
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b01c3099a95993f942b7217feb4bf37ebfcac72a
helm template . --name-template external-secrets-k0s --include-crds
```