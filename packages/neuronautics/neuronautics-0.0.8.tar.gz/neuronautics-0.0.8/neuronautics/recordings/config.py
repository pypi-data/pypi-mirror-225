
import os
import pkg_resources

MAX_WORKERS = os.cpu_count() - 1


UI_NEURONAUTICS = pkg_resources.resource_filename("neuronautics.ui", "neuronautics.ui")
UI_LAYOUT_CREATION = pkg_resources.resource_filename("neuronautics.ui", "layout-creation.ui")
UI_ANALYSIS_CREATION = pkg_resources.resource_filename("neuronautics.ui", "analysis-creation.ui")

JINJA_GRAPH_ANALYSIS = pkg_resources.resource_filename("neuronautics.analysis.templates", "graph-analysis.jinja")
JINJA_BAR_ANALYSIS = pkg_resources.resource_filename("neuronautics.analysis.templates", "bar-analysis.jinja")
JINJA_LINE_ANALYSIS = pkg_resources.resource_filename("neuronautics.analysis.templates", "line-analysis.jinja")
JINJA_IMAGE_ANALYSIS = pkg_resources.resource_filename("neuronautics.analysis.templates", "image-analysis.jinja")
JINJA_BASE_ANALYSIS = pkg_resources.resource_filename("neuronautics.analysis.templates", "base-analysis.jinja")

YML_ANALYSIS_BASE = pkg_resources.resource_filename("neuronautics.analysis", "analysis-base.yml")