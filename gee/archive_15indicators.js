// =====================================================================
// 台西平原 道路（车辆）承载力 15 项指标 GEE 提取 —— 分块导出版（解决内存超限）
// 用法：https://code.earthengine.google.com 粘贴全部 → Run → Tasks 面板会出现 4 个任务，
//       逐个点 RUN（可一次提交，云端排队执行）→ Drive 的 GEE_export 得到 4 个 GeoTIFF，
//       下载后用配套合并脚本拼成单个 15 波段影像。
// =====================================================================

// ============ 1. 参数区 ============
var START = '2022-01-01';
var END   = '2023-12-31';
var SCALE = 30;                  // 输出分辨率（米）
var CRS   = 'EPSG:4326';
var OUT_NAME = 'TaiXi_15indicators_30m';
var FOLDER   = 'GEE_export';
var N_TILES  = 4;                // 南北向分块数
var LAT_MIN  = 21.85, LAT_MAX = 25.30;
var SPLIT_LON = 121.0;           // 竖直切分经线
var STAT_SCALE = 120;            // 计算分位数用的较粗尺度（统计量，省内存）
var BUF = 1500;                  // 每块计算缓冲（米），消除邻域接缝
var DIST_R = 256;                // 距水距离变换搜索半径（像素，约 7.7 km）

// 台湾本岛几何（用内陆点取 GAUL，不依赖名称拼写）
var anchor = ee.Geometry.Point([120.9, 23.9]);
var taiwan = ee.FeatureCollection('FAO/GAUL/2015/level1').filterBounds(anchor);
var taiwanGeom = ee.Feature(taiwan.first()).geometry();
var westBox = ee.Geometry.Rectangle([119.0, 21.0, SPLIT_LON, 26.0], null, false);
var roi = taiwanGeom.intersection(westBox, 1);

// ============ 2. 工具函数 ============
function maskL89(img) {
  var qa = img.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1 << 2).eq(0)
    .and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0))
    .and(qa.bitwiseAnd(1 << 5).eq(0));
  return img.updateMask(mask);
}
function scaleL89(img) {
  var sr = img.select(['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7'])
    .multiply(0.0000275).add(-0.2);
  var st = img.select('ST_B10').multiply(0.00341802).add(149.0);
  return sr.addBands(st).copyProperties(img, ['system:time_start']);
}
// 用全局（粗尺度）分位数归一化，保证各块基准一致；reverse=true 反转方向
function normTile(rawImg, band, reverse, geomExport) {
  var stat = rawImg.select(band).reduceRegion({
    reducer: ee.Reducer.percentile([2, 98]),
    geometry: roi, scale: STAT_SCALE, bestEffort: true,
    maxPixels: 1e13, tileScale: 4
  });
  var p2 = ee.Number(stat.get(band + '_p2'));
  var p98 = ee.Number(stat.get(band + '_p98'));
  var span = p98.subtract(p2).max(1e-6);
  var x = rawImg.select(band).clamp(p2, p98).subtract(p2).divide(span);
  var out = ee.Image(ee.Algorithms.If(reverse, ee.Image(1).subtract(x), x))
    .rename(band).reproject(CRS, null, SCALE);
  return out.clip(geomExport);
}

// ============ 3. 原始指标（全局定义，导出时按块计算） ============
var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterBounds(roi).filterDate(START, END).map(maskL89).map(scaleL89);
var l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
  .filterBounds(roi).filterDate(START, END).map(maskL89).map(scaleL89);
var ls = l8.merge(l9).median();
var blue = ls.select('SR_B2'), green = ls.select('SR_B3'), red = ls.select('SR_B4');
var nir = ls.select('SR_B5'), swir1 = ls.select('SR_B6');
var lst = ls.select('ST_B10')
  .updateMask(ls.select('ST_B10').gte(250).and(ls.select('ST_B10').lte(330))).rename('LST');

var dem = ee.Image('USGS/SRTMGL1_003').select('elevation');
var slope = ee.Terrain.slope(dem).rename('SLOPE');
var slopeRad = slope.multiply(Math.PI / 180);

var sar = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(roi).filterDate(START, END)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .select('VV').median().rename('SAR');

var bd = ee.Image('OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02')
  .select('b0').divide(10).rename('BD');
