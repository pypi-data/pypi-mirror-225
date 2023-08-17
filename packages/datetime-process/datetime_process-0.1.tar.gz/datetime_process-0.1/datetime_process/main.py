import re
from datetime import datetime

def combine_numbers_in_string(input_string):
    parts = input_string.split()  # Split the input string into parts
    combined_parts = []  # To store parts after combining

    i = 0
    while i < len(parts):
        part = parts[i]
        if part.isdigit() and len(part) == 3 and i + 1 < len(parts) and parts[i + 1].isdigit() and len(parts[i + 1]) == 1:
            combined_parts.append(part + parts[i + 1])
            i += 2  # Skip the next part
        # elif part.isdigit() and len(part) == 2 and i + 1 < len(parts) and parts[i + 1].isdigit() and len(parts[i + 1]) == 2:
        #     combined_parts.append(part + parts[i + 1])
        #     i += 2  # Skip the next part
        else:
            combined_parts.append(part)
            i += 1

    combined_string = ' '.join(combined_parts)
    return combined_string

def remove_consecutive_duplicates(input_string):
    words = input_string.split()
    new_words = [words[i] for i in range(len(words)) if i == 0 or words[i] != words[i-1]]
    return ' '.join(new_words)

def special_words(s):
    s = s.replace('đ ế n', 'đến')
    s = re.sub(r'(\w)\s?/(\s+)?', r'\1/', s)
    return s

def some_replace(s):
    s = s.replace('/ ','/')
    s = s.replace(' /','/')
    s = s.replace('. ','.')
    s = s.replace(' .','.')
    s = s.replace('-',' - ')
    return s

def replace_special_chars(s):
    #s = re.sub(r'[:`>()_,~]', ' ', s)
    s = re.sub(r'[:`(),]', ' ', s)
    s = s.replace('đến',' đến ')
    s = s.replace('từ',' từ ')
    s = s.replace(' from',' from ')
    s = s.replace(' to',' to ')
    s = s.replace('[',' ')
    s = s.replace(']',' ')
    s = s.replace('./','.')
    s = s.replace('/.','.')
    s = s.replace('\\', '/')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def clean_date_range(date_range):
    cleaned_range = re.sub(r'\.{2,}', '.', date_range)
    return cleaned_range

def clean_string_sub(input_string):
    input_string = some_replace(input_string)
    input_string = combine_numbers_in_string(input_string)
    input_string = input_string.lower()
    input_string = special_words(input_string)
    input_string = remove_consecutive_duplicates(input_string)
    cleaned = replace_special_chars(input_string)    
    return cleaned

def clean_string(input_string):
    input_string = clean_date_range(input_string)
    input_string = clean_string_sub(input_string)
    input_string = clean_date_range(input_string)
    input_string = some_replace(input_string)
    input_string = replace_special_chars(input_string)
    return input_string

def remove_list_string(text, list_str):
    for sub_str in list_str:
        text = text.replace(sub_str,'')
    return text

MONTH_PATTERN = r"(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)"
DAY_PATTERN = r"\d{1,2}(?:st|nd|rd|th)?\b"
YEAR_PATTERN = r"(?:\d{4}|\d{2}|\d{1})"

MONTH_TO_NUMBER = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4,
            "may": 5, "jun": 6, "jul": 7, "aug": 8,
            "sep": 9, "oct": 10, "nov": 11, "dec": 12,
            "sept":9,
            "january": 1, "february": 2, "march": 3, "april": 4,
            "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }

def sort_date_strings(date_strings):
    date_objects = [datetime.strptime(date_str, '%d/%m/%Y') for date_str in date_strings]
    sorted_dates = sorted(date_objects)
    return [i.strftime('%d/%m/%Y') for i in sorted_dates]

def check_list_subword(text, list_sub):
    for w in list_sub:
        if w in text:
            return True
        
    return False

def pattern_full_1(text):
    def convert_date(match):
        parts = match.split("/")
        day, month, year = map(int, parts)
        return f"{day:02d}/{month:02d}/{year}"
    #23/1/2023
    try:
        #pattern = r"\b(?:\d{1,2}\/\d{1,2}\/\d{4}|\d{1,2}\/\d{1,2}\/\d{4})\b"
        pattern = r"\b(?:\d{1,2}\/\d{1,2}\/\d{4})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        ## print(f'pattern_full_1: {text}')
        return [], text
    
