/* SanityOps batch summary - chart definitions (ECharts + Mermaid) */
(function () {
  var cs = getComputedStyle(document.documentElement);
  function v(name) { return cs.getPropertyValue(name).trim(); }
  var accent = v('--accent'), accent2 = v('--accent2'), ink = v('--ink'), muted = v('--muted'),
      rule = v('--rule'), bg2 = v('--bg2'),
      p0 = v('--p0'), p1 = v('--p1'), p2 = v('--p2'),
      cSp = v('--cat-sp'), cSk = v('--cat-sk'), cTs = v('--cat-ts'), cAs = v('--cat-as');

  var cats = ['system-prompt', 'skill', 'tool-schema', 'agent-suite'];
  var catColors = [cSp, cSk, cTs, cAs];
  var baseGrid = { left: 8, right: 18, top: 34, bottom: 8, containLabel: true };
  var axisCommon = {
    axisLine: { lineStyle: { color: rule } },
    axisTick: { show: false },
    axisLabel: { color: muted, fontSize: 11 }
  };

  function setup(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    return echarts.init(el, null, { renderer: 'svg' });
  }

  /* Figure 1 - stacked severity by category */
  (function () {
    var c = setup('chart-sev'); if (!c) return;
    c.setOption({
      animation: false,
      color: [p0, p1, p2],
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, appendToBody: true },
      legend: { data: ['P0', 'P1', 'P2'], textStyle: { color: muted, fontSize: 11 }, top: 0, icon: 'roundRect', itemWidth: 10, itemHeight: 10 },
      grid: baseGrid,
      xAxis: Object.assign({ type: 'category', data: cats }, axisCommon),
      yAxis: Object.assign({ type: 'value', splitLine: { lineStyle: { color: rule } } }, axisCommon),
      series: [
        { name: 'P0', type: 'bar', stack: 's', data: [171, 76, 26, 552], itemStyle: { color: p0 } },
        { name: 'P1', type: 'bar', stack: 's', data: [122, 101, 51, 292], itemStyle: { color: p1 } },
        { name: 'P2', type: 'bar', stack: 's', data: [5, 8, 52, 17], itemStyle: { color: p2 } }
      ]
    });
    window.addEventListener('resize', function () { c.resize(); });
  })();

  /* Figure 2 - Gate-0 outcomes donut */
  (function () {
    var c = setup('chart-gate'); if (!c) return;
    c.setOption({
      animation: false,
      tooltip: { trigger: 'item', appendToBody: true, formatter: '{b}: {c} ({d}%)' },
      legend: { bottom: 0, textStyle: { color: muted, fontSize: 11 }, icon: 'roundRect', itemWidth: 10, itemHeight: 10 },
      series: [{
        type: 'pie', radius: ['54%', '76%'], center: ['50%', '46%'],
        avoidLabelOverlap: true, label: { color: ink, fontSize: 11, formatter: '{b}\n{c}' },
        labelLine: { lineStyle: { color: rule } },
        data: [
          { value: 11, name: 'Gate-0 Passed', itemStyle: { color: accent2 } },
          { value: 89, name: 'Not passed', itemStyle: { color: p2 } }
        ]
      }]
    });
    window.addEventListener('resize', function () { c.resize(); });
  })();

  /* Figure 4 - risk tier by category */
  (function () {
    var c = setup('chart-tier'); if (!c) return;
    c.setOption({
      animation: false,
      color: [accent, accent2, cAs, p2],
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, appendToBody: true },
      legend: { data: ['L1', 'L2', 'L3', 'mixed / n/a'], textStyle: { color: muted, fontSize: 11 }, top: 0, icon: 'roundRect', itemWidth: 10, itemHeight: 10 },
      grid: baseGrid,
      xAxis: Object.assign({ type: 'category', data: cats }, axisCommon),
      yAxis: Object.assign({ type: 'value', max: 25, splitLine: { lineStyle: { color: rule } } }, axisCommon),
      series: [
        { name: 'L1', type: 'bar', stack: 't', data: [11, 4, 21, 1], itemStyle: { color: accent } },
        { name: 'L2', type: 'bar', stack: 't', data: [6, 18, 1, 11], itemStyle: { color: accent2 } },
        { name: 'L3', type: 'bar', stack: 't', data: [8, 2, 1, 13], itemStyle: { color: cAs } },
        { name: 'mixed / n/a', type: 'bar', stack: 't', data: [0, 1, 2, 0], itemStyle: { color: p2 } }
      ]
    });
    window.addEventListener('resize', function () { c.resize(); });
  })();

  /* Figure 5 - top failed rules */
  (function () {
    var c = setup('chart-rules'); if (!c) return;
    var rows = [
      ['QD-P-2.7.3', 41, 'QD-P'], ['QD-P-2.3.4', 38, 'QD-P'], ['QD-P-2.7.2', 38, 'QD-P'],
      ['QD-P-2.5.2', 37, 'QD-P'], ['QD-P-2.7.1', 33, 'QD-P'], ['QD-S-4.1', 33, 'QD-S'],
      ['QD-S-1.1', 33, 'QD-S'], ['QD-P-2.2.4', 32, 'QD-P'], ['QD-S-1.3', 30, 'QD-S'],
      ['QD-T-2.1', 28, 'QD-T'], ['QD-S-3.4', 26, 'QD-S'], ['QD-S-4.3', 26, 'QD-S'],
      ['QD-T-1.4', 26, 'QD-T'], ['QD-P-2.2.2', 25, 'QD-P'], ['QD-S-1.2', 25, 'QD-S']
    ];
    var fam = { 'QD-P': cSp, 'QD-S': cSk, 'QD-T': cTs };
    var ordered = rows.slice().reverse();
    c.setOption({
      animation: false,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, appendToBody: true },
      grid: { left: 8, right: 40, top: 12, bottom: 8, containLabel: true },
      xAxis: Object.assign({ type: 'value', splitLine: { lineStyle: { color: rule } } }, axisCommon),
      yAxis: Object.assign({ type: 'category', data: ordered.map(function (r) { return r[0]; }) },
        { axisLine: { lineStyle: { color: rule } }, axisTick: { show: false }, axisLabel: { color: ink, fontSize: 11, fontFamily: 'JetBrainsMono' } }),
      series: [{
        type: 'bar',
        data: ordered.map(function (r) { return { value: r[1], itemStyle: { color: fam[r[2]] } }; }),
        label: { show: true, position: 'right', color: muted, fontSize: 10 }
      }]
    });
    window.addEventListener('resize', function () { c.resize(); });
  })();

  /* Figure 6 - FAIL per test case (100) */
  (function () {
    var c = setup('chart-tc'); if (!c) return;
    var sp = [12,7,14,6,10,13,6,13,2,10,10,10,7,7,8,19,19,19,18,19,18,17,8,18,8];
    var sk = [19,12,13,15,9,4,3,0,5,4,0,16,2,3,6,15,9,3,6,4,6,13,5,6,7];
    var ts = [9,6,0,14,23,22,4,2,13,2,2,3,3,3,3,3,2,4,0,3,0,4,2,2,0];
    var as = [53,9,8,89,96,99,87,34,35,9,50,38,10,34,35,2,13,24,17,12,34,18,29,14,12];
    var labels = ['TC-001','TC-018','TC-019','TC-044','TC-045','TC-046','TC-048','TC-051','TC-052','TC-072','TC-073','TC-074','TC-075','TC-076','TC-077','TC-078','TC-079','TC-080','TC-082','TC-083','TC-108','TC-109','TC-110','TC-111','TC-112',
      'TC-002','TC-047','TC-049','TC-053','TC-054','TC-081','TC-138','TC-139','TC-140','TC-141','TC-142','TC-143','TC-144','TC-145','TC-146','TC-147','TC-148','TC-149','TC-150','TC-151','TC-152','TC-153','TC-154','TC-155','TC-156',
      'TC-003','TC-050','TC-182','TC-183','TC-184','TC-185','TC-186','TC-187','TC-188','TC-189','TC-190','TC-191','TC-192','TC-193','TC-194','TC-195','TC-196','TC-197','TC-198','TC-199','TC-200','TC-201','TC-202','TC-205','TC-206',
      'TC-004','TC-005','TC-006','TC-031','TC-032','TC-033','TC-034','TC-035','TC-036','TC-037','TC-038','TC-039','TC-040','TC-041','TC-042','TC-055','TC-056','TC-057','TC-058','TC-059','TC-060','TC-061','TC-062','TC-063','TC-064'];
    var data = sp.concat(sk, ts, as).map(function (val, i) {
      var color = i < 25 ? cSp : (i < 50 ? cSk : (i < 75 ? cTs : cAs));
      return { value: val, itemStyle: { color: color } };
    });
    c.setOption({
      animation: false,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, appendToBody: true },
      grid: { left: 8, right: 12, top: 16, bottom: 74, containLabel: true },
      xAxis: Object.assign({ type: 'category', data: labels },
        { axisLine: { lineStyle: { color: rule } }, axisTick: { show: false },
          axisLabel: { color: muted, fontSize: 8, rotation: 90, interval: 4, fontFamily: 'JetBrainsMono' } }),
      yAxis: Object.assign({ type: 'value', splitLine: { lineStyle: { color: rule } } }, axisCommon),
      series: [{ type: 'bar', data: data, barCategoryGap: '10%' }]
    });
    window.addEventListener('resize', function () { c.resize(); });
  })();

  /* Mermaid */
  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose',
      themeVariables: { fontFamily: 'InstrumentSans, sans-serif', fontSize: '13px' } });
  }
})();
