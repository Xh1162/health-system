const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();

// 中间件
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

// 处理预检请求
app.options('*', cors());

// 配置multer用于文件上传
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'public/uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname))
  }
});

const upload = multer({ storage: storage });

// 数据文件路径
const DATA_DIR = path.join(__dirname, 'data');
const USERS_FILE = path.join(DATA_DIR, 'users.json');
const RECORDS_FILE = path.join(DATA_DIR, 'records.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 从文件加载数据
function loadData() {
  try {
    // 加载用户数据
    let usersData = {};
    if (fs.existsSync(USERS_FILE)) {
      const usersJson = fs.readFileSync(USERS_FILE, 'utf8');
      usersData = JSON.parse(usersJson);
    }
    
    // 加载记录数据
    let recordsData = {};
    if (fs.existsSync(RECORDS_FILE)) {
      const recordsJson = fs.readFileSync(RECORDS_FILE, 'utf8');
      recordsData = JSON.parse(recordsJson);
    }
    
    return { usersData, recordsData };
  } catch (error) {
    console.error('加载数据失败:', error);
    return { usersData: {}, recordsData: {} };
  }
}

// 保存数据到文件
function saveData(usersData, recordsData) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(usersData, null, 2));
    fs.writeFileSync(RECORDS_FILE, JSON.stringify(recordsData, null, 2));
    console.log('数据已保存到文件');
  } catch (error) {
    console.error('保存数据失败:', error);
  }
}

// 将Map转换为对象
function mapToObject(map) {
  return Object.fromEntries(map);
}

// 将用户和记录数据保存到文件
function saveAllData() {
  const usersObj = mapToObject(users);
  const recordsObj = mapToObject(records);
  saveData(usersObj, recordsObj);
}

// 加载初始数据
const { usersData, recordsData } = loadData();

// 模拟用户数据存储
const users = new Map(Object.entries(usersData));
const records = new Map(Object.entries(recordsData));

// 定期保存数据（每5分钟）
setInterval(() => {
  saveAllData();
  console.log('数据已自动保存');
}, 5 * 60 * 1000);

// 在服务器关闭时保存数据
process.on('SIGINT', () => {
  saveAllData();
  console.log('数据已保存，服务器关闭');
  process.exit(0);
});

// 获取完整的资源URL
const getFullResourceUrl = (path) => {
  const baseUrl = process.env.BASE_URL || 'http://localhost:5000';
  return `${baseUrl}${path}`;
};

// 验证token中间件
const authMiddleware = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ message: '未提供认证令牌' });
  }
  
  try {
    const decoded = jwt.verify(token, 'your_jwt_secret');
    req.user = { id: decoded.userId };
    next();
  } catch (error) {
    res.status(401).json({ message: '无效的令牌' });
  }
};

// 登录路由
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  
  console.log('登录请求:', { username });
  
  // 如果用户不存在，创建一个测试用户
  if (!users.has(username)) {
    users.set(username, {
      id: '1',
      username,
      password,
      email: 'test@example.com',
      avatar: '/default-avatar.png'
    });
    
    // 保存用户数据
    saveAllData();
  }
  
  const user = users.get(username);
  
  if (!user || user.password !== password) {
    return res.status(401).json({
      success: false,
      message: '用户名或密码错误'
    });
  }
  
  // 生成 token
  const token = jwt.sign(
    { userId: user.id },
    'your_jwt_secret',
    { expiresIn: '24h' }
  );
  
  res.json({
    success: true,
    data: {
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        avatar: getFullResourceUrl(user.avatar)
      }
    }
  });
});

// 注册路由
app.post('/api/auth/register', (req, res) => {
  const { username, email, password } = req.body;
  
  console.log('注册请求:', { username, email });
  
  if (users.has(username)) {
    return res.status(400).json({
      success: false,
      message: '用户名已被使用'
    });
  }
  
  const user = {
    id: Date.now().toString(),
    username,
    email,
    password,
    avatar: '/default-avatar.png'
  };
  
  users.set(username, user);
  
  // 保存用户数据
  saveAllData();
  
  // 生成 token
  const token = jwt.sign(
    { userId: user.id },
    'your_jwt_secret',
    { expiresIn: '24h' }
  );
  
  res.status(201).json({
    success: true,
    data: {
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        avatar: getFullResourceUrl(user.avatar)
      }
    }
  });
});

