const cfg = [
  {
    "g": [
      [
        -0.01,
        -0.06,
        0.025,
        0.08,
        -0.1
      ],
      [
        -0.03,
        -0.09,
        0,
        0.03,
        -0.08
      ],
      [
        -0.02,
        -0.08,
        0,
        0.02,
        -0.07
      ],
      [
        0,
        -0.05,
        0.01,
        0.02,
        -0.05
      ],
      [
        0.01,
        -0.03,
        0.02,
        0.02,
        -0.03
      ]
    ],
    "gm": [
      0.88,
      0.87,
      0.865,
      0.865,
      0.87
    ],
    "margin": [
      0.315,
      0.285,
      0.27,
      0.265,
      0.27
    ],
    "buy": [
      4,
      3,
      2,
      2,
      2
    ],
    "price": [
      230,
      210,
      200,
      190,
      190
    ],
    "w": [
      0.105,
      0.125
    ],
    "tail": -0.01
  },
  {
    "g": [
      [
        0.11,
        0.04,
        0.11,
        0.95,
        -0.06
      ],
      [
        0.105,
        0.045,
        0.11,
        0.14,
        -0.06
      ],
      [
        0.1,
        0.045,
        0.1,
        0.13,
        -0.05
      ],
      [
        0.085,
        0.035,
        0.085,
        0.1,
        -0.04
      ],
      [
        0.07,
        0.03,
        0.07,
        0.08,
        -0.03
      ]
    ],
    "gm": [
      0.89,
      0.89,
      0.89,
      0.89,
      0.89
    ],
    "margin": [
      0.355,
      0.36,
      0.365,
      0.365,
      0.365
    ],
    "buy": [
      7,
      7,
      7,
      7,
      7
    ],
    "price": [
      285,
      315,
      350,
      385,
      415
    ],
    "w": [
      0.09,
      0.11
    ],
    "tail": 0.025
  },
  {
    "g": [
      [
        0.15,
        0.07,
        0.16,
        1.1,
        -0.05
      ],
      [
        0.14,
        0.075,
        0.17,
        0.2,
        -0.04
      ],
      [
        0.13,
        0.07,
        0.16,
        0.18,
        -0.03
      ],
      [
        0.11,
        0.06,
        0.13,
        0.15,
        -0.02
      ],
      [
        0.09,
        0.05,
        0.11,
        0.12,
        -0.02
      ]
    ],
    "gm": [
      0.887,
      0.888,
      0.888,
      0.89,
      0.89
    ],
    "margin": [
      0.36,
      0.37,
      0.38,
      0.385,
      0.385
    ],
    "buy": [
      7.5,
      8,
      8.5,
      9,
      9
    ],
    "price": [
      320,
      390,
      470,
      550,
      630
    ],
    "w": [
      0.09,
      0.11
    ],
    "tail": 0.03
  },
  {
    "g": [
      [
        0.16,
        0.09,
        0.19,
        1.15,
        -0.05
      ],
      [
        0.18,
        0.12,
        0.22,
        0.24,
        -0.03
      ],
      [
        0.18,
        0.14,
        0.23,
        0.25,
        -0.02
      ],
      [
        0.15,
        0.12,
        0.19,
        0.2,
        -0.01
      ],
      [
        0.12,
        0.09,
        0.15,
        0.16,
        -0.01
      ]
    ],
    "gm": [
      0.88,
      0.877,
      0.875,
      0.88,
      0.885
    ],
    "margin": [
      0.345,
      0.35,
      0.365,
      0.38,
      0.385
    ],
    "buy": [
      6,
      6,
      7,
      8,
      9
    ],
    "price": [
      330,
      440,
      580,
      730,
      870
    ],
    "w": [
      0.095,
      0.115
    ],
    "tail": 0.03
  }
];
const core0 = [7.46,12.04,5.92,0.28,0.85];
const opportunities = [
  {
    "id": "F",
    "name": "新增品牌生产/Foundry工作流",
    "scale": [
      0.15,
      0.5,
      1.1,
      1.9,
      2.8,
      3.6,
      4.3,
      4.9,
      5.4,
      5.8
    ],
    "partial": 0.22,
    "costU": [
      0.08,
      0.1,
      0.09,
      0.07,
      0.06,
      0.05,
      0.045,
      0.04,
      0.035,
      0.03
    ],
    "gm": 0.7,
    "opex": 0.24,
    "cap": 0.03
  },
  {
    "id": "A",
    "name": "新增自主文档代理净升级",
    "scale": [
      0.08,
      0.3,
      0.75,
      1.4,
      2.2,
      3,
      3.8,
      4.5,
      5.1,
      5.6
    ],
    "partial": 0.25,
    "costU": [
      0.07,
      0.09,
      0.1,
      0.09,
      0.07,
      0.065,
      0.06,
      0.05,
      0.04,
      0.035
    ],
    "gm": 0.76,
    "opex": 0.27,
    "cap": 0.02
  },
  {
    "id": "G",
    "name": "新增GEO闭环合同",
    "scale": [
      0.05,
      0.16,
      0.38,
      0.7,
      1.1,
      1.5,
      1.9,
      2.2,
      2.5,
      2.7
    ],
    "partial": 0.28,
    "costU": [
      0.035,
      0.05,
      0.05,
      0.04,
      0.03,
      0.03,
      0.025,
      0.025,
      0.02,
      0.02
    ],
    "gm": 0.73,
    "opex": 0.3,
    "cap": 0.02
  }
];
function opportunity(op,s,forced=false) {
 let p=[1,0,0,0],rows=[];
 const speeds=[.7,1,1.35,1.65], speed=speeds[s]*(op.id==="A"?.78:op.id==="G"?1.12:1);
 for(let y=0;y<10;y++){
  let up=Math.min(.55,.24*speed),uf=[.13,.065,.045,.03][s],ps=Math.min(.50,.22*speed),pf=[.18,.085,.055,.035][s],sf=[.15,.065,.045,.03][s];
  let n=[p[0]*(1-up-uf),p[0]*up+p[1]*(1-ps-pf),p[1]*ps+p[2]*(1-sf),p[3]+p[0]*uf+p[1]*pf+p[2]*sf];
  if(forced) n=y===0?[0,1,0,0]:[0,0,1,0];
  let newFailure=Math.max(0,n[3]-p[3]); p=n;
  const mult=[.65,1,1.35,1.8][s], r=op.scale[y]*mult;
  // each state incremental net revenue; success costs include deployment and shared capacity allocation
  let rev=[0,r*op.partial,r,0],ebit=[-op.costU[y],rev[1]*(op.gm-.40)-op.costU[y]*.5,rev[2]*(op.gm-op.opex)-op.costU[y]*.30,p[3]>0?-.04*newFailure/p[3]:0];
  let cash=ebit.map((e,k)=>e*.78-rev[k]*(op.cap+.015));
  rows.push({p:[...p],rev,ebit,cash,R:p.reduce((a,x,k)=>a+x*rev[k],0),E:p.reduce((a,x,k)=>a+x*ebit[k],0),CF:p.reduce((a,x,k)=>a+x*cash[k],0)});
 }
 return rows;
}
function model(s,options={}) {
 const c=cfg[s], opps=opportunities.map(o=>opportunity(o,s,options.force===o.id));
 let core=core0.slice(), rows=[],cash=5.626,debt=6.645,shares=.4015;
 for(let y=0;y<5;y++){
  core=core.map((v,k)=>v*(1+c.g[y][k]));
  if(options.ordinary){core[0]*=y===0?.99:1;core[1]*=y===0?.97:.99;core[2]*=y===0?.99:1;}
  let cr=core.reduce((a,b)=>a+b,0),R=cr+opps.reduce((a,o)=>a+o[y].R,0);
  let margin=c.margin[y]-(options.ordinary?.015:0),ebit=cr*margin+opps.reduce((a,o)=>a+o[y].E,0);
  let sbc=cr*.081,da=cr*.024,cap=cr*.012,wc=(s===0?-.20:.18)*(y===0?1:.5);
  let cf=cr*margin*.78+da-cap+wc+opps.reduce((a,o)=>a+o[y].CF,0);
  let interest=(debt*.045-cash*.025)*.78, fcf=cf+sbc-interest, buy=c.buy[y],price=c.price[y];
  if(cash+fcf-buy<4) buy=Math.max(sbc,cash+fcf-4);
  cash+=fcf-buy; shares+=(sbc-buy)/price;
  rows.push({core:[...core],cr,R,gm:cr*c.gm[y]+opps.reduce((a,o,k)=>a+o[y].R*opportunities[k].gm,0),ebit,sbc,da,cap,wc,cf,fcf,interest,buy,price,cash,debt,shares});
 }
 // Y6-Y10 extend cash from year5 with core deceleration; opportunity survivals embedded at group tail no probability reset
 const gs=s===0?[-.02,-.02,-.015,-.01,-.01]:s===1?[.065,.055,.045,.035,.025]:s===2?[.09,.075,.06,.045,.03]:[.115,.09,.065,.045,.03];
 let cfs=rows.map(r=>r.cf);
 let coreCF=rows[4].cf-opps.reduce((a,o)=>a+o[4].CF,0);
 gs.forEach((g,i)=>{coreCF*=1+g;cfs.push(coreCF+opps.reduce((a,o)=>a+o[i+5].CF,0));});
 if(options.fade){for(let y=5;y<10;y++)cfs[y]=cfs[y-1]*.96;}
 const tail=options.fade?-.02:c.tail;
 const rw=s===0?[.26,.255,.245,.24]:[.237,.245,.255,.263];
 const fw=[.25,.30,.23,.22];
 function capAt(t){
  if(t===0)return{cash:5.626,debt:6.645,shares:.4015};
  let n=Math.floor(t),f=t-n,prev=n===0?{cash:5.626,debt:6.645,shares:.4015}:rows[n-1];
  if(f===0)return prev;let next=rows[n];
  let q=Math.round(f*4),cum=fw.slice(0,q).reduce((a,b)=>a+b,0);
 return{cash:prev.cash+cum*next.fcf-f*next.buy,debt:6.645,shares:prev.shares+f*(next.shares-prev.shares)};
 }
 function value(t,w){
  let ev=0, terminal=0;
  // annual end discount; current partial year residual included with actual fractional share of annual flow
  for(let i=0;i<10;i++) for(let q=0;q<4;q++){let qt=i+(q+1)/4;if(qt>t)ev+=cfs[i]*fw[q]/(1+w)**(qt-t);}
  terminal=cfs[9]*(1+tail)/(w-tail)/(1+w)**(10-t);
  ev+=terminal;let cap=capAt(t);
  return{v:(ev+cap.cash-cap.debt)/cap.shares,ev,equity:ev+cap.cash-cap.debt,terminalShare:terminal/ev,...cap};
 }
 let vals=[.25,.5,1,3].map(t=>({t,low:value(t,c.w[1]),high:value(t,c.w[0]),mid:value(t,(c.w[0]+c.w[1])/2)}));
 const quarters=rw.map((weight,q)=>{let r=rows[0];let gp=r.gm*weight,ebit=gp-(r.gm-r.ebit)/4;return{R:r.R*weight,GP:gp,EBIT:ebit,CF:r.cf*fw[q],SBC:r.sbc/4,DA:r.da/4,Capex:r.cap/4,FCF:r.fcf*fw[q],buy:r.buy/4};});
 return {s,rows,opps,cfs,vals,quarters};
}
const P0 = 254.86;
const results = cfg.map((_, s) => model(s));
for (const m of results) {
  for (const opportunityYears of m.opps) {
    let lastFailure = 0;
    for (const y of opportunityYears) {
      if (Math.abs(y.p.reduce((a,b)=>a+b,0)-1)>1e-9) throw Error("probability sum");
      if (y.p.some(p=>p<0) || y.p[3]<lastFailure-1e-9) throw Error("invalid state");
      lastFailure = y.p[3];
    }
  }
  console.log(JSON.stringify({
    scenario:m.s,annual:m.rows,quarters:m.quarters,
    opportunities:m.opps,FCFF:m.cfs,
    valuation:m.vals.map(v=>({
      years:v.t,low:v.low,high:v.high,mid:v.mid,
      totalReturn:[v.low.v/P0-1,v.high.v/P0-1],
      annualized:[(v.low.v/P0)**(1/v.t)-1,(v.high.v/P0)**(1/v.t)-1]
    }))
  }));
}
console.log("ordinary",JSON.stringify(model(1,{ordinary:true})));
console.log("cash-life alternative",JSON.stringify(model(1,{fade:true})));
for (const op of opportunities)
  console.log("single success "+op.id,JSON.stringify(model(1,{force:op.id})));
