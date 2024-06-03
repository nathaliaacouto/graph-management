"use client";
import React, { useState } from "react";
import CytoscapeComponent from "react-cytoscapejs";
export default function App() {
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
  return (
    <>
      <div>
        <h1>Graph Management</h1>
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
