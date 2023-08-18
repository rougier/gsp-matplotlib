# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from distutils.core import setup

setup(
    name = 'GSP',
    version = "0",
    description = "Graphic Server Protocol",
    author = "Nicolas P. Rougier",
    author_email = "nicolas.rougier@inria.fr",
    packages = ["gsp", "gsp.core", "gsp.glm", "gsp.visual", "gsp.transform"]
)
