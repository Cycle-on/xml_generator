#!/usr/bin/env python3
"""
Быстрая валидация одного ЦПГ файла
Использование: python validate_one_cpg.py путь_к_файлу.xml
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tests.test_cpg_validation import validate_cpg_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Укажите путь к XML файлу!")
        print("Использование: python validate_one_cpg.py файл.xml")
        print("\nПример:")
        print("python validate_one_cpg.py files/TEST_cpg/rsc-region-05/UpdateCard/card_0_0.xml")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    wsdl_file = "cpg_wsdl_1.wsdl"
    
    if not os.path.exists(xml_file):
        print(f"❌ Файл не найден: {xml_file}")
        sys.exit(1)
    
    if not os.path.exists(wsdl_file):
        print(f"❌ WSDL не найден: {wsdl_file}")
        sys.exit(1)
    
    validate_cpg_file(xml_file, wsdl_file)