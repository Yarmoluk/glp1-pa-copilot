(() => {
  const map = document.querySelector('.ng-map');
  if (!map) return;
  const svg = map.querySelector('svg');
  const layer = svg.querySelector('.ng-paths');
  const ns = 'http://www.w3.org/2000/svg';
  let frame;
  function draw() {
    const box = map.getBoundingClientRect();
    const mobile = matchMedia('(max-width:800px)').matches;
    const rect = el => {
      const r = el.getBoundingClientRect();
      return {left:r.left-box.left, right:r.right-box.left, top:r.top-box.top,
        bottom:r.bottom-box.top, cy:r.top+r.height/2-box.top};
    };
    const line = (d, arrow = false) => {
      const p = document.createElementNS(ns, 'path');
      Object.entries({d, fill:'none', stroke:'#667f9b', 'stroke-width':'1.5',
        'stroke-linecap':'round', 'stroke-linejoin':'round'}).forEach(([k,v])=>p.setAttribute(k,v));
      if (arrow) p.setAttribute('marker-end','url(#ng-arrow)');
      layer.append(p);
    };
    svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
    layer.replaceChildren();
    const root = rect(document.getElementById('ng-wegovy_start'));
    const children = [...map.querySelectorAll('[data-from="ng-wegovy_start"]')].map(rect);
    const ys = children.map(r=>r.cy);
    const sourceX = mobile ? root.left : root.right;
    const busX = mobile ? 7 : sourceX + (children[0].left-sourceX)*0.42;
    const firstY = Math.min(root.cy,...ys), lastY=Math.max(root.cy,...ys);
    // One shared stem and spine; individual arrows keep every target distinct.
    line(`M ${sourceX} ${root.cy} H ${busX}`);
    line(`M ${busX} ${firstY} V ${lastY}`);
    children.forEach(r=>line(`M ${busX} ${r.cy} H ${r.left-2}`,true));
    const dot=document.createElementNS(ns,'circle');
    Object.entries({cx:busX,cy:root.cy,r:'3',fill:'#667f9b'}).forEach(([k,v])=>dot.setAttribute(k,v));
    layer.append(dot);
    const scope=rect(document.getElementById('ng-adult_weight_management'));
    const bmi=rect(document.getElementById('ng-bmi_30_or_27_with_comorbidity'));
    if(mobile){
      const lane=scope.left+10, bend=bmi.cy-7;
      line(`M ${lane} ${scope.bottom} V ${bend} Q ${lane} ${bmi.cy} ${lane+7} ${bmi.cy} H ${bmi.left-2}`,true);
    }else{
      line(`M ${scope.right} ${scope.cy} H ${bmi.left-2}`,true);
    }
  }
  new ResizeObserver(()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(draw)}).observe(map);
  document.fonts.ready.then(draw);
  window.addEventListener('resize',draw);
  draw();
})();
