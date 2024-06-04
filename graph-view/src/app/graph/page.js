"use client";
import { useRouter, useSearchParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import CytoscapeComponent from "react-cytoscapejs";
import { addNode, generateNodePositions, getGraph } from "../api";

export default function Graph() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const graphId = searchParams.get("graphId");

  const [width, setWith] = useState("100%");
  const [height, setHeight] = useState("400px");
  //Adding elements here
  const [graphData, setGraphData] = useState([
    //Node format
    {
      data: { id: "1", label: "Node A" },
      position: { x: 600, y: 100 },
      style: { backgroundColor: "blue" },
    },
    {
      data: { id: "2", label: "Node B" },
      position: { x: 550, y: 300 },
      style: { backgroundColor: "red" },
    },
    //Edge format
    { data: { source: "1", target: "2", label: "Edge from Node1 to Node2" } },
  ]);

  const [updatedGraphView, setUpdatedGraphView] = useState(false);

  useEffect(() => {
    const fetchGraph = async () => {
      const graph = await getGraph(graphId);
      if (graph) {
        const positions = generateNodePositions(graph.nodes);
        const nodes = graph.nodes.map((node) => {
          const position = positions.find((pos) => pos.id === node.id);
          return {
            data: { id: node.id, label: node.id },
            position: { x: position.x, y: position.y },
            style: { backgroundColor: "blue" },
          };
        });

        const edges = graph.links.map((edge) => {
          return {
            data: {
              source: edge.source,
              target: edge.target,
              label: edge.weight,
            },
          };
        });
        setGraphData([...nodes, ...edges]);
      }
    };

    fetchGraph();
  }, [graphId, updatedGraphView]);

  return (
    <>
      <div>
        <h1
          onClick={() => {
            router.push("/");
          }}
          style={{
            cursor: "pointer",
          }}
        >
          Graph Management
        </h1>
        <p>Graph ID: {graphId}</p>
        <div>
          <button
            onClick={async () => {
              const node = prompt("Enter the node name");
              if (node) {
                await addNode(graphId, node).then((newNode) => {
                  if (newNode) {
                    setGraphData((prevGraphData) => {
                      const positions = generateNodePositions([
                        ...prevGraphData.filter((e) => e.data.id),
                        newNode,
                      ]);
                      const updatedNodes = [
                        ...prevGraphData.filter((e) => e.group === "nodes"),
                        {
                          data: { id: newNode.id, label: newNode.id },
                          position: {
                            x: positions.find((pos) => pos.id === newNode.id).x,
                            y: positions.find((pos) => pos.id === newNode.id).y,
                          },
                          style: { backgroundColor: "blue" },
                        },
                      ];
                      return [
                        ...updatedNodes,
                        ...prevGraphData.filter((e) => e.group === "edges"),
                      ];
                    });
                  }
                });
              }
            }}
          >
            Add
          </button>
        </div>
        <div
          style={{
            border: "1px solid",
            backgroundColor: "#f5f6fe",
          }}
        >
          <CytoscapeComponent
            elements={graphData}
            style={{ width: width, height: height }}
          />
        </div>
      </div>
    </>
  );
}
