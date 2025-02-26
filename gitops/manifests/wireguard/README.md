
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e835e15ac199b333417fb34ff2341f6a676c5a3e
helm template . --name-template wireguard-k0s --include-crds
```