import axios from "axios";

export const getGraphs = async () => {
  try {
    const response = await axios.get("http://localhost:8000/get-graphs/");
    if (response.data.graphs) {
      const graphs = response.data.graphs.map((graph) => graph.toString());
      return graphs;
    } else {
      return [];
    }
  } catch (error) {
    return [];
  }
};

export const getGraph = async (graphId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/get-graph/?id=${graphId}`
    );
    if (response.data.graph) {
      return response.data.graph;
    } else {
      return null;
    }
  } catch (error) {
    return null;
  }
};

export const addNode = async (graphId, node) => {
    var bodyFormData = new FormData();
    bodyFormData.append("node", node);
    try {
      const response = await axios.put(
        `http://localhost:8000/add-node/?id=${graphId}`,
        bodyFormData
      );
      if (response.data.graph) {
        return response.data.graph;
      } else {
        return null;
      }
    } catch (error) {
      return null;
    }
}

export const generateNodePositions = (nodes) => {
  const positions = [];
  const spacing = 100; // espaçamento entre os nós
  const cols = Math.ceil(Math.sqrt(nodes.length)); // número de colunas na grade

  nodes.forEach((node, index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    positions.push({
      id: node.id,
      x: col * spacing,
      y: row * spacing,
    });
  });

  return positions;
};
