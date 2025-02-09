# ابتدا کلاس را import کنید (اگر در فایل جداگانه ذخیره شده است)
from final_noise import NoiseGenerator

# مسیر فایل ورودی (فایل اکسل داده‌های اصلی)
input_file = "data.xlsx"


# نوع نویز مورد نظر، مثلا "swap", "split", "stick", "insert", "delete", "replace", "replace_homophones"
noise_types = ["swap", "split", "stick", "insert", "delete", "replace", "replace_homophones" , "repeat"]
noise_type = "swap"

# ایجاد نمونه‌ای از کلاس و اجرای فرآیند نویزگذاری
generator = NoiseGenerator(input_file)
generator.generate_noise(noise_type)

print("فرآیند نویزگذاری به پایان رسید!")
