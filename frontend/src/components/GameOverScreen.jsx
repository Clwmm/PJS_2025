import { apiPost } from "../api";

export default function GameOverScreen({ userName, setGameData }) {
    const resetGame = async () => {
        const res = await apiPost("/reset", { user_name: userName });
        setGameData(res.data);
    };

    return (
        <div className="panel-wrapper game-wrapper">
            <div className="panel-container">
                <h1 className="panel-title gameover-title">GAME OVER</h1>
                <h2 className="panel-subtitle">You lost all your money!</h2>
                <p className="gameover-text">Better luck next time!</p>
                <button className="panel-button" onClick={resetGame}>Play Again</button>
            </div>
        </div>
    );
}

