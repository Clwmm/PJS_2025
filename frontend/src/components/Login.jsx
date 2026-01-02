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
        <div className="login-wrapper">
            <div className="login-container">
                <div className="login-icon">
                    <img src="/casino-icon.svg" alt="Casino" />
                </div>
                <h1 className="login-title">BLACKJACK</h1>
                <h2 className="login-subtitle">Enter your name:</h2>

                <form className="login-form" onSubmit={handleSubmit}>
                    <input
                        className="login-input"
                        type="text"
                        placeholder="Enter your name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        autoFocus
                    />
                    <button className="login-button" type="submit">
                        Start Game
                    </button>
                </form>
            </div>
        </div>
    );
}
