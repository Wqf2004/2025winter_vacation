import os
import json

# 数据文件路径
DATA_DIR = "../dataset"
SAVE_FILE = os.path.join(DATA_DIR, "save.txt")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

class DataManager:
    @staticmethod
    def save_game(moves, board_size):
        """保存游戏"""
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            f.write(f"{board_size}\n")
            for move in moves:
                f.write(f"{move['x']} {move['y']} {move['color']}\n")
    
    @staticmethod
    def load_game():
        """读取游戏"""
        if not os.path.exists(SAVE_FILE):
            return None, []
        
        moves = []
        board_size = 15
        
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.isdigit():
                board_size = int(first_line)
            
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    moves.append({
                        'x': int(parts[0]),
                        'y': int(parts[1]),
                        'color': int(parts[2])
                    })
        
        return board_size, moves
    
    @staticmethod
    def has_save():
        """检查是否有存档"""
        return os.path.exists(SAVE_FILE)
