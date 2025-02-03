import pandas as pd
from split_stick import insert, swap, delete, replace, stick, split

# تعریف نام فایل‌ها
files = ["pn_summary.xlsx", "virastar.xlsx", "medical.xlsx"]
output_file = "noise_data.xlsx"

# پارامترهای نویز
cer_start = 0.1
cer_end = 0.5
cer_step = 0.1

wer_start = 0.01
wer_end = 0.1
wer_step = 0.01

batch_size = 10  # تعداد داده‌هایی که در هر تکرار پردازش می‌شود
save_interval = 1000  # تعداد داده‌هایی که بعد از آن ذخیره می‌شود
rows_per_sheet = 1048576  # حداکثر تعداد سطرهای مجاز در هر شیت اکسل

# دیکشنری برای ذخیره داده‌های هر نوع نویز در شیت‌های جداگانه
results_dict = {
    "insert": [],
    "swap": [],
    "delete": [],
    "replace": [],
    "stick": [],
    "split": []
}

# دیکشنری برای شمارش تعداد شیت‌های ایجادشده
sheet_count = {key: 1 for key in results_dict.keys()}


# تابع ذخیره‌سازی داده‌ها در فایل اکسل بعد از هر 1000 داده
def save_to_excel():
    global sheet_count
    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        for sheet_name, data in results_dict.items():
            if data:
                df = pd.DataFrame(data, columns=["origin", sheet_name, "cer", "wer"])

                # بررسی اینکه تعداد داده‌ها از حداکثر سطرهای مجاز در شیت بیشتر نشود
                while len(df) > rows_per_sheet:
                    df.iloc[:rows_per_sheet].to_excel(writer, sheet_name=f"{sheet_name}_{sheet_count[sheet_name]}",
                                                      index=False)
                    sheet_count[sheet_name] += 1
                    df = df.iloc[rows_per_sheet:]  # حذف داده‌های ذخیره‌شده

                # ذخیره داده‌های باقی‌مانده در شیت مناسب
                df.to_excel(writer, sheet_name=f"{sheet_name}_{sheet_count[sheet_name]}", index=False)

                # افزایش شمارش شیت‌ها برای شیت‌های جدید
                sheet_count[sheet_name] += 1

                # پاک کردن داده‌های ذخیره‌شده از حافظه
                results_dict[sheet_name] = []


# پردازش فایل‌ها
for file in files:
    try:
        df = pd.read_excel(file)
        column_list = df['origin'].tolist()
    except Exception as e:
        print(f"❌ خطا در خواندن فایل {file}: {e}")
        continue  # اگر فایل خوانده نشود، به فایل بعدی بروید

    # ایجاد نویز برای هر مقدار CER و WER
    for cer_value in [cer_start + i * cer_step for i in range(int((cer_end - cer_start) / cer_step) + 1)]:
        for wer_value in [wer_start + i * wer_step for i in range(int((wer_end - wer_start) / wer_step) + 1)]:
            for start_idx in range(0, len(column_list), batch_size):
                end_idx = min(start_idx + batch_size, len(column_list))
                batch = column_list[start_idx:end_idx]

                # اعمال توابع نویز و ذخیره در لیست‌های مربوطه
                results_dict["insert"].extend(
                    zip(batch, insert(batch, cer=cer_value, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))
                results_dict["swap"].extend(
                    zip(batch, swap(batch, cer=cer_value, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))
                results_dict["delete"].extend(
                    zip(batch, delete(batch, cer=cer_value, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))
                results_dict["replace"].extend(
                    zip(batch, replace(batch, cer=cer_value, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))
                results_dict["stick"].extend(
                    zip(batch, stick(batch, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))
                results_dict["split"].extend(
                    zip(batch, split(batch, cer=cer_value, wer=wer_value), [cer_value] * len(batch),
                        [wer_value] * len(batch)))

                # ذخیره‌سازی بعد از هر 1000 داده
                if sum(len(v) for v in results_dict.values()) >= save_interval:
                    save_to_excel()

# ذخیره‌سازی داده‌های باقی‌مانده (اگر کمتر از 1000 باشد)
save_to_excel()

print("✅ داده‌های نویزدار با موفقیت ایجاد و در فایل اکسل ذخیره شدند!")
