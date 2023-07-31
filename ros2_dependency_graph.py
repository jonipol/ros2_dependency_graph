import sys
import xml.etree.ElementTree as ET
import networkx as nx
from pathlib import Path
from pyvis.network import Network
import json


# TODO: setup.py
def main():
    graph = nx.DiGraph()
    # TODO: Check for path validity
    # TODO: Handle arg better
    directory = str(sys.argv[1])
    package_xmls = [xml_path for xml_path in Path(directory).rglob('**/package.xml')]

    # Parse xml and add to graph
    for package_xml in package_xmls:
        root = ET.parse(package_xml).getroot()
        pkg = root.find("name")
        graph.add_node(pkg.text)
        for child in root:
            # TODO: Separate build/exec/test depends. Different color/style arrows?
            if child.tag in ["depend", "build_depend", "exec_depend", "test_depend"]:
                graph.add_node(child.text)
                graph.add_edge(pkg.text, child.text)

    net = Network()
    net.from_nx(graph)
    net.show_buttons(filter_=True)
    options = {
        "configure": {
            "enabled": True
        },
        "interaction": {
            "hover": True
        },
        "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 6,
            "chosen": True,
            "color": {
                "highlight": {
                    "border": "#FF4040",
                    "background": "#EE3B3B"
                },
                "hover": {
                    "border": "#DEB887",
                    "background": "#FFD39B"
                }
            }
        },
        "edges": {
            "arrows": {
                "to": True
            },
            "color": {
                "color": "#00bfff",
                "highlight": "#EE3B3B",
                "hover": "#DEB887"
            }
        },
        "layout": {
            "hierarchical": {
                "enabled": True,
                "levelSeparation": 150,
                "nodeSpacing": 400,
                "treeSpacing": 150,
                "blockShifting": True,
                "edgeMinimization": True,
                "parentCentralization": True,
                "direction": "UD",
                "sortMethod": "directed",
                "shakeTowards": "leaves"
            }
        }
    }
    net.set_options(json.dumps(options))
    # net.toggle_physics(False)
    net.write_html("graph.html")


if __name__ == "__main__":
    main()
