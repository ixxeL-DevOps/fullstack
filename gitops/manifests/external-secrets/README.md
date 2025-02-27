
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 99db783d1a44233ae9f32c17020cea78e4e093b2
helm template . --name-template external-secrets-k0s --include-crds
```