const mongoose = require('mongoose');

const RecordSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  type: {
    type: String,
    enum: ['exercise', 'mood', 'health', 'food'],
    required: true
  },
  // 运动记录字段
  exercise_type: {
    type: String,
    enum: ['walking', 'running', 'cycling', 'swimming', 'yoga', 'gym', 'basketball', 'football', 'other'],
    required: function() { return this.type === 'exercise'; }
  },
  duration: {
    type: Number,
    min: 0,
    required: function() { return this.type === 'exercise'; }
  },
  intensity: {
    type: String,
    enum: ['light', 'medium', 'high'],
    required: function() { return this.type === 'exercise'; }
  },
  // 心情记录字段
  mood_type: {
    type: String,
    enum: ['happy', 'calm', 'sad', 'angry', 'anxious', 'tired', 'excited', 'bored'],
    required: function() { return this.type === 'mood'; }
  },
  // 健康记录字段
  feeling: {
    type: String,
    enum: ['energetic', 'good', 'normal', 'tired'],
    required: function() { return this.type === 'health'; }
  },
  status: {
    type: [String],
    default: [],
    validate: {
      validator: function(v) {
        return this.type !== 'health' || v.length > 0;
      },
      message: '健康记录必须包含至少一个状态'
    }
  },
  // 食物记录字段
  food_name: {
    type: String,
    required: function() { return this.type === 'food'; }
  },
  meal_time: {
    type: String,
    enum: ['breakfast', 'lunch', 'dinner', 'snack'],
    required: function() { return this.type === 'food'; }
  },
  // 通用字段
  note: {
    type: String,
    default: ''
  },
  record_date: {
    type: Date,
    default: Date.now
  },
  created_at: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Record', RecordSchema); 