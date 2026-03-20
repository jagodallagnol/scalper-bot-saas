// ═══════════════════════════════════
// SCALPER BOT · TRADING.JS
// Motore di esecuzione ordini
// ═══════════════════════════════════

const API_TRADING = 'http://localhost:8889/api';

class MotoreTrade {
    constructor() {
        this.posizioniAttive = [];
        this.storicoTrade    = [];
        this.strategiaAttiva = 'scalping_avanzato';
    }

    async eseguiOrdineMarket(side, importo, simbolo = 'XRPUSDT') {
        try {
            const resp = await fetch(`${API_TRADING}/trade`, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ side, quantity: importo, symbol: simbolo })
            });

            const risultato = await risposta.json();

            if (risultato.successo) {
                this.aggiungiAlloStorico({
                    id:        risultato.trade?.orderId || Date.now(),
                    side,
                    importo,
                    prezzo:    risultato.trade?.price || 0,
                    timestamp: new Date().toISOString(),
                    stato:     'eseguito',
                    modalita:  risultato.modalita || 'demo'
                });
                return risultato;
            } else {
                throw new Error(risultato.errore || 'Errore sconosciuto');
            }
        } catch (e) {
            console.error('[MotoreTrade] Errore esecuzione:', e);
            throw e;
        }
    }

    aggiungiAlloStorico(trade) {
        this.storicoTrade.push(trade);
        this.aggiornaDisplayStorico();
    }

    aggiornaDisplayStorico() {
        const el = document.getElementById('storico-trade');
        if (!el) return;
        if (this.storicoTrade.length === 0) {
            el.innerHTML = '<div class="card"><div class="card-row"><span class="card-label">NESSUNA OPERAZIONE</span><span class="card-value">-</span></div></div>';
            return;
        }
        el.innerHTML = this.storicoTrade.slice().reverse().map(t => `
            <div class="card">
                <div class="card-row">
                    <span class="card-label">${t.side === 'BUY' ? '⬆ ACQUISTO' : '⬇ VENDITA'}</span>
                    <span class="card-value" style="color:${t.side === 'BUY' ? 'var(--green)' : 'var(--red)'}">
                        $${parseFloat(t.importo||0).toFixed(2)} USDT
                    </span>
                </div>
                <div class="card-row">
                    <span class="card-label">ORA</span>
                    <span class="card-value">${new Date(t.timestamp).toLocaleTimeString('it-IT')}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">STATO</span>
                    <span class="card-value">${(t.stato||'').toUpperCase()}${t.modalita==='demo'?' (Demo)':''}</span>
                </div>
            </div>
        `).join('');
    }

    calcolaRischioRendimento(prezzoEntrata, stopLoss, takeProfit) {
        const rischio  = Math.abs(prezzoEntrata - stopLoss);
        const profitto = Math.abs(takeProfit - prezzoEntrata);
        return {
            rischio,
            profitto,
            rapporto: profitto / rischio
        };
    }
}

// Istanza globale
const motoreTrade = new MotoreTrade();
