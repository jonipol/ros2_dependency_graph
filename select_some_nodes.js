                   function addChildNodes(nodesToUpdate, node){
                  // Add child nodes for the passed node
                  // Loop around all edges
                  data.edges.forEach(edge => {
                    // Check if connected from the passed node and connected node exists
                    if(edge.from === node.id && data.nodes.get(edge.to)){
                      // Find the child node in the update array
                      let childNode = nodesToUpdate.find(node => node.id === edge.to);

                      // Check if the child node is hidden
                      // If the node is not hidden then it's already been processed
                      // Don't process it again otherwise could get caught in a loop
                      if(childNode.hidden){
                        // Node is currently hidden, therefore hasn't been processed yet
                        // Set node to be displayed
                        childNode.hidden = false;

                        // Recursive call to function to process its children
                        addChildNodes(nodesToUpdate, childNode);
                      }
                    }
                  });
                }

                network.on('select', function (properties) {
                  // Define an array of nodes ot update, this is quicker than
                  // updating each node individually
                  let nodesToUpdate = [];

                  // If no nodes are selected, unhide all hidden nodes
                  if(properties.nodes.length === 0){
                    // Populate array with list of nodes to unhide
                    data.nodes.forEach(node => {
                      if(node.hidden){
                        nodesToUpdate.push({id:node.id, hidden: false});
                      }
                    });

                    // Update nodes and return
                    data.nodes.update(nodesToUpdate);
                    return;
                  }

                  // One or more nodes are selected
                  // Populate array with list of all nodes, hiding them
                  data.nodes.forEach(node => {
                    nodesToUpdate.push({id:node.id, hidden: true});
                  });

                  // Update the arra setting list of selected and connected nodes to unhide
                  properties.nodes.forEach(nodeId => {
                    // Find the selected node in the array
                    let node = nodesToUpdate.find(node => node.id === nodeId);

                    // Update selected node to be displayed
                    node.hidden = false;

                    // Call recursive function to add all dependents
                    addChildNodes(nodesToUpdate, node);
                  });

                  // Submit updates to hide/unhide nodes
                  data.nodes.update(nodesToUpdate);
                });
