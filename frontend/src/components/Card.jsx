export default function Card({ card }) {
    if (card.hidden) return <div className="card card-back">🂠</div>;

    const suitSymbols = {
        'hearts': '♥',        //red
        'diamonds': '♦',      //red
        'clubs': '♣',
        'spades': '♠'
    };

    const suitSymbol = suitSymbols[card.suit];
    const isRed = card.suit === 'hearts' || card.suit === 'diamonds';

    return (
        <div className={`card ${isRed ? 'card-red' : 'card-black'}`}>
            <div className="card-corner card-corner-top">
                <div className="card-value">{card.value}</div>
                <div className="card-suit-small">{suitSymbol}</div>
            </div>
            <div className="card-center">
                <div className="card-suit-large">{suitSymbol}</div>
            </div>
            <div className="card-corner card-corner-bottom">
                <div className="card-suit-small">{suitSymbol}</div>
                <div className="card-value">{card.value}</div>
            </div>
        </div>
    );
}
