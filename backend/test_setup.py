#!/usr/bin/env python3
import sys
import os
import importlib

def test_imports():
    print("🔍 Testing imports...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'torch',
        'transformers',
        'datasets',
        'pytesseract',
        'cv2',
        'numpy',
        'pandas',
        'sklearn'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Import failures: {', '.join(failed_imports)}")
        return False
    
    print("✅ All imports worked!")
    return True

def test_tesseract():
    print("\n🔍 Testing Tesseract...")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        
        # Test Italian language
        langs = pytesseract.get_languages()
        if 'ita' in langs:
            print("✅ Italian language available")
        else:
            print("⚠️  Italian language not found")
            
        return True
    except Exception as e:
        print(f"❌ Tesseract error: {e}")
        return False

def test_database_connection():
    print("\n🔍 Testing database connection...")
    
    try:
        from app.config import settings
        from app.database import engine
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection OK")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_ai_model():
    print("\n🔍 Testing AI model...")
    
    try:
        from app.services.ai_service import ai_service
        print("✅ AI model loaded")
        return True
    except Exception as e:
        print(f"❌ AI model error: {e}")
        return False

def main():
    print("🚀 Testing Family Search OCR Backend configuration\n")
    
    tests = [
        test_imports,
        test_tesseract,
        test_database_connection,
        test_ai_model
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Configuration OK! You can run: python run.py")
        return 0
    else:
        print("❌ Some tests failed. Check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 