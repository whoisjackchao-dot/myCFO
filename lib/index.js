/**
 * dsh-mycfo — 把 myCFO 技能注册进 DSH 的 skill 注册表。
 *
 * 原理：DSH 的 skill 注册表（@deepseek-ai/dsh-skill）接受任意提供方贡献 skill；
 * 插件可以在 apply() 里用 ctx.skills.register(...) 注册一个「运行时 skill」。
 * 这里从本包自带的 skill/ 目录读取 SKILL.md，把正文与资源基目录一起注册，
 * 因此整包可以放在任意位置（profile 的 node_modules 下），不依赖用户目录布局。
 *
 * 不做的事：不写用户文件、不改 profile 配置、不联网。纯只读注册。
 */

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

/** Cordis 插件名（配置树里的行 id 用的是 bundle patch 中的 id）。 */
export const name = 'mycfo-skill'

/** 需要 skill 注册表服务就绪后再 apply。 */
export const inject = ['skills']

/** 包根目录（lib/ 的上一级）。 */
const packageRoot = dirname(dirname(fileURLToPath(import.meta.url)))
const skillDir = join(packageRoot, 'skill')
const skillFile = join(skillDir, 'SKILL.md')

/**
 * 解析 SKILL.md 的 YAML frontmatter（只支持本技能用到的 `key: value` 形式）。
 * @param {string} text 文件全文
 * @returns {{ meta: Record<string, string>, body: string }}
 */
function parseSkillMarkdown(text) {
  const normalized = text.replace(/^\uFEFF/, '')
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(normalized)
  if (!match) throw new Error('SKILL.md 缺少 YAML frontmatter')

  const meta = {}
  for (const line of match[1].split(/\r?\n/)) {
    if (!line.trim() || line.trimStart().startsWith('#')) continue
    const idx = line.indexOf(':')
    if (idx <= 0) continue
    const key = line.slice(0, idx).trim()
    let value = line.slice(idx + 1).trim()
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1)
    }
    meta[key] = value
  }
  return { meta, body: normalized.slice(match[0].length).trimStart() }
}

/**
 * 读取并校验技能定义。
 * @returns {{ meta: Record<string, string>, body: string }}
 */
function loadSkill() {
  const { meta, body } = parseSkillMarkdown(readFileSync(skillFile, 'utf8'))
  if (!meta.name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(meta.name)) {
    throw new Error('SKILL.md frontmatter 的 name 不是合法 kebab-case')
  }
  if (!meta.description) throw new Error('SKILL.md frontmatter 缺少 description')
  return { meta, body }
}

/**
 * Cordis 插件入口。
 * @param {import('@deepseek-ai/cordis').Context} ctx
 */
export function apply(ctx) {
  let skill
  try {
    skill = loadSkill()
  } catch (error) {
    // 技能文件损坏不应拖垮整个 profile：告警后跳过注册。
    console.warn(`[dsh-mycfo] 无法加载技能，已跳过注册：${error.message}`)
    return
  }

  ctx.skills.register({
    name: skill.meta.name,
    description: skill.meta.description,
    ...(skill.meta.whenToUse ? { whenToUse: skill.meta.whenToUse } : {}),
    content: skill.body,
    // 注册表在加载时会校验 source/provider，必须显式给出（register 本身不校验）。
    source: 'runtime',
    path: skillFile,
    resourceBase: { kind: 'directory', path: skillDir },
    metadata: {
      package: 'dsh-mycfo',
      version: '1.0.0',
      profile: 'ecommerce-retail',
    },
    invocation: { modelInvocable: true, userInvocable: true },
  })
}
