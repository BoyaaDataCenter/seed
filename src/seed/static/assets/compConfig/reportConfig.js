const config_ = {
  "line":{
    "totalNum": 100,  // 指标纬度个数总和
    "dimensionsNum": 100,  // 维度的个数
    "indexsNum": 100,  //指标的个数
    "dimensionsLimit":1, // 维度至少的个数
    "tips": "提示：该报表支持多指标多维度配置！请至少配置一个指标和一个维度~",
    "changeList":[]
  },
  "bar":{
    "direction": "cross",
    "totalNum": 100,  // 指标纬度个数总和
    "dimensionsNum": 100,  // 维度的个数
    "indexsNum": 100,  //指标的个数
    "dimensionsLimit":1, // 维度至少的个数
    "tips": "提示：该报表支持多指标多维度配置！请至少配置一个指标和一个维度~",
    "changeList":[['bar', '对比图'], ['pie', '饼状图']]
  },
  "pie":{
    "totalNum": 100,  // 指标纬度个数总和
    "dimensionsNum": 100,  // 维度的个数
    "indexsNum": 100,  //指标的个数
    "dimensionsLimit":1, // 维度至少的个数
    "tips": "提示：该报表支持多指标多维度配置！请至少配置一个指标和一个维度~",
    "changeList":[['pie', '饼状图'], ['bar', '对比图']]
  },
  "linestack":{
    "totalNum": 100,  // 指标纬度个数总和
    "dimensionsNum": 100,  // 维度的个数
    "indexsNum": 1,  //指标的个数
    "dimensionsLimit":2, // 维度至少的个数
    "tips": "提示：该报表只支持单指标多维度配置！维度中必须有fdate这个维度",
    "changeList":[['linestack', '对比趋势图'],['bar', '对比图'], ['pie', '饼状图']],
    "limit": {
      "dimensions": ["fdate"]
    }
  }
}

export {config_};
