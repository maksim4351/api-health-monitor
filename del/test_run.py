#!/usr/bin/env python3
"""
Простой скрипт для тестирования API Health Monitor без установки пакета.
Запустите: python test_run.py
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

from api_monitor.loader import load_config
from api_monitor.checker import check_all_apis
from api_monitor.reporter import print_report, get_exit_code

def main():
    """Тестовый запуск мониторинга."""
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        print(f"❌ Файл конфигурации не найден: {config_path}")
        print("Создайте файл config.yaml или укажите путь к нему")
        return 1
    
    try:
        print("📋 Загрузка конфигурации...")
        config = load_config(str(config_path))
        print(f"✅ Загружено {len(config.apis)} API для проверки\n")
        
        print("🔍 Начинаю проверку API...\n")
        results = check_all_apis(config.apis)
        
        print("📊 Результаты проверки:\n")
        print_report(results, config.output_format)
        
        exit_code = get_exit_code(results)
        successful = sum(1 for r in results if r.success)
        total = len(results)
        
        print(f"\n📈 Статистика: {successful}/{total} успешных проверок")
        
        if exit_code == 0:
            print("✅ Все API доступны!")
        else:
            print("⚠️  Некоторые API недоступны")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())


