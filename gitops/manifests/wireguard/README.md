
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout fa5ddc1f38c79b2a74cf3fe6946c2a5b89078457
helm template . --name-template wireguard-k0s --include-crds
```