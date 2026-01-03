import { apiPost } from "../api";
import Card from "./Card";

export default function GameScreen({ userName, gameData, setGameData }) {

    const hit = async () => {
        const res = await apiPost("/hit", { user_name: userName });
        setGameData(res.data);
    };

    const stand = async () => {
        const res = await apiPost("/stand", { user_name: userName });
        setGameData(res.data);
    };

    return (
        <div className="panel-wrapper game-wrapper">
            <div className="panel-container">
                <h1 className="panel-title">BLACKJACK</h1>
                <h2 className="panel-subtitle">Your turn</h2>

                <div className="game-section">
                    <h3 className="game-section-title">Dealer</h3>
                    <div className="game-cards">
                        {gameData.dealer.cards.map((c, i) => (
                            <Card key={i} card={c} />
                        ))}
                    </div>
                </div>

                <div className="game-section">
                    <h3 className="game-section-title">You</h3>
                    <div className="game-cards">
                        {gameData.player.cards.map((c, i) => (
                            <Card key={i} card={c} />
                        ))}
                    </div>
                </div>

                <div className="game-actions">
                    <button className="panel-button" onClick={hit}>Hit</button>
                    <button className="panel-button" onClick={stand}>Stand</button>
                </div>
            </div>
        </div>
    );
}
