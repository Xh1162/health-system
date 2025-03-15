const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Record = require('../models/Record');

// 获取所有记录
router.get('/all', auth, async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 7;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);
    
    const records = await Record.find({
      user: req.user.id,
      created_at: { $gte: startDate }
    }).sort({ created_at: -1 });
    
    res.json(records);
  } catch (error) {
    console.error('获取记录错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 获取特定类型的记录
router.get('/:type', auth, async (req, res) => {
  try {
    const { type } = req.params;
    const days = parseInt(req.query.days) || 7;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);
    
    const records = await Record.find({
      user: req.user.id,
      type,
      created_at: { $gte: startDate }
    }).sort({ created_at: -1 });
    
    res.json(records);
  } catch (error) {
    console.error('获取记录错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 创建记录
router.post('/', auth, async (req, res) => {
  try {
    const { type, ...recordData } = req.body;
    
    if (!type) {
      return res.status(400).json({ message: '记录类型不能为空' });
    }
    
    const newRecord = new Record({
      user: req.user.id,
      type,
      ...recordData
    });
    
    const record = await newRecord.save();
    res.json(record);
  } catch (error) {
    console.error('创建记录错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 更新记录
router.put('/:id', auth, async (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    // 确保用户只能更新自己的记录
    const record = await Record.findOne({ _id: id, user: req.user.id });
    
    if (!record) {
      return res.status(404).json({ message: '记录不存在或无权限' });
    }
    
    // 更新记录
    const updatedRecord = await Record.findByIdAndUpdate(
      id,
      { $set: updateData },
      { new: true }
    );
    
    res.json(updatedRecord);
  } catch (error) {
    console.error('更新记录错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

// 删除记录
router.delete('/:id', auth, async (req, res) => {
  try {
    const { id } = req.params;
    
    // 确保用户只能删除自己的记录
    const record = await Record.findOne({ _id: id, user: req.user.id });
    
    if (!record) {
      return res.status(404).json({ message: '记录不存在或无权限' });
    }
    
    await Record.findByIdAndDelete(id);
    res.json({ message: '记录已删除' });
  } catch (error) {
    console.error('删除记录错误:', error.message);
    res.status(500).json({ message: '服务器错误' });
  }
});

module.exports = router; 