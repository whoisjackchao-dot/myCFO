<#
.SYNOPSIS
  一键把 myCFO 安装为 DSH profile 插件。

.DESCRIPTION
  在 profile 目录执行 `dsh plugin add <本目录>`，dsh 会用 pnpm 安装本包并把它
  加入 dsh.profile.bundles；重启 DSH 后 company-ops 技能即可在会话中使用。

.EXAMPLE
  .\install.ps1
  .\install.ps1 -Profile web
  .\install.ps1 -Uninstall
#>
param(
  [string]$Profile = 'desktop',
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command dsh -ErrorAction SilentlyContinue)) {
  throw '未找到 dsh 命令。请先安装 DeepSeek Harness（npm i -g @deepseek-ai/dsh）。'
}

if ($Uninstall) {
  Write-Host "从 profile '$Profile' 移除 myCFO 插件..."
  & dsh plugin --profile $Profile remove dsh-mycfo
  if ($LASTEXITCODE -ne 0) { throw '移除失败' }
  Write-Host '已移除。重启 DSH 生效。'
  exit 0
}

$src = $PSScriptRoot
Write-Host "安装 myCFO 插件到 profile '$Profile'"
Write-Host "  来源: $src"
& dsh plugin --profile $Profile add $src
if ($LASTEXITCODE -ne 0) { throw '安装失败（可加 -Verbose 查看 dsh 输出）' }

Write-Host ''
Write-Host '完成。请重启 DSH，然后在会话里说：'
Write-Host '  「帮我做一次公司体检」「这个月要交多少税」「要不要转一般纳税人」'
