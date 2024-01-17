import re

def format_sec_ch_ua(original_ua_string):
    # Знайти всі компоненти з версіями
    components = re.findall(r'\"([^"]+)\";v=\"(\d+\.\d+)\"', original_ua_string)

    # Формування нового рядка
    formatted_components = []
    for name, version in components:
        if name == " Not A;Brand":
            name = "Not_A Brand"  # Змінити форматування
        # Додавання інших умов для різних браузерів, якщо необхідно
        formatted_components.append(f'"{name}";v="{version}"')

    return ', '.join(formatted_components)

# Приклад використання
original_ua_string = '" Not A;Brand";v="99", "Chromium";v="112", "Microsoft Edge";v="112"'
formatted_ua_string = format_sec_ch_ua(original_ua_string)

print(f"Formatted Sec-CH-UA: {formatted_ua_string}")

# " Not A;Brand";v="99", "Chromium";v="112", "Microsoft Edge";v="112"
# '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'