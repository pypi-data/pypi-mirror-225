from __future__ import annotations

import holoviews as hv
import numpy as np
import panel as pn

from holonote.annotate import Annotator

hv.extension("bokeh")


annotator = Annotator({'TIME': np.datetime64}, fields=['description'])
element = annotator.overlay(hv.Curve([]))
# b = pn.widgets.Button(name="A")
# b.on_click(lambda *e: annotator.add_annotation(description="2") and annotator.commit())
pn.Row(element).servable()

# Steps:
# Click on a plot with no annotatoions
