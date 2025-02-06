import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from split_stick import swap, split, insert, delete, replace

def process_noise(df, noise_type, cer_values, wer_values):
    output_file_path = os.path.join(r'D:\noise generator', f"{noise_type}_noise.xlsx")
    total_rows = len(df)

    # تقسیم داده‌ها به ۲۵ گروه ۴۰۰۰ تایی
    chunk_size = 4000
    num_chunks = total_rows // chunk_size
    if total_rows % chunk_size != 0:
        num_chunks += 1

    print(f"Total rows: {total_rows}, Total chunks: {num_chunks}")

    new_data_list = []

    print(f"Processing {noise_type} noise...")

    for i in tqdm(range(num_chunks), desc=f"Processing {noise_type} noise", position=0, leave=True):
        cer_value = cer_values[i % len(cer_values)]
        wer_value = wer_values[i % len(wer_values)]

        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_rows)

        for idx in range(start_idx, end_idx):
            org = df['origin'].iloc[idx]

            if noise_type == 'insert':
                result_token = insert([org], cer=cer_value, wer=wer_value)[0]
            elif noise_type == 'delete':
                result_token = delete([org], cer=cer_value, wer=wer_value)[0]
            elif noise_type == 'swap':
                result_token = swap([org], cer=cer_value, wer=wer_value)[0]
            elif noise_type == 'replace':
                result_token = replace([org], cer=cer_value, wer=wer_value)[0]

            new_data_list.append({"origin": org, "noise": result_token})

    df_new = pd.DataFrame(new_data_list)

    # اگر فایل از قبل وجود داشته باشد، داده‌های جدید را اضافه کن
    if os.path.exists(output_file_path):
        existing_df = pd.read_excel(output_file_path, sheet_name=None)
        sheet_names = list(existing_df.keys())

        with pd.ExcelWriter(output_file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            for i in range(0, len(df_new), 1_000_000):
                sheet_index = len(sheet_names) + (i // 1_000_000) + 1
                df_new.iloc[i:i + 1_000_000].to_excel(writer, sheet_name=f"Sheet_{sheet_index}", index=False)
    else:
        with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
            for i in range(0, len(df_new), 1_000_000):
                df_new.iloc[i:i + 1_000_000].to_excel(writer, sheet_name=f"Sheet_{i // 1_000_000 + 1}", index=False)

    print(f"{noise_type.capitalize()} noise processing completed successfully! Data saved to {output_file_path}.\n")


# تنظیم مقادیر CER و WER
cer_values = np.linspace(0.05, 0.3, 25)
wer_values = np.linspace(0.01, 0.1, 25)

# فایل‌های ورودی
input_files = {
    "pn_summary": r'D:\noise generator\pn_summary.xlsx',
    "virastar": r'D:\noise generator\virastar.xlsx',
    "medical": r'D:\noise generator\medical.xlsx'
}

# نویزها
noise_types = ["insert", "delete", "swap", "replace"]

# پردازش هر فایل
for file_name, file_path in input_files.items():
    df = pd.read_excel(file_path)

    if 'origin' not in df.columns:
        print(f"Warning: 'origin' column not found in {file_name}. Please check the file.")
        continue

    # فقط 100,000 داده
    df = df.head(100000)

    for noise_type in noise_types:
        process_noise(df, noise_type, cer_values, wer_values)
