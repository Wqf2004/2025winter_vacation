import streamlit as st
import random
import time
import os
from data_manager import DataManager

# 页面配置
st.set_page_config(page_title='扫雷游戏', page_icon='💣', layout='centered', 
                 initial_sidebar_state='collapsed')

# 自定义CSS - 紧凑布局
st.markdown("""
<style>
    /* 整体容器 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 标题 */
    h1 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 10px !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        height: 40px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 8px;
    }
    
    /* Metric卡片 */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        flex: 1;
        min-width: 100px;
    }
    
    /* 游戏网格 */
    .game-cell {
        width: 28px !important;
        height: 28px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
    }
    
    /* Streamlit按钮样式优化 */
    .stButton > button {
        padding: 0 !important;
        min-height: 28px !important;
        font-size: 12px !important;
        line-height: 1 !important;
        margin: 0 !important;
    }

    /* 游戏网格列布局 */
    div[data-testid="column"] {
        padding: 1px !important;
    }
    
    .game-cell.hidden {
        background-color: #e0e0e0;
        border: 1px solid #999;
    }
    
    .game-cell.revealed-0 {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    
    .game-cell.flagged {
        background-color: #ffcccc;
        border: 1px solid #ff9999;
    }
    
    .game-cell.mine {
        background-color: #ff6666;
        border: 1px solid #ff0000;
    }
    
    /* 数字颜色 */
    .num-1 { color: #0000ff; }
    .num-2 { color: #008000; }
    .num-3 { color: #ff0000; }
    .num-4 { color: #000080; }
    .num-5 { color: #800000; }
    .num-6 { color: #008080; }
    .num-7 { color: #000000; }
    .num-8 { color: #808080; }
    
    /* 输入控件 */
    .stSelectbox, .stNumberInput {
        flex: 1;
    }
    
    /* 去除多余间距 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'game_map' not in st.session_state:
    st.session_state.game_map = []
if 'revealed' not in st.session_state:
    st.session_state.revealed = []
if 'flagged' not in st.session_state:
    st.session_state.flagged = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'mines_remaining' not in st.session_state:
    st.session_state.mines_remaining = 10
if 'last_clicked' not in st.session_state:
    st.session_state.last_clicked = None

# 游戏参数
DIFFICULTIES = {
    '简单': {'rows': 9, 'cols': 9, 'mines': 10},
    '中等': {'rows': 10, 'cols': 10, 'mines': 10},
    '困难': {'rows': 16, 'cols': 16, 'mines': 40}
}

def login_page():
    st.title('💣 扫雷游戏')
    
    tab1, tab2 = st.tabs(['🔐 登录', '📝 注册'])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            login_name = st.text_input('用户名', key='login_name')
        with col2:
            login_pass = st.text_input('密码', type='password', key='login_pass')
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button('🔑 登录', use_container_width=True):
                if login_name and login_pass:
                    success, user = DataManager.login_user(login_name, login_pass)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.page = 'menu'
                        st.rerun()
                    else:
                        st.error('用户名或密码错误')
                else:
                    st.warning('请输入用户名和密码')
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            reg_name = st.text_input('用户名', key='reg_name')
        with col2:
            reg_pass = st.text_input('密码', type='password', key='reg_pass')
        reg_confirm = st.text_input('确认密码', type='password', key='reg_confirm')
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button('✅ 注册', use_container_width=True):
                if reg_name and reg_pass:
                    if reg_pass == reg_confirm:
                        success, message = DataManager.register_user(reg_name, reg_pass)
                        if success:
                            st.success(message)
                            st.info('请登录')
                        else:
                            st.error(message)
                    else:
                        st.error('两次密码不一致')
                else:
                    st.warning('请输入用户名和密码')

def main_menu():
    st.title(f'💣 扫雷游戏 - {st.session_state.user["name"]}')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('🎮 开始游戏', use_container_width=True):
            st.session_state.page = 'game'
            st.rerun()
    with col2:
        if st.button('🏆 排行榜', use_container_width=True):
            st.session_state.page = 'ranking'
            st.rerun()
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button('🚪 退出登录', use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.page = 'login'
            st.rerun()

def init_game(difficulty):
    config = DIFFICULTIES[difficulty]
    rows, cols, mines = config['rows'], config['cols'], config['mines']
    
    st.session_state.rows = rows
    st.session_state.cols = cols
    st.session_state.mines_count = mines
    st.session_state.game_map = [[0] * cols for _ in range(rows)]
    st.session_state.revealed = [[False] * cols for _ in range(rows)]
    st.session_state.flagged = [[False] * cols for _ in range(rows)]
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.start_time = None
    st.session_state.mines_remaining = mines
    st.session_state.first_click = True
    st.session_state.last_clicked = None

def place_mines(first_row, first_col):
    rows = st.session_state.rows
    cols = st.session_state.cols
    mines = st.session_state.mines_count
    
    # 随机放置地雷
    positions = [(i, j) for i in range(rows) for j in range(cols) 
                if not (abs(i - first_row) <= 1 and abs(j - first_col) <= 1)]
    random.shuffle(positions)
    
    for i in range(mines):
        row, col = positions[i]
        st.session_state.game_map[row][col] = -1
    
    # 计算周围地雷数
    for i in range(rows):
        for j in range(cols):
            if st.session_state.game_map[i][j] != -1:
                count = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if st.session_state.game_map[ni][nj] == -1:
                                count += 1
                st.session_state.game_map[i][j] = count

def reveal_cell(row, col):
    if row < 0 or row >= st.session_state.rows or col < 0 or col >= st.session_state.cols:
        return
    if st.session_state.revealed[row][col] or st.session_state.flagged[row][col]:
        return
    
    st.session_state.revealed[row][col] = True
    
    if st.session_state.game_map[row][col] == -1:
        st.session_state.game_over = True
        return
    
    if st.session_state.game_map[row][col] == 0:
        # 递归翻开周围的格子
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di != 0 or dj != 0:
                    reveal_cell(row + di, col + dj)

def check_win():
    rows = st.session_state.rows
    cols = st.session_state.cols
    
    won = True
    for i in range(rows):
        for j in range(cols):
            if st.session_state.game_map[i][j] != -1 and not st.session_state.revealed[i][j]:
                won = False
                break
        if not won:
            break
    
    if won:
        st.session_state.game_won = True
        st.session_state.game_over = True
        elapsed = int(time.time() - st.session_state.start_time)
        DataManager.update_best_time(st.session_state.user['name'], elapsed)
        DataManager.save_score(st.session_state.user['name'], elapsed)

def game_page():
    st.title('💣 扫雷游戏')
    
    # 顶部控制栏 - 紧凑布局
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        difficulty = st.selectbox('难度', ['简单', '中等', '困难'], label_visibility='collapsed')
    
    with col2:
        if st.button('🔄 新游戏', use_container_width=True):
            init_game(difficulty)
            st.rerun()
    
    with col3:
        if st.button('🔙 返回', use_container_width=True):
            st.session_state.page = 'menu'
            st.rerun()
    
    with col4:
        elapsed = 0
        if st.session_state.start_time and not st.session_state.game_over:
            elapsed = int(time.time() - st.session_state.start_time)
        elif st.session_state.start_time and 'start_time_elapsed' in st.session_state:
            elapsed = int(st.session_state.start_time_elapsed)
        st.metric(f'⏱️ {elapsed}秒', '', '')
    
    # 初始化游戏
    if not st.session_state.game_map or st.session_state.rows != DIFFICULTIES[difficulty]['rows']:
        init_game(difficulty)
    
    # 剩余雷数
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric(f'💣 {st.session_state.mines_remaining}', '剩余', '')
    with col2:
        # 游戏结果提示
        if st.session_state.game_over:
            if st.session_state.game_won:
                st.success('🎉 恭喜你赢了!')
            else:
                st.error('💥 游戏结束!')
    
    # 游戏网格
    rows = st.session_state.rows
    cols = st.session_state.cols
    
    # 点击格子快速操作
    col1, col2, col3 = st.columns(3)
    with col1:
        row_num = st.number_input('行', min_value=1, max_value=rows,
                                  value=st.session_state.get('row_num_input', 1))
        # 保存用户输入的值
        st.session_state.row_num_input = row_num
    with col2:
        col_num = st.number_input('列', min_value=1, max_value=cols,
                                  value=st.session_state.get('col_num_input', 1))
        # 保存用户输入的值
        st.session_state.col_num_input = col_num
    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            if st.button('▶️ 翻开', use_container_width=True, key='reveal_btn'):
                r, c = row_num - 1, col_num - 1
                if 0 <= r < rows and 0 <= c < cols and not st.session_state.game_over:
                    # 如果已标记，左击会自动取消标记
                    if st.session_state.flagged[r][c]:
                        st.session_state.flagged[r][c] = False
                        st.session_state.mines_remaining += 1
                    if st.session_state.first_click:
                        place_mines(r, c)
                        st.session_state.first_click = False
                        st.session_state.start_time = time.time()
                    reveal_cell(r, c)
                    check_win()
                    if st.session_state.game_over and st.session_state.start_time:
                        st.session_state.start_time_elapsed = time.time() - st.session_state.start_time
                    st.rerun()
        with col3b:
            if st.button('🚩 标记', use_container_width=True, key='flag_btn'):
                r, c = row_num - 1, col_num - 1
                if 0 <= r < rows and 0 <= c < cols and not st.session_state.game_over:
                    if not st.session_state.revealed[r][c]:
                        st.session_state.flagged[r][c] = not st.session_state.flagged[r][c]
                        if st.session_state.flagged[r][c]:
                            st.session_state.mines_remaining -= 1
                        else:
                            st.session_state.mines_remaining += 1
                    st.rerun()
    
    # 游戏网格显示 - 使用Streamlit按钮实现可点击格子
    st.markdown('<div style="display: flex; flex-direction: column; align-items: center; gap: 0px;">', unsafe_allow_html=True)

    for i in range(rows):
        cols_layout = st.columns(cols)
        for j in range(cols):
            with cols_layout[j]:
                if st.session_state.revealed[i][j]:
                    if st.session_state.game_map[i][j] == -1:
                        st.markdown(f'<div class="game-cell mine">💣</div>', unsafe_allow_html=True)
                    else:
                        num = st.session_state.game_map[i][j]
                        if num == 0:
                            st.markdown('<div class="game-cell revealed-0"></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="game-cell revealed-0 num-{num}">{num}</div>', unsafe_allow_html=True)
                elif st.session_state.flagged[i][j]:
                    st.markdown(f'<div class="game-cell flagged">🚩</div>', unsafe_allow_html=True)
                else:
                    # 每个格子是一个可点击的按钮，点击只填入行列号
                    cell_key = f'cell_{i}_{j}'
                    if st.button(' ', key=cell_key, help=f'点击填入: {i+1}行{j+1}列',
                                use_container_width=True):
                        # 只更新输入框，不直接翻开
                        st.session_state.row_num_input = i + 1
                        st.session_state.col_num_input = j + 1
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 操作提示
    st.markdown('''
    <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 8px; margin-top: 8px;">
        <p style="margin: 0; color: white; text-align: center; font-size: 12px;">
            💡 <strong>操作方式:</strong> 点击格子填入行列号 → 点击"翻开"或"标记"按钮执行操作
        </p>
    </div>
    ''', unsafe_allow_html=True)

def ranking_page():
    st.title('🏆 排行榜')
    
    users = DataManager.load_users()
    
    # 按最佳成绩排序
    valid_users = [u for u in users if u.get('best_time', -1) != -1]
    valid_users.sort(key=lambda x: x.get('best_time', float('inf')))
    
    if valid_users:
        data = []
        for i, user in enumerate(valid_users):
            data.append({
                '🏅': i + 1,
                '👤 用户名': user['name'],
                '⏱️ 最佳时间': f'{user["best_time"]}秒'
            })
        st.table(data)
    else:
        st.info('暂无记录')
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🔙 返回', use_container_width=True):
            st.session_state.page = 'menu'
            st.rerun()

# 路由
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'menu':
    main_menu()
elif st.session_state.page == 'game':
    game_page()
elif st.session_state.page == 'ranking':
    ranking_page()
