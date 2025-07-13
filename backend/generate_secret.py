#!/usr/bin/env python3

import secrets
import os
import re

def generate_secret_key():
    return secrets.token_urlsafe(32)

def update_env_file(secret_key):
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print(f"❌ File {env_file} not found")
        print("💡 Run: cp env.example .env")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    pattern = r'SECRET_KEY=.*'
    replacement = f'SECRET_KEY={secret_key}'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        with open(env_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Secret key updated in {env_file}")
        return True
    else:
        print("❌ SECRET_KEY line not found in .env file")
        return False

def update_docker_compose(secret_key):
    compose_file = 'docker-compose.yml'
    
    if not os.path.exists(compose_file):
        print(f"⚠️  File {compose_file} not found")
        return False
    
    with open(compose_file, 'r') as f:
        content = f.read()
    
    pattern = r'SECRET_KEY=.*'
    replacement = f'SECRET_KEY={secret_key}'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        with open(compose_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Secret key updated in {compose_file}")
        return True
    else:
        print("⚠️  SECRET_KEY line not found in docker-compose.yml")
        return False

def main():
    print("🔐 Generating new secret key for Family Search OCR...")
    
    secret_key = generate_secret_key()
    print(f"🔑 New secret key: {secret_key}")
    
    env_updated = update_env_file(secret_key)
    compose_updated = update_docker_compose(secret_key)
    
    print("\n📋 Summary:")
    print(f"   Secret Key: {secret_key}")
    print(f"   .env updated: {'✅' if env_updated else '❌'}")
    print(f"   docker-compose.yml updated: {'✅' if compose_updated else '❌'}")
    
    if env_updated or compose_updated:
        print("\n💡 Remember to restart the application after updating the secret key!")
    else:
        print("\n⚠️  No files were updated. Check if the files exist.")

if __name__ == "__main__":
    main() 