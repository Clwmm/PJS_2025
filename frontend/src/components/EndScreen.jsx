import { useState } from "react";
import { apiPost } from "../api";
import Card from "./Card";

export default function EndScreen({ userName, gameData, setGameData }) {
    const [bet, setBet] = useState("");

    const newBet = async () => {
        const res = await apiPost("/placeBet", {
            user_name: userName,
            bet: Number(bet),
        });
        setGameData(res.data);
    };

    return (
        <div>
            <h2>Result: {gameData.result}</h2>
            <p>Balance: {gameData.playerBalance}</p>
            <p>Bet was: {gameData.bet}</p>

            <h3>Dealer</h3>
            <div className="cards-row">
                {gameData.dealer.cards.map((c, i) => (
                    <Card key={i} card={c} />
                ))}
            </div>

            <h3>You</h3>
            <div className="cards-row">
                {gameData.player.cards.map((c, i) => (
                    <Card key={i} card={c} />
                ))}
            </div>

            <h3>Play again</h3>
            <input
                type="number"
                value={bet}
                onChange={(e) => setBet(e.target.value)}
            />
            <button onClick={newBet}>Place Bet</button>
        </div>
    );
}
