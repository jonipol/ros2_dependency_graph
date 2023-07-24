import sys
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
# from networkx.drawing.nx_pydot import write_dot


def main():
    graph = nx.DiGraph()
    directory = str(sys.argv[0])
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

    nx.draw(graph, with_labels=True, font_weight="bold")
    # pos = nx.nx_agraph.graphviz_layout(graph)
    # pos = nx.spring_layout(graph)
    # nx.draw(graph, pos=pos, with_labels=True)
    # write_dot(graph, 'file.dot')
    plt.show()


if __name__ == "__main__":
    main()
