from setuptools import setup
import site
import os


def generate_sitecustomize():
    sitecustomize_content = '''
import sys
import builtins

def my_import_hook(name, *args, **kwargs):
    if name == 'torch':
        from cuda2mlu import torch_proxy
    return original_import(name, *args, **kwargs)

original_import = builtins.__import__
builtins.__import__ = my_import_hook

'''

    site_packages_dir = site.getsitepackages()[0]
    sitecustomize_path = os.path.join(site_packages_dir, "sitecustomize.py")
    with open(sitecustomize_path, "w") as f:
        f.write(sitecustomize_content)

def remove_sitecustomize():
    site_packages_dir = site.getsitepackages()[0]
    sitecustomize_path = os.path.join(site_packages_dir, "sitecustomize.py")

    if os.path.exists(sitecustomize_path):
        os.remove(sitecustomize_path)

generate_sitecustomize()

setup(
    name="cuda2mlu",
    version="0.1",
    description="A package that rewrites torch device CUDA  to use MLU",
    packages=["cuda2mlu"],
    install_requires=["torch"],
    setup_requires=["torch"],
    python_requires=">=3.6"
)

