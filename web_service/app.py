@app.route('/generate')
def generate():
    def generate_output():
        capture = OutputCapture()
        sys.stdout = capture
        sys.stderr = capture
        
        def output_callback(text):
            yield f"data: {text}\n\n"
        
        capture.add_callback(output_callback)
        
        try:
            # Очищаем директорию перед генерацией
            clear_dir()
            
            # Выводим сообщение о начале генерации
            yield f"data: Начинаю генерацию...\n\n"
            
            if TAKE_CONSTANTS_FROM_FILE:
                # Генерация для одного региона
                generate_region_files()
                yield f"data: Генерация для региона region1 завершена\n\n"
            else:
                # Генерация для всех регионов
                for constants_dict in get_next_constants():
                    region_name = constants_dict["region_name/constant name"]
                    yield f"data: Генерация для региона {region_name}...\n\n"
                    globals().update(constants_dict)
                    generate_region_files(region_name=region_name)
                    yield f"data: Генерация для региона {region_name} завершена\n\n"
            
            # Подсчитываем количество сгенерированных файлов
            ukios_files = get_ukios_files()
            file_count = len(ukios_files)
            
            # Выводим сообщение о завершении
            yield f"data: Генерация завершена успешно, сгенерировано файлов: {file_count}\n\n"
            
        except Exception as e:
            yield f"data: Ошибка в генерации: {str(e)}\n\n"
        finally:
            sys.stdout = capture.stdout
            sys.stderr = capture.stderr
            capture.remove_callback(output_callback)
            yield "event: done\ndata: \n\n"
    
    return Response(stream_with_context(generate_output()), 
                   mimetype='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'X-Accel-Buffering': 'no'
                   }) 

def get_ukios_files():
    files = []
    base_path = os.path.join('files', 'TEST')
    
    # Проверяем существование базовой директории
    if not os.path.exists(base_path):
        return files
        
    # Перебираем все регионы
    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region)
        if os.path.isdir(region_path):
            # Проверяем наличие подпапки Ukios
            ukios_path = os.path.join(region_path, 'Ukios')
            if os.path.exists(ukios_path):
                # Ищем XML файлы только в директории Ukios
                for filename in os.listdir(ukios_path):
                    if filename.endswith('.xml'):
                        files.append(f"{region}/Ukios/{filename}")
    
    return sorted(files) 