import json
import re


def decode_escaped_content(content):

    def replace_hex(match):
        hex_part = match.group(0)
        # 提取所有十六进制字节
        bytes_list = re.findall(r'\\x([0-9a-fA-F]{2})', hex_part)
        if bytes_list:
            try:
                byte_data = bytes(int(b, 16) for b in bytes_list)
                return byte_data.decode('utf-8', errors='ignore')
            except:
                return hex_part
        return hex_part

    # 替换所有连续的 \xXX 序列
    result = re.sub(r'(\\x[0-9a-fA-F]{2})+', replace_hex, content)
    return result


def decode_json_inplace(filepath):

    # 1. 读取原始文件内容（作为普通文本）
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    print("原始内容片段（前200字符）:")
    print(raw_content[:200])
    print()

    # 2. 解码所有 \x 序列
    decoded_content = decode_escaped_content(raw_content)

    print("解码后内容片段（前200字符）:")
    print(decoded_content[:200])
    print()

    # 3. 现在可以作为标准 JSON 解析了
    try:
        data = json.loads(decoded_content)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        # 如果还有问题，尝试更宽松的解析
        # 有些地方可能有不规范的转义
        return

    # 4. 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 完成！已转换 {filepath}")

    # 验证结果
    print("\n=== 验证结果 ===")
    if 'potion' in data and data['potion']:
        first_item = data['potion'][0]['data'][0]
        print(f"第一个商品: {first_item.get('name')} - {first_item.get('price')}金币")

    if 'player_coin' in data:
        print(f"玩家金币: {data['player_coin']}")


# 使用
decode_json_inplace('shop_data.json')