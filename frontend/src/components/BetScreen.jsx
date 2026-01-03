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
        <div className="panel-wrapper bet-wrapper">
            <div className="panel-container">
                <h1 className="panel-title">BLACKJACK</h1>
                <h2 className="panel-subtitle">Place your bet</h2>
                
                <div className="info-box">
                    <span className="info-label">Balance:</span>
                    <span className="info-value">{gameData.playerBalance}</span>
                </div>

                <form className="panel-form" onSubmit={(e) => { e.preventDefault(); placeBet(); }}>
                    <div className="bet-input-wrapper">
                        <input
                            className="panel-input bet-input"
                            type="number"
                            value={bet}
                            onChange={(e) => setBet(e.target.value)}
                            placeholder="Enter bet amount"
                            min="1"
                            max={gameData.playerBalance}
                            autoFocus
                        />
                        <div className="bet-input-spinner">
                            <button
                                type="button"
                                className="bet-spinner-button bet-spinner-up"
                                onClick={() => {
                                    const current = Number(bet);
                                    const newValue = Math.min(current + 1, gameData.playerBalance);
                                    setBet(String(newValue));
                                }}
                            />
                            <button
                                type="button"
                                className="bet-spinner-button bet-spinner-down"
                                onClick={() => {
                                    const current = Number(bet);
                                    const newValue = Math.max(current - 1, 1);
                                    setBet(String(newValue));
                                }}
                            />
                        </div>
                    </div>
                    <button className="panel-button" type="submit">Bet</button>
                </form>
            </div>
        </div>
    );
}
