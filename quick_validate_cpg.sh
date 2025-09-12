#!/bin/bash
echo "🚀 Генерация тестовых ЦПГ файлов..."
python main.py --mode cpg --files-count 2 --xmls 3

echo ""
echo "✅ Генерация завершена. Проверяем валидность..."
echo ""

# Запуск валидации
cd tests
python test_cpg_validation.py
