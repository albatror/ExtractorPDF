
#!/usr/bin/env python3
"""
Script de démarrage pour l'application complète d'extraction PDF
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class ApplicationManager:
    """Gestionnaire de l'application complète"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = False
        
    def check_dependencies(self):
        """Vérifie les dépendances système"""
        print("🔍 Vérification des dépendances...")
        
        # Vérifier Python
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            print("❌ Python 3.8+ requis")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}")
        
        # Vérifier Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()}")
            else:
                print("❌ Node.js non trouvé")
                return False
        except FileNotFoundError:
            print("❌ Node.js non installé")
            return False
        
        # Vérifier npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()}")
            else:
                print("❌ npm non trouvé")
                return False
        except FileNotFoundError:
            print("❌ npm non installé")
            return False
        
        return True
    
    def setup_backend(self):
        """Configure le backend Python"""
        print("\n🐍 Configuration du backend Python...")
        
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Dossier backend non trouvé")
            return False
        
        # Créer l'environnement virtuel s'il n'existe pas
        venv_dir = backend_dir / "venv"
        if not venv_dir.exists():
            print("📦 Création de l'environnement virtuel...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        
        # Déterminer le chemin de l'exécutable Python dans le venv
        if os.name == 'nt':  # Windows
            python_exe = venv_dir / "Scripts" / "python.exe"
            pip_exe = venv_dir / "Scripts" / "pip.exe"
        else:  # Unix/Linux/Mac
            python_exe = venv_dir / "bin" / "python"
            pip_exe = venv_dir / "bin" / "pip"
        
        # Installer les dépendances
        print("📦 Installation des dépendances Python...")
        requirements_file = backend_dir / "requirements.txt"
        if requirements_file.exists():
            subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)])
        
        # Créer les dossiers nécessaires
        logs_dir = backend_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        temp_dir = backend_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        print("✅ Backend configuré")
        return str(python_exe)
    
    def setup_frontend(self):
        """Configure le frontend React"""
        print("\n⚛️  Configuration du frontend React...")
        
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Dossier frontend non trouvé")
            return False
        
        # Installer les dépendances npm
        print("📦 Installation des dépendances npm...")
        os.chdir(frontend_dir)
        result = subprocess.run(["npm", "install"])
        os.chdir("..")
        
        if result.returncode != 0:
            print("❌ Erreur lors de l'installation npm")
            return False
        
        print("✅ Frontend configuré")
        return True
    
    def start_backend(self, python_exe):
        """Démarre le serveur backend"""
        print("\n🚀 Démarrage du backend...")
        
        backend_dir = Path("backend")
        os.chdir(backend_dir)
        
        # Démarrer uvicorn
        self.backend_process = subprocess.Popen([
            python_exe, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
        os.chdir("..")
        
        # Attendre que le backend soit prêt
        print("⏳ Attente du démarrage du backend...")
        time.sleep(5)
        
        # Vérifier que le backend répond
        try:
            import requests
            response = requests.get("http://localhost:8000/", timeout=10)
            if response.status_code == 200:
                print("✅ Backend démarré sur http://localhost:8000")
                return True
        except:
            pass
        
        print("❌ Le backend ne répond pas")
        return False
    
    def start_frontend(self):
        """Démarre le serveur frontend"""
        print("\n🌐 Démarrage du frontend...")
        
        frontend_dir = Path("frontend")
        os.chdir(frontend_dir)
        
        # Démarrer le serveur de développement React
        env = os.environ.copy()
        env["BROWSER"] = "none"  # Empêcher l'ouverture automatique du navigateur
        
        self.frontend_process = subprocess.Popen([
            "npm", "start"
        ], env=env)
        
        os.chdir("..")
        
        print("⏳ Attente du démarrage du frontend...")
        time.sleep(10)
        
        print("✅ Frontend démarré sur http://localhost:3000")
        return True
    
    def run_tests(self):
        """Exécute les tests d'intégration"""
        print("\n🧪 Exécution des tests d'intégration...")
        
        backend_dir = Path("backend")
        test_script = backend_dir / "integration_test.py"
        
        if test_script.exists():
            os.chdir(backend_dir)
            result = subprocess.run([sys.executable, "integration_test.py"])
            os.chdir("..")
            
            if result.returncode == 0:
                print("✅ Tests d'intégration réussis")
                return True
            else:
                print("❌ Certains tests ont échoué")
                return False
        else:
            print("⚠️  Script de test non trouvé")
            return True
    
    def signal_handler(self, signum, frame):
        """Gestionnaire de signal pour arrêt propre"""
        print("\n🛑 Arrêt de l'application...")
        self.stop()
        sys.exit(0)
    
    def stop(self):
        """Arrête tous les processus"""
        self.running = False
        
        if self.backend_process:
            print("🛑 Arrêt du backend...")
            self.backend_process.terminate()
            self.backend_process.wait()
        
        if self.frontend_process:
            print("🛑 Arrêt du frontend...")
            self.frontend_process.terminate()
            self.frontend_process.wait()
    
    def run(self, run_tests=False):
        """Lance l'application complète"""
        print("🚀 Démarrage de l'application d'extraction PDF")
        print("=" * 50)
        
        # Configurer le gestionnaire de signal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Vérifications préliminaires
            if not self.check_dependencies():
                print("❌ Dépendances manquantes")
                return False
            
            # Configuration
            python_exe = self.setup_backend()
            if not python_exe:
                return False
            
            if not self.setup_frontend():
                return False
            
            # Démarrage des services
            if not self.start_backend(python_exe):
                return False
            
            if not self.start_frontend():
                return False
            
            # Tests optionnels
            if run_tests:
                self.run_tests()
            
            # Affichage des informations
            print("\n" + "=" * 50)
            print("🎉 Application démarrée avec succès !")
            print("=" * 50)
            print("🌐 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8000")
            print("📚 Documentation API: http://localhost:8000/docs")
            print("=" * 50)
            print("💡 Utilisez Ctrl+C pour arrêter l'application")
            print("=" * 50)
            
            # Maintenir l'application en vie
            self.running = True
            while self.running:
                time.sleep(1)
                
                # Vérifier que les processus sont toujours actifs
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Le backend s'est arrêté de manière inattendue")
                    break
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Le frontend s'est arrêté de manière inattendue")
                    break
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage: {e}")
            return False
        
        finally:
            self.stop()

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Démarrage de l'application d'extraction PDF")
    parser.add_argument("--test", action="store_true", help="Exécuter les tests d'intégration")
    parser.add_argument("--backend-only", action="store_true", help="Démarrer seulement le backend")
    parser.add_argument("--frontend-only", action="store_true", help="Démarrer seulement le frontend")
    
    args = parser.parse_args()
    
    manager = ApplicationManager()
    
    if args.backend_only:
        if manager.check_dependencies():
            python_exe = manager.setup_backend()
            if python_exe:
                manager.start_backend(python_exe)
                print("Backend démarré. Appuyez sur Ctrl+C pour arrêter.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    manager.stop()
    
    elif args.frontend_only:
        if manager.check_dependencies():
            if manager.setup_frontend():
                manager.start_frontend()
                print("Frontend démarré. Appuyez sur Ctrl+C pour arrêter.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    manager.stop()
    
    else:
        success = manager.run(run_tests=args.test)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
