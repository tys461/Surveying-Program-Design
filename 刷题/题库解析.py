import re
import json
import os

def parse_questions(text):
    """
    从给定的文本中解析出所有题目，返回列表。
    文本格式要求：
    - 专题标题以 '专题' 开头
    - 题型标题为 '一、单项选择题'、'二、多项选择题'、'三、判断题'
    - 题目编号为数字加点或圆括号，如 '1.' 或 '1)'
    - 选项以 A. B. C. D. 或 A． B． 等分隔
    - 答案在括号中或单独一行，如 '（D）' 或 '答案：D'
    - 解析在 '解析：' 或 'Explanation:' 后
    """
    questions = []
    # 按专题分割
    topic_blocks = re.split(r'(专题[一二三四五六七八九十]+)', text)
    # topic_blocks 格式：['', '专题一', '内容...', '专题二', '内容...']
    current_topic = ""
    for i, block in enumerate(topic_blocks):
        if re.match(r'专题[一二三四五六七八九十]+', block):
            current_topic = block.strip()
        elif block.strip():
            # 解析当前专题下的题目
            questions.extend(parse_topic_block(block, current_topic))
    return questions

def parse_topic_block(block, topic):
    """
    解析一个专题下的所有题目
    """
    questions = []
    # 按题型分割
    type_patterns = {
        'single': r'一、单项选择题',
        'multi': r'二、多项选择题',
        'judge': r'三、判断题'
    }
    # 找到各题型位置
    positions = []
    for qtype, pattern in type_patterns.items():
        match = re.search(pattern, block)
        if match:
            positions.append((match.start(), qtype, pattern))
    # 按位置排序
    positions.sort(key=lambda x: x[0])
    # 提取每个题型的内容
    for idx, (start, qtype, pattern) in enumerate(positions):
        end = positions[idx+1][0] if idx+1 < len(positions) else len(block)
        content = block[start:end]
        # 去掉题型标题
        content = re.sub(pattern, '', content)
        # 解析题目
        if qtype == 'single':
            questions.extend(parse_single_choice(content, topic))
        elif qtype == 'multi':
            questions.extend(parse_multi_choice(content, topic))
        elif qtype == 'judge':
            questions.extend(parse_judge(content, topic))
    return questions

def parse_single_choice(text, topic):
    """
    解析单项选择题
    """
    questions = []
    # 按题号分割，题号格式：数字. 或 数字)
    # 注意：题号可能在行首，也可能在中间
    pattern = r'(\d+)[.、)）]\s*'
    parts = re.split(pattern, text)
    # parts[0] 是分割前的垃圾，之后每两个为一组：题号，内容
    for i in range(1, len(parts)-1, 2):
        qid = int(parts[i])
        content = parts[i+1].strip()
        if not content:
            continue
        # 提取选项：A. ... B. ... C. ... D. ...
        options = []
        option_pattern = r'([A-D])[.、．]\s*([^\n]*?)(?=\s*[A-D][.、．]|$|\n)'
        opt_matches = list(re.finditer(option_pattern, content, re.DOTALL))
        if opt_matches:
            # 选项之前的文本是题干
            first_opt_start = opt_matches[0].start()
            question_text = content[:first_opt_start].strip()
            for m in opt_matches:
                opt_letter = m.group(1)
                opt_text = m.group(2).strip()
                # 清理可能的换行
                opt_text = ' '.join(opt_text.split())
                options.append(f"{opt_letter}. {opt_text}")
        else:
            # 没有选项，可能是题目不完整，跳过或作为纯文本
            question_text = content
            options = []

        # 提取答案：通常在题干末尾或独立行，如（D）或 答案：D
        answer = None
        # 尝试匹配 (D) 或 D
        ans_match = re.search(r'[（(]\s*([A-D])\s*[）)]', question_text)
        if ans_match:
            answer = ans_match.group(1)
            # 从题干中移除答案标记
            question_text = re.sub(r'[（(]\s*[A-D]\s*[）)]', '', question_text).strip()
        else:
            # 尝试在题干后面找 "答案：D"
            ans_match2 = re.search(r'答案[：:]\s*([A-D])', question_text)
            if ans_match2:
                answer = ans_match2.group(1)
                question_text = re.sub(r'答案[：:]\s*[A-D]', '', question_text).strip()

        if answer is None:
            # 有时答案在解析前
            pass

        # 提取解析：解析：...
        explanation = ""
        expl_match = re.search(r'解析[：:]\s*([^\n]*)', content, re.DOTALL)
        if expl_match:
            explanation = expl_match.group(1).strip()
            # 从内容中移除解析部分，以免影响其他
        # 如果题干中含有解析，移除它
        if expl_match:
            content = content.replace(expl_match.group(0), '')

        # 清理题干中的多余空白
        question_text = ' '.join(question_text.split())

        questions.append({
            'id': qid,
            'topic': topic,
            'type': 'single',
            'question': question_text,
            'options': options,
            'answer': answer,
            'explanation': explanation
        })
    return questions

