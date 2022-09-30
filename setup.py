#[metadata]
#name = analysis-tools-ir
#version = 0.0.2
#author = Ayuei
#description = Common analysis tools for IR
#    classifiers =
#Programming Language :: Python :: 3
#License :: OSI Approved :: MIT License
#Operating System :: OS Independent
#
#[options]
#package_dir = src
#packages = find:
#python_requires = >=3.10
#
#
#[options.packages.find]
#where = src

from setuptools import setup, find_packages
import os, subprocess


os.makedirs("src/analysis_tools_ir/evaluate/bin", exist_ok=True)
subprocess.Popen(["make", "-C", "src/analysis_tools_ir/evaluate/trec_eval"],
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

os.replace("src/analysis_tools_ir/evaluate/trec_eval/trec_eval",
           "src/analysis_tools_ir/evaluate/bin/trec_eval")

setup(
    name='analysis-tools-ir',
    version='0.0.3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    url='',
    license='GNU GPLv3',
    author='Vincent Nguyen',
    author_email="vincent.nguyen@anu.edu.au",
    description='Common analysis tools for IR',
)
