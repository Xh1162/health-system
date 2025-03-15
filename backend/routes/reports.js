const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Record = require('../models/Record');

// 获取健康报告汇总数据
router.get('/summary', auth, async (req, res) => {
  try {
    const userId = req.user.id;
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    // 获取用户最近30天的所有记录
    const records = await Record.find({
      user: userId,
      created_at: { $gte: thirtyDaysAgo }
    }).sort({ created_at: -1 });

    if (records.length === 0) {
      return res.json({
        analysis: {
          exerciseStats: {
            totalMinutes: 0,
            averagePerDay: 0,
            mostFrequentType: 'walking',
            intensityDistribution: {
              light: 0,
              medium: 0,
              high: 0
            }
          },
          moodStats: {
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
          healthStats: {
            commonIssues: []
          }
        },
        trends: {
          exerciseTrends: {
            weeklyMinutes: 0,
            weeklyChange: 0,
            intensityAvg: 'medium',
            intensityChange: 0,
            frequency: 0,
            frequencyChange: 0
          },
          moodTrends: {
            positiveRate: 0,
            positiveChange: 0,
            stability: 'medium',
            stabilityChange: 0,
            previousMood: 'calm',
            currentMood: 'calm'
          },
          healthTrends: {
            sleepQuality: 'medium',
            sleepChange: 0,
            issueFrequency: 0,
            issueChange: 0,
            overallScore: 0,
            scoreChange: 0
          },
          dateRange: {
            start: thirtyDaysAgo,
            end: new Date()
          }
        }
      });
    }

    // 计算分析数据
    const analysis = {
      exerciseStats: calculateExerciseStats(records),
      moodStats: calculateMoodStats(records),
      healthStats: calculateHealthStats(records)
    };
    
    // 计算趋势数据
    const trends = calculateTrends(records, thirtyDaysAgo);

    res.json({
      analysis,
      trends
    });
  } catch (error) {
    console.error('获取报告数据失败:', error);
    res.status(500).json({ message: '获取报告数据失败' });
  }
});

// 计算运动统计数据
function calculateExerciseStats(records) {
  const exerciseRecords = records.filter(r => r.type === 'exercise');
  
  const totalMinutes = exerciseRecords.reduce((sum, r) => sum + (r.duration || 0), 0);
  const averagePerDay = Math.round(totalMinutes / 30);
  
  // 计算运动类型分布
  const typeCount = {};
  exerciseRecords.forEach(r => {
    typeCount[r.exercise_type] = (typeCount[r.exercise_type] || 0) + 1;
  });
  
  const mostFrequentType = Object.entries(typeCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'walking';
  
  // 计算强度分布
  const intensityCount = { light: 0, medium: 0, high: 0 };
  exerciseRecords.forEach(r => {
    intensityCount[r.intensity] = (intensityCount[r.intensity] || 0) + 1;
  });
  
  const total = Object.values(intensityCount).reduce((a, b) => a + b, 0);
  const intensityDistribution = {};
  Object.entries(intensityCount).forEach(([key, value]) => {
    intensityDistribution[key] = total ? Math.round((value / total) * 100) : 0;
  });

  return {
    totalMinutes,
    averagePerDay,
    mostFrequentType,
    intensityDistribution
  };
}

// 计算心情统计数据
function calculateMoodStats(records) {
  const moodRecords = records.filter(r => r.type === 'mood');
  
  // 计算心情分布
  const moodCount = {};
  const moodTypes = ['happy', 'calm', 'sad', 'angry', 'anxious', 'tired', 'excited', 'bored'];
  
  // 初始化所有心情类型为0
  moodTypes.forEach(type => {
    moodCount[type] = 0;
  });
  
  // 统计实际记录
  moodRecords.forEach(r => {
    if (r.mood_type && moodTypes.includes(r.mood_type)) {
      moodCount[r.mood_type] = (moodCount[r.mood_type] || 0) + 1;
    }
  });
  
  const total = Object.values(moodCount).reduce((a, b) => a + b, 0);
  const distribution = {};
  Object.entries(moodCount).forEach(([key, value]) => {
    distribution[key] = total ? Math.round((value / total) * 100) : 0;
  });
  
  const mostFrequent = Object.entries(moodCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm';

  return {
    distribution,
    mostFrequent
  };
}

// 计算健康状况统计数据
function calculateHealthStats(records) {
  const healthRecords = records.filter(r => r.type === 'health');
  
  // 统计常见问题
  const issueCount = {};
  healthRecords.forEach(r => {
    if (Array.isArray(r.status)) {
      r.status.forEach(status => {
        issueCount[status] = (issueCount[status] || 0) + 1;
      });
    }
  });
  
  const commonIssues = Object.entries(issueCount)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)
    .map(([type, count]) => ({ type, count }));

  return {
    commonIssues
  };
}

// 计算趋势数据
function calculateTrends(records, startDate) {
  // 将记录按周分组
  const now = new Date();
  const oneWeekAgo = new Date(now);
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  
  const twoWeeksAgo = new Date(oneWeekAgo);
  twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 7);
  
  const currentWeekRecords = records.filter(r => new Date(r.created_at) >= oneWeekAgo);
  const previousWeekRecords = records.filter(r => 
    new Date(r.created_at) >= twoWeeksAgo && new Date(r.created_at) < oneWeekAgo
  );
  
  // 运动趋势
  const exerciseTrends = calculateExerciseTrends(currentWeekRecords, previousWeekRecords);
  
  // 心情趋势
  const moodTrends = calculateMoodTrends(currentWeekRecords, previousWeekRecords);
  
  // 健康趋势
  const healthTrends = calculateHealthTrends(currentWeekRecords, previousWeekRecords);

  return {
    exerciseTrends,
    moodTrends,
    healthTrends,
    dateRange: {
      start: startDate,
      end: now
    }
  };
}

// 计算运动趋势
function calculateExerciseTrends(currentWeekRecords, previousWeekRecords) {
  // 当前周运动记录
  const currentExerciseRecords = currentWeekRecords.filter(r => r.type === 'exercise');
  // 上一周运动记录
  const previousExerciseRecords = previousWeekRecords.filter(r => r.type === 'exercise');
  
  // 计算每周运动时长
  const currentWeekMinutes = currentExerciseRecords.reduce((sum, r) => sum + (r.duration || 0), 0);
  const previousWeekMinutes = previousExerciseRecords.reduce((sum, r) => sum + (r.duration || 0), 0);
  
  // 计算变化百分比
  let weeklyChange = 0;
  if (previousWeekMinutes > 0) {
    weeklyChange = Math.round(((currentWeekMinutes - previousWeekMinutes) / previousWeekMinutes) * 100);
  }
  
  // 计算运动频率
  const frequency = currentExerciseRecords.length;
  const previousFrequency = previousExerciseRecords.length;
  
  let frequencyChange = 0;
  if (previousFrequency > 0) {
    frequencyChange = Math.round(((frequency - previousFrequency) / previousFrequency) * 100);
  }
  
  // 计算平均强度
  const intensityMap = { light: 1, medium: 2, high: 3 };
  const intensitySum = currentExerciseRecords.reduce((sum, r) => sum + (intensityMap[r.intensity] || 2), 0);
  const intensityAvg = intensitySum > 0 && currentExerciseRecords.length > 0 
    ? (intensitySum / currentExerciseRecords.length <= 1.5 ? 'light' : 
       intensitySum / currentExerciseRecords.length <= 2.5 ? 'medium' : 'high')
    : 'medium';
  
  const previousIntensitySum = previousExerciseRecords.reduce((sum, r) => sum + (intensityMap[r.intensity] || 2), 0);
  const previousIntensityAvg = previousIntensitySum > 0 && previousExerciseRecords.length > 0 
    ? previousIntensitySum / previousExerciseRecords.length
    : 2;
  const currentIntensityAvgValue = intensitySum > 0 && currentExerciseRecords.length > 0 
    ? intensitySum / currentExerciseRecords.length
    : 2;
  
  let intensityChange = 0;
  if (previousIntensityAvg > 0) {
    intensityChange = Math.round(((currentIntensityAvgValue - previousIntensityAvg) / previousIntensityAvg) * 100);
  }
  
  return {
    weeklyMinutes: currentWeekMinutes,
    weeklyChange,
    intensityAvg,
    intensityChange,
    frequency,
    frequencyChange
  };
}

// 计算心情趋势
function calculateMoodTrends(currentWeekRecords, previousWeekRecords) {
  // 当前周心情记录
  const currentMoodRecords = currentWeekRecords.filter(r => r.type === 'mood');
  // 上一周心情记录
  const previousMoodRecords = previousWeekRecords.filter(r => r.type === 'mood');
  
  // 积极情绪类型
  const positiveTypes = ['happy', 'excited', 'calm'];
  
  // 计算积极情绪比例
  const currentPositiveCount = currentMoodRecords.filter(r => positiveTypes.includes(r.mood_type)).length;
  const currentPositiveRate = currentMoodRecords.length > 0 
    ? Math.round((currentPositiveCount / currentMoodRecords.length) * 100)
    : 0;
  
  const previousPositiveCount = previousMoodRecords.filter(r => positiveTypes.includes(r.mood_type)).length;
  const previousPositiveRate = previousMoodRecords.length > 0 
    ? Math.round((previousPositiveCount / previousMoodRecords.length) * 100)
    : 0;
  
  // 计算变化百分比
  let positiveChange = 0;
  if (previousPositiveRate > 0) {
    positiveChange = Math.round(((currentPositiveRate - previousPositiveRate) / previousPositiveRate) * 100);
  }
  
  // 计算情绪稳定性
  const moodTypes = currentMoodRecords.map(r => r.mood_type);
  const uniqueMoodTypes = [...new Set(moodTypes)].length;
  const stability = uniqueMoodTypes <= 2 ? 'high' : uniqueMoodTypes <= 4 ? 'medium' : 'low';
  
  const previousMoodTypes = previousMoodRecords.map(r => r.mood_type);
  const previousUniqueMoodTypes = [...new Set(previousMoodTypes)].length;
  
  // 稳定性变化 (负数表示更稳定)
  let stabilityChange = 0;
  if (previousUniqueMoodTypes > 0) {
    stabilityChange = Math.round(((uniqueMoodTypes - previousUniqueMoodTypes) / previousUniqueMoodTypes) * -100);
  }
  
  // 获取当前和之前的主要情绪
  const moodCount = {};
  currentMoodRecords.forEach(r => {
    moodCount[r.mood_type] = (moodCount[r.mood_type] || 0) + 1;
  });
  
  const currentMood = Object.entries(moodCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm';
  
  const previousMoodCount = {};
  previousMoodRecords.forEach(r => {
    previousMoodCount[r.mood_type] = (previousMoodCount[r.mood_type] || 0) + 1;
  });
  
  const previousMood = Object.entries(previousMoodCount)
    .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm';
  
  return {
    positiveRate: currentPositiveRate,
    positiveChange,
    stability,
    stabilityChange,
    previousMood,
    currentMood
  };
}

// 计算健康趋势
function calculateHealthTrends(currentWeekRecords, previousWeekRecords) {
  // 当前周健康记录
  const currentHealthRecords = currentWeekRecords.filter(r => r.type === 'health');
  // 上一周健康记录
  const previousHealthRecords = previousWeekRecords.filter(r => r.type === 'health');
  
  // 睡眠质量
  const goodSleepStatus = 'sleep_well';
  const badSleepStatus = 'sleep_bad';
  
  const currentGoodSleepCount = currentHealthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes(goodSleepStatus)
  ).length;
  
  const currentBadSleepCount = currentHealthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes(badSleepStatus)
  ).length;
  
  const sleepQuality = currentGoodSleepCount > currentBadSleepCount ? 'high' : 
                       currentGoodSleepCount < currentBadSleepCount ? 'low' : 'medium';
  
  const previousGoodSleepCount = previousHealthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes(goodSleepStatus)
  ).length;
  
  const previousBadSleepCount = previousHealthRecords.filter(r => 
    Array.isArray(r.status) && r.status.includes(badSleepStatus)
  ).length;
  
  // 睡眠质量变化
  const currentSleepRatio = currentHealthRecords.length > 0 
    ? (currentGoodSleepCount - currentBadSleepCount) / currentHealthRecords.length
    : 0;
  
  const previousSleepRatio = previousHealthRecords.length > 0 
    ? (previousGoodSleepCount - previousBadSleepCount) / previousHealthRecords.length
    : 0;
  
  let sleepChange = 0;
  if (previousSleepRatio !== 0) {
    sleepChange = Math.round(((currentSleepRatio - previousSleepRatio) / Math.abs(previousSleepRatio)) * 100);
  }
  
  // 健康问题频率
  const issueFrequency = currentHealthRecords.reduce((count, r) => 
    count + (Array.isArray(r.status) ? r.status.length : 0), 0
  );
  
  const previousIssueFrequency = previousHealthRecords.reduce((count, r) => 
    count + (Array.isArray(r.status) ? r.status.length : 0), 0
  );
  
  // 问题频率变化 (正数表示问题增加)
  let issueChange = 0;
  if (previousIssueFrequency > 0) {
    issueChange = Math.round(((issueFrequency - previousIssueFrequency) / previousIssueFrequency) * 100);
  }
  
  // 整体健康评分 (0-100)
  const healthFactors = {
    goodSleep: currentGoodSleepCount * 5,
    badSleep: -currentBadSleepCount * 3,
    issues: -issueFrequency * 2
  };
  
  const baseScore = 70;
  const scoreFactors = Object.values(healthFactors).reduce((sum, factor) => sum + factor, 0);
  const overallScore = Math.max(0, Math.min(100, baseScore + scoreFactors));
  
  // 上周健康评分
  const previousHealthFactors = {
    goodSleep: previousGoodSleepCount * 5,
    badSleep: -previousBadSleepCount * 3,
    issues: -previousIssueFrequency * 2
  };
  
  const previousScoreFactors = Object.values(previousHealthFactors).reduce((sum, factor) => sum + factor, 0);
  const previousOverallScore = Math.max(0, Math.min(100, baseScore + previousScoreFactors));
  
  // 评分变化
  let scoreChange = 0;
  if (previousOverallScore > 0) {
    scoreChange = Math.round(((overallScore - previousOverallScore) / previousOverallScore) * 100);
  }
  
  return {
    sleepQuality,
    sleepChange,
    issueFrequency,
    issueChange,
    overallScore,
    scoreChange
  };
}

module.exports = router; 