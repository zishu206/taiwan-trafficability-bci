# -*- coding: utf-8 -*-
# 雨季/台风后时相真实重算（需在已认证 ee 环境运行：earthengine authenticate）
# 思路：动态指标按雨季窗口重取，静态指标与权重不变，重算 BCI 并统计等级跃迁。
import ee
ee.Initialize()

STUDY = ee.Geometry.Rectangle([119.307678, 21.901555, 120.99997, 24.959780])
# 雨季窗口（台湾中南部主汛期，可按台风过程改日期）
WET = ee.Filter.date('2023-06-01', '2023-09-30')
DRY = ee.Filter.date('2023-10-01', '2024-04-30')

# 静态指标（不随季节变化，直接复用既有图层）：NLI, BD, CLAY, SAL,
# RELIEF, SLOPE, CURV, DISTW, LULC —— 这里仅示意动态层重取
def l8_median(date_filter):
    l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filter(date_filter).filterBounds(STUDY)
    return l8.median().clip(STUDY)

def s1_median(date_filter):
    s1 = ee.ImageCollection('COPERNICUS/S1_GRD').filter(date_filter) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    return s1.median().clip(STUDY)

wet_l8, dry_l8 = l8_median(WET), l8_median(DRY)
wet_s1, dry_s1 = s1_median(WET), s1_median(DRY)

# 动态指标在 wet_l8/wet_s1 上按与旱季完全相同的函数重算：
# NDVI、MNDWI、FVC、LST、盐度（光学），SAR（雷达），以及由 MNDWI 派生的 WDENS。
# 静态层与 13 项全局权重保持不变（权重见论文 4.4）。
# 之后：
#   BCI_wet = sum(w_i * x_i_wet)，用同一断点 0.606/0.672 分级；
#   与 BCI_dry 逐像元比较，输出 BCI 下降量与等级跃迁比例。
# 示例（假设已组装 bci_wet、bci_dry 两个单波段 Image）：
#   diff = bci_dry.subtract(bci_wet)
#   g_wet = ee.Image(1).where(bci_wet.gte(0.606), 2).where(bci_wet.gte(0.672), 3)
#   g_dry = ee.Image(1).where(bci_dry.gte(0.606), 2).where(bci_dry.gte(0.672), 3)
#   transition = g_wet.lt(g_dry).reduceRegion(
#       reducer=ee.Reducer.mean(), geometry=STUDY, scale=30, maxPixels=1e13)
#   print(transition.getInfo())
print('脚本为模板：补全动态指标计算与权重后即可运行，静态层与权重不变。')
