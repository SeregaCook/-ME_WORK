from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageEnhance
import os
import random
import math
import hashlib
from concurrent.futures import ThreadPoolExecutor

# =============================================================================
# ЧАСТЬ 1: БАЗОВЫЕ ОПЕРАЦИИ И ИСПРАВЛЕНИЕ БАГОВ
# =============================================================================

def basic_operations_demo():
    """Демонстрация базовых операций с изображениями"""
    print("=== БАЗОВЫЕ ОПЕРАЦИИ ===")
    
    # Создаем тестовое изображение если нет входных файлов
    if not os.path.exists("./input"):
        os.makedirs("./input", exist_ok=True)
        create_test_images()
    
    try:
        # 1. Открываем изображение
        image = Image.open("./input/photo1.jpg")
        
        # 2. Показываем информацию о изображении
        print(f"Формат: {image.format}")
        print(f"Размер: {image.size}")
        print(f"Режим: {image.mode}")
        
        # 3. Сохраняем в другом формате
        image.save("./output/photo1_basic.png")
        
        # 4. Изменяем размер
        new_size = (400, int(image.height * 400 / image.width))
        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # 5. Поворачиваем
        rotated_image = image.rotate(45, expand=True)
        
        # 6. Конвертируем в черно-белое
        grayscale_image = image.convert("L")
        
        # 7. Обрезаем изображение
        cropped_image = image.crop((100, 100, 400, 400))
        
        # Сохраняем результаты
        resized_image.save("./output/photo1_resized.jpg")
        rotated_image.save("./output/photo1_rotated.jpg")
        grayscale_image.save("./output/photo1_bw.jpg")
        cropped_image.save("./output/photo1_cropped.jpg")
        
        print("Базовые операции завершены!")
        
    except Exception as e:
        print(f"Ошибка в базовых операциях: {e}")

def create_test_images():
    """Создает тестовые изображения если их нет"""
    print("Создание тестовых изображений...")
    for i in range(3):
        # Создаем градиентные изображения
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        for x in range(0, 800, 10):
            for y in range(0, 600, 10):
                color = (
                    (x + i*100) % 255,
                    (y + i*50) % 255, 
                    (x + y + i*30) % 255
                )
                draw.rectangle([x, y, x+9, y+9], fill=color)
        
        img.save(f"./input/photo{i+1}.jpg")
    print("Тестовые изображения созданы!")

# =============================================================================
# ЧАСТЬ 2: ИСПРАВЛЕНИЕ БАГОВ (Часть 1 РПО)
# =============================================================================

def create_collage_from_folder_fixed(folder_path, output_path, rows=2, cols=2):
    """ИСПРАВЛЕННАЯ ВЕРСИЯ: Создает коллаж из изображений в папке"""
    images = []
    
    # ИСПРАВЛЕНИЕ БАГА 1: Используем os.path.join для правильных путей
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, file)
            try:
                img = Image.open(img_path)
                images.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {file}: {e}")
    
    if len(images) < rows * cols:
        print(f"Недостаточно изображений: {len(images)} вместо {rows * cols}")
        return
    
    # ИСПРАВЛЕНИЕ БАГА 2: Приводим все к одному размеру вместо предположения
    thumbnail_size = (200, 200)
    
    collage_width = cols * thumbnail_size[0]
    collage_height = rows * thumbnail_size[1]
    collage = Image.new('RGB', (collage_width, collage_height), 'white')
    
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(images):
                # Ресайзим изображение
                img_copy = images[index].copy()
                img_copy.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                
                # ИСПРАВЛЕНИЕ БАГА 3: Правильные координаты
                x_offset = j * thumbnail_size[0]
                y_offset = i * thumbnail_size[1]
                collage.paste(img_copy, (x_offset, y_offset))
    
    collage.save(output_path)
    print(f"Коллаж сохранен: {output_path}")

