
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 97414698a78aaf5eba75a7d031220a36dcf3233b
helm template . --name-template wireguard-k0s --include-crds
```