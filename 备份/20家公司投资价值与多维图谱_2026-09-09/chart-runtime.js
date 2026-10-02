function mountInvestmentChart(rootId, view) {
  const root = document.getElementById(rootId);
  const data = JSON.parse(root.querySelector('script[type="application/json"]').textContent);
  const plot = root.querySelector('.plots');
  const legend = root.querySelector('.legend');
  const detail = root.querySelector('.selection');
  const tip = root.querySelector('.tooltip');
  const color = i => `var(--viz-series-${i + 1})`;
  const fmt = v => v == null ? '缺失' : `${v >= 0 ? '+' : ''}${v.toFixed(1)}%`;
  const pe = v => v == null ? '缺失' : `${v.toFixed(2)}倍`;
  const range = a => `${fmt(a[0])}～${fmt(a[1])}`;
  const categoryNames = ['基准即有正面格', '从乐观开始', '从突破开始', '四行均无正面格'];
  const defenseNames = ['较强', '中等', '偏弱'];
  const active = new Set([0, 1, 2, 3]);
  let selected = null;
  let redraw;
  let timer;
  const all = data.companies;
  function tooltip(text, event) {
    tip.textContent = text;
    tip.style.display = 'block';
    const r = root.getBoundingClientRect();
    const b = tip.getBoundingClientRect();
    const left = Math.max(4, Math.min(event.clientX - r.left + 14, r.width - b.width - 4));
    const top = Math.max(4, event.clientY - r.top - b.height - 12);
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
  }
  function pin(d, text) {
    selected = d.t;
    detail.textContent = text;
    root.querySelectorAll('.observation').forEach(el => {
      el.style.stroke = el.getAttribute('data-ticker') === selected ? 'var(--foreground)' : 'none';
      el.style.strokeWidth = '1.7';
    });
  }
  function legendButtons(labels, count) {
    legend.replaceChildren();
    labels.forEach((label, i) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-pressed', 'true');
      const swatch = document.createElement('span');
      swatch.className = 'swatch';
      swatch.style.background = color(i);
      button.append(swatch, document.createTextNode(label + (count ? ` · ${count(i)}` : '')));
      button.addEventListener('click', () => {
        if (active.has(i)) active.delete(i); else active.add(i);
        button.setAttribute('aria-pressed', String(active.has(i)));
        button.style.opacity = active.has(i) ? '1' : '.4';
        redraw();
      });
      legend.append(button);
    });
  }
  function makeSvg(container, width, height, title, description) {
    const svg = d3.select(container).append('svg').attr('class', 'investment-plot').attr('viewBox', `0 0 ${width} ${height}`).attr('role', 'img').attr('aria-label', title);
    svg.append('title').text(title);
    svg.append('desc').text(description);
    return svg;
  }
  function axes(svg, x, y, frame, xlabel, ylabel, xFormatter, yFormatter, xTicks, yTicks) {
    svg.append('rect').attr('data-chart-frame', '').attr('x', frame.l).attr('y', frame.t).attr('width', frame.r - frame.l).attr('height', frame.b - frame.t).attr('fill', 'none').attr('stroke', 'var(--border)');
    const xa = d3.axisBottom(x).ticks(frame.r - frame.l < 330 ? 4 : 6).tickSizeOuter(0);
    const ya = d3.axisLeft(y).ticks(5).tickSizeOuter(0);
    if (xFormatter) xa.tickFormat(xFormatter);
    if (yFormatter) ya.tickFormat(yFormatter);
    if (xTicks) xa.tickValues(xTicks);
    if (yTicks) ya.tickValues(yTicks);
    svg.append('g').attr('class', 'axis x-axis').attr('transform', `translate(0,${frame.b})`).call(xa);
    svg.append('g').attr('class', 'axis y-axis').attr('transform', `translate(${frame.l},0)`).call(ya);
    svg.append('text').attr('class', 'axis-title').attr('data-axis', 'x').attr('x', (frame.l + frame.r) / 2).attr('y', frame.b + 50).attr('text-anchor', 'middle').text(xlabel);
    svg.append('text').attr('class', 'axis-title').attr('data-axis', 'y').attr('transform', `translate(15,${(frame.t + frame.b) / 2}) rotate(-90)`).attr('text-anchor', 'middle').text(ylabel);
  }
  function padded(values, fraction = .08, log = false) {
    const extent = d3.extent(values.filter(Number.isFinite));
    if (log) return [extent[0] / Math.pow(extent[1] / extent[0], fraction), extent[1] * Math.pow(extent[1] / extent[0], fraction)];
    const gap = (extent[1] - extent[0] || 1) * fraction;
    return [extent[0] - gap, extent[1] + gap];
  }
  function tidy(svg, frame) {
    // Measure all labels at the actual rendered size; remove optional labels first.
    const overlap = (a, b) => a.left < b.right + 4 && a.right + 4 > b.left && a.top < b.bottom + 4 && a.bottom + 4 > b.top;
    for (const axis of ['.x-axis', '.y-axis']) {
      const kept = [];
      svg.node().querySelectorAll(`${axis} .tick text`).forEach(el => {
        const b = el.getBoundingClientRect();
        if (kept.some(a => overlap(a, b))) el.style.visibility = 'hidden';
        else kept.push(b);
      });
    }
    const used = [...svg.node().querySelectorAll('.tick text,.axis-title')].filter(el => el.style.visibility !== 'hidden').map(el => el.getBoundingClientRect());
    svg.node().querySelectorAll('.direct-ticker').forEach(el => {
      const b = el.getBoundingClientRect();
      const box = el.getBBox();
      if (box.x < frame.l + 4 || box.x + box.width > frame.r - 4 || box.y < frame.t + 4 || box.y + box.height > frame.b - 4 || used.some(a => overlap(a, b))) el.remove();
      else used.push(b);
    });
  }
  function logTicks(domain, width) {
    let ticks = [];
    for (let exponent = Math.floor(Math.log10(domain[0])); exponent <= Math.ceil(Math.log10(domain[1])); exponent++) {
      for (const multiplier of [1, 2, 5]) {
        const v = multiplier * 10 ** exponent;
        if (v >= domain[0] && v <= domain[1]) ticks.push(v);
      }
    }
    const max = width < 430 ? 4 : 7;
    if (ticks.length > max) ticks = ticks.filter((_, i) => i % Math.ceil(ticks.length / max) === 0);
    return ticks;
  }
  function scatter() {
    let rows, cfg;
    if (view === 'momentum') {
      rows = all.filter(d => d.p[2] != null && d.sameDay && d.b36);
      cfg = {
        x: d => 1 + d.p[2] / 100, y: d => d.b36[0], cat: d => d.g,
        xlog: true, xlabel: '一年涨跌幅（%，对数财富）', ylabel: '基准三年条件回报下沿（%）',
        text: d => `${d.t} ${d.n}\n过去一年 ${fmt(d.p[2])}｜3个月 ${fmt(d.p[0])}\n基准三年 ${range(d.b36)}\n突破三年 ${range(d.u36)}\n${categoryNames[d.g]}${d.k ? `｜入选第${d.k}位` : ''}`,
        summary: d => `${d.t}｜一年股价 ${fmt(d.p[2])}｜基准三年 ${range(d.b36)}`,
        labels: ['ADBE', 'MU', 'PNR', 'FLNC', 'SNDK', 'AXTI', 'VRT', 'IREN', 'ET', 'NVDA', 'MSFT', 'TSM']
      };
    } else if (view === 'valuation') {
      rows = all.filter(d => d.q[1] > 0 && d.q[2] > 0);
      cfg = {
        x: d => d.q[1], y: d => d.q[2], cat: d => d.g, xlog: true, ylog: true,
        xlabel: 'TTM PE（倍，对数刻度）', ylabel: 'Forward PE（倍，对数刻度）',
        text: d => `${d.t} ${d.n}\nTTM PE ${pe(d.q[1])}｜Forward PE ${pe(d.q[2])}\n报价 ${d.q[0]} USD｜${d.quoteDate}\n${categoryNames[d.g]}\nForward预测期与会计调整未统一`,
        summary: d => `${d.t}｜TTM ${pe(d.q[1])}｜Forward ${pe(d.q[2])}｜${d.quoteDate}`,
        labels: ['MU', 'ADBE', 'ST', 'GOOGL', 'AMZN', 'NVDA', 'ASML', 'AVGO', 'SMCI', 'AEP']
      };
    } else {
      rows = all.filter(d => d.k && d.mdd != null);
      cfg = {
        x: d => -d.mdd, y: d => d.u36[0], cat: d => defenseNames.indexOf(d.defense), range: d => d.u36,
        xlabel: '过去一年最大收盘回撤深度（%）', ylabel: '突破三年条件回报（%）',
        text: d => `${d.t} ${d.n}\n经营防御 ${d.defense}｜现价防御 ${d.priceDefense}\n一年最大回撤 ${fmt(d.mdd)}\n悲观三年 ${range(d.d36)}\n基准三年 ${range(d.b36)}\n突破三年 ${range(d.u36)}\n关键业务：${d.upside}`,
        summary: d => `${d.t}｜经营防御 ${d.defense}｜最大回撤 ${fmt(d.mdd)}｜突破 ${range(d.u36)}`,
        labels: data.selected
      };
    }
    legendButtons(view === 'risk' ? defenseNames.map(x => `经营防御：${x}`) : categoryNames, i => rows.filter(d => cfg.cat(d) === i).length);
    redraw = () => {
      plot.replaceChildren();
      const width = Math.max(1, plot.getBoundingClientRect().width);
      const height = width < 430 ? 410 : 460;
      const frame = {l: 76, r: width - 18, t: 20, b: height - 70};
      let xd = padded(rows.map(cfg.x), .085, cfg.xlog);
      let yd = padded(rows.flatMap(d => cfg.range ? cfg.range(d) : [cfg.y(d)]).concat(view === 'momentum' ? [0] : view === 'risk' ? [100] : []), .085, cfg.ylog);
      if (view === 'valuation') xd = yd = padded(rows.flatMap(d => [cfg.x(d), cfg.y(d)]), .085, true);
      const x = (cfg.xlog ? d3.scaleLog() : d3.scaleLinear()).domain(xd).range([frame.l + 7, frame.r - 7]);
      const y = (cfg.ylog ? d3.scaleLog() : d3.scaleLinear()).domain(yd).range([frame.b - 7, frame.t + 7]);
      const svg = makeSvg(plot, width, height, root.querySelector('h3').textContent, `${rows.length}家公司。${cfg.xlabel}；${cfg.ylabel}。点可选择查看完整条件范围。条件回报不是收益预测或最大损失。`);
      const xf = view === 'momentum' ? v => `${Math.round((v - 1) * 100)}%` : view === 'valuation' ? v => `${v < 1 ? v.toFixed(1) : v}` : v => `${v}%`;
      axes(svg, x, y, frame, cfg.xlabel, cfg.ylabel, xf, view === 'valuation' ? v => `${v < 1 ? v.toFixed(1) : v}` : v => `${v}%`, cfg.xlog ? logTicks(xd, width) : undefined, cfg.ylog ? logTicks(yd, width) : undefined);
      if (view === 'valuation') {
        svg.append('line').attr('x1', x(xd[0])).attr('y1', y(xd[0])).attr('x2', x(xd[1])).attr('y2', y(xd[1])).attr('stroke', 'var(--border)');
      } else {
        const ref = view === 'risk' ? 100 : 0;
        svg.append('line').attr('x1', frame.l).attr('x2', frame.r).attr('y1', y(ref)).attr('y2', y(ref)).attr('stroke', 'var(--border)');
        if (view === 'momentum' && xd[0] < 1 && xd[1] > 1) svg.append('line').attr('x1', x(1)).attr('x2', x(1)).attr('y1', frame.t).attr('y2', frame.b).attr('stroke', 'var(--border)');
      }
      const visible = rows.filter(d => active.has(cfg.cat(d)));
      if (cfg.range) svg.append('g').selectAll('line').data(visible).join('line').attr('x1', d => x(cfg.x(d))).attr('x2', d => x(cfg.x(d))).attr('y1', d => y(cfg.range(d)[0])).attr('y2', d => y(cfg.range(d)[1])).attr('stroke', d => color(cfg.cat(d))).attr('stroke-width', 2).attr('opacity', .45);
      svg.append('g').selectAll('circle').data(visible).join('circle').attr('class', 'observation').attr('data-ticker', d => d.t).attr('cx', d => x(cfg.x(d))).attr('cy', d => y(cfg.y(d))).attr('r', d => d.k ? 5 : 3.5).attr('fill', d => color(cfg.cat(d))).attr('opacity', d => d.k ? 1 : .67).attr('stroke', d => d.t === selected ? 'var(--foreground)' : 'none').append('title').text(cfg.text);
      for (const ticker of cfg.labels) {
        const d = visible.find(d => d.t === ticker);
        if (!d) continue;
        const px = x(cfg.x(d)), py = y(cfg.y(d));
        const right = px < (frame.l + frame.r) / 2;
        svg.append('text').attr('class', 'direct-ticker').attr('x', px + (right ? 8 : -8)).attr('y', py - 6).attr('text-anchor', right ? 'start' : 'end').text(d.t);
      }
      const focus = svg.append('circle').attr('r', 8).attr('fill', 'none').attr('stroke', 'var(--foreground)').attr('visibility', 'hidden');
      const nearest = event => {
        const [px, py] = d3.pointer(event, svg.node());
        let best, bestDistance = Infinity;
        for (const d of visible) {
          const yy = cfg.range ? Math.max(y(cfg.range(d)[1]), Math.min(y(cfg.range(d)[0]), py)) : y(cfg.y(d));
          const distance = Math.hypot(x(cfg.x(d)) - px, yy - py);
          if (distance < bestDistance) {best = d; bestDistance = distance;}
        }
        return best;
      };
      svg.append('rect').attr('data-chart-hit', '').attr('data-chart-hover-overlay', 'nearest-point').attr('x', frame.l).attr('y', frame.t).attr('width', frame.r - frame.l).attr('height', frame.b - frame.t).attr('fill', 'transparent').on('pointermove', event => {
        const d = nearest(event); if (!d) return;
        focus.attr('cx', x(cfg.x(d))).attr('cy', y(cfg.y(d))).attr('visibility', 'visible'); tooltip(cfg.text(d), event);
      }).on('pointerleave', () => {tip.style.display = 'none'; focus.attr('visibility', 'hidden');}).on('click', event => {
        const d = nearest(event); if (d) pin(d, cfg.summary(d));
      });
      tidy(svg, frame);
    };
    const first = rows.find(d => d.t === 'ADBE') || rows[0];
    detail.textContent = cfg.summary(first);
    redraw();
  }
  function performance() {
    const selectedRows = data.selected.map(t => all.find(d => d.t === t));
    const rows = selectedRows.concat(data.benchmarks);
    const titles = ['最近3个月', '最近半年', '最近一年'];
    legend.textContent = '同一美元证券 · 股价涨跌幅，不含现金分配 · 指数ETF列于底部';
    const domain = padded(rows.flatMap(d => d.p).concat([0]), .1);
    redraw = () => {
      plot.replaceChildren();
      titles.forEach((title, j) => {
        const panel = document.createElement('div'); panel.className = 'facet'; plot.append(panel);
        const heading = document.createElement('div'); heading.className = 'panel-title'; heading.textContent = title; panel.append(heading);
        const width = Math.max(1, panel.getBoundingClientRect().width);
        const height = rows.length * 24 + 90;
        const frame = {l: 66, r: width - 16, t: 14, b: height - 66};
        const x = d3.scaleSymlog().constant(30).domain(domain).range([frame.l + 7, frame.r - 7]);
        const y = d3.scalePoint().domain(rows.map(d => d.t)).range([frame.t + 18, frame.b - 12]);
        const svg = makeSvg(panel, width, height, title, '20家公司及SPY、QQQ、SMH的同日累计价格收益。横轴使用有符号对数压缩，不改变标注数值。');
        const ticks = [-50, 0, 100, 600].filter(v => v >= domain[0] && v <= domain[1]);
        axes(svg, x, y, frame, '股价涨跌幅（%，压缩刻度）', '公司 / ETF', v => `${v}%`, v => v, ticks, rows.map(d => d.t));
        svg.append('line').attr('x1', x(0)).attr('x2', x(0)).attr('y1', frame.t).attr('y2', frame.b).attr('stroke', 'var(--border)');
        rows.forEach(d => {
          const value = d.p[j], yy = y(d.t), xx = x(value);
          svg.append('line').attr('x1', x(0)).attr('x2', xx).attr('y1', yy).attr('y2', yy).attr('stroke', d.k ? color(j) : 'var(--foreground)').attr('stroke-width', 3).attr('opacity', d.k ? .78 : .55);
          svg.append('circle').attr('cx', xx).attr('cy', yy).attr('r', 3).attr('fill', d.k ? color(j) : 'var(--foreground)');
          const right = xx + 54 < frame.r;
          svg.append('text').attr('x', xx + (right ? 7 : -7)).attr('y', yy - 6).attr('text-anchor', right ? 'start' : 'end').text(fmt(value));
        });
        const hit = svg.append('rect').attr('data-chart-hit', '').attr('data-chart-hover-overlay', 'nearest-point').attr('x', frame.l).attr('y', frame.t).attr('width', frame.r - frame.l).attr('height', frame.b - frame.t).attr('fill', 'transparent');
        const near = event => {const [, py] = d3.pointer(event, svg.node()); return rows.reduce((a,b) => Math.abs(y(a.t)-py) < Math.abs(y(b.t)-py) ? a : b);};
        const msg = d => `${d.t}｜3个月 ${fmt(d.p[0])}｜半年 ${fmt(d.p[1])}｜一年 ${fmt(d.p[2])}`;
        hit.on('pointermove', event => tooltip(msg(near(event)), event)).on('pointerleave', () => tip.style.display = 'none').on('click', event => pin(near(event), msg(near(event))));
        tidy(svg, frame);
      });
    };
    detail.textContent = '价格窗口：2026-06-09 / 2026-03-09 / 2025-09-09 → 2026-09-09';
    redraw();
  }
  function sectors() {
    const rows = all.filter(d => d.sameDay && d.b36);
    const months = [6,12,36];
    const groups = data.sectors;
    const annual = (d, m) => {const r=d[`b${m}`]; return 100*(Math.pow(1+(r[0]+r[1])/200,12/m)-1);};
    const domain = padded(rows.flatMap(d => months.map(m => annual(d,m))).concat([0,12]), .07);
    legend.textContent = '细线：最小至最大 · 粗线：25%—75%分位 · 圆点：中位数 · 竖线：年化12%';
    redraw = () => {
      plot.replaceChildren();
      months.forEach((m,j) => {
        const panel = document.createElement('div'); panel.className='facet'; plot.append(panel);
        const heading=document.createElement('div'); heading.className='panel-title'; heading.textContent=m===6?'6个月（机械年化）':m===12?'12个月':'36个月（年化）'; panel.append(heading);
        const width=Math.max(1,panel.getBoundingClientRect().width), height=groups.length*33+90;
        const frame={l:120,r:width-16,t:16,b:height-64};
        const x=d3.scaleLinear().domain(domain).range([frame.l+7,frame.r-7]);
        const y=d3.scalePoint().domain(groups.map(d=>d.short)).range([frame.t+12,frame.b-12]);
        const svg=makeSvg(panel,width,height,heading.textContent,'191家公司按行业分组。先计算每家公司基准条件区间中点的机械年化，再展示跨公司分布；区间中点不是期望回报。');
        axes(svg,x,y,frame,'基准区间中点年化（%）','行业',v=>`${v}%`,v=>v,undefined,groups.map(d=>d.short));
        svg.append('line').attr('x1',x(12)).attr('x2',x(12)).attr('y1',frame.t).attr('y2',frame.b).attr('stroke','var(--foreground)').attr('opacity',.35);
        const summary=[];
        groups.forEach(group=>{
          const member=rows.filter(d=>d.s===group.name), values=member.map(d=>annual(d,m)).sort(d3.ascending);
          const [low,high]=d3.extent(values), q1=d3.quantile(values,.25), med=d3.median(values), q3=d3.quantile(values,.75), yy=y(group.short);
          svg.append('line').attr('x1',x(low)).attr('x2',x(high)).attr('y1',yy).attr('y2',yy).attr('stroke',color(j)).attr('opacity',.55);
          svg.append('line').attr('x1',x(q1)).attr('x2',x(q3)).attr('y1',yy).attr('y2',yy).attr('stroke',color(j)).attr('stroke-width',7).attr('opacity',.5);
          svg.append('circle').attr('cx',x(med)).attr('cy',yy).attr('r',4).attr('fill',color(j));
          summary.push({t:group.short,yy,text:`${group.short}｜${member.length}家公司｜${m}个月\n基准中点机械年化：中位数 ${fmt(med)}\n25%—75%分位 ${fmt(q1)}～${fmt(q3)}\n最低 ${fmt(low)}｜最高 ${fmt(high)}`});
        });
        const nearest=event=>{const [,py]=d3.pointer(event,svg.node());return summary.reduce((a,b)=>Math.abs(a.yy-py)<Math.abs(b.yy-py)?a:b);};
        svg.append('rect').attr('data-chart-hit','').attr('data-chart-hover-overlay','nearest-point').attr('x',frame.l).attr('y',frame.t).attr('width',frame.r-frame.l).attr('height',frame.b-frame.t).attr('fill','transparent').on('pointermove',event=>tooltip(nearest(event).text,event)).on('pointerleave',()=>tip.style.display='none').on('click',event=>{detail.textContent=nearest(event).text.replaceAll('\n','｜');});
        tidy(svg,frame);
      });
    };
    detail.textContent='191家公司｜9月9日报价机械重算｜中点及跨公司分位都不是概率加权预期';
    redraw();
  }
  if(view==='performance') performance(); else if(view==='sectors') sectors(); else scatter();
  let lastWidth=root.getBoundingClientRect().width;
  new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-lastWidth)>1){lastWidth=width;clearTimeout(timer);timer=setTimeout(()=>redraw(),80);}}).observe(root);
}
