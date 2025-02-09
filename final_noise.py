from __future__ import annotations
import random
import pandas as pd

class NoiseGenerator:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.df = pd.read_excel(input_file)
        self.sheet_name = "Sheet1"

    def swap(self, tokens: list, wer: float, *cer: float) -> list:
        flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]

            # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
            words = token_for_change.split()
            num_words_to_change = max(1, int(len(words) * wer))

            valid_indices = [i for i in range(len(words)) if len(words[i]) > 3]

            if len(valid_indices) < num_words_to_change:
                num_words_to_change = len(valid_indices)

            words_to_change_indices = random.sample(valid_indices, num_words_to_change) if valid_indices else []

            # تغییرات را اعمال کن: جابجایی تنها بین حروف مجاور
            for idx in words_to_change_indices:
                word = words[idx]
                pos = random.randint(0, len(word) - 2)  # انتخاب یک موقعیت تصادفی برای جابجایی
                word_as_list = list(word)
                word_as_list[pos], word_as_list[pos + 1] = word_as_list[pos + 1], word_as_list[pos]
                words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def split(self,tokens: list, wer: float, cer: float) -> tuple[list, list[int]]:
        flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]

            # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
            num_words_to_change = max(1, int(len(token_for_change.split()) * wer))
            words = token_for_change.split()

            # انتخاب کلمات برای تغییر
            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            # تغییرات را اعمال کن: اضافه کردن فاصله در داخل کلمات انتخاب‌شده
            for idx in words_to_change_indices:
                word = words[idx]
                if len(word) > 2:  # اطمینان از امکان افزودن فاصله
                    num_changes = max(1, int(len(word) * cer))
                    changes_indices = random.sample(range(1, len(word)), num_changes)

                    word_as_list = list(word)
                    for char_idx in sorted(changes_indices, reverse=True):
                        word_as_list.insert(char_idx, ' ')

                    words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def stick(self,tokens: list, wer: float, *cer: float) -> list:
        noisy_tokens = []  # لیست برای نگهداری جملات نویزدار
        for sentence in tokens:
            words = sentence.split()  # شکستن جمله به کلمات
            if len(words) < 2:  # اگر جمله کمتر از دو کلمه داشته باشد، تغییری اعمال نشود
                noisy_tokens.append(sentence)
                continue
            num_pairs_to_modify = min(max(1, int(len(words) * wer)), len(words) - 1)
            flagged_indices = sorted(random.sample(range(len(words) - 1), num_pairs_to_modify), reverse=True)

            for idx in flagged_indices:
                words[idx] = words[idx] + words[idx + 1]
                del words[idx + 1]  # حذف کلمه بعدی
            noisy_tokens.append(" ".join(words))  # بازسازی جمله
        return noisy_tokens

    def insert(self,tokens: list, wer: float, cer: float, alphabet: str = "ضصثقفغعهخحجچگکمنتالبیسشظطزرذدپوژآ") -> tuple[
        list, list[int]]:
        flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]

            # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
            num_words_to_change = max(1, int(len(token_for_change.split()) * wer))
            words = token_for_change.split()

            # انتخاب کلمات برای تغییر
            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            # تغییرات را اعمال کن: افزودن حروف تصادفی در داخل کلمات انتخاب‌شده
            for idx in words_to_change_indices:
                word = words[idx]
                if len(word) > 2:  # اطمینان از امکان افزودن حروف
                    num_changes = max(1, int(len(word) * cer))
                    changes_indices = random.sample(range(len(word) + 1),
                                                    num_changes)  # موقعیت‌هایی برای افزودن حروف انتخاب کن

                    word_as_list = list(word)
                    for char_idx in sorted(changes_indices, reverse=True):
                        random_char = random.choice(alphabet)
                        word_as_list.insert(char_idx, random_char)

                    words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def delete(self, tokens: list, wer: float, cer: float) -> tuple[list, list[int]]:
        flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]

            # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
            num_words_to_change = max(1, int(len(token_for_change.split()) * wer))
            words = token_for_change.split()

            # انتخاب کلمات برای تغییر
            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            # تغییرات را اعمال کن: حذف حروف تصادفی از داخل کلمات انتخاب‌شده
            for idx in words_to_change_indices:
                word = words[idx]
                if len(word) > 3:  # اگر طول کلمه بیشتر از 4 حرف باشد تغییرات را اعمال کن
                    num_changes = max(1, int(len(word) * cer))
                    changes_indices = random.sample(range(len(word)),
                                                    num_changes)  # موقعیت‌هایی برای حذف حروف انتخاب کن

                    word_as_list = list(word)
                    for char_idx in sorted(changes_indices, reverse=True):
                        del word_as_list[char_idx]

                    words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def replace(self, tokens: list[str], wer: float, cer: float, alphabet: str = "ضصثقفغعهخحجچگکمنتالبیسشظطزرذدپوژآ") -> \
    tuple[list[str], list[int]]:
        flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]

            # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
            num_words_to_change = max(1, int(len(token_for_change.split()) * wer))
            words = token_for_change.split()

            # انتخاب کلمات برای تغییر
            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            # تغییرات را اعمال کن: حذف حروف تصادفی و جایگزینی آن‌ها با حروف دیگر
            for idx in words_to_change_indices:
                word = words[idx]
                if len(word) > 3:  # اگر طول کلمه بیشتر از 4 حرف باشد تغییرات را اعمال کن
                    num_changes = max(1, int(len(word) * cer))
                    changes_indices = random.sample(range(len(word)),
                                                    num_changes)  # موقعیت‌هایی برای جایگزینی حروف انتخاب کن

                    word_as_list = list(word)
                    for char_idx in changes_indices:
                        punctuation_marks = ['.', ',', ';', ':', '!', '?', '-', '(', ')', '[', ']', '{', '}', '"',
                                             "'",
                                             '...', '  ']
                        if char_idx in punctuation_marks:
                            continue
                        else:
                            random_char = random.choice(alphabet)
                            word_as_list[char_idx] = random_char  # جایگزینی حرف با یک حرف تصادفی

                    words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def replace_homophones(self, tokens: list[str], wer: float, *cer: float) -> list[str]:
        """
        جایگزینی حروف هم‌آوا در کلمات با توجه به میزان WER.

        Args:
            tokens: لیستی از رشته‌ها (توکن‌ها).
            wer: نسبت کلماتی که باید تغییر کنند.

        Returns:
            لیستی از رشته‌ها (توکن‌ها) با حروف هم‌آوای جایگزین شده.
        """
        homophone_map = {
            'ا': ['آ'],
            'ث': ['س', 'ص'],
            'س': ['ث', 'ص'],
            'ص': ['س', 'ث'],
            'ذ': ['ز', 'ض'],
            'ز': ['ذ', 'ض'],
            'ض': ['ز', 'ذ'],
            'ت': ['ط'],
            'ط': ['ت'],
            'ح': ['ه'],
            'ه': ['ح'],
            'ق': ['غ'],
            'غ': ['ق'],
            'ک': ['گ'],
            'گ': ['ک']
        }

        modified_tokens = []
        for token in tokens:
            words = token.split()
            num_words_to_change = max(1, int(len(words) * wer))

            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            modified_words = words[:]
            for idx in words_to_change_indices:
                word = words[idx]
                modified_word = list(word)
                homophone_indices = [i for i, char in enumerate(word) if char in homophone_map]

                if homophone_indices:
                    char_idx = random.choice(homophone_indices)
                    modified_word[char_idx] = random.choice(homophone_map[modified_word[char_idx]])

                modified_words[idx] = "".join(modified_word)

            modified_tokens.append(" ".join(modified_words))

        return modified_tokens

    def repeat(self, tokens: list, wer: float, cer: float) -> list:
        flagged_for_change = list(range(len(tokens)))

        for for_change in flagged_for_change:
            token_for_change = tokens[for_change]
            words = token_for_change.split()

            num_words_to_change = max(1, int(len(words) * wer))
            words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

            for idx in words_to_change_indices:
                word = words[idx]
                if len(word) > 1:
                    num_repeats = max(1, int(len(word) * cer))
                    repeat_indices = random.sample(range(len(word)), num_repeats)

                    word_as_list = list(word)
                    for repeat_index in sorted(repeat_indices, reverse=True):
                        word_as_list.insert(repeat_index, word_as_list[repeat_index])

                    words[idx] = ''.join(word_as_list)

            tokens[for_change] = ' '.join(words)

        return tokens

    def noise_generator(self, noise_type: str):
        output_file = f"noisy_{noise_type}.xlsx"
        if noise_type in ['swap', 'stick', 'replace_homophones' ]:
            wer_start, wer_end, wer_step = 0.01, 0.2, 0.01
            batch_size = len(self.df) // 20
        else:
            cer_start, cer_end, cer_step = 0.1, 0.5, 0.1
            wer_start, wer_end, wer_step = 0.01, 0.1, 0.01
            batch_size = len(self.df) // 50

        try:
            existing_data = pd.read_excel(self.output_file, sheet_name=self.sheet_name, engine="openpyxl")
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=["origin", "noise"])

        total_rows = len(self.df)
        processed_rows = 0

        for cer_value in ([cer_start + i * cer_step for i in range(int((cer_end - cer_start) / cer_step) + 1)] if noise_type not in ['swap', 'stick', 'replace_homophones'] else [None]):
            for wer_value in [wer_start + i * wer_step for i in range(int((wer_end - wer_start) / wer_step) + 1)]:
                start_idx = processed_rows
                end_idx = min(processed_rows + batch_size, total_rows)
                if start_idx >= total_rows:
                    break
                column_list = self.df['origin'].iloc[start_idx:end_idx].tolist()
                org = column_list.copy()
                if noise_type == 'swap':
                    result_tokens = self.swap(column_list, wer=wer_value)
                elif noise_type == 'split':
                    result_tokens = self.split(column_list, wer=wer_value, cer=cer_value)
                elif noise_type == 'stick':
                    result_tokens = self.stick(column_list, wer=wer_value)
                elif noise_type == 'insert':
                    result_tokens = self.insert(column_list, wer=wer_value, cer=cer_value)
                elif noise_type == 'delete':
                    result_tokens = self.delete(column_list, wer=wer_value, cer=cer_value)
                elif noise_type == 'replace':
                    result_tokens = self.replace(column_list, wer=wer_value, cer=cer_value)
                elif noise_type == 'replace_homophones':
                    result_tokens = self.replace_homophones(column_list, wer=wer_value)
                elif noise_type == 'repeat':
                    result_tokens = self.repeat(column_list, wer=wer_value, cer=cer_value)
                else:
                    print("noise type is not valid")
                new_data = {"origin": org, "noise": result_tokens}
                df_new = pd.DataFrame(new_data)
                combined_data = pd.concat([existing_data, df_new], ignore_index=True)

                with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
                    combined_data.to_excel(writer, sheet_name=self.sheet_name, index=False)

                existing_data = combined_data
                processed_rows = end_idx
                if processed_rows >= total_rows:
                    break
        print(f"Processing complete. Output saved to {output_file}")
