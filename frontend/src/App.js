import React, { useState, useEffect } from "react";
import TerminalComponent from "./TerminalComponent";

function App() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/items/")
            .then(response => response.json())
            .then(data => setItems(data));
    }, []);

    return (
        <div>
            {/* <h1>Items List</h1>
            <ul>
                {items.map(item => (
                    <li key={item.id}>{item.name} - {item.description}</li>
                ))}
            </ul> */}
            <TerminalComponent />
        </div>
    );
}

export default App;
