import io
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("kube_bench_report_converter_2/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setup(name='kube-bench-report-converter-2',
      version=version,
      description='Converts kube-bench checks console output to CSV.',
      long_description=readme,
      long_description_content_type="text/markdown",
      keywords='kube-bench report convert csv',
      url='https://github.com/pjaudiomv/kube-bench-report-converter-2',
      project_urls={
          "Code": "https://github.com/pjaudiomv/kube-bench-report-converter-2",
          "Issue tracker": "https://github.com/pjaudiomv/kube-bench-report-converter-2/issues",
      },
      author='Patrick Joyce',
      author_email='pjaudiomv@gmail.com',
      maintainer="Patrick Joyce",
      maintainer_email="pjaudiomv@gmail.com",
      license='MIT',
      packages=['kube_bench_report_converter_2'],
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*,!=3.5.*',
      install_requires=[],
      classifiers=[
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['kube-bench-report-converter-2=kube_bench_report_converter_2.command_line:main'],
      }
)
