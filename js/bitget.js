// ═══════════════════════════════════
// SCALPER BOT · BITGET.JS
// WebSocket per prezzi in tempo reale
// ═══════════════════════════════════

class BitgetStream {
    constructor() {
        this.ws = null;
        this.simbolo = 'XRPUSDT';
        this.listeners = [];
        this.connesso = false;
    }

    connetti(simbolo = 'XRPUSDT') {
        this.simbolo = simbolo;
        const wsUrl = 'wss://ws.bitget.com/v2/ws/public';
        try {
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                this.connesso = true;
                console.log('[Bitget WS] Connesso');
                const msg = {
                    "op": "subscribe",
                    "args": [{
                        "instType": "USDT-FUTURES",
                        "channel":  "ticker",
                        "instId":   this.simbolo
                    }]
                };
                this.ws.send(JSON.stringify(msg));
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.data && data.data[0]) {
                        this.notificaListeners(data.data[0]);
                    }
                } catch {}
            };

            this.ws.onerror = () => console.warn('[Bitget WS] Errore connessione');
            this.ws.onclose = () => {
                this.connesso = false;
                console.log('[Bitget WS] Disconnesso — riconnessione tra 5s');
                setTimeout(() => this.connetti(this.simbolo), 5000);
            };
        } catch (e) {
            console.warn('[Bitget WS] Impossibile connettersi:', e.message);
        }
    }

    aggiungiListener(callback) {
        this.listeners.push(callback);
    }

    notificaListeners(data) {
        this.listeners.forEach(cb => cb(data));
    }

    disconnetti() {
        if (this.ws) this.ws.close();
    }
}

// Esporta istanza globale
const bitgetStream = new BitgetStream();
