# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from distutils.core import setup

setup(
    name = 'GSP',
    version = "0",
    description = "Graphic Server Protocol",
    author = "Nicolas P. Rougier",
    author_email = "nicolas.rougier@inria.fr",
    packages = [ "gsp",
                 "gsp.core",
                 "gsp.visual",
                 "gsp.transform"])
