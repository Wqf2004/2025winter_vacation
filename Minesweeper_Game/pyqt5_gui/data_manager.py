import os
import json

# 数据文件路径
DATA_DIR = "../dataset"
USER_FILE = os.path.join(DATA_DIR, "user.txt")
RANK_FILE = os.path.join(DATA_DIR, "rank.txt")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

class DataManager:
    @staticmethod
    def load_users():
        """加载用户数据"""
        users = []
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 3:
                            users.append({
                                'name': parts[0],
                                'pass': parts[1],
                                'best_time': int(parts[2]) if len(parts) > 2 else -1
                            })
        return users
    
    @staticmethod
    def save_users(users):
        """保存用户数据"""
        with open(USER_FILE, 'w', encoding='utf-8') as f:
            for user in users:
                f.write(f"{user['name']} {user['pass']} {user.get('best_time', -1)}\n")
    
    @staticmethod
    def register_user(name, password):
        """注册新用户"""
        users = DataManager.load_users()
        
        # 检查用户名是否存在
        for user in users:
            if user['name'] == name:
                return False, "用户名已存在"
        
        users.append({
            'name': name,
            'pass': password,
            'best_time': -1
        })
        
        DataManager.save_users(users)
        return True, "注册成功"
    
    @staticmethod
    def login_user(name, password):
        """用户登录"""
        users = DataManager.load_users()
        
        for user in users:
            if user['name'] == name and user['pass'] == password:
                return True, user
        
        return False, None
    
    @staticmethod
    def update_best_time(name, time_used):
        """更新用户最佳成绩"""
        users = DataManager.load_users()
        
        for user in users:
            if user['name'] == name:
                if user.get('best_time', -1) == -1 or time_used < user.get('best_time', -1):
                    user['best_time'] = time_used
        
        DataManager.save_users(users)
    
    @staticmethod
    def save_score(name, time_used):
        """保存游戏成绩"""
        with open(RANK_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{name} {time_used}\n")
    
    @staticmethod
    def load_rankings():
        """加载排行榜"""
        rankings = []
        if os.path.exists(RANK_FILE):
            with open(RANK_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            rankings.append({
                                'name': parts[0],
                                'time': int(parts[1])
                            })
        
        # 按时间排序
        rankings.sort(key=lambda x: x['time'])
        return rankings[:10]  # 返回前10名
