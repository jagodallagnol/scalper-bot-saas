#!/usr/bin/env python3
"""
SCALPER BOT · START SCRIPT
Avvia sia il backend che il frontend
"""

import subprocess
import os
import sys
import time
import webbrowser
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("🚀 SCALPER BOT · STARTUP")
    print("="*60 + "\n")

def print_step(step, description):
    print(f"[{step}] {description}")

def check_dependencies():
    """Verifica le dipendenze necessarie"""
    print_step("1/4", "Verifica dipendenze...")
    
    try:
        import flask
        import flask_cors
        import ccxt
        import pandas
        print("✅ Tutte le dipendenze sono installate\n")
        return True
    except ImportError as e:
        print(f"❌ Dipendenza mancante: {e}")
        print("\nInstalla le dipendenze con:")
        print("  pip install -r requirements.txt")
        print()
        return False

def check_env():
    """Verifica file .env"""
    print_step("2/4", "Verifica configurazione...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  File .env non trovato")
        print("\nCrea un file .env con:")
        print("""
BITGET_API_KEY=your_api_key
BITGET_API_SECRET=your_api_secret
BITGET_PASSWORD=your_api_password
TRADING_PAIR=XRPUSDT
LEVERAGE=5
MIN_AMOUNT=100
TARGET_GAIN=2
CHECK_INTERVAL=5
""")
        print("\nNota: Potrai anche inserire le credenziali dall'interfaccia web\n")
    else:
        print("✅ File .env trovato\n")

def start_api_server():
    """Avvia il server API"""
    print_step("3/4", "Avvio backend API (http://localhost:5000)...")
    
    try:
        # Avvia in background
        process = subprocess.Popen(
            [sys.executable, 'api_server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Aspetta che il server sia pronto
        time.sleep(3)
        
        # Verifica che sia in esecuzione
        if process.poll() is None:
            print("✅ Backend API avviato\n")
            return process
        else:
            print("❌ Backend API non si è avviato")
            return None
    except Exception as e:
        print(f"❌ Errore nell'avvio del backend: {e}\n")
        return None

def start_http_server():
    """Avvia il server HTTP"""
    print_step("4/4", "Avvio server web (http://localhost:8081)...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'http.server', '8081'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        time.sleep(1)
        
        if process.poll() is None:
            print("✅ Server web avviato\n")
            return process
        else:
            print("❌ Server web non si è avviato")
            return None
    except Exception as e:
        print(f"❌ Errore nell'avvio del server web: {e}\n")
        return None

def open_browser():
    """Apri il browser"""
    time.sleep(1)
    print("🌐 Apertura browser...")
    try:
        webbrowser.open('http://localhost:8081')
        print("✅ Browser aperto\n")
    except:
        print("⚠️  Apri manualmente: http://localhost:8081\n")

def print_info():
    """Stampa info di accesso"""
    print("="*60)
    print("✨ SCALPER BOT È PRONTO!")
    print("="*60)
    print()
    print("📍 Accesso:")
    print("   Web Interface: http://localhost:8081")
    print("   API Backend:   http://localhost:5000")
    print()
    print("⚙️  Configurazione:")
    print("   • Accedi a Settings per aggiungere credenziali Bitget")
    print("   • Imposta i parametri di scalping")
    print("   • Avvia il bot dal tab Trade")
    print()
    print("📊 Dashboard:")
    print("   • Visualizza prezzi in tempo reale")
    print("   • Monitora il portafoglio")
    print("   • Esegui trade manuali")
    print()
    print("🛑 Per fermare:")
    print("   Premi CTRL+C nel terminale")
    print()
    print("="*60 + "\n")

def main():
    os_name = os.name
    
    # Cambia directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print_header()
    
    # Verifica
    if not check_dependencies():
        sys.exit(1)
    
    check_env()
    
    # Avvia server API
    api_process = start_api_server()
    if not api_process:
        sys.exit(1)
    
    # Avvia server web
    web_process = start_http_server()
    if not web_process:
        api_process.terminate()
        sys.exit(1)
    
    # Apri browser
    open_browser()
    
    # Info
    print_info()
    
    # Mantieni in esecuzione
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Arresto dei servizi...")
        api_process.terminate()
        web_process.terminate()
        print("✅ Servizi arrestati")
        sys.exit(0)

if __name__ == '__main__':
    main()