def create_smart_gradient_fixed(size=(400, 400), start_color=(255,0,0), end_color=(0,0,255)):
    """ИСПРАВЛЕННАЯ ВЕРСИЯ: Создает умный градиент"""
    img = Image.new('RGB', size, color=start_color)
    draw = ImageDraw.Draw(img)
    
    for x in range(size[0]):
        for y in range(size[1]):
            # ИСПРАВЛЕНИЕ БАГА 4 и 5: Правильная интерполяция всех каналов
            ratio_x = x / (size[0] - 1) if size[0] > 1 else 0
            ratio_y = y / (size[1] - 1) if size[1] > 1 else 0
            
            # Комбинируем градиенты по X и Y
            r = start_color[0] * (1 - ratio_x) + end_color[0] * ratio_x
            g = start_color[1] * (1 - ratio_y) + end_color[1] * ratio_y
            b = start_color[2] * (1 - (ratio_x + ratio_y)/2) + end_color[2] * ((ratio_x + ratio_y)/2)
            
            # Ограничиваем значения
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            
            draw.point((x, y), fill=(r, g, b))
    
    return img

def debug_fixed_functions():
    """Демонстрация исправленных функций"""
    print("\n=== ИСПРАВЛЕНИЕ БАГОВ ===")
    
    # Создаем тестовые градиенты
    gradient1 = create_smart_gradient_fixed((400, 300), (255, 100, 0), (0, 100, 255))
    gradient1.save("./output/gradient_fixed_1.jpg")
    
    gradient2 = create_smart_gradient_fixed((300, 400), (100, 255, 100), (255, 100, 255))
    gradient2.save("./output/gradient_fixed_2.jpg")
    
    # Создаем коллаж
    create_collage_from_folder_fixed("./input", "./output/collage_fixed.jpg", 2, 2)
    
    print("Исправленные функции протестированы!")

# =============================================================================
# ЧАСТЬ 3: АНАЛИЗ И УМНАЯ ОБРАБОТКА (Часть 2 РПО)
# =============================================================================

def analyze_dominant_color(image_path):
    """
    Анализирует изображение и определяет:
    - Доминирующий цвет (RGB)
    - Цветовую температуру (теплое/холодное/нейтральное)
    - Яркость изображения (темное/среднее/светлое)
    """
    with Image.open(image_path) as img:
        # Конвертируем в RGB если нужно
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Получаем гистограмму
        hist = img.histogram()
        
        # Анализируем доминирующий цвет
        r_hist = hist[0:256]
        g_hist = hist[256:512] 
        b_hist = hist[512:768]
        
        # Находим наиболее частые значения для каждого канала
        r_dominant = r_hist.index(max(r_hist))
        g_dominant = g_hist.index(max(g_hist))
        b_dominant = b_hist.index(max(b_hist))
        
        # Вычисляем средний цвет
        stat = ImageStat.Stat(img)
        mean_color = [int(x) for x in stat.mean]
        
        # Определяем цветовую температуру
        warmth = (mean_color[0] - mean_color[2]) / 255.0
        if warmth > 0.1:
            color_temp = "теплое"
        elif warmth < -0.1:
            color_temp = "холодное"
        else:
            color_temp = "нейтральное"
        
        # Определяем яркость
        brightness = sum(mean_color) / 3 / 255.0
        if brightness < 0.3:
            brightness_level = "темное"
        elif brightness < 0.7:
            brightness_level = "среднее"
        else:
            brightness_level = "светлое"
        
        return {
            'dominant_rgb': (r_dominant, g_dominant, b_dominant),
            'mean_rgb': tuple(mean_color),
            'color_temperature': color_temp,
            'brightness': brightness_level,
            'warmth_index': warmth
        }

