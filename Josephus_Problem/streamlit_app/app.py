"""
Josephus环问题 - Streamlit网页版
包含四种变体的可视化实现
"""
import streamlit as st
from typing import List, Tuple


def josephus_with_names_visual(names: List[str], k: int, m: int) -> Tuple[List[str], List[str]]:
    """带人名的Josephus环问题"""
    n = len(names)
    people = list(range(n))
    result = []
    steps = []

    current = k - 1

    for round_num in range(1, n + 1):
        current = (current + m - 1) % len(people)
        eliminated = people.pop(current)
        result.append(names[eliminated])
        steps.append(f"第{round_num}轮: 编号{eliminated+1}({names[eliminated]})出列")

    return result, steps


def reverse_josephus_visual(n: int, m: int, x: int) -> Tuple[int, List[str]]:
    """反Josephus环问题"""
    for k in range(1, n + 1):
        people = list(range(n))
        current = k - 1

        for _ in range(n - 1):
            current = (current + m - 1) % len(people)
            people.pop(current)

        if people[0] + 1 == x:
            return k, [f"从第{k}人开始，第{x}人最后出列"]

    return -1, []


def josephus_variant_visual(k: int, max_search: int = 1000) -> Tuple[int, List[str]]:
    """Josephus环问题的变形"""
    for m in range(1, max_search + 1):
        people = list(range(1, 2 * k + 1))
        current = 0

        good_eliminated = False
        while len(people) > k and not good_eliminated:
            current = current % len(people)
            eliminated = people.pop(current)
            if eliminated <= k:
                good_eliminated = True
            current = current % len(people) if people else 0

        if len(people) == k and all(p <= k for p in people):
            return m, [f"最小m={m}, 剩余: {people}"]

    return -1, []


def linear_counting_visual(n: int, x: int, cards: List[int]) -> Tuple[List[int], int, List[str]]:
    """直线型报数问题"""
    people = list(range(1, n + 1))
    current_card_idx = 0
    steps = []

    steps.append(f"初始: {people}")

    while len(people) > x:
        if current_card_idx >= len(cards):
            break

        m = cards[current_card_idx]
        current_card_idx += 1
        current_idx = 0

        eliminated_round = []
        while current_idx < len(people) and len(people) > x:
            current_idx = (current_idx + m - 1) % len(people)
            eliminated_round.append(people.pop(current_idx))
            current_idx = current_idx % len(people) if people else 0

        steps.append(f"卡片{current_card_idx}(m={m}): 出列{eliminated_round}, 剩余{people}")

    return people, current_card_idx, steps


def main():
    st.set_page_config(page_title="Josephus环问题", page_icon="🔄", layout="wide")
    st.title("🔄 Josephus环问题可视化")

    problem_type = st.sidebar.selectbox(
        "选择问题类型",
        ["(1) 带人名的Josephus环问题", "(2) 反Josephus环问题",
         "(3) Josephus环问题的变形", "(4) 直线型报数问题"]
    )

    if problem_type == "(1) 带人名的Josephus环问题":
        st.markdown("## 带人名的Josephus环问题")
        col1, col2, col3 = st.columns(3)
        with col1:
            n = st.number_input("人数n", 1, 64, 5)
        with col2:
            k = st.number_input("起始k", 1, n, 2)
        with col3:
            m = st.number_input("报数m", 1, 100, 3)

        names_input = st.text_area("人名", "Caobainan\nMazhongyi\nShenyongqiang\nTaozhengyi\nJiangdebing")
        names = [name.strip() for name in names_input.strip().split('\n')[:n]]

        if st.button("模拟"):
            eliminated, steps = josephus_with_names_visual(names, k, m)
            st.success("出列顺序:")
            for i, name in enumerate(eliminated, 1):
                st.write(f"{i}. {name}")

    elif problem_type == "(2) 反Josephus环问题":
        st.markdown("## 反Josephus环问题")
        col1, col2, col3 = st.columns(3)
        with col1:
            n = st.number_input("人数n", 1, 50, 41)
        with col2:
            m = st.number_input("报数m", 1, 100, 3)
        with col3:
            x = st.number_input("目标x", 1, n, 3)

        if st.button("搜索k值"):
            k, process = reverse_josephus_visual(n, m, x)
            if k != -1:
                st.success(f"k = {k}")
            else:
                st.error("未找到")

    elif problem_type == "(3) Josephus环问题的变形":
        st.markdown("## Josephus环问题的变形")
        k = st.number_input("好人数量k", 1, 7, 3)
        st.info(f"总人数={2*k}")

        if st.button("搜索最小m"):
            m, process = josephus_variant_visual(k)
            if m != -1:
                st.success(f"最小m = {m}")
            else:
                st.error("未找到")

    elif problem_type == "(4) 直线型报数问题":
        st.markdown("## 直线型报数问题")
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("人数n", 1, 50, 10)
        with col2:
            x = st.number_input("幸存人数X", 1, n, 2)

        cards_input = st.text_area("卡片数值(空格分隔)", "3 5 4 3 2 9 6 10 10 6 2 6 7 3 4 7 4 5 3 2")
        cards = list(map(int, cards_input.split()))

        if st.button("模拟"):
            lucky, used, steps = linear_counting_visual(n, x, cards)
            st.success(f"幸存者: {lucky}")
            st.info(f"使用卡片: {used}")


if __name__ == "__main__":
    main()
