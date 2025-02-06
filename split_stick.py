from __future__ import annotations
import random

def swap(tokens: list, cer: float, wer: float) -> tuple[list, list[int]]:
    flagged_for_change = list(range(len(tokens)))  # تمام داده‌ها انتخاب می‌شوند

    for for_change in flagged_for_change:
        token_for_change = tokens[for_change]

        # تعداد کلمات انتخابی برای تغییر بر اساس WER محاسبه می‌شود
        num_words_to_change = max(1, int(len(token_for_change.split()) * wer))
        words = token_for_change.split()

        # انتخاب کلمات برای تغییر
        words_to_change_indices = random.sample(range(len(words)), num_words_to_change)

        # تغییرات را اعمال کن: جابجایی تصادفی حروف در داخل کلمات انتخاب‌شده
        for idx in words_to_change_indices:
            word = words[idx]
            if len(word) > 2:  # اطمینان از امکان جابجایی حروف
                num_swaps = max(1, int(len(word) * cer))
                for _ in range(num_swaps):
                    # انتخاب دو موقعیت تصادفی برای جابجایی
                    pos1, pos2 = random.sample(range(len(word)), 2)
                    # جابجایی حروف
                    word_as_list = list(word)
                    word_as_list[pos1], word_as_list[pos2] = word_as_list[pos2], word_as_list[pos1]

                    word = ''.join(word_as_list)

                words[idx] = word

        tokens[for_change] = ' '.join(words)

    return tokens



def split(tokens: list, cer: float, wer: float) -> tuple[list, list[int]]:
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
            if len(word) > 1:  # اطمینان از امکان افزودن فاصله
                num_changes = max(1, int(len(word) * cer))
                changes_indices = random.sample(range(1, len(word)), num_changes)

                word_as_list = list(word)
                for char_idx in sorted(changes_indices, reverse=True):
                    word_as_list.insert(char_idx, ' ')

                words[idx] = ''.join(word_as_list)

        tokens[for_change] = ' '.join(words)

    return tokens

def stick(tokens: list, wer: float) -> list:
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

def insert(tokens: list, cer: float, wer: float, alphabet: str = "ابتثجحخدذرزسشصضطظعغفقکگلمنوهی") -> tuple[list, list[int]]:
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
                changes_indices = random.sample(range(len(word) + 1), num_changes)  # موقعیت‌هایی برای افزودن حروف انتخاب کن

                word_as_list = list(word)
                for char_idx in sorted(changes_indices, reverse=True):
                    random_char = random.choice(alphabet)
                    word_as_list.insert(char_idx, random_char)

                words[idx] = ''.join(word_as_list)

        tokens[for_change] = ' '.join(words)

    return tokens

def delete(tokens: list, cer: float, wer: float) -> tuple[list, list[int]]:
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
                changes_indices = random.sample(range(len(word)), num_changes)  # موقعیت‌هایی برای حذف حروف انتخاب کن

                word_as_list = list(word)
                for char_idx in sorted(changes_indices, reverse=True):
                    del word_as_list[char_idx]

                words[idx] = ''.join(word_as_list)

        tokens[for_change] = ' '.join(words)

    return tokens

def replace(tokens: list[str], cer: float, wer: float, alphabet: str = "ابتثجحخدذرزسشصضطظعغفقکگلمنوهی") -> tuple[list[str], list[int]]:
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
                changes_indices = random.sample(range(len(word)), num_changes)  # موقعیت‌هایی برای جایگزینی حروف انتخاب کن

                word_as_list = list(word)
                for char_idx in changes_indices:
                    punctuation_marks = ['.', ',', ';', ':', '!', '?', '-', '(', ')', '[', ']', '{', '}', '"', "'",
                                         '...', '  ']
                    if char_idx in punctuation_marks:
                        continue
                    else:
                        random_char = random.choice(alphabet)
                        word_as_list[char_idx] = random_char  # جایگزینی حرف با یک حرف تصادفی

                words[idx] = ''.join(word_as_list)

        tokens[for_change] = ' '.join(words)

    return tokens


def replace_homophones(tokens: list[str]) -> list[str]:
    """
    جایگزینی حروف هم‌آوا در کلمات با حروف هم‌آوای دیگر.

    Args:
        tokens: لیستی از رشته‌ها (توکن‌ها).

    Returns:
        لیستی از رشته‌ها (توکن‌ها) با حروف هم‌آوای جایگزین شده.
    """

    homophone_map = {
        'ا': [ 'آ'],
        'ث': ['س', 'ص'],
        'س': ['ث', 'ص'],
        'ص': ['س' , 'ث'],
        'ذ': ['ز' , 'ض'],
        'ز': ['ذ', 'ض'],
        'ض': ['ز' , 'ذ'],
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
        modified_words = []
        for word in words:
            modified_word = ""
            for char in word:
                if char in homophone_map and random.random() < 0.5:  # احتمال 50% برای جایگزینی

                    homophones = homophone_map[char]
                    modified_char = random.choice(homophones)
                    modified_word += modified_char
                else:
                    modified_word += char
            modified_words.append(modified_word)
        modified_tokens.append(" ".join(modified_words))

    return modified_tokens


# مثال استفاده
#tokens = ["اکنون به‌گونه‌ای تغییر کرده است که اگر طول کلمه کمتر از 4 حرف باشد، نویز کم‌نویسی روی آن اعمال نمی‌شود و به سراغ کلمات دیگر می‌رود. این تغییر به بهبود خوانایی کلمات کوتاه کمک می‌کند."]
#noisy_tokens = replace_homophones(tokens)
#print(noisy_tokens)
