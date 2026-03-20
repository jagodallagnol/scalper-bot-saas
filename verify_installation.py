#!/usr/bin/env python3
"""
Verification Script - Controlla se tutto è installato e pronto
Verifica che tutte le dipendenze e i file siano in posto
"""

import sys
import os
import importlib
import subprocess

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║          XRP SCALPER BOT - ADVANCED EDITION - VERIFICATION               ║
║                    Sistema di verifica installazione                     ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

# ============ CHECK PYTHON VERSION ============
print("\n📋 1. Verifica versione Python...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"   ✅ Python {python_version.major}.{python_version.minor} - OK")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} - Richiesto 3.8+")
    sys.exit(1)

# ============ CHECK REQUIRED PACKAGES ============
print("\n📦 2. Verifica pacchetti richiesti...")

packages = {
    'pandas': 'Data manipulation',
    'numpy': 'Numerical computing',
    'ccxt': 'Bitget API access',
    'ta': 'Technical analysis indicators',
    'dotenv': 'Environment variables',
    'matplotlib': 'Plotting (optional for visualization)',
}

missing_packages = []

for package, description in packages.items():
    try:
        module = importlib.import_module(package)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {package:<15} v{version:<10} - {description}")
    except ImportError:
        print(f"   ❌ {package:<15} NOT INSTALLED - {description}")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Pacchetti mancanti: {', '.join(missing_packages)}")
    print("   Esegui: pip install -r requirements.txt")
else:
    print("\n   ✅ Tutti i pacchetti richiesti sono installati!")

# ============ CHECK FILE STRUCTURE ============
print("\n📁 3. Verifica struttura dei file...")

required_files = {
    'config.py': 'Original configuration',
    'advanced_config.py': 'Advanced configuration',
    'strategy.py': 'Original strategy',
    'advanced_scalper_strategy.py': 'Advanced strategy',
    'backtester.py': 'Original backtester',
    'advanced_backtester.py': 'Advanced backtester',
    'backtest.py': 'Original backtest script',
    'advanced_backtest.py': 'Advanced backtest script',
    'data_manager.py': 'Data manager',
    'requirements.txt': 'Dependencies',
    'README.md': 'Documentation',
}

missing_files = []

for filename, description in required_files.items():
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"   ✅ {filename:<30} ({size} bytes) - {description}")
    else:
        print(f"   ❌ {filename:<30} NOT FOUND - {description}")
        missing_files.append(filename)

if missing_files:
    print(f"\n⚠️  File mancanti: {', '.join(missing_files)}")
else:
    print("\n   ✅ Tutti i file richiesti sono presenti!")

# ============ CHECK DATA FILES ============
print("\n💾 4. Verifica file di dati...")

if os.path.exists('data'):
    csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
    if csv_files:
        print(f"   ✅ Cartella 'data' trovata con {len(csv_files)} file CSV:")
        for f in csv_files:
            size = os.path.getsize(os.path.join('data', f))
            lines = len(open(os.path.join('data', f)).readlines())
            print(f"      • {f} ({lines} righe, {size} bytes)")
    else:
        print("   ⚠️  Cartella 'data' vuota - Esegui: python download_data.py")
else:
    print("   ⚠️  Cartella 'data' non trovata")
    os.makedirs('data', exist_ok=True)
    print("   ✅ Creata cartella 'data'")

# ============ CHECK .ENV FILE ============
print("\n🔐 5. Verifica configurazione Bitget API...")

if os.path.exists('.env'):
    print("   ✅ File .env trovato")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('BITGET_API_KEY')
    api_secret = os.getenv('BITGET_SECRET_KEY')
    password = os.getenv('BITGET_PASSWORD')
    
    if api_key and api_secret and password:
        print("   ✅ BITGET_API_KEY trovata")
        print("   ✅ BITGET_SECRET_KEY trovata")
        print("   ✅ BITGET_PASSWORD trovata")
        print("   ⚠️  Non visualizziamo le chiavi per sicurezza")
    else:
        print("   ⚠️  API keys non configurate (opzionale se usi solo backtest)")
        print("      Per trading live: Copia .env.example a .env e configura")
