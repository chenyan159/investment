"""只用报告参数做能力/敏感性测试，不输出概率预测，不修改任何正式资料。"""
from pathlib import Path
import json, math

OUT=Path(__file__).parent
tests=[]
def add(name,inputs,results,meaning,limit):
    tests.append(dict(name=name,inputs=inputs,results=results,meaning=meaning,limit=limit))

# MU原文282—305：以FY2026Q3技术收入为基准。
mu_r0=4*31.328
mu_base=mu_r0*1.25
mu_more=mu_r0*1.35
mu_more_lower_price=mu_more*.90
assert math.isclose(mu_more-mu_base,12.5312)
assert math.isclose(mu_more_lower_price-mu_base,-4.38592)
add('MU：供给超预期与价格联动',
    {'DRAM_quarter_revenue_B':31.328,'base_delivery_index':1.25,'report_demand_index':1.35,'test_supply_index':1.35},
    {'base_DRAM_revenue_B':mu_base,'higher_supply_same_price_B':mu_more,'revenue_delta_B':mu_more-mu_base,'higher_supply_price_down_10pct_B':mu_more_lower_price,'joint_delta_B':mu_more_lower_price-mu_base,'revenue_breakeven_price_decline_pct':100*(1-1.25/1.35)},
    '产能增量不是单向利好，必须同时研究竞争扩产和合同价格传导；原文min公式在需求增加而供给不变时不产生销量增量。',
    '1.35的需求是报告假设，测试把供给提高到该值；10%降价是试验值。没有证明这一供给与价格组合会发生。未计算利润，因为DRAM单独成本未披露。')

# SNDK原文374—389：FY2026基准、FY2027指数。
sd_base=20.248*1.15*1.82
sd_up=20.248*1.25*1.82
sd_same_income=sd_up*.92
assert math.isclose(sd_base,42.379064)
assert math.isclose(sd_same_income,sd_base)
add('SNDK：超预期交付为何可能不超预期收入',
    {'base_revenue_B':20.248,'base_volume_index':1.15,'base_price_index':1.82,'test_volume_index':1.25},
    {'base_revenue_B':sd_base,'more_volume_same_price_B':sd_up,'delta_B':sd_up-sd_base,'price_decline_erasing_revenue_gain_pct':8.0,'after_8pct_price_decline_B':sd_same_income},
    '对量增和价格下降的可行联动缺少单独研究；同一收入也不等于同一利润，因为更多bit有生产成本。',
    '1.25是审阅者假设而非产能事实。没有把它用作预测上沿，也没有假设NBM全部可重定价。')

# GOOGL原文245—251，当前报告只示范50万/100万单周运行率。
add('GOOGL Waymo：从近期运行率延伸至经济重要性门槛',
    {'report_weekly_rides':1_000_000,'report_test_net_fare_range_USD':[20,35],'report_test_contribution_per_ride_USD':5,'audit_target_annual_contribution_B':1},
    {'report_annual_revenue_range_B':[1_000_000*52*20/1e9,1_000_000*52*35/1e9],'annual_contribution_B':1_000_000*52*5/1e9,'weekly_rides_needed_for_1B_contribution':1e9/52/5,'growth_multiple_from_1M_weekly':(1e9/52/5)/1_000_000},
    '报告已有单位经济，可继续识别多大规模才改变公司经济结果；需要车辆日、城市密度、许可、固定成本与Alphabet权益桥。',
    '5美元贡献是原报告示意假设，未扣城市固定费及持续研发；1B是经济重要性压力标尺，不是公司应达到的目标。未给估值。')

# CRDO原文213及369，不重复加入已包含的未来产品池。
add('CRDO OmniConnect：一个已经出现的正面研究样本',
    {'assumed_adopting_XPUs':50_000,'assumed_content_per_XPU_USD':2000,'report_FY2028_ALC_and_OmniConnect_combined_B':.07},
    {'conditional_revenue_B':50_000*2000/1e9,'at_10000_XPUs_B':10_000*2000/1e9,'FY2028_group_central_B':3.2},
    '新品已有条件规模，不应把所有报告归为只会写NA。但该单一算例与2028合并70M分配、被替代连接及增量利润仍没有完整对账。',
    '50k和2k均为原报告假设，100M不是新增订单，也不能整笔加在3.2B中心之上。')

# SMCI原文249—257：64B*11%-2.15B。
sm_op=64*.11-2.15
sm_op_test=64*.14-2.15
assert math.isclose(sm_op_test-sm_op,1.92)
add('SMCI：利润率改善是否可能改变结论',
    {'revenue_B':64,'base_GM':.11,'test_GM':.14,'opex_B':2.15},
    {'base_OP_B':sm_op,'test_OP_B':sm_op_test,'delta_OP_B':sm_op_test-sm_op,'delta_OP_pct':100*(sm_op_test/sm_op-1)},
    '需要研究系统责任、客户组合、软件附着与采购成本何时支持不同于中心的利润率；只测试回款改善不会回答这个问题。',
    '14%仅为能力测试，并非推荐中心或概率判断；Q1指引反对机械延用Q4的17.5%，不能因上行敏感就认为应上调预测。')

# GNRC原文222：单位连接净年收入10—30美元。
add('GNRC ecobee：单位连接模型距离重大机会还有多远',
    {'assumed_net_annual_revenue_per_paid_connection_USD':[10,30],'test_annual_revenue_M':100},
    {'paid_connections_needed_range':[100e6/30,100e6/10],'share_of_report_2027_group_revenue_pct':100*.1/5.755},
    '100M收入需333万—1000万真实付费连接；活跃、授权、可调度与付费不可混用。缺少连接池、合同经济和边际成本，无法从潜在GW判断投资重要性。',
    '10—30美元是原报告敏感性变量，100M是审阅压力标尺，不是预测。未给软件倍数。')

out={'purpose':'报告内容能力压力测试，不是重新运行AI或修改prompt后的A/B实验，也不是收益回测。','tests':tests}
(OUT/'能力压力测试.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8-sig')
print(json.dumps(out,ensure_ascii=False,indent=2))
