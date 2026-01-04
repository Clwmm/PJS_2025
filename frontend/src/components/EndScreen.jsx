import Card from "./Card";
import GameOverScreen from "./GameOverScreen";

export default function EndScreen({ userName, gameData, setGameData }) {
    //no money = game over screen
    if (gameData.playerBalance === 0) {
        return <GameOverScreen userName={userName} setGameData={setGameData} />;
    }
    const playAgain = () => {
        setGameData({
            gameState: "bet",
            playerBalance: gameData.playerBalance
        });
    };

    //text for the result of the game
    const getResultText = () => {
        if (gameData.result === "player") return "You Win!";
        if (gameData.result === "dealer") return "Dealer Wins!";
        return "Draw!";
    };

    //css classes for the result of the game
    const getResultClass = () => {
        if (gameData.result === "player") return "end-result end-result-win";
        if (gameData.result === "dealer") return "end-result end-result-lose";
        return "end-result end-result-draw";
    };

    return (
        <div className="panel-wrapper end-wrapper">
            <div className="panel-container">
                <h1 className="panel-title">BLACKJACK</h1>
                <div className={getResultClass()}>{getResultText()}</div>

                <div className="end-info">
                    <div className="info-box">
                        <span className="info-label">Balance:</span>
                        <span className="info-value">{gameData.playerBalance}</span>
                    </div>
                    <div className="info-box">
                        <span className="info-label">Bet was:</span>
                        <span className="info-value">{gameData.bet}</span>
                    </div>
                </div>

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
                    <button className="panel-button" onClick={playAgain}>Play Again</button>
                </div>
            </div>
        </div>
    );
}
