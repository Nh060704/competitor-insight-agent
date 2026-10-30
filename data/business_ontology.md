# 业务对象数据字典

## 1. 竞品公司 (Competitor)

| 属性 | 类型 | 说明 |
|------|------|------|
| name | string | 公司名称 |
| website | string | 官网地址 |
| industry | string | 所属行业 |
| founded_year | int | 成立年份 |
| employee_count | string | 员工规模 |
| funding_stage | string | 融资阶段 |

**关系：**
- 一个竞品公司 → 拥有多个产品 (Product)
- 一个竞品公司 → 有多个定价方案 (PricingPlan)

---

## 2. 产品 (Product)

| 属性 | 类型 | 说明 |
|------|------|------|
| name | string | 产品名称 |
| description | string | 产品介绍 |
| target_user | string | 目标用户群体 |
| launch_date | date | 发布日期 |
| status | enum | 状态：开发中/已上线/已下线 |

**关系：**
| 一个产品 → 属于一个竞品公司
| 一个产品 → 对应多个定价方案

---

## 3. 定价方案 (PricingPlan)

| 属性 | 类型 | 说明 |
|------|------|------|
| name | string | 方案名称（如：基础版/专业版/企业版） |
| price_monthly | float | 月付价格 |
| price_yearly | float | 年付价格 |
| features | list[string] | 功能列表 |
| user_limit | string | 用户数限制 |

---

## 4. 内容更新 (ContentUpdate)

| 属性 | 类型 | 说明 |
|------|------|------|
| title | string | 更新标题 |
| content | text | 更新内容 |
| publish_date | date | 发布日期 |
| category | enum | 分类：产品更新/功能发布/营销活动/其他 |

---

## 指标口径

- **竞品数量**：当前监控的竞品公司总数
- **采集成功率**：成功采集页面数 / 总请求页面数
- **知识库文档数**：向量库中存储的文档切片总数
