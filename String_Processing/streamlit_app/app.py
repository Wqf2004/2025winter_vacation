"""
字符串处理 - Streamlit网页版
包含四个问题的可视化实现
"""
import streamlit as st
from collections import Counter
from typing import List, Tuple


def calculate_dna_inversion(dna: str) -> int:
    """计算DNA逆序数"""
    order = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    count = 0
    for i in range(len(dna)):
        for j in range(i + 1, len(dna)):
            if order[dna[i]] > order[dna[j]]:
                count += 1
    return count


def string_sort_function(strings: List[str]) -> List[Tuple[str, float]]:
    """字符串排序"""
    counter = Counter(strings)
    n = len(strings)
    result = []
    for s in sorted(counter.keys()):
        percentage = counter[s] / n * 100
        result.append((s, percentage))
    return result


def arrange_words(dictionary: List[str], word: str) -> List[str]:
    """整理单词"""
    word_len = len(word)
    word_counter = Counter(word)
    matches = []
    for dict_word in dictionary:
        if len(dict_word) == word_len:
            if Counter(dict_word) == word_counter:
                matches.append(dict_word)
    return sorted(matches)


def string_type_statistics(strings: List[str], n: int) -> List[int]:
    """字符串种类统计"""
    counter = Counter(strings)
    result = [0] * (n + 1)
    for count in counter.values():
        result[count] += 1
    return result[1:n + 1]


def main():
    st.set_page_config(page_title="字符串处理", page_icon="📝", layout="wide")
    st.title("📝 字符串处理系统")

    problem_type = st.sidebar.selectbox(
        "选择问题类型",
        ["(1) DNA排序", "(2) 字符串排序",
         "(3) 整理单词", "(4) 字符串种类统计"]
    )

    if problem_type == "(1) DNA排序":
        st.markdown("## DNA排序")
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("字符串个数n", 1, 100, 6)
        with col2:
            m = st.number_input("字符串长度m", 1, 100, 10)

        dnas_input = st.text_area("DNA字符串(每行一个)", """AACATGAAGG
TTTTGGCCAA
TTTGGCCAAA
GATCAGATTT
CCCGGGGGGA
ATCGATGCAT""")

        if st.button("排序"):
            dnas = [line.strip() for line in dnas_input.strip().split('\n')][:n]
            results = [(dna, calculate_dna_inversion(dna)) for dna in dnas]
            results.sort(key=lambda x: x[1])

            st.success("排序结果:")
            for i, (dna, inv) in enumerate(results, 1):
                st.write(f"{i}. {dna} (逆序数: {inv})")

    elif problem_type == "(2) 字符串排序":
        st.markdown("## 字符串排序")
        strings_input = st.text_area("字符串(每行一个)", """Red Alder
Ash
Aspen
Basswood
Ash
Beech
Yellow Birch
Ash
Cherry
Cottonwood
Ash
Cypress
Red Elm
Gum
Hackberry
White Oak
Hickory
Pecan
Hard Maple
White Oak
Soft Maple
Red Oak
Red Oak
White Oak
Poplan
Sassafras
Sycamore
Black WaInut
Willow""")

        if st.button("排序"):
            strings = [line.strip() for line in strings_input.strip().split('\n') if line.strip()]
            result = string_sort_function(strings)

            st.success("排序结果:")
            for s, pct in result:
                st.write(f"{s} {pct:.4f}%")

    elif problem_type == "(3) 整理单词":
        st.markdown("## 整理单词")
        st.info("输入字典和要整理的字符串")

        dict_input = st.text_area("字典(每行一个单词)", """tarp
given
score
refund
only
trap
work
earn
course
pepper
part""")

        word_input = st.text_input("要整理的字符串", "aptr")

        if st.button("查找"):
            dictionary = [line.strip() for line in dict_input.strip().split('\n') if line.strip()]
            matches = arrange_words(dictionary, word_input)

            if matches:
                st.success("匹配的单词:")
                for match in matches:
                    st.write(match)
            else:
                st.error("NOT A VALID WORD")

    elif problem_type == "(4) 字符串种类统计":
        st.markdown("## 字符串种类统计")
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("字符串个数n", 1, 100, 9)
        with col2:
            m = st.number_input("字符串长度m", 1, 20, 6)

        strings_input = st.text_area("字符串(每行一个)", """AAAAAA
ACACAC
GTTTTG
ACACAC
GTTTTG
ACACAC
ACACAC
TCCCCC
TCCCCC""")

        if st.button("统计"):
            strings = [line.strip() for line in strings_input.strip().split('\n')][:n]
            result = string_type_statistics(strings, n)

            st.success("统计结果:")
            for i, count in enumerate(result, 1):
                st.write(f"出现{i}次的字符串种类数: {count}")


if __name__ == "__main__":
    main()
