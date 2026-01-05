#!/usr/bin/env python3
"""
Скрипт для проверки совместимости с Python 3.8
"""

import sys

def check_python_version():
    """Проверяет версию Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Требуется Python 3.8 или выше. Текущая версия: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python версия: {version.major}.{version.minor}.{version.micro}")
    return True

def check_features():
    """Проверяет наличие необходимых функций Python."""
    features = {
        "dataclasses": False,
        "typing": False,
        "pathlib": False,
        "f-strings": False,
    }
    
    # Проверка dataclasses (Python 3.7+)
    try:
        from dataclasses import dataclass
        features["dataclasses"] = True
        print("✅ dataclasses доступен")
    except ImportError:
        print("❌ dataclasses недоступен (требуется Python 3.7+)")
    
    # Проверка typing (Python 3.5+, улучшен в 3.8)
    try:
        from typing import Dict, List, Optional, Any
        features["typing"] = True
        print("✅ typing доступен")
    except ImportError:
        print("❌ typing недоступен")
    
    # Проверка pathlib (Python 3.4+)
    try:
        from pathlib import Path
        features["pathlib"] = True
        print("✅ pathlib доступен")
    except ImportError:
        print("❌ pathlib недоступен")
    
    # Проверка f-strings (Python 3.6+)
    test_string = f"test {1+1}"
    if test_string == "test 2":
        features["f-strings"] = True
        print("✅ f-strings доступны")
    else:
        print("❌ f-strings недоступны")
    
    return all(features.values())

def check_imports():
    """Проверяет импорт модулей проекта."""
    try:
        import api_monitor
        print("✅ api_monitor импортирован")
        
        from api_monitor.loader import load_config, APIConfig
        print("✅ loader модуль импортирован")
        
        from api_monitor.checker import check_api, CheckResult
        print("✅ checker модуль импортирован")
        
        from api_monitor.reporter import format_table, format_json, format_csv
        print("✅ reporter модуль импортирован")
        
        from api_monitor.cli import main
        print("✅ cli модуль импортирован")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def main():
    """Главная функция."""
    print("=" * 50)
    print("Проверка совместимости с Python 3.8")
    print("=" * 50)
    print()
    
    if not check_python_version():
        sys.exit(1)
    
    print()
    print("Проверка функций Python:")
    print("-" * 50)
    if not check_features():
        print("\n❌ Некоторые функции недоступны")
        sys.exit(1)
    
    print()
    print("Проверка импорта модулей:")
    print("-" * 50)
    if not check_imports():
        print("\n❌ Ошибки при импорте модулей")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("✅ Все проверки пройдены! Проект совместим с Python 3.8+")
    print("=" * 50)
    return 0

if __name__ == "__main__":
    sys.exit(main())