// 头像上传路由
app.post('/api/auth/avatar/:userId', (req, res, next) => {
  console.log('头像上传 - 请求开始处理');
  console.log('头像上传 - 请求路径:', req.path);
  console.log('头像上传 - 请求方法:', req.method);
  console.log('头像上传 - 请求头:', req.headers);
  console.log('头像上传 - 请求参数:', req.params);
  
  // 提取token
  const authHeader = req.headers['authorization'];
  console.log('头像上传 - Authorization头:', authHeader);
  
  if (!authHeader) {
    console.log('头像上传 - 没有Authorization头');
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
  
  const token = authHeader.split(' ')[1];
  console.log('头像上传 - 提取的token:', token);
  
  if (!token) {
    console.log('头像上传 - 没有token');
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
  
  try {
    console.log('头像上传 - 验证token');
    const decoded = jwt.verify(token, 'your_jwt_secret');
    console.log('头像上传 - 解码的token:', decoded);
    
    if (!decoded.userId) {
      console.log('头像上传 - token中没有userId');
      return res.status(401).json({
        success: false,
        message: '无效的token'
      });
    }
    
    req.user = { id: decoded.userId };
    console.log('头像上传 - 设置req.user:', req.user);
    next();
  } catch (error) {
    console.error('头像上传 - token验证失败:', error);
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
}, upload.single('avatar'), (req, res) => {
  console.log('头像上传 - 文件处理开始');
  console.log('头像上传 - 请求参数:', req.params);
  console.log('头像上传 - 认证用户:', req.user);
  console.log('头像上传 - 上传文件:', req.file);
  
  const { userId } = req.params;
  console.log('头像上传 - 查找用户ID:', userId);
  
  // 检查是否有文件上传
  if (!req.file) {
    console.log('头像上传 - 没有文件上传');
    return res.status(400).json({
      success: false,
      message: '没有文件上传'
    });
  }
  
  // 查找用户
  let foundUser = null;
  console.log('头像上传 - 用户列表:', Array.from(users.entries()));
  
  for (const [username, user] of users.entries()) {
    console.log(`检查用户 ${username}:`, user);
    if (user.id === userId) {
      foundUser = user;
      break;
    }
  }
  
  if (foundUser) {
    console.log('头像上传 - 找到用户:', foundUser);
    
    // 设置头像路径
    const avatarPath = `/uploads/${req.file.filename}`;
    foundUser.avatar = avatarPath;
    
    // 保存用户数据
    saveAllData();
    
    console.log('头像上传 - 更新后的用户:', foundUser);
    console.log('头像上传 - 头像完整URL:', getFullResourceUrl(avatarPath));
    
    res.json({
      success: true,
      data: {
        avatar: getFullResourceUrl(avatarPath)
      }
    });
  } else {
    console.log('头像上传 - 未找到用户');
    res.status(404).json({
      success: false,
      message: '用户不存在'
    });
  }
});

// 获取所有记录
app.get('/api/records/all', authMiddleware, (req, res) => {
  const days = parseInt(req.query.days) || 30;  // 默认返回30天的记录
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);
  
  const userRecords = records.get(req.user.id) || [];
  const filteredRecords = userRecords.filter(record => 
    new Date(record.created_at) >= startDate
  );
  
  res.json(filteredRecords);
});

// 创建记录
app.post('/api/records', authMiddleware, (req, res) => {
  const { type, ...recordData } = req.body;
  
  if (!type) {
    return res.status(400).json({ message: '记录类型不能为空' });
  }
  
  const newRecord = {
    id: Date.now().toString(),
    user: req.user.id,
    type,
    ...recordData,
    created_at: new Date()
  };
  
  if (!records.has(req.user.id)) {
    records.set(req.user.id, []);
  }
  
  records.get(req.user.id).push(newRecord);
  
  // 保存记录数据
  saveAllData();
  
  res.status(201).json(newRecord);
});

// 获取报告摘要
app.get('/api/reports/summary', authMiddleware, (req, res) => {
  const userRecords = records.get(req.user.id) || [];
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  
  // 过滤最近30天的记录
  const recentRecords = userRecords.filter(record => 
    new Date(record.created_at) >= thirtyDaysAgo
  );
  
  // 计算运动统计数据
  const exerciseRecords = recentRecords.filter(record => record.type === 'exercise');
  const totalExerciseMinutes = exerciseRecords.reduce((sum, record) => sum + (parseInt(record.duration) || 0), 0);
  
  // 计算运动类型分布
  const exerciseTypes = {};
  exerciseRecords.forEach(record => {
    const type = record.exercise_type || 'other';
    exerciseTypes[type] = (exerciseTypes[type] || 0) + 1;
  });
  
  // 找出最常见的运动类型
  let mostFrequentType = 'walking';
  let maxCount = 0;
  for (const [type, count] of Object.entries(exerciseTypes)) {
    if (count > maxCount) {
      maxCount = count;
      mostFrequentType = type;
    }
  }
  
  // 计算强度分布
  const intensityDistribution = {
    light: 0,
    medium: 0,
    high: 0
  };
  
  exerciseRecords.forEach(record => {
    const intensity = record.intensity || 'medium';
    if (intensityDistribution[intensity] !== undefined) {
      intensityDistribution[intensity]++;
    }
  });
  
  // 计算强度百分比
  const totalIntensityCount = Object.values(intensityDistribution).reduce((sum, count) => sum + count, 0);
  if (totalIntensityCount > 0) {
    for (const intensity in intensityDistribution) {
      intensityDistribution[intensity] = Math.round((intensityDistribution[intensity] / totalIntensityCount) * 100);
    }
  }
  
  // 计算心情统计数据
  const moodRecords = recentRecords.filter(record => record.type === 'mood');
  
  // 计算心情分布
  const moodDistribution = {
    happy: 0,
    calm: 0,
    sad: 0,
    angry: 0,
    anxious: 0,
    tired: 0,
    excited: 0,
    bored: 0
  };
  
  moodRecords.forEach(record => {
    const mood = record.mood_type || 'calm';
    if (moodDistribution[mood] !== undefined) {
      moodDistribution[mood]++;
    }
  });
  
  // 计算心情百分比
  const totalMoodCount = Object.values(moodDistribution).reduce((sum, count) => sum + count, 0);
  if (totalMoodCount > 0) {
    for (const mood in moodDistribution) {
      moodDistribution[mood] = Math.round((moodDistribution[mood] / totalMoodCount) * 100);
    }
  }
  
  // 找出最常见的心情
  let mostFrequentMood = 'calm';
  maxCount = 0;
  for (const [mood, count] of Object.entries(moodDistribution)) {
    if (count > maxCount) {
      maxCount = count;
      mostFrequentMood = mood;
    }
  }
  
  // 计算健康统计数据
  const healthRecords = recentRecords.filter(record => record.type === 'health');
  
  // 计算常见健康问题
  const healthIssues = {};
  healthRecords.forEach(record => {
    if (Array.isArray(record.status)) {
      record.status.forEach(status => {
        healthIssues[status] = (healthIssues[status] || 0) + 1;
      });
    }
  });
  
  // 转换为数组格式
  const commonIssues = Object.entries(healthIssues)
    .map(([type, count]) => ({ type, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 3);
  
  // 计算趋势数据
  const twoWeeksAgo = new Date();
  twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  
  const currentWeekRecords = recentRecords.filter(record => 
    new Date(record.created_at) >= oneWeekAgo
  );
  
  const previousWeekRecords = recentRecords.filter(record => 
    new Date(record.created_at) >= twoWeeksAgo && 
    new Date(record.created_at) < oneWeekAgo
  );
  
  // 计算运动趋势
  const currentWeekExercises = currentWeekRecords.filter(record => record.type === 'exercise');
  const previousWeekExercises = previousWeekRecords.filter(record => record.type === 'exercise');
  
  const currentWeekMinutes = currentWeekExercises.reduce((sum, record) => sum + (parseInt(record.duration) || 0), 0);
  const previousWeekMinutes = previousWeekExercises.reduce((sum, record) => sum + (parseInt(record.duration) || 0), 0);
  
  const weeklyChange = previousWeekMinutes > 0 
    ? Math.round(((currentWeekMinutes - previousWeekMinutes) / previousWeekMinutes) * 100) 
    : 0;
  
  // 计算心情趋势
  const currentWeekMoods = currentWeekRecords.filter(record => record.type === 'mood');
  const previousWeekMoods = previousWeekRecords.filter(record => record.type === 'mood');
  
  // 计算积极情绪比例
  const positiveTypes = ['happy', 'calm', 'excited'];
  
  const currentPositiveCount = currentWeekMoods.filter(record => 
    positiveTypes.includes(record.mood_type)
  ).length;
  
  const previousPositiveCount = previousWeekMoods.filter(record => 
    positiveTypes.includes(record.mood_type)
  ).length;
  
  const currentPositiveRate = currentWeekMoods.length > 0 
    ? Math.round((currentPositiveCount / currentWeekMoods.length) * 100) 
    : 0;
  
  const previousPositiveRate = previousWeekMoods.length > 0 
    ? Math.round((previousPositiveCount / previousWeekMoods.length) * 100) 
    : 0;
  
  const positiveChange = previousPositiveRate > 0 
    ? currentPositiveRate - previousPositiveRate 
    : 0;
  
  // 获取当前和之前的主要心情
  let currentMood = 'calm';
  let previousMood = 'calm';
  
  if (currentWeekMoods.length > 0) {
    const moodCounts = {};
    currentWeekMoods.forEach(record => {
      moodCounts[record.mood_type] = (moodCounts[record.mood_type] || 0) + 1;
    });
    
    let maxCount = 0;
    for (const [mood, count] of Object.entries(moodCounts)) {
      if (count > maxCount) {
        maxCount = count;
        currentMood = mood;
      }
    }
  }
  
  if (previousWeekMoods.length > 0) {
    const moodCounts = {};
    previousWeekMoods.forEach(record => {
      moodCounts[record.mood_type] = (moodCounts[record.mood_type] || 0) + 1;
    });
    
    let maxCount = 0;
    for (const [mood, count] of Object.entries(moodCounts)) {
      if (count > maxCount) {
        maxCount = count;
        previousMood = mood;
      }
    }
  }
  
  // 计算健康趋势
  const currentWeekHealth = currentWeekRecords.filter(record => record.type === 'health');
  const previousWeekHealth = previousWeekRecords.filter(record => record.type === 'health');
  
  // 计算睡眠质量
  const goodSleepStatus = 'sleep_well';
  const badSleepStatus = 'sleep_bad';
  
  const currentGoodSleep = currentWeekHealth.filter(record => 
    Array.isArray(record.status) && record.status.includes(goodSleepStatus)
  ).length;
  
  const currentBadSleep = currentWeekHealth.filter(record => 
    Array.isArray(record.status) && record.status.includes(badSleepStatus)
  ).length;
  
  const previousGoodSleep = previousWeekHealth.filter(record => 
    Array.isArray(record.status) && record.status.includes(goodSleepStatus)
  ).length;
  
  const previousBadSleep = previousWeekHealth.filter(record => 
    Array.isArray(record.status) && record.status.includes(badSleepStatus)
  ).length;
  
  // 计算睡眠质量评分 (0-100)
  const currentSleepScore = currentWeekHealth.length > 0 
    ? Math.round((currentGoodSleep / (currentGoodSleep + currentBadSleep || 1)) * 100) 
    : 50;
  
  const previousSleepScore = previousWeekHealth.length > 0 
    ? Math.round((previousGoodSleep / (previousGoodSleep + previousBadSleep || 1)) * 100) 
    : 50;
  
  const sleepChange = previousSleepScore > 0 
    ? currentSleepScore - previousSleepScore 
    : 0;
  
  // 睡眠质量描述
  let sleepQuality = 'medium';
  if (currentSleepScore >= 70) {
    sleepQuality = 'good';
  } else if (currentSleepScore <= 30) {
    sleepQuality = 'bad';
  }
  
  // 计算健康问题频率
  const currentIssueCount = currentWeekHealth.reduce((sum, record) => 
    sum + (Array.isArray(record.status) ? record.status.length : 0), 0
  );
  
  const previousIssueCount = previousWeekHealth.reduce((sum, record) => 
    sum + (Array.isArray(record.status) ? record.status.length : 0), 0
  );
  
  const currentIssueFreq = currentWeekHealth.length > 0 
    ? Math.round(currentIssueCount / currentWeekHealth.length) 
    : 0;
  
  const previousIssueFreq = previousWeekHealth.length > 0 
    ? Math.round(previousIssueCount / previousWeekHealth.length) 
    : 0;
  
  const issueChange = previousIssueFreq > 0 
    ? Math.round(((currentIssueFreq - previousIssueFreq) / previousIssueFreq) * 100) 
    : 0;
  
  // 计算总体健康评分
  const overallScore = Math.round(
    (currentSleepScore * 0.4) + 
    (currentPositiveRate * 0.3) + 
    (Math.max(0, 100 - currentIssueFreq * 10) * 0.3)
  );
  
  const previousOverallScore = Math.round(
    (previousSleepScore * 0.4) + 
    (previousPositiveRate * 0.3) + 
    (Math.max(0, 100 - previousIssueFreq * 10) * 0.3)
  );
  
  const scoreChange = previousOverallScore > 0 
    ? overallScore - previousOverallScore 
    : 0;
  
  // 构建报告数据
  const reportData = {
    analysis: {
      exerciseStats: {
        totalMinutes: totalExerciseMinutes,
        averagePerDay: Math.round(totalExerciseMinutes / 30),
        mostFrequentType: mostFrequentType,
        intensityDistribution: intensityDistribution
      },
      moodStats: {
        distribution: moodDistribution,
        mostFrequent: mostFrequentMood
      },
      healthStats: {
        commonIssues: commonIssues
      }
    },
    trends: {
      exerciseTrends: {
        weeklyMinutes: currentWeekMinutes,
        weeklyChange: weeklyChange,
        intensityAvg: 'medium',
        intensityChange: 0,
        frequency: currentWeekExercises.length,
        frequencyChange: previousWeekExercises.length > 0 
          ? Math.round(((currentWeekExercises.length - previousWeekExercises.length) / previousWeekExercises.length) * 100) 
          : 0
      },
      moodTrends: {
        positiveRate: currentPositiveRate,
        positiveChange: positiveChange,
        stability: currentPositiveRate > 70 ? 'high' : (currentPositiveRate > 40 ? 'medium' : 'low'),
        stabilityChange: positiveChange,
        previousMood: previousMood,
        currentMood: currentMood
      },
      healthTrends: {
        sleepQuality: sleepQuality,
        sleepChange: sleepChange,
        issueFrequency: currentIssueFreq,
        issueChange: issueChange,
        overallScore: overallScore,
        scoreChange: scoreChange
      },
      dateRange: {
        start: thirtyDaysAgo,
        end: new Date()
      }
    },
    summary: {
      totalRecords: recentRecords.length,
      foodRecords: recentRecords.filter(record => record.type === 'food').length,
      exerciseRecords: exerciseRecords.length,
      moodRecords: moodRecords.length,
      exerciseMinutes: totalExerciseMinutes,
      sleepQuality: {
        good: healthRecords.filter(record => 
          Array.isArray(record.status) && record.status.includes('sleep_well')
        ).length,
        bad: healthRecords.filter(record => 
          Array.isArray(record.status) && record.status.includes('sleep_bad')
        ).length
      },
      recentMoods: moodRecords
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5)
        .map(record => ({
          type: record.mood_type,
          date: record.created_at
        }))
    }
  };
  
  res.json(reportData);
});

// 获取用户信息
app.get('/api/user/info', authMiddleware, (req, res) => {
  // 遍历所有用户，查找匹配ID的用户
  let foundUser = null;
  for (const [username, user] of users.entries()) {
    if (user.id === req.user.id) {
      foundUser = user;
      break;
    }
  }
  
  if (foundUser) {
    res.json({
      id: foundUser.id,
      username: foundUser.username,
      email: foundUser.email,
      avatar: getFullResourceUrl(foundUser.avatar),
      created_at: new Date(),
      email_verified: false,
      phone_verified: false
    });
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
});

// 获取记录统计
app.get('/api/records/stats', authMiddleware, (req, res) => {
  const days = parseInt(req.query.days) || 30;
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);
  
  const userRecords = records.get(req.user.id) || [];
  const recentRecords = userRecords.filter(record => 
    new Date(record.created_at) >= startDate
  );
  
  // 计算统计数据
  const stats = {
    total: recentRecords.length,
    byType: {
      exercise: recentRecords.filter(r => r.type === 'exercise').length,
      mood: recentRecords.filter(r => r.type === 'mood').length,
      health: recentRecords.filter(r => r.type === 'health').length,
      food: recentRecords.filter(r => r.type === 'food').length
    },
    lastRecord: recentRecords[0] || null,
    periodStart: startDate,
    periodEnd: new Date()
  };
  
  res.json(stats);
});

// 删除记录
app.delete('/api/records/:id', authMiddleware, (req, res) => {
  const { id } = req.params;
  const userRecords = records.get(req.user.id) || [];
  
  // 查找记录索引
  const recordIndex = userRecords.findIndex(record => record.id === id);
  
  if (recordIndex === -1) {
    return res.status(404).json({ message: '记录不存在或无权限删除' });
  }
  
  // 删除记录
  userRecords.splice(recordIndex, 1);
  
  // 保存记录数据
  saveAllData();
  
  res.json({ success: true, message: '记录已删除' });
});

// 获取个性化健康建议
app.get('/api/recommendations', authMiddleware, (req, res) => {
  const userRecords = records.get(req.user.id) || [];
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  
  // 过滤最近30天的记录
  const recentRecords = userRecords.filter(record => 
    new Date(record.created_at) >= thirtyDaysAgo
  );
  
  // 获取当前季节
  const currentDate = new Date();
  const month = currentDate.getMonth();
  let season = '';
  
  if (month >= 2 && month <= 4) {
    season = 'spring'; // 春季 (3-5月)
  } else if (month >= 5 && month <= 7) {
    season = 'summer'; // 夏季 (6-8月)
  } else if (month >= 8 && month <= 10) {
    season = 'autumn'; // 秋季 (9-11月)
  } else {
    season = 'winter'; // 冬季 (12-2月)
  }
  
  // 分析用户健康状况
  const healthRecords = recentRecords.filter(record => record.type === 'health');
  const moodRecords = recentRecords.filter(record => record.type === 'mood');
  const exerciseRecords = recentRecords.filter(record => record.type === 'exercise');
  
  // 分析睡眠质量
  const goodSleepCount = healthRecords.filter(record => 
    Array.isArray(record.status) && record.status.includes('sleep_well')
  ).length;
  
  const badSleepCount = healthRecords.filter(record => 
    Array.isArray(record.status) && record.status.includes('sleep_bad')
  ).length;
  
  const sleepQuality = goodSleepCount > badSleepCount ? 'good' : 
                       badSleepCount > goodSleepCount ? 'bad' : 'normal';
  
  // 分析常见健康问题
  const healthIssues = {};
  healthRecords.forEach(record => {
    if (Array.isArray(record.status)) {
      record.status.forEach(status => {
        healthIssues[status] = (healthIssues[status] || 0) + 1;
      });
    }
  });
  
  // 转换为数组格式并排序
  const commonIssues = Object.entries(healthIssues)
    .map(([type, count]) => ({ type, count }))
    .sort((a, b) => b.count - a.count);
  
  // 分析心情
  const positiveTypes = ['happy', 'calm', 'excited'];
  const negativeTypes = ['sad', 'angry', 'anxious', 'tired', 'bored'];
  
  const positiveCount = moodRecords.filter(record => 
    positiveTypes.includes(record.mood_type)
  ).length;
  
  const negativeCount = moodRecords.filter(record => 
    negativeTypes.includes(record.mood_type)
  ).length;
  
  const moodStatus = positiveCount > negativeCount ? 'positive' : 
                    negativeCount > positiveCount ? 'negative' : 'neutral';
  
  // 分析运动情况
  const totalExerciseMinutes = exerciseRecords.reduce((sum, record) => 
    sum + (parseInt(record.duration) || 0), 0
  );
  
  const avgExerciseMinutesPerDay = exerciseRecords.length > 0 
    ? Math.round(totalExerciseMinutes / 30) 
    : 0;
  
  const exerciseFrequency = exerciseRecords.length / 30; // 每天平均运动次数
  
  const exerciseLevel = exerciseFrequency >= 0.7 ? 'high' : 
                       exerciseFrequency >= 0.3 ? 'medium' : 'low';
  
  // 根据分析结果生成食物推荐
  const foodRecommendations = [];
  
  // 季节性食物推荐
  const seasonalFoods = {
    spring: [
      { name: '芦笋', benefits: '富含维生素K和叶酸，有助于排毒和抗炎' },
      { name: '菠菜', benefits: '富含铁质和抗氧化剂，增强免疫力' },
      { name: '草莓', benefits: '富含维生素C和抗氧化剂，促进心脏健康' }
    ],
    summer: [
      { name: '西瓜', benefits: '水分充足，有助于保持水分平衡和降温' },
      { name: '黄瓜', benefits: '低热量，富含水分，有助于消暑和排毒' },
      { name: '番茄', benefits: '富含番茄红素，保护皮肤免受紫外线伤害' }
    ],
    autumn: [
      { name: '南瓜', benefits: '富含维生素A和抗氧化剂，增强免疫力' },
      { name: '苹果', benefits: '富含膳食纤维和抗氧化剂，促进消化健康' },
      { name: '红薯', benefits: '富含复合碳水化合物和β-胡萝卜素，稳定血糖' }
    ],
    winter: [
      { name: '柑橘', benefits: '富含维生素C，增强免疫力' },
      { name: '白萝卜', benefits: '有助于消化和预防感冒' },
      { name: '羽衣甘蓝', benefits: '富含维生素K、A和C，抗炎和抗氧化' }
    ]
  };
  
  // 添加季节性食物推荐
  foodRecommendations.push(...seasonalFoods[season]);
  
  // 根据健康状况添加特定食物推荐
  if (sleepQuality === 'bad') {
    foodRecommendations.push(
      { name: '樱桃', benefits: '含有天然褪黑素，有助于改善睡眠' },
      { name: '香蕉', benefits: '富含镁和色氨酸，促进放松和睡眠' }
    );
  }
  
  if (commonIssues.some(issue => issue.type === 'fatigue')) {
    foodRecommendations.push(
      { name: '菠菜', benefits: '富含铁质，有助于缓解疲劳' },
      { name: '三文鱼', benefits: '富含omega-3脂肪酸和B族维生素，增强能量' }
    );
  }
  
  if (moodStatus === 'negative') {
    foodRecommendations.push(
      { name: '深色巧克力', benefits: '含有多酚和镁，有助于提升心情' },
      { name: '蓝莓', benefits: '富含抗氧化剂，有助于减轻压力和焦虑' }
    );
  }
  
  // 根据分析结果生成运动推荐
  const exerciseRecommendations = [];
  
  // 季节性运动推荐
  const seasonalExercises = {
    spring: [
      { name: '户外散步', benefits: '享受春季温和气候，增加维生素D摄入' },
      { name: '骑自行车', benefits: '提高心肺功能，欣赏春季风景' }
    ],
    summer: [
      { name: '游泳', benefits: '全身运动，避免高温天气下过度出汗' },
      { name: '晨练或傍晚锻炼', benefits: '避开高温时段，减少中暑风险' }
    ],
    autumn: [
      { name: '徒步旅行', benefits: '欣赏秋季风景，增强心肺功能' },
      { name: '瑜伽', benefits: '增强身体柔韧性，为冬季做准备' }
    ],
    winter: [
      { name: '室内健身', benefits: '避免寒冷天气，保持运动习惯' },
      { name: '太极拳', benefits: '温和运动，增强平衡感和身体协调性' }
    ]
  };
  
  // 添加季节性运动推荐
  exerciseRecommendations.push(...seasonalExercises[season]);
  
  // 根据健康状况添加特定运动推荐
  if (sleepQuality === 'bad') {
    exerciseRecommendations.push(
      { name: '瑜伽', benefits: '放松身心，改善睡眠质量' },
      { name: '温和有氧运动', benefits: '如散步，有助于调节生物钟' }
    );
  }
  
  if (exerciseLevel === 'low') {
    exerciseRecommendations.push(
      { name: '每日快走', benefits: '低强度开始，逐渐建立运动习惯' },
      { name: '伸展运动', benefits: '增加柔韧性，为更高强度运动做准备' }
    );
  } else if (exerciseLevel === 'high') {
    exerciseRecommendations.push(
      { name: '间歇训练', benefits: '提高运动效率，节省时间' },
      { name: '力量训练', benefits: '增强肌肉，提高基础代谢率' }
    );
  }
  
  if (moodStatus === 'negative') {
    exerciseRecommendations.push(
      { name: '有氧舞蹈', benefits: '释放内啡肽，提升心情' },
      { name: '团体运动', benefits: '增加社交互动，减轻孤独感' }
    );
  }
  
  // 生成健康生活方式建议
  const lifestyleRecommendations = [];
  
  // 基础建议
  lifestyleRecommendations.push(
    { title: '保持规律作息', description: '每天固定时间睡觉和起床，有助于调节生物钟' },
    { title: '多喝水', description: '每天至少饮用2升水，保持身体水分平衡' },
    { title: '减少屏幕时间', description: '睡前一小时避免使用电子设备，改善睡眠质量' }
  );
  
  // 根据健康状况添加特定生活方式建议
  if (sleepQuality === 'bad') {
    lifestyleRecommendations.push(
      { title: '睡前放松', description: '睡前进行深呼吸或冥想，帮助身心放松' },
      { title: '优化睡眠环境', description: '保持卧室安静、黑暗和凉爽，提高睡眠质量' }
    );
  }
  
  if (commonIssues.some(issue => issue.type === 'fatigue')) {
    lifestyleRecommendations.push(
      { title: '合理安排休息', description: '工作45-50分钟后休息5-10分钟，避免过度疲劳' },
      { title: '补充维生素B族', description: '考虑适当补充B族维生素，增强能量代谢' }
    );
  }
  
  if (moodStatus === 'negative') {
    lifestyleRecommendations.push(
      { title: '阳光暴露', description: '每天至少接触15-30分钟阳光，增加维生素D合成' },
      { title: '社交活动', description: '定期参与社交活动，增强社会联系' }
    );
  }
  
  // 构建推荐数据
  const recommendations = {
    season,
    healthSummary: {
      sleepQuality,
      commonIssues: commonIssues.slice(0, 3),
      moodStatus,
      exerciseLevel
    },
    recommendations: {
      food: foodRecommendations,
      exercise: exerciseRecommendations,
      lifestyle: lifestyleRecommendations
    }
  };
  
  res.json(recommendations);
});

// 提供静态文件访问
app.use(express.static('public'));

// 确保上传目录存在
const uploadsDir = path.join(__dirname, 'public/uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// 静态文件服务
app.use('/uploads', express.static(path.join(__dirname, 'public/uploads')));
app.use('/default-avatar.png', express.static(path.join(__dirname, 'public/default-avatar.png')));

// 启动服务器
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
}); 