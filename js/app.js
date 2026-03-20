// ═══════════════════════════════════
// SCALPER BOT · APP.JS
// ═══════════════════════════════════

const API_URL = 'http://localhost:8889/api';

class ScalperApp {
    constructor() {
        this.currentTab = 'dashboard';
        this.isConnected = false;
        this.botRunning = false;
        this.currentExchange = localStorage.getItem('current_exchange') || 'bitget';
        this.priceData = {};
        this.portfolio = {
            totalBalance: 0,
            availableBalance: 0,
            trades: [],
            positions: []
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadExchangeSettings();
        this.checkConnection();
        this.startPriceFetch();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });

        document.querySelectorAll('.footer-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabName = e.currentTarget.dataset.tabNav;
                this.switchTab(tabName);
            });
        });

        // Buttons
        document.getElementById('start-bot').addEventListener('click', () => this.startBot());
        document.getElementById('stop-bot').addEventListener('click', () => this.stopBot());
        document.getElementById('connect-wallet').addEventListener('click', () => this.connectWallet());
        document.getElementById('save-api').addEventListener('click', () => this.saveAPICredentials());
        document.getElementById('save-params').addEventListener('click', () => this.saveParams());
        document.getElementById('change-exchange').addEventListener('click', () => this.changeExchange());

        // Trade buttons
        document.querySelectorAll('.btn-success, .btn-danger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.target.textContent.includes('ACQUISTA') ? 'buy' : 'sell';
                this.executeTrade(type);
            });
        });
    }

    switchTab(tabName) {
        // Hide all tab contents
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Remove active from tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });

        document.querySelectorAll('.footer-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        const tabElement = document.getElementById(tabName);
        if (tabElement) {
            tabElement.classList.add('active');
        }

        // Set active tab button
        document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');
        document.querySelector(`[data-tab-nav="${tabName}"]`)?.classList.add('active');

        this.currentTab = tabName;
        
        // Carica dati specifici per il tab
        if (tabName === 'dashboard') {
            this.updateDashboard();
        } else if (tabName === 'positions') {
            this.loadPositions();
        } else if (tabName === 'settings') {
            this.updateExchangeInfo();
        }
    }

    async checkConnection() {
        try {
            const response = await fetch(`${API_URL}/status`);
            if (response.ok) {
                const data = await response.json();
                this.isConnected = true;
                this.updateConnectionStatus(true);
                console.log('✅ Connesso al backend');
            }
        } catch (error) {
            this.updateConnectionStatus(false);
            console.log('Backend non disponibile, tentando riconnessione tra 5 secondi...');
            setTimeout(() => this.checkConnection(), 5000);
        }
    }

    updateConnectionStatus(connected) {
        const statusEl = document.getElementById('live-status');
        const marketStatusEl = document.getElementById('market-status');
        
        if (connected) {
            statusEl.textContent = 'ONLINE';
            statusEl.parentElement.parentElement.querySelector('.live-dot').style.boxShadow = '0 0 5px #ccff00';
            marketStatusEl.className = 'status';
            marketStatusEl.textContent = '✓ CONNESSO A BITGET';
            marketStatusEl.style.borderColor = '#00ff88';
            marketStatusEl.style.background = 'rgba(0,255,136,0.05)';
        } else {
            statusEl.textContent = 'OFFLINE';
            marketStatusEl.className = 'status error';
            marketStatusEl.textContent = '✗ OFFLINE - Connessione al server fallita';
        }
    }

    startPriceFetch() {
        setInterval(() => {
            if (this.isConnected) {
                this.fetchPrice();
                this.fetchBalance();
                this.updateDashboard();
            }
        }, 5000); // Aggiorna ogni 5 secondi

        // Prima fetch immediata
        if (this.isConnected) {
            this.fetchPrice();
            this.fetchBalance();
            this.updateDashboard();
        }
    }

    async fetchPrice() {
        try {
            const response = await fetch(`${API_URL}/price`);
            const data = await response.json();
            this.updatePriceDisplay(data);
        } catch (error) {
            console.error('Errore nel fetch del prezzo:', error);
        }
    }

    updatePriceDisplay(data) {
        if (!data) return;

        // Header price
        document.getElementById('current-price').textContent = `$${parseFloat(data.price).toFixed(4)}`;
        
        const change = parseFloat(data.change24h || 0);
        const changeEl = document.getElementById('price-change');
        changeEl.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
        changeEl.className = `price-change ${change < 0 ? 'negative' : ''}`;

        // Dashboard price info
        document.getElementById('price-current').textContent = `$${parseFloat(data.price).toFixed(4)}`;
        document.getElementById('price-high').textContent = `$${parseFloat(data.high24h || 0).toFixed(4)}`;
        document.getElementById('price-low').textContent = `$${parseFloat(data.low24h || 0).toFixed(4)}`;
        document.getElementById('volume').textContent = `${(parseFloat(data.volume24h || 0) / 1000000).toFixed(2)}M`;

        this.priceData = data;
    }

    async fetchBalance() {
        try {
            const response = await fetch(`${API_URL}/balance`);
            const data = await response.json();
            this.updateBalanceDisplay(data);
        } catch (error) {
            console.error('Errore nel fetch del saldo:', error);
        }
    }

    updateBalanceDisplay(data) {
        if (!data) return;

        document.getElementById('total-balance').textContent = `$${parseFloat(data.total || 0).toFixed(2)}`;
        document.getElementById('available-balance').textContent = `$${parseFloat(data.available || 0).toFixed(2)}`;

        // Posizioni
        if (data.positions) {
            this.portfolio.positions = data.positions;
        }
    }

    async updateDashboard() {
        try {
            const response = await fetch(`${API_URL}/market-data`);
            const data = await response.json();
            
            if (data.indicators) {
                const ema5El = document.getElementById('ema5-value');
                const ema20El = document.getElementById('ema20-value');
                const rsiEl = document.getElementById('rsi-value');
                const signalEl = document.getElementById('signal-value');

                if (ema5El) ema5El.textContent = data.indicators.ema5 ? data.indicators.ema5.toFixed(4) : 'N/A';
                if (ema20El) ema20El.textContent = data.indicators.ema20 ? data.indicators.ema20.toFixed(4) : 'N/A';
                
                if (rsiEl && data.indicators.rsi) {
                    const rsi = data.indicators.rsi;
                    rsiEl.textContent = rsi.toFixed(2);
                    rsiEl.style.color = rsi > 70 ? 'var(--red)' : rsi < 30 ? 'var(--green)' : 'var(--lime)';
                }

                if (signalEl) {
                    const sig = data.indicators.signal || 'HOLD';
                    signalEl.textContent = sig;
                    signalEl.style.color = sig === 'BUY' ? 'var(--green)' : sig === 'SELL' ? 'var(--red)' : 'var(--lime)';
                }
            }
        } catch (error) {
            console.error('Errore nel caricamento dashboard:', error);
        }
    }

    async loadPositions() {
        try {
            const response = await fetch(`${API_URL}/trades`);
            const data = await response.json();
            
            // Calcola PnL totale
            let totalPnL = 0;
            if (data.trades && data.trades.length > 0) {
                totalPnL = data.trades.reduce((sum, t) => sum + (parseFloat(t.profit) || 0), 0);

                const tradesHtml = data.trades.map(trade => `
                    <div class="card" style="margin-bottom:6px">
                        <div class="card-row">
                            <span class="card-label">SIDE</span>
                            <span class="card-value" style="color:${trade.side === 'SELL' ? 'var(--red)' : 'var(--green)'}">${trade.side || 'BUY'}</span>
                        </div>
                        <div class="card-row">
                            <span class="card-label">IMPORTO</span>
                            <span class="card-value">$${parseFloat(trade.quantity || 0).toFixed(2)}</span>
                        </div>
                        <div class="card-row">
                            <span class="card-label">PREZZO</span>
                            <span class="card-value">$${parseFloat(trade.price || 0).toFixed(4)}</span>
                        </div>
                        <div class="card-row">
                            <span class="card-label">TEMPO</span>
                            <span class="card-value">${new Date(trade.time || trade.timestamp || Date.now()).toLocaleTimeString()}</span>
                        </div>
                        <div class="card-row">
                            <span class="card-label">P&L</span>
                            <span class="card-value" style="color:${(trade.profit || 0) >= 0 ? 'var(--green)' : 'var(--red)'}">${trade.profit ? '$' + parseFloat(trade.profit).toFixed(2) : 'N/A'}</span>
                        </div>
                    </div>
                `).join('');
                
                const tradesEl = document.getElementById('trades-history');
                if (tradesEl) tradesEl.innerHTML = tradesHtml;
            } else {
                const tradesEl = document.getElementById('trades-history');
                if (tradesEl) tradesEl.innerHTML = '<div class="card"><div class="card-row"><span class="card-label">NESSUN TRADE</span><span class="card-value">-</span></div></div>';
            }

            // Aggiorna PnL e gain totale
            document.getElementById('pnl').textContent = `${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`;
            document.getElementById('pnl').style.color = totalPnL >= 0 ? 'var(--green)' : 'var(--red)';

            const totalGain = (totalPnL / 1000 * 100).toFixed(2);
            document.getElementById('total-gain').textContent = `${totalGain >= 0 ? '+' : ''}${totalGain}%`;
            document.getElementById('total-gain').style.color = totalGain >= 0 ? 'var(--green)' : 'var(--red)';

            // Aggiorna trade count
            document.getElementById('total-trades').textContent = data.count || 0;

            this.portfolio = data;
        } catch (error) {
            console.error('Errore nel caricamento posizioni:', error);
        }
    }

    async startBot() {
        try {
            const response = await fetch(`${API_URL}/bot/start`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.botRunning = true;
                document.getElementById('strategy-status').textContent = 'RUNNING';
                document.getElementById('strategy-status').style.color = '#00ff88';
                this.showNotification('✅ Bot avviato con successo!');
            }
        } catch (error) {
            this.showNotification('❌ Errore nell\'avvio del bot', 'error');
            console.error(error);
        }
    }

    async stopBot() {
        try {
            const response = await fetch(`${API_URL}/bot/stop`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.botRunning = false;
                document.getElementById('strategy-status').textContent = 'STOPPED';
                document.getElementById('strategy-status').style.color = '#ff3333';
                this.showNotification('🛑 Bot fermato');
            }
        } catch (error) {
            this.showNotification('❌ Errore nel fermo del bot', 'error');
            console.error(error);
        }
    }

    connectWallet() {
        this.switchTab('settings');
        document.getElementById('api-key').focus();
        this.showNotification('📝 Inserisci le tue credenziali Bitget');
    }

    saveAPICredentials() {
        const apiKey = document.getElementById('api-key').value;
        const apiSecret = document.getElementById('api-secret').value;

        if (!apiKey || !apiSecret) {
            this.showNotification('⚠️  Inserisci API Key e Secret', 'error');
            return;
        }

        localStorage.setItem('bitget_apikey', apiKey);
        localStorage.setItem('bitget_apisecret', apiSecret);

        this.showNotification('✅ Credenziali salvate!');
        
        // Send to backend
        this.sendCredentialsToBackend(apiKey, apiSecret);
    }

    async sendCredentialsToBackend(apiKey, apiSecret) {
        try {
            await fetch(`${API_URL}/credentials`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ apiKey, apiSecret })
            });
        } catch (error) {
            console.error('Errore nell\'invio credenziali', error);
        }
    }

    saveParams() {
        const params = {
            minAmount: document.getElementById('min-amount')?.value || '10',
            targetGain: document.getElementById('target-gain')?.value || '1.5',
            checkInterval: document.getElementById('check-interval')?.value || '5'
        };

        localStorage.setItem('scalper_params', JSON.stringify(params));
        this.showNotification('✅ Parametri salvati!');
    }

    async executeTrade(type) {
        const amount = parseFloat(document.getElementById('trade-amount')?.value || 0);
        const stopLoss = parseFloat(document.getElementById('stop-loss')?.value || 0);
        const takeProfit = parseFloat(document.getElementById('take-profit')?.value || 0);

        if (!amount || amount <= 0) {
            this.showNotification('⚠️  Importo non valido', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/trade`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    side: type.toUpperCase() === 'BUY' ? 'BUY' : 'SELL',
                    quantity: amount
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.showNotification(`✅ Trade ${type.toUpperCase()} eseguito!`);
                this.loadPositions();
            } else {
                this.showNotification(data.message || '❌ Errore nell\'esecuzione', 'error');
            }
        } catch (error) {
            this.showNotification('❌ Errore nella connessione', 'error');
            console.error(error);
        }
    }

    loadExchangeSettings() {
        // Carica le impostazioni di exchange salvate
        const savedExchange = localStorage.getItem('current_exchange') || 'bitget';
        const exchangeSelect = document.getElementById('exchange-selector');
        if (exchangeSelect) {
            exchangeSelect.value = savedExchange;
        }
        this.currentExchange = savedExchange;
        this.updateExchangeInfo();
    }

    updateExchangeInfo() {
        // Aggiorna il display delle info exchange
        const exchangeMap = {
            'binance': 'BINANCE',
            'bitget': 'BITGET'
        };
        const infoPair = {
            'binance': 'XRP/USDT',
            'bitget': 'XRP/USDT'
        };
        
        document.getElementById('info-exchange').textContent = exchangeMap[this.currentExchange];
        document.getElementById('info-pair').textContent = infoPair[this.currentExchange];
    }

    async changeExchange() {
        // Cambia l'exchange e ricarica i dati
        const newExchange = document.getElementById('exchange-selector')?.value || 'bitget';
        
        if (newExchange === this.currentExchange) {
            this.showNotification('⚠️  Stai già usando ' + newExchange.toUpperCase(), 'warning');
            return;
        }
        
        try {
            // Invia il cambio al backend
            const response = await fetch(`${API_URL}/exchange/switch`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ exchange: newExchange })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentExchange = newExchange;
                localStorage.setItem('current_exchange', newExchange);
                this.updateExchangeInfo();
                this.showNotification(`✅ Cambio a ${newExchange.toUpperCase()} completato!`);
                
                // Ricarica i dati
                setTimeout(() => {
                    this.fetchPrice();
                    this.fetchBalance();
                }, 500);
            } else {
                this.showNotification(`❌ Errore: ${data.message}`, 'error');
            }
        } catch (error) {
            this.showNotification('❌ Errore nel cambio exchange', 'error');
            console.error(error);
        }
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `status ${type === 'error' ? 'error' : type === 'warning' ? 'warning' : ''}`;
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.top = '60px';
        notification.style.right = '14px';
        notification.style.zIndex = '1000';
        notification.style.maxWidth = '300px';
        notification.style.animation = 'slideIn 0.3s ease-out';
        notification.style.padding = '12px 16px';
        notification.style.borderRadius = '4px';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.scalperApp = new ScalperApp();
});

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(300px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(300px); opacity: 0; }
    }
`;
document.head.appendChild(style);
