# 业务资料协议

票价区编号0、1、2，合成线路互通且相邻票价区均为合法路径。区间票价按跨区数量，联程减价不低于零，乘客资助按该程普通优惠后金额计算，日封顶作用于covered_lines，补贴报销只认subsidized_lines。营业日从04:00开始，日封顶不因联营承运方而重复建立。路径候选是可行范围而非唯一恢复答案。个人退款与联营清算使用不同回执，禁止以清算是否到账替代个人已付状态。

所有数字、身份和业务来件均为合成。记录的稳定编号只在对应表内唯一，跨表关联以明确字段为准。布尔值为原来源明确回报，空字符串引用表示没有已知对应。金额如有均用整数分，比例为0至1，其他单位在字段中注明。

## riders

仅在票务用途内可链接的匿名乘客资质。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| category | string | ordinary、student或assisted |
| valid_from | string | 资质生效日 |
| valid_to | string | 资质失效日 |
| tokens | array | 本用途允许链接的票卡键 |

## fare_contracts

联营票价与资金约定；金额单位分。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| operator | string | 承运方 |
| valid_from | string | 生效日 |
| valid_to | string | 终止日 |
| base_minor | number | 普通单程基本票价 |
| per_zone_minor | number | 每跨一个票价区加价 |
| transfer_minutes | number | 联程允许换乘分钟 |
| transfer_discount_minor | number | 符合换乘的该程减价 |
| daily_cap_minor | number | 该合同日封顶分 |
| covered_lines | array | 封顶包含的线路 |
| subsidized_lines | array | 财政资助认可线路 |
| student_share | number | 学生对基础应收的支付比例 |
| assisted_share | number | 资助类乘客对基础应收的支付比例 |
| fund_limit_minor | number | 本期该方资助额度分 |
| shared_interaction | string | 叠加交互减免的分担约定 |
| business_day_start_hour | number | 营业日开始小时 |

## journeys

乘车原件；缺失出站只提供合法目的区候选。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| rider_id | string | 乘客用途键 |
| token | string | 乘车时票卡键 |
| line | string | 线路 |
| operator | string | 实际承运方 |
| entered_at | string | 入站或上车时点 |
| exit_at | nullable_string | 出站时点，空值为未知 |
| known_at | string | 此版本获知时间 |
| origin_zone | number | 入站票价区 |
| destination_options | array | 资料能支持的合法目的区候选 |
| chain_hint | string | 联程线索，仍须核实有效时限 |
| receipt_key | string | 原扣款编号 |

引用关系：rider_id 对应 riders.id。

## charges

乘客实际扣款，不代表最终应收。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| journey_id | string | 原行程 |
| at | string | 扣款时点 |
| known_at | string | 扣款获知时间 |
| charged_minor | number | 实际扣款分 |

引用关系：journey_id 对应 journeys.id。

## late_exits

后补的原始出站证明。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| journey_id | string | 被补全的行程 |
| exit_at | string | 实际出站时点 |
| known_at | string | 证明收到时间 |
| destination_zone | number | 证明的目的区 |

引用关系：journey_id 对应 journeys.id。

## refund_receipts

已付个人退款原件。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| charge_id | string | 退款对应的原扣款 |
| amount_minor | number | 已退款分 |
| paid_at | string | 已经支付的时点 |
| status | string | paid或pending |

引用关系：charge_id 对应 charges.id。

## settlements

已确认与在途联营清算。

| 字段 | 格式 | 含义 |
| --- | --- | --- |
| id | string | 记录的稳定编号 |
| operator | string | 承运方 |
| period_start | string | 期初 |
| period_end | string | 期末 |
| confirmed_minor | number | 原确认的资助额分 |
| adjustment_allowed | boolean | 下期是否允许本合同差额调整 |
| confirmed_at | string | 确认时点 |