def pattern_full_2(text):
    def convert_date(match):
        parts = match.split("/")
        day, month, year_string = int(parts[0]), int(parts[1]), parts[2]
        if len(year_string) == 1:
            year_string = f'0{year_string}'
        year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
        year = int(year_prefix +year_string) 
        return f"{day:02d}/{month:02d}/{year}"
    #23/1/23
    #2/12/23
    try:
        #pattern = r"\b(?:\d{1,2}\/\d{1,2}\/\d{1,2}|\d{1,2}\/\d{1,2}\/\d{1,2})\b"
        pattern = r"\b(?:\d{1,2}\/\d{1,2}\/\d{1,2})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        ## print(f'pattern_full_2: {text}')
        return [], text

def pattern_full_3(text):
    def convert_date(match):
        parts = match.split(".")
        day, month, year = map(int, parts)
        return f"{day:02d}/{month:02d}/{year}"
    #23.1.2023
    #2.12.2023
    try:
        #pattern = r"\b(?:\d{1,2}\.\d{1,2}\.\d{4}|\d{1,2}\.\d{1,2}\.\d{4})\b"
        pattern = r"\b(?:\d{1,2}\.\d{1,2}\.\d{4})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        ## print(f'pattern_full_3: {text}')
        return [], text

def pattern_full_4(text):
    def convert_date(match):
        parts = match.split(".")
        day, month, year_string = int(parts[0]), int(parts[1]), parts[2]
        if len(year_string) == 1:
            year_string = f'0{year_string}'
        year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
        year = int(year_prefix +year_string) 
        return f"{day:02d}/{month:02d}/{year}"
    #23.1.23
    #2.12.97
    try:
        #pattern = r"\b(?:\d{1,2}.\d{1,2}.\d{2}|\d{1,2}.\d{1,2}.\d{2})\b"
        pattern = r"\b(?:\d{1,2}\.\d{1,2}\.\d{2})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        # print(f'pattern_full_4: {text}')
        return [], text

def pattern_full_5(text):
    def convert_date(match):
        parts = match.split(" ")
        day, month_name, year_string = parts[0], parts[1], parts[2]
        day = re.sub(r"(st|nd|rd|th)", "", day)
        day = int(day)
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        month_number = MONTH_TO_NUMBER.get(month_name)
        return f"{day:02d}/{month_number:02d}/{year}"
    #27th april 2019 
    #27th april 2019 
    #27 april 2019 
    try:
        DATE_PATTERN = fr"(?<!\S)({DAY_PATTERN}\s{MONTH_PATTERN}\s{YEAR_PATTERN})\b"
        matches = re.findall(DATE_PATTERN, text, re.IGNORECASE)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        return [], text


def pattern_mm_yyyy_1(text):
    #1/2021
    #1.2021
    def convert_date(match):
        if '.' in match:
            parts = match.split(".")
        elif '/' in match:
            parts = match.split("/")
        month, year_string = parts[0], parts[1]
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        return f"{1:02d}/{int(month):02d}/{year}"
    try:
        #pattern = r"\b\d{1,2}[./]\d{2,4}"
        pattern = r"\b\d{1,2}[./](?:\d{2}|\d{4})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        # print(f'pattern_mm_yyyy_1: {text}')
        return [], text

def pattern_mm_yyyy_2(text):
    #2021/1
    #2021.1
    def convert_date(match):
        if '.' in match:
            parts = match.split(".")
        elif '/' in match:
            parts = match.split("/")
        year_string, month = parts[0], parts[1]
        year = int(year_string)
        return f"{1:02d}/{int(month):02d}/{year}"
    try:
        #pattern = r"\b(\d{4}\.\d{1,2}|\d{4}/\d{1,2})\b"
        pattern = r"\b(\d{4}[./]\d{1,2})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches)
        return [convert_date(match) for match in matches], text
    except:
        # print(f'pattern_mm_yyyy_2: {text}')
        return [], text

def pattern_mm_yyyy_3(text):
    # january 02
    # may 21
    # august 97
    def get_string_match(text):
        pattern = fr"(?<!\S)({MONTH_PATTERN}[ /.]{YEAR_PATTERN})\b"

        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        return matches

    def convert_date(match):
        match = match.replace('/',' ').replace('.',' ')

        parts = match.split(" ")
        month_name = parts[0]
        year_string = parts[1]
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        month_number = MONTH_TO_NUMBER.get(month_name)
        return f"{1:02d}/{month_number:02d}/{year}"
    
    try:
        complete_matches  = get_string_match(text)
        if complete_matches == []:
            return [], text
        if complete_matches!=[]:
            text = remove_list_string(text,complete_matches) 
        return [convert_date(match) for match in complete_matches], text
    except:
        # print(f'pattern_mm_yyyy_3: {text}')
        return [], text
    
