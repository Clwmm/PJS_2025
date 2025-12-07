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
        <div>
            <h2>Your turn</h2>

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

            <button onClick={hit}>Hit</button>
            <button onClick={stand}>Stand</button>
        </div>
    );
}
