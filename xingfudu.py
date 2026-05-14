# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:29:27 2026

@author: qianxinyan
"""

# -*- coding: utf-8 -*-
from openai import OpenAI
import time

client = OpenAI(
    api_key="sk-f29acb702c434c1289b45d86e2a64b63",
    base_url="https://api.deepseek.com"
)

# 情感判断（你要的英文精准指令）
def get_sentiment(text):
    prompt = f'''
Task rules:
1. determine whether the text is related to emotions, feelings, evaluations, parks, green spaces, nature, or related activities.
Relevant content includes: all expressions of emotions (happiness, joy, sorrow, being busy, feeling tired), all evaluations (really good, really bad), parks, green spaces, gardens, lawns, woodlands, riverside greenbelts, trails, plazas, as well as various activities carried out here (walking, jogging, exercising, resting, playing, relaxing, leisure, viewing scenery, happiness, joy, comfort, pleasure, satisfaction).
2. If the text is NOT relevant, output ONLY 3.
3. If the text IS relevant, judge its emotion: output 1 for positive, 0 for negative.
Final output: ONLY 1, 0, or 3. NO extra words, NO explanation!

Text: {text}
Output:
'''
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        res = response.choices[0].message.content.strip()
        if res in ['1', '0', '3']:
            return res
        else:
            return "invalid"
    except:
        return "error"

# ==================== 主程序 ====================
if __name__ == "__main__":
    file_path = "G:/园林年会/1.csv"
    output_path = "G:/园林年会/wenben_result_100155-5w.csv"

    # 最终修复：中文CSV不乱码编码
    with open(file_path, "r", encoding="gb18030") as f:
        lines = f.readlines()

    with open(output_path, "w", encoding="utf-8-sig") as f:
        header = lines[0].strip() + ",sentiment(1=正,0=负)\n"
        f.write(header)
        
        # 逐行处理
        for line in lines[1:]:
            # 清理换行、空格
            current_line = line.strip()


            # 正常处理
            weibo = current_line.split(",")[0]
            result = get_sentiment(weibo)
            f.write(f"{current_line},{result}\n")
            print(f"【结果】{result} | {weibo}")
            time.sleep(0.5)

    print("🎉 全部处理完成！")