"use client";
import Image from "next/image";
import styles from "./page.module.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { getGraphs } from "./api";
import { useRouter } from "next/navigation";

const ClickableList = ({ items, router }) => {
  const [selectedItem, setSelectedItem] = useState(null);

  const handleClick = (item) => {
    router.push(`/graph/?graphId=${item}`);
  };

  return (
    <div>
      {items && items.length > 0 ? (
        <ul>
          {items.map((item, index) => (
            <li
              key={index}
              onClick={() => handleClick(item)}
              style={{ cursor: "pointer", margin: "5px 0" }}
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p>Não há itens</p>
      )}
      {selectedItem && <p>Você selecionou: {selectedItem}</p>}
    </div>
  );
};

export default function Home() {
  // const items = ["Item 1", "Item 2", "Item 3"];
  // console.log(getGraphs());
  const [items, setItems] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const fetchGraphs = async () => {
      const graphs = await getGraphs();
      console.log(graphs + "teste");
      setItems(graphs);
    };

    fetchGraphs();
  }, []);

  return (
    <div
      style={{
        backgroundColor: "#f5f6fe",
      }}
    >
      <h1
        onClick={() => {
          router.push("/");
        }}
        style={{ cursor: "pointer" }}
      >
        Graph Management
      </h1>
      <ClickableList items={items} router={router} />
    </div>
  );
}
