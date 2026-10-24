/**
 * 冒烟测试：用假的 ctx 跑一遍插件 apply()，断言注册出来的 skill 定义合法。
 * 不需要启动 DSH，也不需要安装任何依赖。
 *
 *   node test/smoke.mjs
 */
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { apply, name, inject } from '../lib/index.js'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const registered = []
const ctx = {
  skills: {
    register(skill) {
      registered.push(skill)
      return () => {}
    },
  },
}

apply(ctx)

assert.equal(name, 'mycfo-skill', 'Cordis 插件名')
assert.deepEqual(inject, ['skills'], '必须注入 skills 服务')
assert.equal(registered.length, 1, '只注册一个 skill')

const skill = registered[0]
assert.equal(skill.name, 'company-ops', 'skill 名称应为 company-ops')
assert.ok(skill.description.length > 30, 'description 不能太短')
assert.ok(skill.content.length > 2000, 'SKILL.md 正文应被完整注册')
assert.ok(!skill.content.trimStart().startsWith('---'), '正文不应包含 frontmatter')
assert.ok(skill.content.includes('公司经营 CFO'), '正文内容正确')
assert.equal(skill.resourceBase.kind, 'directory')
assert.ok(skill.resourceBase.path.endsWith(`${join('', 'skill')}`), '资源目录应指向 skill/')
assert.ok(skill.path.endsWith('SKILL.md'))
assert.equal(skill.source, 'runtime', '注册表加载时校验 source，必须显式给出')
assert.equal(skill.invocation.modelInvocable, true)
assert.equal(skill.invocation.userInvocable, true)

// 资源必须真的存在，否则模型按相对路径加载会失败
const required = [
  'references/tax-cn.md',
  'references/tax-planning.md',
  'references/financial-analysis.md',
  'references/budget-cashflow.md',
  'references/ecommerce-retail.md',
  'references/ecommerce-accounting.md',
  'references/ecommerce-tax.md',
  'references/open-source-map.md',
  'scripts/checkup.py',
  'scripts/tax_mode_compare.py',
  'scripts/ecom_unit_econ.py',
  'assets/company-profile.md',
  'assets/ecommerce-profile.md',
  'assets/monthly-tax-calendar.md',
  'assets/sample-company.json',
  'assets/sample-ecommerce-tax.json',
  'assets/sample-ecommerce-unit.json',
]
for (const rel of required) {
  readFileSync(join(root, 'skill', rel))
}

// 包清单自检：bundle patch 必须存在，否则装进 profile 也不会成为一层
const pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'))
assert.ok(pkg.dsh?.bundle?.patch, 'package.json 必须声明 dsh.bundle.patch')
readFileSync(join(root, pkg.dsh.bundle.patch))
assert.equal(pkg.dshWorkshop?.type, 'plugin')

console.log(
  `smoke ok — ${skill.name} (${skill.content.length} chars, ${required.length} resources, ${pkg.name}@${pkg.version})`,
)
