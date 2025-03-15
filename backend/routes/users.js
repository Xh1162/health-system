const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const User = require('../models/User');

// 获取用户信息
router.get('/profile', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.id).select('-password');
    res.json(user);
  } catch (error) {
    console.error('获取用户信息错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 更新用户信息
router.put('/profile', auth, async (req, res) => {
  try {
    const { username, email, profile } = req.body;
    
    // 构建更新对象
    const updateFields = {};
    if (username) updateFields.username = username;
    if (email) updateFields.email = email;
    if (profile) updateFields.profile = profile;
    
    // 更新用户信息
    const user = await User.findByIdAndUpdate(
      req.user.id,
      { $set: updateFields },
      { new: true }
    ).select('-password');
    
    res.json(user);
  } catch (error) {
    console.error('更新用户信息错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 更新用户头像
router.put('/avatar', auth, async (req, res) => {
  try {
    const { avatar } = req.body;
    
    if (!avatar) {
      return res.status(400).json({ message: '头像 URL 不能为空' });
    }
    
    // 更新用户头像
    const user = await User.findByIdAndUpdate(
      req.user.id,
      { $set: { avatar } },
      { new: true }
    ).select('-password');
    
    res.json(user);
  } catch (error) {
    console.error('更新用户头像错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

module.exports = router; 