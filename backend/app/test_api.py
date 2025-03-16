"""
API测试脚本
用于测试Flask API的功能
"""

import requests
import json
from pprint import pprint

BASE_URL = 'http://localhost:5000/api'

def test_login():
    """测试登录API"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(url, json=data)
    print(f"登录状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("登录成功!")
        print(f"Token: {result.get('token')}")
        return result.get('token')
    else:
        print(f"登录失败: {response.text}")
        return None

def test_get_current_user(token):
    """测试获取当前用户API"""
    url = f"{BASE_URL}/auth/current_user"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"获取当前用户状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("获取当前用户成功!")
        pprint(result)
    else:
        print(f"获取当前用户失败: {response.text}")

def test_get_profile(token):
    """测试获取用户资料API"""
    url = f"{BASE_URL}/user/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"获取用户资料状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("获取用户资料成功!")
        pprint(result)
    else:
        print(f"获取用户资料失败: {response.text}")

def test_admin_dashboard(token):
    """测试管理员仪表板API"""
    url = f"{BASE_URL}/admin/dashboard"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"获取管理员仪表板状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("获取管理员仪表板成功!")
        pprint(result)
    else:
        print(f"获取管理员仪表板失败: {response.text}")

def test_create_record(token):
    """测试创建记录API"""
    url = f"{BASE_URL}/records/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 创建运动记录
    exercise_data = {
        "type": "exercise",
        "exercise_type": "跑步",
        "duration": 30,
        "intensity": 4,
        "note": "今天跑步感觉很好"
    }
    
    response = requests.post(url, json=exercise_data, headers=headers)
    print(f"创建运动记录状态码: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("创建运动记录成功!")
        pprint(result)
    else:
        print(f"创建运动记录失败: {response.text}")
    
    # 创建心情记录
    mood_data = {
        "type": "mood",
        "mood_type": "happy",
        "note": "今天心情很好"
    }
    
    response = requests.post(url, json=mood_data, headers=headers)
    print(f"创建心情记录状态码: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("创建心情记录成功!")
        pprint(result)
    else:
        print(f"创建心情记录失败: {response.text}")

def test_get_records(token):
    """测试获取记录API"""
    url = f"{BASE_URL}/records/all"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"获取所有记录状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("获取所有记录成功!")
        pprint(result)
    else:
        print(f"获取所有记录失败: {response.text}")

def test_generate_report(token):
    """测试生成报告API"""
    url = f"{BASE_URL}/reports/generate"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "type": "weekly"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"生成报告状态码: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("生成报告成功!")
        pprint(result)
        return result.get('id')
    else:
        print(f"生成报告失败: {response.text}")
        return None

def test_get_report(token, report_id):
    """测试获取报告API"""
    if not report_id:
        print("没有报告ID，跳过测试")
        return
    
    url = f"{BASE_URL}/reports/{report_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"获取报告状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("获取报告成功!")
        pprint(result)
    else:
        print(f"获取报告失败: {response.text}")

def run_tests():
    """运行所有测试"""
    print("开始测试API...")
    
    # 登录并获取token
    token = test_login()
    if not token:
        print("登录失败，无法继续测试")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 测试获取当前用户
    test_get_current_user(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试获取用户资料
    test_get_profile(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试管理员仪表板
    test_admin_dashboard(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试创建记录
    test_create_record(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试获取记录
    test_get_records(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试生成报告
    report_id = test_generate_report(token)
    
    print("\n" + "="*50 + "\n")
    
    # 测试获取报告
    test_get_report(token, report_id)
    
    print("\n" + "="*50 + "\n")
    print("API测试完成!")

if __name__ == "__main__":
    run_tests() 