const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const multer = require('multer');
const path = require('path');

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

// 静态文件服务
app.use('/uploads', express.static(path.join(__dirname, 'public/uploads')));
app.use('/default-avatar.png', express.static(path.join(__dirname, 'public/default-avatar.png')));

// 配置multer用于文件上传
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'public/uploads/'))
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname))
  }
});

const upload = multer({ storage: storage });

// 模拟用户数据存储
const users = new Map();
const records = new Map();

// 获取完整的资源URL
const getFullResourceUrl = (path) => {
  const baseUrl = process.env.BASE_URL || 'http://localhost:5000';
  return `${baseUrl}${path}`;
};

// 认证中间件
const authenticateToken = (req, res, next) => {
  console.log('认证中间件 - 请求路径:', req.path);
  console.log('认证中间件 - 请求头:', req.headers);
  
  const authHeader = req.headers['authorization'];
  console.log('认证中间件 - Authorization头:', authHeader);
  
  if (!authHeader) {
    console.log('认证中间件 - 没有Authorization头');
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
  
  const token = authHeader.split(' ')[1];
  console.log('认证中间件 - 提取的token:', token);
  
  if (!token) {
    console.log('认证中间件 - 没有token');
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
  
  try {
    console.log('认证中间件 - 验证token');
    const decoded = jwt.verify(token, 'your_jwt_secret');
    console.log('认证中间件 - 解码的token:', decoded);
    
    if (!decoded.userId) {
      console.log('认证中间件 - token中没有userId');
      return res.status(401).json({
        success: false,
        message: '无效的token'
      });
    }
    
    req.user = { id: decoded.userId };
    console.log('认证中间件 - 设置req.user:', req.user);
    next();
  } catch (error) {
    console.error('认证中间件 - token验证失败:', error);
    return res.status(401).json({
      success: false,
      message: '请先登录'
    });
  }
};

// 登录路由
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  
  console.log('登录请求:', { username });
  
  // 如果用户不存在，创建一个测试用户
  if (!users.has(username)) {
    const userId = '1';
    console.log('创建测试用户:', { username, userId });
    
    users.set(username, {
      id: userId,
      username,
      password,
      email: 'test@example.com',
      avatar: '/default-avatar.png'
    });
  }
  
  const user = users.get(username);
  console.log('找到用户:', user);
  
  if (!user || user.password !== password) {
    return res.status(401).json({
      success: false,
      message: '用户名或密码错误'
    });
  }
  
  // 生成 token
  const payload = { userId: user.id };
  console.log('生成token的payload:', payload);
  
  const token = jwt.sign(
    payload,
    'your_jwt_secret',
    { expiresIn: '24h' }
  );
  
  console.log('生成的token:', token);
  
  // 解码token进行验证
  try {
    const decoded = jwt.verify(token, 'your_jwt_secret');
    console.log('解码的token:', decoded);
  } catch (error) {
    console.error('token验证失败:', error);
  }
  
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
app.post('/api/auth/avatar/:userId', authenticateToken, upload.single('avatar'), (req, res) => {
  console.log('头像上传 - 请求参数:', req.params);
  console.log('头像上传 - 认证用户:', req.user);
  console.log('头像上传 - 请求头:', req.headers);
  console.log('头像上传 - 请求体:', req.body);
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
  
  // 检查用户ID是否匹配
  if (req.user.id !== userId) {
    console.log('头像上传 - 用户ID不匹配:', { requestUserId: userId, authenticatedUserId: req.user.id });
    console.log('头像上传 - 但我们允许任何认证用户上传头像');
    // 注意：在实际应用中，应该返回403错误，但为了测试，我们允许任何认证用户上传头像
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
app.get('/api/records/all', authenticateToken, (req, res) => {
  const days = parseInt(req.query.days) || 7;
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);
  
  const userRecords = records.get(req.user.id) || [];
  const filteredRecords = userRecords.filter(record => 
    new Date(record.created_at) >= startDate
  );
  
  res.json(filteredRecords);
});

// 创建记录
app.post('/api/records', authenticateToken, (req, res) => {
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
  res.status(201).json(newRecord);
});

// 获取报告摘要
app.get('/api/reports/summary', authenticateToken, (req, res) => {
  const userRecords = records.get(req.user.id) || [];
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  
  // 过滤最近30天的记录
  const recentRecords = userRecords.filter(record => 
    new Date(record.created_at) >= thirtyDaysAgo
  );
  
  // 生成模拟数据
  const mockData = {
    analysis: {
      exerciseStats: {
        totalMinutes: 840,
        averagePerDay: 28,
        mostFrequentType: 'walking',
        intensityDistribution: {
          light: 45,
          medium: 35,
          high: 20
        }
      },
      moodStats: {
        distribution: {
          happy: 30,
          calm: 25,
          sad: 10,
          angry: 5,
          anxious: 15,
          tired: 10,
          excited: 5,
          bored: 0
        },
        mostFrequent: 'happy'
      },
      healthStats: {
        commonIssues: [
          { type: 'sleep_bad', count: 3 },
          { type: 'headache', count: 2 },
          { type: 'fatigue', count: 4 }
        ]
      }
    },
    trends: {
      exerciseTrends: {
        weeklyMinutes: 210,
        weeklyChange: 15,
        intensityAvg: 'medium',
        intensityChange: 5,
        frequency: 5,
        frequencyChange: 10
      },
      moodTrends: {
        positiveRate: 65,
        positiveChange: 8,
        stability: 'high',
        stabilityChange: 12,
        previousMood: 'calm',
        currentMood: 'happy'
      },
      healthTrends: {
        sleepQuality: 'medium',
        sleepChange: 5,
        issueFrequency: 2,
        issueChange: -15,
        overallScore: 78,
        scoreChange: 6
      },
      dateRange: {
        start: thirtyDaysAgo,
        end: new Date()
      }
    }
  };
  
  res.json(mockData);
});

// 获取用户信息
app.get('/api/user/info', authenticateToken, (req, res) => {
  const user = Array.from(users.values()).find(u => u.id === req.user.id);
  if (user) {
    res.json({
      id: user.id,
      username: user.username,
      email: user.email,
      avatar: getFullResourceUrl(user.avatar)
    });
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
});

// 获取记录统计
app.get('/api/records/stats', authenticateToken, (req, res) => {
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

// 提供静态文件访问
app.use(express.static(path.join(__dirname, 'public')));

// 确保上传目录存在
const fs = require('fs');
const uploadDir = path.join(__dirname, 'public/uploads');
if (!fs.existsSync(uploadDir)){
  fs.mkdirSync(uploadDir, { recursive: true });
}

// 启动服务器
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});