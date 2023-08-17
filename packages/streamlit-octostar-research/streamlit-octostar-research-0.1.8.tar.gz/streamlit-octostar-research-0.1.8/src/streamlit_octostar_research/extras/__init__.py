from streamlit_octostar_research.configure import octostar_component_func as _component_func
from streamlit_octostar_research.support import require

@require("key")
@require("path")
@require("name")
@require("nodes")
def create_link_chart(key=None,path=None,name=None,nodes=None,edges=None,draft=True):
    component_value = _component_func(
        call='octostar:desktop:extras:createLinkChart',
        replyTo=key,
        args=[{"path": path, "name": name, "nodes": nodes, "edges": edges, "draft": draft}]
    )
    return component_value