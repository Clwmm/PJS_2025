import { useState } from "react";
import Login from "./components/Login";
import BetScreen from "./components/BetScreen";
import GameScreen from "./components/GameScreen";
import EndScreen from "./components/EndScreen";

function App() {
    const [userName, setUserName] = useState("");
    const [gameData, setGameData] = useState(null);

    if (!userName) {
        return <Login onLogin={(name, data) => { setUserName(name); setGameData(data); }} />;
    }

    if (!gameData) return <div>Loading...</div>;

    const state = gameData.gameState;

    switch (state) {
        case "bet":
            return <BetScreen userName={userName} gameData={gameData} setGameData={setGameData} />;
        case "pTurn":
            return <GameScreen userName={userName} gameData={gameData} setGameData={setGameData} />;
        case "end":
            return <EndScreen userName={userName} gameData={gameData} setGameData={setGameData} />;
        default:
            return <div>Unknown state</div>;
    }
}

export default App;
