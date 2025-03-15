const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Record = require('../models/Record');

// 获取用户健康数据概览
router.get('/overview', auth, async (req, res) => {
  try {
    const userId = req.user.id;
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    // 获取最近30天的所有记录
    const records = await Record.find({
      user: userId,
      created_at: { $gte: thirtyDaysAgo }
    }).sort({ created_at: -1 });

    // 计算健康数据概览
    const overview = calculateHealthOverview(records);

    res.json({
      success: true,
      data: overview
    });
  } catch (error) {
    console.error('获取健康数据概览失败:', error);
    res.status(500).json({
      success: false,
      message: '获取健康数据概览失败'
    });
  }
});

// 获取用户健康趋势数据
router.get('/trends', auth, async (req, res) => {
  try {
    const userId = req.user.id;
    const days = parseInt(req.query.days) || 30;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    // 获取指定时间范围内的记录
    const records = await Record.find({
      user: userId,
      created_at: { $gte: startDate }
    }).sort({ created_at: 1 });

    // 计算健康趋势数据
    const trends = calculateHealthTrends(records);

    res.json({
      success: true,
      data: trends
    });
  } catch (error) {
    console.error('获取健康趋势数据失败:', error);
    res.status(500).json({
      success: false,
      message: '获取健康趋势数据失败'
    });
  }
});

// 计算健康数据概览
function calculateHealthOverview(records) {
  const overview = {
    exercise: {
      totalMinutes: 0,
      averagePerDay: 0,
      mostFrequentType: 'walking',
      intensityDistribution: {
        light: 0,
        medium: 0,
        high: 0
      }
    },
    mood: {
      distribution: {
        happy: 0,
        calm: 0,
        sad: 0,
        angry: 0,
        anxious: 0,
        tired: 0,
        excited: 0,
        bored: 0
      },
      mostFrequent: 'calm'
    },
    health: {
      commonIssues: [],
      sleepQuality: 'medium',
      overallScore: 70
    }
  };

  // 计算运动数据
  const exerciseRecords = records.filter(r => r.type === 'exercise');
  overview.exercise.totalMinutes = exerciseRecords.reduce((sum, r) => sum + (r.duration || 0), 0);
  overview.exercise.averagePerDay = Math.round(overview.exercise.totalMinutes / 30);

  // 计算运动类型分布
  const exerciseTypeCount = {};
  exerciseRecords.forEach(r => {
    exerciseTypeCount[r.exercise_type] = (exerciseTypeCount[r.exercise_type] || 0) + 1;
  });
  overview.exercise.mostFrequentType = Object.entries(exerciseTypeCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'walking';

  // 计算运动强度分布
  const intensityCount = { light: 0, medium: 0, high: 0 };
  exerciseRecords.forEach(r => {
    intensityCount[r.intensity] = (intensityCount[r.intensity] || 0) + 1;
  });
  const totalExercise = Object.values(intensityCount).reduce((a, b) => a + b, 0);
  Object.entries(intensityCount).forEach(([key, value]) => {
    overview.exercise.intensityDistribution[key] = totalExercise ? Math.round((value / totalExercise) * 100) : 0;
  });

  // 计算心情数据
  const moodRecords = records.filter(r => r.type === 'mood');
  const moodCount = {};
  moodRecords.forEach(r => {
    moodCount[r.mood_type] = (moodCount[r.mood_type] || 0) + 1;
  });
  overview.mood.mostFrequent = Object.entries(moodCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm';

  // 计算心情分布
  const totalMoods = Object.values(moodCount).reduce((a, b) => a + b, 0);
  Object.entries(moodCount).forEach(([key, value]) => {
    overview.mood.distribution[key] = totalMoods ? Math.round((value / totalMoods) * 100) : 0;
  });

  // 计算健康数据
  const healthRecords = records.filter(r => r.type === 'health');
  const issueCount = {};
  healthRecords.forEach(r => {
    if (Array.isArray(r.status)) {
      r.status.forEach(status => {
        issueCount[status] = (issueCount[status] || 0) + 1;
      });
    }
  });

  // 获取最常见的健康问题
  overview.health.commonIssues = Object.entries(issueCount)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)
    .map(([type, count]) => ({ type, count }));

  // 计算睡眠质量
  const goodSleepCount = healthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes('sleep_well')
  ).length;
  const badSleepCount = healthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes('sleep_bad')
  ).length;

  overview.health.sleepQuality = goodSleepCount > badSleepCount ? 'high' : 
                                goodSleepCount < badSleepCount ? 'low' : 'medium';

  // 计算整体健康评分
  const healthFactors = {
    goodSleep: goodSleepCount * 5,
    badSleep: -badSleepCount * 3,
    issues: -Object.values(issueCount).reduce((a, b) => a + b, 0) * 2
  };
  const scoreFactors = Object.values(healthFactors).reduce((sum, factor) => sum + factor, 0);
  overview.health.overallScore = Math.max(0, Math.min(100, 70 + scoreFactors));

  return overview;
}

// 计算健康趋势数据
function calculateHealthTrends(records) {
  const trends = {
    exercise: [],
    mood: [],
    health: []
  };

  // 按日期分组记录
  const recordsByDate = {};
  records.forEach(record => {
    const date = record.created_at.toISOString().split('T')[0];
    if (!recordsByDate[date]) {
      recordsByDate[date] = [];
    }
    recordsByDate[date].push(record);
  });

  // 计算每日趋势
  Object.entries(recordsByDate).forEach(([date, dayRecords]) => {
    // 运动趋势
    const exerciseRecords = dayRecords.filter(r => r.type === 'exercise');
    const exerciseMinutes = exerciseRecords.reduce((sum, r) => sum + (r.duration || 0), 0);
    trends.exercise.push({
      date,
      minutes: exerciseMinutes,
      intensity: calculateAverageIntensity(exerciseRecords)
    });

    // 心情趋势
    const moodRecords = dayRecords.filter(r => r.type === 'mood');
    if (moodRecords.length > 0) {
      const moodCount = {};
      moodRecords.forEach(r => {
        moodCount[r.mood_type] = (moodCount[r.mood_type] || 0) + 1;
      });
      const dominantMood = Object.entries(moodCount)
        .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm';
      trends.mood.push({
        date,
        mood: dominantMood
      });
    }

    // 健康趋势
    const healthRecords = dayRecords.filter(r => r.type === 'health');
    if (healthRecords.length > 0) {
      const issues = healthRecords.reduce((acc, r) => {
        if (Array.isArray(r.status)) {
          r.status.forEach(status => acc.push(status));
        }
        return acc;
      }, []);
      trends.health.push({
        date,
        issues,
        sleepQuality: calculateSleepQuality(healthRecords)
      });
    }
  });

  return trends;
}

// 计算平均运动强度
function calculateAverageIntensity(exerciseRecords) {
  if (exerciseRecords.length === 0) return 'medium';
  
  const intensityMap = { light: 1, medium: 2, high: 3 };
  const intensitySum = exerciseRecords.reduce((sum, r) => 
    sum + (intensityMap[r.intensity] || 2), 0);
  const average = intensitySum / exerciseRecords.length;
  
  return average <= 1.5 ? 'light' : average <= 2.5 ? 'medium' : 'high';
}

// 计算睡眠质量
function calculateSleepQuality(healthRecords) {
  const goodSleepCount = healthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes('sleep_well')
  ).length;
  const badSleepCount = healthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes('sleep_bad')
  ).length;
  
  return goodSleepCount > badSleepCount ? 'high' : 
         goodSleepCount < badSleepCount ? 'low' : 'medium';
}

module.exports = router; 