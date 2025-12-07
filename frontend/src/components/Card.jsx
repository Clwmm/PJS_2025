export default function Card({ card }) {
    if (card.hidden) return <div className="card back">🂠</div>;

    return (
        <div className="card">
            {card.value} {card.suit}
        </div>
    );
}
