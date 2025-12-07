import { useState } from "react";
import { apiPost } from "../api";

export default function BetScreen({ userName, gameData, setGameData }) {
    const [bet, setBet] = useState("");

    const placeBet = async () => {
        const res = await apiPost("/placeBet", {
            user_name: userName,
            bet: Number(bet),
        });
        setGameData(res.data);
    };

    return (
        <div>
            <h2>Place your bet</h2>
            <p>Balance: {gameData.playerBalance}</p>

            <input
                type="number"
                value={bet}
                onChange={(e) => setBet(e.target.value)}
            />
            <button onClick={placeBet}>Bet</button>
        </div>
    );
}