def pattern_mm_yyyy_4(text):
    # january2002
    # may2
    # august97
    def split(text):
        year =''
        month_name = ''
        for char in text:
            if char.isdigit():
                year += char
            else:
                month_name += char
        return month_name, year
    def get_string_match(text):
        pattern = fr"(?<!\S)({MONTH_PATTERN}{YEAR_PATTERN})\b"

        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        return matches

    def convert_date(match):
        parts = split(match)
        month_name = parts[0]
        year_string = parts[1]
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        month_number = MONTH_TO_NUMBER.get(month_name)
        return f"{1:02d}/{month_number:02d}/{year}"
    try:
        complete_matches  = get_string_match(text)
        if complete_matches == []:
            return [], text
        if complete_matches!=[]:
            text = remove_list_string(text,complete_matches) 
    
        return [convert_date(match) for match in complete_matches], text
    except:
        # print(f'pattern_mm_yyyy_3: {text}')
        return [], text

def pattern_mm_yyyy_5(text):
    #01 năm 2012
    try:
        pattern = r"\b\d{1,2}\snăm\s\d{4}\b"
        matches = re.findall(pattern, text)
        matches_out = []
        if matches!=[]:
            text = remove_list_string(text,matches) 
    
        for match in matches:
            splt = match.split("năm")
            month = int(splt[0])
            year = int(splt[1])
            matches_out.append(datetime(year, month, 1).strftime('%d/%m/%Y'))
        return matches_out, text
    except:
        # print(f'pattern_mm_yyyy_5: {text}')
        return [], text

def pattern_mm_yyyy_6(text):
    # th10 15
    # th10/15
    # th10.15
    # t2 2022
    # t2/2022
    # t2.2022
    try:
        A = r"(?:t|th)\d{1,2}?\b"
        pattern = fr"\b({A}[ /.]{YEAR_PATTERN})\b"
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches!=[]:
            text = remove_list_string(text,matches) 
        matches_out = []
        for match in matches:
            match = match.replace("/",' ').replace('.'," ")
            match = match.replace('th','')
            match = match.replace('t','')
            parts = match.split()
            month = int(parts[0])
            year_string = parts[1]
            if len(year_string) == 4:
                year = int(year_string)
            elif len(year_string) == 1:
                year_string = f"0{year_string}"
                year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
                year = int(year_prefix +year_string)
            elif len(year_string) == 2:
                year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
                year = int(year_prefix +year_string)
            matches_out.append(f"{1:02d}/{month:02d}/{year}")
        return matches_out, text
    except:
        # print(f'pattern_mm_yyyy_6: {text}')
        return [], text

def pattern_mm_yyyy_7(text):
    #01 2012
    try:
        pattern = r"\b\d{1,2}\s\d{4}\b"
        matches = re.findall(pattern, text)
        matches_out = []
        if matches!=[]:
            text = remove_list_string(text,matches) 
        for match in matches:
            splt = match.split(" ")
            month = int(splt[0])
            year = int(splt[1])
            matches_out.append(datetime(year, month, 1).strftime('%d/%m/%Y'))
        return matches_out, text
    except:
        # print(f'pattern_mm_yyyy_7: {text}')
        return [], text

def pattern_mm_yyyy_8(text):
    # oct - 2021
    def get_string_match(text):
        pattern  = rf"({MONTH_PATTERN}\s\-\s{YEAR_PATTERN})\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        return matches

    def convert_date(match):
        parts = match.split("-")
        month_name = parts[0].strip()
        year_string = parts[1].strip()
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        month_number = MONTH_TO_NUMBER.get(month_name)
        return f"{1:02d}/{month_number:02d}/{year}"
    
    try:
        complete_matches  = get_string_match(text)
        if complete_matches == []:
            return [], text
        if complete_matches!=[]:
            text = remove_list_string(text,complete_matches) 
        
        return [convert_date(match) for match in complete_matches if convert_date(match)!=''], text
    except:
        return [], text

def pattern_mm_yyyy_9(text):
    #1 - 2021
    def convert_date(match):
        parts = match.split("-")
        month, year_string = parts[0].strip(), parts[1].strip()
        if len(year_string) == 4:
            year = int(year_string)
        elif len(year_string) == 1:
            year_string = f"0{year_string}"
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        elif len(year_string) == 2:
            year_prefix = "20" if 0 <= int(year_string) <= 30 else "19"
            year = int(year_prefix +year_string)
        else:
            return ""
        return f"{1:02d}/{int(month):02d}/{year}"
    try:
        pattern = rf"\b(\d{1,2}\s\-\s{YEAR_PATTERN})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches) 
     
        return [convert_date(match) for match in matches if convert_date(match)!=""], text
    except:
        return [], text