else:
    print("   ℹ️  File .env non trovato (OK se usi solo backtest)")
    print("      Per trading live: cp .env.example .env")

# ============ TEST IMPORTS ============
print("\n🧪 6. Test di import dei moduli...")

try:
    import config
    print("   ✅ config.py - importato con successo")
except Exception as e:
    print(f"   ❌ config.py - errore: {e}")

try:
    import advanced_config
    print("   ✅ advanced_config.py - importato con successo")
except Exception as e:
    print(f"   ❌ advanced_config.py - errore: {e}")

try:
    from data_manager import DataManager
    print("   ✅ DataManager - importato con successo")
except Exception as e:
    print(f"   ⚠️  DataManager - errore: {e} (richiede dati)")

try:
    from strategy import ScalperStrategy
    print("   ✅ ScalperStrategy (original) - importato con successo")
except Exception as e:
    print(f"   ⚠️  ScalperStrategy - errore: {e}")

try:
    from advanced_scalper_strategy import AdvancedScalperStrategy
    print("   ✅ AdvancedScalperStrategy - importato con successo")
except Exception as e:
    print(f"   ❌ AdvancedScalperStrategy - errore: {e}")

try:
    from backtester import Backtester
    print("   ✅ Backtester (original) - importato con successo")
except Exception as e:
    print(f"   ⚠️  Backtester - errore: {e}")

try:
    from advanced_backtester import AdvancedBacktester
    print("   ✅ AdvancedBacktester - importato con successo")
except Exception as e:
    print(f"   ❌ AdvancedBacktester - errore: {e}")

# ============ CHECK SYSTEM INFO ============
print("\n💻 7. Informazioni di sistema...")

import platform
print(f"   OS: {platform.system()} {platform.release()}")
print(f"   Processor: {platform.processor()}")
print(f"   Python Implementation: {platform.python_implementation()}")

# ============ FINAL SUMMARY ============
print("\n" + "="*76)
print("RIEPILOGO VERIFICA")
print("="*76)

all_good = True

if missing_packages:
    print(f"\n❌ Pacchetti mancanti: {', '.join(missing_packages)}")
    print("   Soluzione: pip install -r requirements.txt")
    all_good = False
else:
    print("\n✅ Tutti i pacchetti sono installati")

if missing_files:
    print(f"\n❌ File mancanti: {', '.join(missing_files)}")
    all_good = False
else:
    print("✅ Tutti i file richiesti sono presenti")

if not os.path.exists('data') or not any(f.endswith('.csv') for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))):
    print("\n⚠️  DATI STORICI MANCANTI:")
    print("   Esegui: python download_data.py")
    all_good = False
else:
    print("✅ Dati storici trovati")

# ============ RECOMMENDED NEXT STEPS ============
print("\n" + "="*76)
print("PROSSIMI PASSI")
print("="*76)

if all_good:
    print("""
✅ Il sistema è PRONTO! Puoi procedere con:

1️⃣  Esegui il backtest avanzato:
    python advanced_backtest.py

2️⃣  Visualizza i risultati:
    python advanced_visualize.py

3️⃣  Per live trading (SOLO SE IL BACKTEST È POSITIVO):
    - Configura .env con le tue API keys
    - python live_trading.py

📚 Consulta:
   - README.md per documentazione completa
   - QUICK_START.py per una guida rapida
   - COMPARISON.py per confrontare le strategie
""")
else:
    print("""
⚠️  Il sistema ha problemi. Esegui i comandi sopra per risolverli.

Hai bisogno di aiuto? Controlla:
  - README.md sezione Troubleshooting
  - I file di log nel progetto
  - La tua connessione internet (se scarichi dati)
""")

print("\n" + "="*76)
if all_good:
    print("✅ VERIFICA COMPLETATA - TUTTO OK!")
else:
    print("⚠️  VERIFICA COMPLETATA - ALCUNI PROBLEMI TROVATI")
print("="*76 + "\n")
