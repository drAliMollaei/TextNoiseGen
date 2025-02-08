import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from split_stick import swap, split, insert, delete, replace, replace_homophones, stick


def apply_noise(noise_function, text, cer=0.1, wer=0.2):
    """
    اعمال نویز مشخص شده روی متن ورودی
    """
    if noise_function == stick:
        return noise_function([text], cer=cer, wer=wer)[0]  # ارسال cer و wer برای stick
    else:
        return noise_function([text])[0]


def process_noise(df, noise_type, noise_function, output_dir):
    """
    پردازش داده‌ها برای ایجاد نویز مشخص و ذخیره در فایل اکسل جداگانه
    """
    output_file = os.path.join(output_dir, f"noise_{noise_type}.xlsx")  # ایجاد فایل جدا برای هر نویز

    total_rows = len(df)
    chunk_size = 4000
    num_chunks = (total_rows + chunk_size - 1) // chunk_size

    print(f"Processing {noise_type} noise...")

    new_data_list = []
    for i in tqdm(range(num_chunks), desc=f"Processing {noise_type} noise", position=0, leave=True):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_rows)

        for idx in range(start_idx, end_idx):
            org = df['origin'].iloc[idx]
            noise_text = apply_noise(noise_function, org)
            new_data_list.append({"origin": org, "noise": noise_text})

    df_new = pd.DataFrame(new_data_list)

    # بررسی وجود فایل و اضافه کردن داده‌ها
    if os.path.exists(output_file):
        with pd.ExcelWriter(output_file, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            df_new.to_excel(writer, sheet_name="NoiseData", index=False, header=False, startrow=writer.sheets["NoiseData"].max_row)
    else:
        df_new.to_excel(output_file, sheet_name="NoiseData", index=False)

    print(f"{noise_type.capitalize()} noise processing completed successfully! Data saved to {output_file}.")



# مسیر فایل‌های ورودی
input_files = {
    "pn_summary": r'D:\noise generator\pn_summary.xlsx',
    "virastar": r'D:\noise generator\virastar.xlsx',
    "medical": r'D:\noise generator\medical.xlsx'
}

# مسیر خروجی برای فایل‌های نویزی
output_dir = r'D:\noise generator'

# تعریف انواع نویزها و توابع مربوطه
noise_functions = {
    "insert": insert,
    "delete": delete,
    "swap": swap,
    "replace": replace,
    "split": split,
    "stick": stick,
    "replace_homophones": replace_homophones
}

# پردازش هر فایل برای همه نویزها
for file_name, file_path in input_files.items():
    df = pd.read_excel(file_path)

    if 'origin' not in df.columns:
        print(f"Warning: 'origin' column not found in {file_name}. Please check the file.")
        continue

    df = df.head(100000)  # محدود کردن به 100,000 داده

    for noise_type, noise_function in noise_functions.items():
        process_noise(df, noise_type, noise_function, output_dir)  # ارسال مسیر دایرکتوری، نه فایل

