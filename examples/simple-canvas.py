# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Simple light example

This example doesn't do much, it just makes a simple plot
"""
from gsp.core import Canvas

canvas = Canvas(512, 512, 100.0)
canvas.render("simple-canvas.png")


