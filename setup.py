#!/usr/bin/env python
"""
Quick setup script for SentimentIQ development environment.
Run this script to set up everything needed for development.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        return False

def main():
    """Main setup function."""
    print("🚀 SentimentIQ Development Setup")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # Step 1: Check Python version
    print(f"\n📌 Python version: {sys.version}")
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required!")
        return False
    
    # Step 2: Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Determine activate command
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    # Step 3: Upgrade pip
    run_command(f"{activate_cmd}pip install --upgrade pip", "Upgrading pip")
    
    # Step 4: Install dependencies
    if not run_command(f"{activate_cmd}pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Step 5: Install dev dependencies
    if not run_command(f"{activate_cmd}pip install -r requirements-dev.txt", "Installing development dependencies"):
        print("⚠️  Development dependencies installation failed, but you can continue")
    
    # Step 6: Set up environment file
    if not Path(".env").exists():
        print("\n⚙️  Setting up environment variables...")
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Creating .env file")
            print("✅ .env file created from .env.example")
            print("⚠️  Please update .env with your configuration!")
        else:
            print("⚠️  .env.example not found!")
    
    # Step 7: Initialize database
    print(f"\n📊 Initializing database...")
    init_db_code = """
import sys
sys.path.insert(0, '.')
from app.database import init_db
init_db()
print('✅ Database initialized!')
"""
    
    run_command(
        f"{activate_cmd}python -c \"{init_db_code}\"",
        "Initializing database"
    )
    
    # Step 8: Run tests (optional)
    print("\n🧪 Running tests...")
    print("To run tests, use: pytest")
    print("For coverage: pytest --cov=app")
    
    # Final message
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Update .env file with your configuration")
    print("2. Activate virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run the server: uvicorn app.main:app --reload")
    print("4. Visit http://localhost:8000/api/docs for interactive documentation")
    print("\n💡 For more information, see README.md and EXAMPLES.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
