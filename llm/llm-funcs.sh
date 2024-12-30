# This file defines two zsh functions for working with llm and Sublime Text
# This file is meant to be sourced, e.g., `. llm-funcs.sh`.
# The functions are adapted from 
# https://rtl.chrisadams.me.uk/2024/12/how-i-use-llms-neat-tricks-with-simons-llm-tool/
# See also the README in this directory.

# Change this definition for your preferred model.
export LLM_MODEL=llama3.3

# Open a temp file in Sublime Text, output the contents when closed, then pipe
# that output to llm.
# NOTE: I tried using $EDITOR, but zsh seems to interpret "subl -w" as the command.
# If you prefer VSCode, see the embedded comments about what to use instead of "subl -w".
prompt-llm() {
    # Create a temporary file
    tempfile=$(mktemp)

    # Open the editor on the file and wait for it to close.
    # For VSCode, use "code --wait" instead of "subl -w.
    subl -w $tempfile

    # If the file has content, output it and then remove the file.
    if [[ -s $tempfile ]]
    then
        cat $tempfile
        rm $tempfile
    else
        rm $tempfile
        return 1
    fi | llm --model $LLM_MODEL 
}

# Pipe a question into llm and display the output in Sublime Text
# For VSCode, use "code -" instead of "subl -w.
llm-subl() {
    question="$@"
    llm --model $LLM_MODEL "$question" | subl -w 
}
