import { useState } from "react";
import { apiPost } from "../api";

export default function Login({ onLogin }) {
    const [name, setName] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await apiPost("/gameState", { user_name: name });
        onLogin(name, res.data);
    };

    return (
        <div style={{ padding: 20 }}>
            <h2>Enter your name:</h2>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <button type="submit">Start</button>
            </form>
        </div>
    );
}
