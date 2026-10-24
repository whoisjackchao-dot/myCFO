<#
.SYNOPSIS
  一键把 myCFO 安装为 DSH profile 插件。

.DESCRIPTION
  在 profile 目录执行 `dsh plugin add <本目录>`，dsh 会用 pnpm 安装本包并把它
  加入 dsh.profile.bundles；重启 DSH 后 company-ops 技能即可在会话中使用。

.EXAMPLE
  .\install.ps1                          # 用当前目录安装到 desktop profile
  .\install.ps1 -Profile web             # 装到 web profile
  .\install.ps1 -FromGitHub              # 自动从 GitHub 拉取后安装（真正的"一键"）
  .\install.ps1 -Uninstall               # 卸载
#>
param(
  [string]$Profile = 'desktop',
  [switch]$FromGitHub,
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$RepoUrl = 'https://github.com/whoisjackchao-dot/myCFO.git'

if (-not (Get-Command dsh -ErrorAction SilentlyContinue)) {
  throw '未找到 dsh 命令。请先安装 DeepSeek Harness（npm i -g @deepseek-ai/dsh），或从 DSH 安装目录自带的 dsh 运行。'
}

if ($Uninstall) {
  Write-Host "从 profile '$Profile' 移除 myCFO 插件..."
  & dsh plugin --profile $Profile remove dsh-mycfo
  if ($LASTEXITCODE -ne 0) { throw '移除失败' }
  Write-Host '已移除。重启 DSH 生效。'
  exit 0
}

if ($FromGitHub) {
  $tmp = Join-Path $env:TEMP ("mycfo-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
  Write-Host "从 GitHub 拉取到 $tmp ..."
  & git clone --depth 1 $RepoUrl $tmp
  if ($LASTEXITCODE -ne 0) { throw 'git clone 失败，请检查网络或改用本地目录安装。' }
  $src = $tmp
} else {
  $src = $PSScriptRoot
}

Write-Host "安装 myCFO 插件到 profile '$Profile'"
Write-Host "  来源: $src"
& dsh plugin --profile $Profile add $src
if ($LASTEXITCODE -ne 0) { throw '安装失败。' }

Write-Host ''
Write-Host '完成。请重启 DSH，然后在会话里说：'
Write-Host '  「帮我做一次公司体检」「这个月要交多少税」「要不要转一般纳税人」'
Write-Host ''
Write-Host "更新：重新运行本脚本；或 dsh plugin --profile $Profile update dsh-mycfo"