def smart_processing(image_path, output_path):
    """
    Автоматически определяет тип изображения и применяет оптимальную обработку:
    - ПОРТРЕТ: легкое размытие фона, коррекция кожи
    - ПЕЙЗАЖ: усиление насыщенности, контраста  
    - ТЕКСТ: повышение резкости, конвертация в ч/б
    - НОЧНОЕ: шумоподавление, коррекция экспозиции
    """
    with Image.open(image_path) as img:
        analysis = analyze_dominant_color(image_path)
        img_working = img.copy()
        
        # Эвристики для классификации
        r, g, b = analysis['mean_rgb']
        
        # Определяем тип изображения
        image_type = "unknown"
        
        # Эвристика для портрета: много телесных оттенков
        skin_tone_ratio = (r / max(g, 1))
        if 0.8 < skin_tone_ratio < 1.4 and r > 100 and g > 70 and b > 50:
            image_type = "portrait"
        
        # Эвристика для пейзажа: много зеленого или синего
        elif g > r and g > b and g > 100:
            image_type = "landscape"
        
        # Эвристика для ночного: низкая яркость, но с контрастом
        elif analysis['brightness'] == "темное" and max(r, g, b) - min(r, g, b) > 50:
            image_type = "night"
        
        # Применяем соответствующую обработку
        if image_type == "portrait":
            # Легкое размытие фона и улучшение кожи
            enhancer = ImageEnhance.Color(img_working)
            img_working = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Contrast(img_working)
            img_working = enhancer.enhance(1.05)
            
        elif image_type == "landscape":
            # Усиление насыщенности и контраста
            enhancer = ImageEnhance.Color(img_working)
            img_working = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Contrast(img_working)
            img_working = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Sharpness(img_working)
            img_working = enhancer.enhance(1.5)
            
        elif image_type == "night":
            # Шумоподавление и коррекция яркости
            img_working = img_working.filter(ImageFilter.SMOOTH)
            enhancer = ImageEnhance.Brightness(img_working)
            img_working = enhancer.enhance(1.3)
            
        else:
            # Стандартное улучшение
            enhancer = ImageEnhance.Contrast(img_working)
            img_working = enhancer.enhance(1.1)
        
        img_working.save(output_path)
        print(f"Обработано как {image_type}: {output_path}")
        return image_type

def demo_smart_processing():
    """Демонстрация умной обработки"""
    print("\n=== УМНАЯ ОБРАБОТКА ===")
    
    # Анализ доминирующего цвета
    for i in range(1, 4):
        input_path = f"./input/photo{i}.jpg"
        if os.path.exists(input_path):
            analysis = analyze_dominant_color(input_path)
            print(f"Анализ photo{i}.jpg: {analysis}")
            
            # Умная обработка
            output_path = f"./output/photo{i}_smart.jpg"
            image_type = smart_processing(input_path, output_path)
            print(f"Тип изображения: {image_type}")

# =============================================================================
# ЧАСТЬ 4: ПАКЕТНАЯ ОБРАБОТКА И ОПТИМИЗАЦИЯ (Часть 3 РПО)
# =============================================================================

def apply_complex_filters(img):
    """Имитация сложной обработки для тестирования производительности"""
    # Несколько операций для демонстрации
    result = img.copy()
    result = result.filter(ImageFilter.SHARPEN)
    result = result.filter(ImageFilter.SMOOTH)
    enhancer = ImageEnhance.Contrast(result)
    result = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.1)
    return result

def slow_batch_processor(input_folder, output_folder):
    """Медленная версия обработки (для сравнения)"""
    print("Запуск медленной обработки...")
    os.makedirs(output_folder, exist_ok=True)
    
    processed_count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"slow_{filename}")
            
            with Image.open(input_path) as img:
                result = apply_complex_filters(img)
                result.save(output_path)
            
            processed_count += 1
            print(f"Медленная обработка: {filename}")
    
    print(f"Медленная обработка завершена: {processed_count} файлов")