def parse_multi_choice(text, topic):
    """
    解析多项选择题
    """
    questions = []
    # 类似单选的解析，但答案可能是多个字母
    pattern = r'(\d+)[.、)）]\s*'
    parts = re.split(pattern, text)
    for i in range(1, len(parts)-1, 2):
        qid = int(parts[i])
        content = parts[i+1].strip()
        if not content:
            continue
        # 提取选项
        options = []
        option_pattern = r'([A-D])[.、．]\s*([^\n]*?)(?=\s*[A-D][.、．]|$|\n)'
        opt_matches = list(re.finditer(option_pattern, content, re.DOTALL))
        if opt_matches:
            first_opt_start = opt_matches[0].start()
            question_text = content[:first_opt_start].strip()
            for m in opt_matches:
                opt_letter = m.group(1)
                opt_text = m.group(2).strip()
                opt_text = ' '.join(opt_text.split())
                options.append(f"{opt_letter}. {opt_text}")
        else:
            question_text = content
            options = []

        # 提取答案：可能是 (ABCD) 或 (A)(B)(C) 或 答案：ABC
        answer = None
        # 尝试匹配 (ABCD) 或 (A B C D)
        ans_match = re.search(r'[（(]\s*([A-D]+)\s*[）)]', question_text)
        if ans_match:
            answer = list(ans_match.group(1))
            question_text = re.sub(r'[（(]\s*[A-D]+\s*[）)]', '', question_text).strip()
        else:
            # 尝试 "答案：ABC"
            ans_match2 = re.search(r'答案[：:]\s*([A-D]+)', question_text)
            if ans_match2:
                answer = list(ans_match2.group(1))
                question_text = re.sub(r'答案[：:]\s*[A-D]+', '', question_text).strip()
        # 有时答案分散，如 "A、B、C"
        if not answer:
            ans_match3 = re.search(r'[A-D]\s*[、，,]\s*[A-D]', question_text)
            if ans_match3:
                # 提取所有大写字母
                ans_letters = re.findall(r'[A-D]', ans_match3.group())
                if ans_letters:
                    answer = ans_letters
                    # 移除这部分
                    question_text = re.sub(r'[A-D]\s*[、，,]\s*[A-D]', '', question_text).strip()
        if answer and isinstance(answer, str):
            answer = [answer]  # 统一为列表

        # 解析
        explanation = ""
        expl_match = re.search(r'解析[：:]\s*([^\n]*)', content, re.DOTALL)
        if expl_match:
            explanation = expl_match.group(1).strip()
            content = content.replace(expl_match.group(0), '')

        question_text = ' '.join(question_text.split())
        questions.append({
            'id': qid,
            'topic': topic,
            'type': 'multi',
            'question': question_text,
            'options': options,
            'answer': answer,
            'explanation': explanation
        })
    return questions

def parse_judge(text, topic):
    """
    解析判断题
    """
    questions = []
    # 判断题格式：题号. 题目内容（正确/错误）
    pattern = r'(\d+)[.、)）]\s*'
    parts = re.split(pattern, text)
    for i in range(1, len(parts)-1, 2):
        qid = int(parts[i])
        content = parts[i+1].strip()
        if not content:
            continue
        # 提取题目内容（去掉括号内的答案）
        question_text = content
        answer = None
        # 答案通常在括号内： （√） 或 （×） 或 （正确） （错误）
        ans_match = re.search(r'[（(]\s*([√×正确错误])\s*[）)]', question_text)
        if ans_match:
            ans = ans_match.group(1)
            if ans in ['√', '正确']:
                answer = '正确'
            elif ans in ['×', '错误']:
                answer = '错误'
            question_text = re.sub(r'[（(]\s*[√×正确错误]\s*[）)]', '', question_text).strip()
        else:
            # 可能答案在末尾 "答案：正确"
            ans_match2 = re.search(r'答案[：:]\s*(正确|错误)', question_text)
            if ans_match2:
                answer = ans_match2.group(1)
                question_text = re.sub(r'答案[：:]\s*(正确|错误)', '', question_text).strip()
        # 解析
        explanation = ""
        expl_match = re.search(r'解析[：:]\s*([^\n]*)', content, re.DOTALL)
        if expl_match:
            explanation = expl_match.group(1).strip()
            content = content.replace(expl_match.group(0), '')

        question_text = ' '.join(question_text.split())
        questions.append({
            'id': qid,
            'topic': topic,
            'type': 'judge',
            'question': question_text,
            'options': ['正确', '错误'],
            'answer': answer,
            'explanation': explanation
        })
    return questions

def main():
    # 读取原始文本文件
    input_file = 'raw.txt'   # 将你提供的PDF内容粘贴到此文件
    output_file = 'questions.json'

    if not os.path.exists(input_file):
        print(f"请将PDF文本内容保存为 {input_file} 并放在当前目录")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    questions = parse_questions(text)

    # 去重（按id和topic）
    seen = set()
    unique_questions = []
    for q in questions:
        key = (q['id'], q['topic'])
        if key not in seen:
            seen.add(key)
            unique_questions.append(q)

    # 保存为JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_questions, f, ensure_ascii=False, indent=2)

    print(f"成功解析 {len(unique_questions)} 道题目，保存至 {output_file}")

if __name__ == '__main__':
    main()