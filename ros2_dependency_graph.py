import xml.etree.ElementTree as ET
import networkx as nx
from pathlib import Path


def get_graph_networkx() -> nx.DiGraph:
    graph = nx.DiGraph()
    # TODO: Check for path validity
    # TODO: Handle arg better
    # directory = str(sys.argv[1])
    # directory = "E:\koodailuja\\ros2_dependency_graph\\test\mock_package"
    directory = "/ros2_dependency_graph/test/mock_package"
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

    return graph


def networkx_plt():
    graph = get_graph_networkx()

    graphviz_graph = nx.nx_agraph.to_agraph(graph)
    graphviz_graph.draw("g.png", args='-Gsize=50 -Gratio=0.5 -Gdpi=400', prog="dot")


# TODO: setup.py
def main():
    networkx_plt()


if __name__ == "__main__":
    main()
