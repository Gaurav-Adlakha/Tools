#!/bin/bash
# Simple Claude Code + Bedrock enabler

export AWS_PROFILE=dev-account-powerschool
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export ANTHROPIC_MODEL="us.anthropic.claude-sonnet-4-20250514-v1:0"
unset ANTHROPIC_API_KEY

echo "✅ Claude Code configured for Bedrock"
echo "Test: claude --print 'Are you on Bedrock?'" 
