import streamlit as st
from data_manager import DataManager

# 页面配置
st.set_page_config(page_title='五子棋游戏', page_icon='⚫', layout='centered')

# 自定义CSS - 紧凑布局
st.markdown("""
<style>
    /* 棋盘格子样式 */
    .board-cell {
        width: 28px !important;
        height: 28px !important;
        padding: 0 !important;
        margin: 1px !important;
        border-radius: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    /* 按钮样式 */
    .stButton > button {
        padding: 2px 8px !important;
        font-size: 13px !important;
        min-height: 28px !important;
        width: 28px !important;
    }

    /* 输入框样式 */
    .stNumberInput {
        padding: 0 !important;
    }

    /* 列布局 */
    div[data-testid="column"] {
        padding: 2px !important;
    }

    /* Metric卡片 */
    div[data-testid="stMetric"] {
        padding: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# 常量定义
EMPTY = 0
BLACK = 1
WHITE = 2

# 方向数组
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

# 初始化session state
if 'board' not in st.session_state:
    st.session_state.board = [[EMPTY for _ in range(15)] for _ in range(15)]
if 'moves' not in st.session_state:
    st.session_state.moves = []
if 'current_player' not in st.session_state:
    st.session_state.current_player = BLACK
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 0  # 0: 人-人, 1: 人-计, 2: 计-人
if 'board_size' not in st.session_state:
    st.session_state.board_size = 15

def init_board(size=15):
    """初始化棋盘"""
    st.session_state.board = [[EMPTY for _ in range(size)] for _ in range(size)]
    st.session_state.moves = []
    st.session_state.current_player = BLACK
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.board_size = size

def reset_board():
    """重置棋盘"""
    size = st.session_state.board_size
    st.session_state.board = [[EMPTY for _ in range(size)] for _ in range(size)]
    st.session_state.moves = []
    st.session_state.current_player = BLACK
    st.session_state.game_over = False
    st.session_state.winner = None

def calc_value(x, y, color):
    """计算位置价值"""
    board = st.session_state.board
    size = st.session_state.board_size
    opponent = WHITE if color == BLACK else BLACK
    values = [0, 100, 600, 6000, 40000]
    total_score = 0
    
    center = size // 2
    
    for dx, dy in DIRECTIONS:
        # 进攻
        count = 1
        blocked = 0
        
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == color:
                    count += 1
                elif board[ny][nx] == EMPTY:
                    break
                else:
                    blocked += 1
                    break
            else:
                blocked += 1
                break
        
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == color:
                    count += 1
                elif board[ny][nx] == EMPTY:
                    break
                else:
                    blocked += 1
                    break
            else:
                blocked += 1
                break
        
        if count >= 5:
            return 100000
        if count <= 4:
            total_score += values[count] * (2 - blocked)
        
        # 防守
        block_count = 1
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == opponent:
                    block_count += 1
                else:
                    break
            else:
                break
        
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == opponent:
                    block_count += 1
                else:
                    break
            else:
                break
        
        if block_count >= 3 and block_count < len(values):
            total_score += values[block_count] // 2
    
    # 位置权重（靠近中心）
    total_score += (center - abs(center - x)) * (center - abs(center - y))
    
    return total_score

def ai_move():
    """AI下棋"""
    if st.session_state.game_over:
        return
    
    board = st.session_state.board
    size = st.session_state.board_size
    color = st.session_state.current_player
    
    # 第一步下在中心
    if not st.session_state.moves:
        center = size // 2
        make_move(center, center, color)
        return
    
    # 计算最佳位置
    best_score = -1
    best_pos = None
    
    for y in range(size):
        for x in range(size):
            if board[y][x] == EMPTY:
                score = calc_value(x, y, color)
                if score > best_score:
                    best_score = score
                    best_pos = (x, y)
    
    if best_pos:
        make_move(best_pos[0], best_pos[1], color)

def make_move(x, y, color):
    """落子"""
    st.session_state.board[y][x] = color
    st.session_state.moves.append({'x': x, 'y': y, 'color': color})

    # 检查胜负
    winner = check_winner(x, y, color)
    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
    else:
        # 切换玩家
        st.session_state.current_player = WHITE if color == BLACK else BLACK

def make_click_move(x, y):
    """点击格子落子"""
    if st.session_state.game_over:
        return

    # 检查是否是AI的回合
    ai_turn = False
    if st.session_state.game_mode == 1 and st.session_state.current_player == WHITE:
        ai_turn = True
    elif st.session_state.game_mode == 2 and st.session_state.current_player == BLACK:
        ai_turn = True

    if not ai_turn and st.session_state.board[y][x] == EMPTY:
        make_move(x, y, st.session_state.current_player)
        st.rerun()

def check_winner(x, y, color):
    """检查胜负"""
    board = st.session_state.board
    size = st.session_state.board_size
    
    for dx, dy in DIRECTIONS:
        count = 1
        
        # 正方向
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == color:
                    count += 1
                else:
                    break
            else:
                break
        
        # 反方向
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if 0 <= nx < size and 0 <= ny < size:
                if board[ny][nx] == color:
                    count += 1
                else:
                    break
            else:
                break
        
        if count >= 5:
            return color
    
    return None

def undo_move():
    """悔棋"""
    if st.session_state.game_mode == 0:
        # 双人模式撤销两步
        for _ in range(min(2, len(st.session_state.moves))):
            if st.session_state.moves:
                move = st.session_state.moves.pop()
                st.session_state.board[move['y']][move['x']] = EMPTY
        st.session_state.current_player = BLACK if len(st.session_state.moves) % 2 == 0 else WHITE
    else:
        # AI模式撤销一步
        if st.session_state.moves:
            move = st.session_state.moves.pop()
            st.session_state.board[move['y']][move['x']] = EMPTY
            st.session_state.current_player = BLACK
    
    st.session_state.game_over = False
    st.session_state.winner = None

def render_board():
    """渲染棋盘"""
    board = st.session_state.board
    size = st.session_state.board_size

    for y in range(size):
        row_cols = st.columns(size)
        for x in range(size):
            with row_cols[x]:
                cell_key = f'cell_{y}_{x}'

                if board[y][x] == BLACK:
                    st.markdown('<div class="board-cell" style="background-color: black; border-radius: 50%;"></div>', unsafe_allow_html=True)
                elif board[y][x] == WHITE:
                    st.markdown('<div class="board-cell" style="background-color: white; border: 2px solid #333; border-radius: 50%;"></div>', unsafe_allow_html=True)
                else:
                    # 空格子，点击可落子
                    if st.button('', key=cell_key, help=f'({x+1},{y+1})',
                               use_container_width=True):
                        make_click_move(x, y)

def main():
    st.title('⚫ 五子棋游戏')
    
    # 游戏模式选择 - 紧凑布局
    game_mode = st.radio('模式', ['人-人', '人-计', '计-人'], horizontal=True)
    if game_mode == '人-人':
        st.session_state.game_mode = 0
    elif game_mode == '人-计':
        st.session_state.game_mode = 1
    else:
        st.session_state.game_mode = 2
    
    # 信息栏
    col1, col2, col3 = st.columns(3)

    with col1:
        player_name = '黑方' if st.session_state.current_player == BLACK else '白方'
        st.metric('当前', player_name)

    with col2:
        st.metric('步数', len(st.session_state.moves))

    with col3:
        if st.session_state.game_over:
            winner_name = '黑方' if st.session_state.winner == BLACK else '白方'
            st.success(f'{winner_name}获胜!')
        elif len(st.session_state.moves) >= st.session_state.board_size * st.session_state.board_size:
            st.info('平局!')

    # 游戏结束通知
    if st.session_state.game_over:
        winner_name = '黑方' if st.session_state.winner == BLACK else '白方'
        st.toast(f'🎉 {winner_name}获胜！', icon='🏆')

    # 棋盘
    render_board()
    
    # 操作区域 - 紧凑布局
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        row = st.number_input('行', min_value=1, max_value=st.session_state.board_size, value=1, key='row_input')

    with col2:
        col_input = st.number_input('列', min_value=1, max_value=st.session_state.board_size, value=1, key='col_input')

    with col3:
        if st.button('落子', use_container_width=True):
            if not st.session_state.game_over:
                # 检查是否是AI的回合
                ai_turn = False
                if st.session_state.game_mode == 1 and st.session_state.current_player == WHITE:
                    ai_turn = True
                elif st.session_state.game_mode == 2 and st.session_state.current_player == BLACK:
                    ai_turn = True

                if not ai_turn:
                    x, y = col_input - 1, row - 1
                    if st.session_state.board[y][x] == EMPTY:
                        make_move(x, y, st.session_state.current_player)
                        st.rerun()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('悔棋', use_container_width=True):
            undo_move()
            st.rerun()

    with col2:
        if st.button('新游戏', use_container_width=True):
            reset_board()
            st.rerun()
    
    # 保存和读取
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('保存', use_container_width=True):
            DataManager.save_game(st.session_state.moves, st.session_state.board_size)
            st.success('游戏已保存!')
    
    with col2:
        if st.button('读取', use_container_width=True):
            board_size, moves = DataManager.load_game()
            if moves:
                st.session_state.board_size = board_size
                st.session_state.board = [[EMPTY for _ in range(board_size)] for _ in range(board_size)]
                st.session_state.moves = []
                for move in moves:
                    st.session_state.board[move['y']][move['x']] = move['color']
                    st.session_state.moves.append(move)
                    st.session_state.current_player = WHITE if move['color'] == BLACK else BLACK
                st.session_state.game_mode = 0  # 设置为对战模式
                st.session_state.game_over = False
                st.session_state.winner = None
                st.success('游戏已读取!')
                st.rerun()
            else:
                st.warning('没有存档!')
    
    # AI自动下棋
    if not st.session_state.game_over:
        if st.session_state.game_mode == 1 and st.session_state.current_player == WHITE:
            ai_move()
            st.rerun()
        elif st.session_state.game_mode == 2 and st.session_state.current_player == BLACK:
            ai_move()
            st.rerun()
    
    # 操作说明
    st.markdown('''
    <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 8px; margin-top: 10px;">
        <p style="margin: 0; color: white; text-align: center; font-size: 12px;">
            💡 <strong>操作方式:</strong> 点击棋盘格子直接落子，或使用行列号输入
        </p>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