var clay = ee.Image('OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02')
  .select('b0').rename('CLAY');

var dwLabel = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
  .filterBounds(roi).filterDate(START, END).select('label').mode();
var lulc = dwLabel.remap({
  from: [0, 1, 2, 3, 4, 5, 6, 7, 8],
  to:   [0.10, 0.45, 0.55, 0.25, 0.60, 0.50, 0.90, 0.85, 0.55],
  bandName: 'label', defaultValue: 0.5
}).rename('LULC').reproject(CRS, null, SCALE);

// 衍生指标
var mndwi = green.subtract(swir1).divide(green.add(swir1)).clamp(-1, 1);
var water = mndwi.gt(0.0).rename('WATER');
var sal = red.multiply(nir).sqrt().rename('SAL');
var litho = ee.Image(0.5).rename('NLI').reproject(CRS, null, SCALE);  // 岩性占位
var zMin = dem.reduceNeighborhood(ee.Reducer.min(), ee.Kernel.circle(3, 'pixels'));
var zMax = dem.reduceNeighborhood(ee.Reducer.max(), ee.Kernel.circle(3, 'pixels'));
var relief = zMax.subtract(zMin).rename('RELIEF');
var lapKernel = ee.Kernel.fixed(3, 3, [[0, 1, 0], [1, -4, 1], [0, 1, 0]], 1);
var curv = dem.convolve(lapKernel).abs().rename('CURV');
var distWater = water.selfMask()
  .fastDistanceTransform(DIST_R, 'pixels')
  .select('distance').sqrt().multiply(SCALE).rename('DISTW');
var waterDens = water.reduceNeighborhood(
  ee.Reducer.mean(), ee.Kernel.circle(10, 'pixels')).rename('WDENS');
var ndwi = green.subtract(nir).divide(green.add(nir)).clamp(-1, 1).rename('NDWI');
var twi = slopeRad.tan().add(0.005).pow(-1).log().clamp(-5, 10).rename('TWI');
var ndvi = nir.subtract(red).divide(nir.add(red)).clamp(-1, 1).rename('NDVI');

// ============ 4. 分块构建并导出 ============
function buildStack(geomExport) {
  var bands = [
    litho,
    normTile(bd, 'BD', false, geomExport),
    normTile(clay, 'CLAY', true, geomExport),
    normTile(sal, 'SAL', true, geomExport),
    normTile(relief, 'RELIEF', true, geomExport),
    normTile(slope, 'SLOPE', true, geomExport),
    normTile(curv, 'CURV', true, geomExport),
    normTile(distWater, 'DISTW', false, geomExport),
    normTile(waterDens, 'WDENS', true, geomExport),
    normTile(ndwi, 'NDWI', true, geomExport),
    normTile(twi, 'TWI', true, geomExport),
    normTile(sar, 'SAR', false, geomExport),
    normTile(lst, 'LST', false, geomExport),
    normTile(ndvi, 'NDVI', true, geomExport),
    lulc.clip(geomExport)
  ];
  return ee.Image.cat(bands).clip(geomExport);
}

for (var i = 0; i < N_TILES; i++) {
  (function (idx) {
    var y0 = LAT_MIN + (LAT_MAX - LAT_MIN) * idx / N_TILES;
    var y1 = LAT_MIN + (LAT_MAX - LAT_MIN) * (idx + 1) / N_TILES;
    var tileBox = ee.Geometry.Rectangle([119.0, y0, SPLIT_LON, y1], null, false);
    var tileGeom = taiwanGeom.intersection(tileBox, 1);
    var stack = buildStack(tileGeom);
    Export.image.toDrive({
      image: stack,
      description: OUT_NAME + '_part' + (idx + 1),
      folder: FOLDER,
      fileNamePrefix: OUT_NAME + '_part' + (idx + 1),
      region: tileGeom,
      scale: SCALE,
      crs: CRS,
      maxPixels: 1e13
    });
  })(i);
}

print('已生成 ' + N_TILES + ' 个分块导出任务，请到 Tasks 面板逐个点 RUN');
// 岩性 NLI 与严谨 TWI 的替换说明同前：拿到岩性矢量 / 本地 D8 汇流结果后替换对应波段。