def optimized_batch_processor(input_folder, output_folder, max_workers=4):
    """Оптимизированная многопоточная версия"""
    print("Запуск оптимизированной обработки...")
    
    # Создаем выходную папку если нет
    os.makedirs(output_folder, exist_ok=True)
    
    # Собираем все файлы заранее (оптимизация I/O)
    files = [f for f in os.listdir(input_folder) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    def process_single_file(filename):
        try:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"fast_{filename}")
            
            with Image.open(input_path) as img:
                # Предварительная обработка и кэширование в памяти
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                result = apply_complex_filters(img)
                # Оптимизированные настройки сохранения
                result.save(output_path, "JPEG", quality=85, optimize=True)
            
            print(f"Быстрая обработка: {filename}")
            return True
            
        except Exception as e:
            print(f"Ошибка обработки {filename}: {e}")
            return False
    
    # Используем ThreadPoolExecutor для параллельной обработки
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_file, files))
    
    success_count = sum(results)
    print(f"Оптимизированная обработка завершена: {success_count}/{len(files)} файлов")
    return success_count

def demo_optimization():
    """Демонстрация оптимизации производительности"""
    print("\n=== ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    
    import time
    
    # Тестируем медленную версию
    start_time = time.time()
    slow_batch_processor("./input", "./output/slow_results")
    slow_time = time.time() - start_time
    
    # Тестируем оптимизированную версию
    start_time = time.time()
    optimized_batch_processor("./input", "./output/fast_results", max_workers=2)
    fast_time = time.time() - start_time
    
    print(f"\nСравнение производительности:")
    print(f"Медленная версия: {slow_time:.2f} секунд")
    print(f"Быстрая версия: {fast_time:.2f} секунд")
    print(f"Ускорение: {slow_time/fast_time:.1f}x")

# =============================================================================
# ЧАСТЬ 5: ГЕНЕРАТИВНАЯ ГРАФИКА И ВОДЯНЫЕ ЗНАКИ
# =============================================================================

def create_generative_art(width=800, height=600, filename="./output/generative_art.png"):
    """Создает генеративное абстрактное изображение"""
    # Создаем новое изображение
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Генерируем 50 случайных кругов
    for _ in range(50):
        # Случайные параметры круга
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(10, 100)
        
        # Случайный цвет с прозрачностью
        color = (
            random.randint(0, 255),
            random.randint(0, 255), 
            random.randint(0, 255)
        )
        
        # Рисуем круг
        draw.ellipse(
            [x-radius, y-radius, x+radius, y+radius],
            fill=color,
            outline=None
        )
    
    # Добавляем несколько линий для структуры
    for _ in range(10):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        
        line_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        
        draw.line([x1, y1, x2, y2], fill=line_color, width=3)
    
    # Сохраняем результат
    img.save(filename, "PNG")
    print(f"Генеративное искусство сохранено как {filename}")

def generate_personal_watermark(user_id, username, size=(200, 100)):
    """
    Создает уникальный водяной знак на основе user_id и username
    """
    # Создаем базовое изображение с альфа-каналом
    watermark = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    
    # Генерируем цветовую схему из хеша user_id
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()
    
    # Берем первые 6 символов для цвета
    base_color = (
        int(user_hash[0:2], 16) % 200 + 55,
        int(user_hash[2:4], 16) % 200 + 55, 
        int(user_hash[4:6], 16) % 200 + 55,
        180  # Прозрачность
    )
    
    # Создаем геометрический паттерн из инициалов
    initials = ''.join([name[0].upper() for name in username.split()])[:2]
    if len(initials) < 2:
        initials = username[:2].upper()
    
    # Рисуем фон паттерна
    pattern_size = 20
    for i in range(0, size[0], pattern_size):
        for j in range(0, size[1], pattern_size):
            # Чередуем прозрачность для сложного паттерна
            alpha = 80 + (i + j) % 100
            color = (*base_color[:3], alpha)
            
            # Рисуем геометрические фигуры на основе хеша
            hash_val = int(user_hash[(i//pattern_size + j//pattern_size) % 32], 16)
            
            if hash_val % 3 == 0:
                # Круг
                draw.ellipse([i, j, i+pattern_size-5, j+pattern_size-5], 
                           fill=color)
            elif hash_val % 3 == 1:
                # Квадрат
                draw.rectangle([i+2, j+2, i+pattern_size-3, j+pattern_size-3], 
                             fill=color)
            else:
                # Треугольник
                draw.polygon([(i+pattern_size//2, j+2), 
                            (i+2, j+pattern_size-3),
                            (i+pattern_size-3, j+pattern_size-3)], 
                           fill=color)
    
    # Добавляем текст инициалов
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Позиционируем текст
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Рисуем текст с обводкой для читаемости
    text_color = (*base_color[:3], 220)
    outline_color = (0, 0, 0, 150)
    
    # Обводка
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), initials, font=font, fill=outline_color)
    
    # Основной текст
    draw.text((x, y), initials, font=font, fill=text_color)
    
    # Добавляем скрытые элементы (едва заметные линии)
    for i in range(3):
        line_y = size[1] * (i + 1) // 4
        line_alpha = 30
        draw.line([(0, line_y), (size[0], line_y)], 
                 fill=(*base_color[:3], line_alpha), width=1)
    
    return watermark

def apply_advanced_watermark(base_image, watermark, position='bottom-right', opacity=0.7):
    """Применяет водяной знак к изображению"""
    # Масштабируем водяной знак пропорционально основному изображению
    wm_width = base_image.width // 4
    wm_height = watermark.height * wm_width // watermark.width
    watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
    
    # Создаем копию основного изображения
    result = base_image.copy().convert('RGBA')
    
    # Позиционируем водяной знак
    if position == 'bottom-right':
        x = result.width - watermark.width - 10
        y = result.height - watermark.height - 10
    elif position == 'center':
        x = (result.width - watermark.width) // 2
        y = (result.height - watermark.height) // 2
    else:  # top-left
        x = 10
        y = 10
    
    # Накладываем водяной знак
    result.alpha_composite(watermark, (x, y))
    
    return result.convert('RGB')

def demo_generative_and_watermarks():
    """Демонстрация генеративной графики и водяных знаков"""
    print("\n=== ГЕНЕРАТИВНАЯ ГРАФИКА И ВОДЯНЫЕ ЗНАКИ ===")
    
    # Создаем генеративное искусство
    for i in range(2):
        create_generative_art(filename=f"./output/generative_art_{i+1}.png")
    
    # Создаем водяные знаки для разных пользователей
    users = [
        (12345, "Иван Петров"),
        (67890, "Анна Сидорова"), 
        (54321, "Петр Иванов")
    ]
    
    for user_id, username in users:
        watermark = generate_personal_watermark(user_id, username)
        watermark.save(f"./output/watermark_{user_id}.png")
        print(f"Создан водяной знак для: {username} (ID: {user_id})")
    
    # Применяем водяной знак к тестовому изображению
    if os.path.exists("./input/photo1.jpg"):
        base_image = Image.open("./input/photo1.jpg")
        watermark = generate_personal_watermark(12345, "Тестовый Пользователь")
        watermarked = apply_advanced_watermark(base_image, watermark)
        watermarked.save("./output/photo1_watermarked.jpg")
        print("Водяной знак применен к тестовому изображению")

# =============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# =============================================================================

def main():
    """Главная функция, запускающая все демонстрации"""
    print("🚀 ЗАПУСК АВТОМАТИЗАЦИИ ОБРАБОТКИ ИЗОБРАЖЕНИЙ")
    print("=" * 50)
    
    # Создаем папки если их нет
    os.makedirs("./input", exist_ok=True)
    os.makedirs("./output", exist_ok=True)
    
    try:
        # Часть 1: Базовые операции
        basic_operations_demo()
        
        # Часть 2: Исправление багов
        debug_fixed_functions()
        
        # Часть 3: Умная обработка
        demo_smart_processing()
        
        # Часть 4: Оптимизация производительности  
        demo_optimization()
        
        # Часть 5: Генеративная графика и водяные знаки
        demo_generative_and_watermarks()
        
        print("\n" + "=" * 50)
        print("✅ ВСЕ ЗАДАНИЯ УСПЕШНО ВЫПОЛНЕНЫ!")
        print("Результаты сохранены в папке ./output/")
        
    except Exception as e:
        print(f"❌ Ошибка в основном потоке: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()