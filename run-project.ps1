param(
    [Parameter(Mandatory = $true)]
    [string]$Project
)

$ErrorActionPreference = "Stop"

$projectMap = @{
    "1"  = "projects/01-ai-chat-terminal"
    "01" = "projects/01-ai-chat-terminal"
    "2"  = "projects/02-text-summarizer"
    "02" = "projects/02-text-summarizer"
    "3"  = "projects/03-mood-detector"
    "03" = "projects/03-mood-detector"
    "4"  = "projects/04-chatbot-with-memory"
    "04" = "projects/04-chatbot-with-memory"
    "5"  = "projects/05-ai-faq-bot"
    "05" = "projects/05-ai-faq-bot"
    "6"  = "projects/06-ai-code-reviewer"
    "06" = "projects/06-ai-code-reviewer"
    "7"  = "projects/07-chatbot-with-ui"
    "07" = "projects/07-chatbot-with-ui"
    "8"  = "projects/08-document-qa-app"
    "08" = "projects/08-document-qa-app"
    "9"  = "projects/09-meeting-notes-summarizer"
    "09" = "projects/09-meeting-notes-summarizer"
    "10" = "projects/10-ai-agent-with-tools"
    "11" = "projects/11-full-rag-pipeline"
    "12" = "projects/12-ai-powered-saas-feature"
    "13" = "projects/13-multi-agent-system"
    "14" = "projects/14-fine-tuned-model"
    "15" = "projects/15-end-to-end-ai-product"
}

$target = if ($projectMap.ContainsKey($Project)) { $projectMap[$Project] } else { "projects/$Project" }
$projectPath = Join-Path $PSScriptRoot $target
$mainPath = Join-Path $projectPath "main.py"

if (-not (Test-Path $projectPath)) {
    throw "Project folder not found: $projectPath"
}

if (-not (Test-Path $mainPath)) {
    throw "main.py not found in: $projectPath"
}

Push-Location $projectPath
try {
    $projectName = Split-Path $projectPath -Leaf

    if ($projectName -in @("07-chatbot-with-ui", "08-document-qa-app")) {
        streamlit run main.py
    }
    elseif ($projectName -in @("12-ai-powered-saas-feature", "15-end-to-end-ai-product")) {
        uvicorn main:app --reload
    }
    else {
        python main.py
    }
}
finally {
    Pop-Location
}