def pattern_mm_yyyy_10(text):
    #2021 - 1
    def convert_date(match):
        parts = match.split("-")
        year_string, month = parts[0].strip(), parts[1].strip()
        year = int(year_string)
        return f"{1:02d}/{int(month):02d}/{year}"
    try:
        pattern = r"\b(\d{4}\s\-\s\d{1,2})\b"
        matches = re.findall(pattern, text)
        if matches!=[]:
            text = remove_list_string(text,matches) 
        return [convert_date(match) for match in matches if convert_date(match)!=""], text
    except:
        return [], text

def pattern_mm_yyyy_11(text):
    # 2018 sep.
    def get_string_match(text):
        pattern = rf"(\d{{4}}\s{MONTH_PATTERN})\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        return matches

    def convert_date(match):
        parts = match.split(" ")
        month_name = parts[1].strip()
        year_string = parts[0].strip()
        year = int(year_string)
        month_number = MONTH_TO_NUMBER.get(month_name)
        return f"{1:02d}/{month_number:02d}/{year}"
    
    try:
        complete_matches  = get_string_match(text)
        if complete_matches == []:
            return [], text
        if complete_matches!=[]:
            text = remove_list_string(text,complete_matches) 
        return [convert_date(match) for match in complete_matches if convert_date(match)!=''], text
    except:
        return [], text

# def pattern_yyyy(text):
#     def is_four_digit_number(variable):
#         if isinstance(variable, str) and len(variable) == 4 and variable.isdigit():
#             return True
#         return False
#     try:
#         parts = text.split()
#         all_year = [i.strip() for i in parts if is_four_digit_number(i.strip())]
#         matches_out = []
#         for year in all_year:
#             year = int(year)
#             matches_out.append(datetime(year, 1, 1).strftime('%d/%m/%Y'))
#         return list(set(matches_out)), text
#     except:
#         # print(f'pattern_yyyy: {text}')
#         return [], text
    

def pattern_yyyy(text):
    def convert_date(match):
        return f"{1:02d}/{1:02d}/{int(match)}"
    try:
        pattern = rf"(\d{{4}})\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches == []:
            return [], text
        
        return [convert_date(match) for match in matches], text
    except:
        # print(f'pattern_yyyy: {text}')
        return [], text
def pattern_now(text):
    try:
        keywords = ["now", "present", "hiện nay", "bây giờ", "nay", 'hiện tại']
        has_keyword = any(keyword in text for keyword in keywords)

        if has_keyword:
            current_date = datetime.now().date().strftime('%d/%m/%Y')
            return [current_date], text
        else:
            return [], text
    except:
        # print(f'pattern_now: {text}')
        return [], text

def main_patterns(text):
    text = clean_string(text)
    text_raw = text
    out = []
    info, text = pattern_full_1(text)
    out.extend(info)
    info, text = pattern_full_2(text)
    out.extend(info)
    info, text = pattern_full_3(text)
    out.extend(info)
    info, text = pattern_full_4(text)
    out.extend(info)
    info, text = pattern_full_5(text)
    out.extend(info)

    info, text = pattern_mm_yyyy_1(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_2(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_3(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_4(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_5(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_6(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_7(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_8(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_9(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_10(text)
    out.extend(info)
    info, text = pattern_mm_yyyy_11(text)
    out.extend(info)
    info, text = pattern_yyyy(text)
    out.extend(info)
    info, text = pattern_now(text)
    out.extend(info)
    out = list(set(out))
    if len(out) == 0:
        return {
            "start": None,
            "end": None,
        }
    elif len(out) == 1:
        if check_list_subword(text_raw, ['from','từ']):
            return {
                "start": out[0],
                "end": None,
            }
        elif check_list_subword(text_raw, ['to', 'đến']):
            return {
                "start": None,
                "end": out[0],
            }
        else:
            return {
                "start": out[0],
                "end": None,
            }
    else:
        out_sorted = sort_date_strings(out)
        return {
            "start": out_sorted[0],
            "end": out_sorted[-1],
        }

def norm_date_times(text):
    try:
        out = main_patterns(text)
    except:
        return {
            "start": None,
            "end": None,
        }

if __name__ == "__main__":
    text = """
03 / 2006 - 12/2006
"""
    text = clean_string(text)
    print(text)
    print(main_patterns(text))