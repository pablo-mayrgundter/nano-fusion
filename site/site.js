/* Hover layer for the screening chart: a crosshair and one tooltip that lists every fuel.
   The chart itself is static SVG written by sim/plot_pair_fusion.py; this only adds reading aids. */
(function () {
  var dataEl = document.getElementById('pf-data');
  if (!dataEl) return;
  var data = JSON.parse(dataEl.textContent);
  var SUP = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
  var BAND = [Math.log10(2e-11), Math.log10(2e-7)];

  function p10(v) {
    return '10' + String(Math.round(v)).replace(/[-0-9]/g, function (c) { return SUP[c]; });
  }
  function rateAt(series, lam) {
    var l = data.lams;
    if (lam <= l[0]) return series[0];
    for (var i = 0; i < l.length - 1; i++) {
      if (lam <= l[i + 1]) {
        var t = Math.log(lam / l[i]) / Math.log(l[i + 1] / l[i]);
        return series[i] + t * (series[i + 1] - series[i]);
      }
    }
    return series[series.length - 1];
  }
  function fmtLam(lam) {
    return (lam < 1 ? lam.toFixed(2) : lam < 10 ? lam.toFixed(1) : lam.toFixed(0)) + ' pm';
  }

  Array.prototype.forEach.call(document.querySelectorAll('svg.pf-chart'), function (svg) {
    var g = svg.dataset, left = +g.left, top = +g.top, w = +g.w, h = +g.h;
    var xlo = +g.xlo, xhi = +g.xhi, vw = +g.vw, lamMin = data.lams[0];
    var wrap = svg.closest('.pf-wrap'), tip = wrap.querySelector('.pf-tip'), cross = svg.querySelector('.pf-cross');
    var current = null;

    function show(lam) {
      lam = Math.min(Math.pow(10, xhi), Math.max(lamMin, lam));
      current = lam;
      var x = left + (Math.log10(lam) - xlo) / (xhi - xlo) * w;
      cross.setAttribute('x1', x); cross.setAttribute('x2', x);
      cross.setAttribute('y1', top); cross.setAttribute('y2', top + h);
      cross.setAttribute('visibility', 'visible');
      while (tip.firstChild) tip.removeChild(tip.firstChild);
      var head = document.createElement('div');
      head.className = 'h';
      head.textContent = 'screening length ' + fmtLam(lam);
      tip.appendChild(head);
      var inBand = [];
      data.fuels.forEach(function (name, k) {
        var v = rateAt(data.series[k], lam);
        var row = document.createElement('div');
        row.className = 'r';
        var dot = document.createElement('i');
        dot.style.setProperty('--c', 'var(--s' + (k + 1) + ')');
        var label = document.createElement('span');
        label.textContent = name;
        var val = document.createElement('b');
        val.textContent = p10(v) + ' /s';
        row.appendChild(dot); row.appendChild(label); row.appendChild(val);
        tip.appendChild(row);
        if (v >= BAND[0]) inBand.push(name);
      });
      var note = document.createElement('div');
      note.className = 'n';
      note.textContent = inBand.length ? 'enough for a battery: ' + inBand.join(', ') : 'not enough for a battery';
      tip.appendChild(note);
      tip.classList.add('on');
      var box = svg.getBoundingClientRect(), outer = wrap.getBoundingClientRect();
      var px = box.left - outer.left + x * box.width / vw;
      var tw = tip.offsetWidth, room = outer.width - tw - 2;
      var lx = px + 14;
      if (lx > room) lx = px - tw - 14;
      tip.style.left = Math.max(0, Math.min(room, lx)) + 'px';
      tip.style.top = (box.top - outer.top + (top + 8) * box.height / (+g.vh)) + 'px';
    }
    function hide() {
      current = null;
      cross.setAttribute('visibility', 'hidden');
      tip.classList.remove('on');
    }
    function fromPointer(e) {
      var box = svg.getBoundingClientRect();
      var x = (e.clientX - box.left) * vw / box.width;
      if (x < left - 4 || x > left + w + 4) { hide(); return; }
      show(Math.pow(10, xlo + (x - left) / w * (xhi - xlo)));
    }
    svg.addEventListener('pointermove', fromPointer);
    svg.addEventListener('pointerdown', fromPointer);
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hide(); });
    svg.addEventListener('focus', function () { if (current === null) show(1.5); });
    svg.addEventListener('blur', hide);
    svg.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 1.25 : 1.06;
      if (e.key === 'ArrowLeft') { show((current || 1.5) / step); e.preventDefault(); }
      else if (e.key === 'ArrowRight') { show((current || 1.5) * step); e.preventDefault(); }
      else if (e.key === 'Escape') { hide(); }
    });
  });
})();
