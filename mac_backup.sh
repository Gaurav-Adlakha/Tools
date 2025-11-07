export PATH=~/.npm-global/bin:$PATH

. "$HOME/.local/bin/env"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
alias c='cursor'
alias code='open -a "Visual Studio Code" .'
alias jl="jupyter lab"
export ANTHROPIC_PROVIDER=bedrock
export AWS_REGION=us-east-1
export DISABLE_PROMPT_CACHING=true
export AWS_PROFILE=dev
export CLAUDE_CODE_USE_BEDROCK=1
alias g="git"
# Snowflake MCP Environment Variables


# Updated UV Jupyter Kernel Setup Function
uvkernel() {
    local python_version=${1:-3.9}
    echo "Setting up kernel with Python $python_version"
    uv python install $python_version && \
    uv venv .venv --python $python_version && \
    source .venv/bin/activate && \
    if [ -f "requirements.txt" ]; then
        echo "Installing requirements.txt..."
        uv pip install -r requirements.txt ipykernel jupyter fastcore
    else
        echo "No requirements.txt found, installing only ipykernel..."
        uv pip install ipykernel jupyter fastcore
    fi && \
    python -m ipykernel install --user --name $(basename $PWD) --display-name "$(basename $PWD) (Python $python_version)"
}

#search file and folder
se() {
    local folder_name="$1"
    local file_name="$2"

    if [ ! -z "$folder_name" ]; then
        echo "=== Folders named '$folder_name' ==="
        rg --files ~/ 2>/dev/null | grep -o ".*/.*$folder_name.*/" | sort -u
    fi

    if [ ! -z "$file_name" ]; then
        echo "=== Files named '$file_name' ==="
        rg --files --hidden --glob "*$file_name*" ~/ 2>/dev/null
    fi
}


. "$HOME/.atuin/bin/env"

# cursor rules
cr() {
    [[ "$1 $2" == "add fastai" ]] && {
        mkdir -p .cursor/rules
        curl -s -o .cursor/rules/fastai_cursor_rule.mdc https://raw.githubusercontent.com/Gaurav-Adlakha/Tools/main/fastai_cursor_rule.md
        echo "✓ fastai cursor rule downloaded"
    }
    
    [[ "$1 $2" == "add fasthtml" ]] && {
        mkdir -p .cursor/rules
        curl -s -o .cursor/rules/fasthtml.mdc https://www.fastht.ml/docs/llms-ctx.txt
        echo "✓ fasthtml context file downloaded"
    }
    
    [[ "$1 $2" == "add monsterui" ]] && {
        mkdir -p .cursor/rules
        curl -s -o .cursor/rules/monsterui.mdc https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/llms-ctx-full.txt
        echo "✓ monsterui documentation downloaded"
    }
    
    [[ "$1 $2" == "add all" ]] && {
        mkdir -p .cursor/rules
        echo "Downloading all cursor rules..."
        curl -s -o .cursor/rules/fastai_cursor_rule.mdc https://raw.githubusercontent.com/Gaurav-Adlakha/Tools/main/fastai_cursor_rule.md
        echo "✓ fastai cursor rule downloaded"
        curl -s -o .cursor/rules/fasthtml.mdc https://www.fastht.ml/docs/llms-ctx.txt
        echo "✓ fasthtml context file downloaded"
        curl -s -o .cursor/rules/monsterui.mdc https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/llms-ctx-full.txt
        echo "✓ monsterui documentation downloaded"
        echo "🎉 All cursor rules downloaded successfully!"
    }
}

eval "$(atuin init zsh)"
