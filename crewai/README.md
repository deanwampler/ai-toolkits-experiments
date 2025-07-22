# README for Crew AI Experiments

June 28, 2025

I went through the [Crew documentation and tutorials](https://docs.crewai.com/en/introduction). See also the [examples repo](https://github.com/crewAIInc/crewAI-examples/tree/main).

## First Crew

### Install Crew and Set Up LLM Inference

The [first crew](https://docs.crewai.com/en/guides/crews/first-crew) tutorial tells you to first [install crew](https://docs.crewai.com/en/installation), which worked easily. Then it says to [set up your LLM inference choice](https://docs.crewai.com/en/concepts/llms#setting-up-your-llm). It recommends setting the properties in a `.env` file, but doesn't say where that is, except if you already have a crew project created, which I don't at this point. I'll just create it in my current working directory for now.

I'll use Ollama and `llama3.3:70b`. So, my `.env` file is this:

```
llm = LLM(
    model="ollama/llama3.3:70b",
    base_url="http://localhost:11434"
)
```

> [!NOTE]
> [Farther down](https://docs.crewai.com/en/concepts/llms#structured-llm-calls) the LLM page, it discusses using `pydantic` for structured LLM calls. I'll investigate this later. There are other features discussed here, too.

### Step 1: Create a New CrewAI Project

To remember which order the projects were created in, I'll prepend a number to each name used in the docs. So,

```shell
crewai create crew 01_research_crew
cd 01_research_crew
```

It looks like `.env` file defined may not be right. I got several lines like this:

```
python-dotenv could not parse statement starting at line 2
```

Then, it prompted me to setup the inference service I want:

```
...
Creating folder 01_research_crew...
Cache expired or not found. Fetching provider data from the web...
Downloading  [####################################]  563037/26228
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. huggingface
7. ollama
8. watson
9. bedrock
10. azure
11. cerebras
12. sambanova
13. other
q. Quit
Enter the number of your choice or 'q' to quit: 7
Select a model to use for Ollama:
1. ollama/llama3.1
2. ollama/mixtral
q. Quit
Enter the number of your choice or 'q' to quit: 1
API keys and model saved to .env file
Selected model: ollama/llama3.1
  - Created 01_research_crew/.gitignore
  - Created 01_research_crew/pyproject.toml
  - Created 01_research_crew/README.md
  - Created 01_research_crew/knowledge/user_preference.txt
  - Created 01_research_crew/src/01_research_crew/__init__.py
  - Created 01_research_crew/src/01_research_crew/main.py
  - Created 01_research_crew/src/01_research_crew/crew.py
  - Created 01_research_crew/src/01_research_crew/tools/custom_tool.py
  - Created 01_research_crew/src/01_research_crew/tools/__init__.py
  - Created 01_research_crew/src/01_research_crew/config/agents.yaml
  - Created 01_research_crew/src/01_research_crew/config/tasks.yaml
Crew 01_research_crew created successfully!
```

So, I deleted the top-level `.env` file. Note that the prompts didn't give me the option to use `llama3.3`. I picked `llama3.1`, but I then edited the new `01_research_crew/.env` to use `llama3.3:70b`. It is now:

```shell
MODEL=ollama/llama3.3:70b
API_BASE=http://localhost:11434
```

Clicking through the generated code, I see a python class named `01ResearchCrew` in `01_research_crew/crew.py`. This is not a valid python class name, so I'm going to delete this project and just recreate it as originally suggested: `research_crew`. I suppose editing all bad names would also work...

### Step 3: Configure Your Agents

The tutorial's suggested content for `src/research_crew/config/agents.yaml` is different than what was generated. The only significant difference appears to be the addition of the LLM specification. I used the tutorial's version with my model.

I won't comment further on any differences I find between the tutorial documentation and the generated code. I'll just go with the tutorial's suggestions...

### Step 7: Set Up Your Environment Variables

You are asked to create a [Serper]() account, which is a Google Search API, then add your API key to `.env`.

### Step 8: Install Dependencies

Running `crewai install`, I got the following C++ compilation error:

```
Using CPython 3.13.3 interpreter at: /opt/homebrew/opt/python@3.13/bin/python3.13
Creating virtual environment at: .venv
Resolved 228 packages in 2.00s
   Built research-crew @ file:///Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew
   Built pypika==0.48.9
  × Failed to build `chroma-hnswlib==0.7.6`
  ├─▶ The build backend returned an error
  ╰─▶ Call to `setuptools.build_meta.build_wheel` failed (exit status: 1)

      [stdout]
      running bdist_wheel
      running build
      running build_ext
      creating var/folders/sp/vv93lnzn04d_8grh0l5d2j2w0000gn/T
      clang++ -fno-strict-overflow -Wsign-compare -Wunreachable-code -fno-common -dynamic
      -DNDEBUG -g -O3 -Wall -I/Users/deanwampler/.cache/uv/builds-v0/.tmpfALcUs/include
      -I/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/include/python3.13
      -c /var/folders/sp/vv93lnzn04d_8grh0l5d2j2w0000gn/T/tmpxpy6l4am.cpp -o
      var/folders/sp/vv93lnzn04d_8grh0l5d2j2w0000gn/T/tmpxpy6l4am.o -std=c++14
      clang++ -fno-strict-overflow -Wsign-compare -Wunreachable-code -fno-common -dynamic
      -DNDEBUG -g -O3 -Wall -I/Users/deanwampler/.cache/uv/builds-v0/.tmpfALcUs/include
      -I/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/include/python3.13
      -c /var/folders/sp/vv93lnzn04d_8grh0l5d2j2w0000gn/T/tmpt_fdmr9z.cpp -o
      var/folders/sp/vv93lnzn04d_8grh0l5d2j2w0000gn/T/tmpt_fdmr9z.o -fvisibility=hidden
      building 'hnswlib' extension
      creating build/temp.macosx-15.0-arm64-cpython-313/python_bindings
      clang++ -fno-strict-overflow -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -O3
      -Wall -I/Users/deanwampler/.cache/uv/builds-v0/.tmpfALcUs/lib/python3.13/site-packages/pybind11/include
      -I/Users/deanwampler/.cache/uv/builds-v0/.tmpfALcUs/lib/python3.13/site-packages/numpy/_core/include
      -I./hnswlib/ -I/Users/deanwampler/.cache/uv/builds-v0/.tmpfALcUs/include
      -I/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/include/python3.13 -c ./python_bindings/bindings.cpp
      -o build/temp.macosx-15.0-arm64-cpython-313/python_bindings/bindings.o -O3 -stdlib=libc++ -mmacosx-version-min=10.7
      -DVERSION_INFO=\"0.7.6\" -std=c++14 -fvisibility=hidden

      [stderr]
      ./python_bindings/bindings.cpp:1:10: fatal error: 'iostream' file not found
          1 | #include <iostream>
            |          ^~~~~~~~~~
      1 error generated.
      error: command '/usr/bin/clang++' failed with exit code 1

      hint: This usually indicates a problem with the package or the build environment.
  help: `chroma-hnswlib` (v0.7.6) was included because `research-crew` (v0.1.0) depends on `crewai` (v0.134.0) which depends on
        `chromadb` (v0.5.23) which depends on `chroma-hnswlib`
An error occurred while running the crew: Command '['uv', 'sync']' returned non-zero exit status 1.
```

If it can't find `iostream`, that suggests XCode and tools aren't properly set up on my Mac. This is not uncommon. From [this StackOverflow post](), the solution was to reinstall the XCode command-line tools:

```shell
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

Then `crewai install` worked fine.

Now try `crew run`:

```
$ crewai run
Running the Crew
/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/pysbd/segmenter.py:66: SyntaxWarning: invalid escape sequence '\s'
  for match in re.finditer('{0}\s*'.format(re.escape(sent)), self.original_text):
/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/pysbd/lang/arabic.py:29: SyntaxWarning: invalid escape sequence '\.'
  txt = re.sub('(?<={0})\.'.format(am), '∯', txt)
/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/pysbd/lang/persian.py:29: SyntaxWarning: invalid escape sequence '\.'
  txt = re.sub('(?<={0})\.'.format(am), '∯', txt)
/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/pydantic/fields.py:1093: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'required'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
  warn(
╭────────────────────────────────────────────────────── Crew Execution Started ───────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  Crew Execution Started                                                                                                             │
│  Name: crew                                                                                                                         │
│  ID: ac865c67-8c12-48e9-aaad-367d349360dd                                                                                           │
│  Tool Args:                                                                                                                         │
│                                                                                                                                     │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: 275531a8-5763-456c-a168-3ea671677d42
    Status: Executing Task...
╭───────────────────────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  Agent: Senior Research Specialist for Artificial Intelligence in Healthcare                                                        │
│                                                                                                                                     │
│  Task: Conduct thorough research on Artificial Intelligence in Healthcare. Focus on: 1. Key concepts and definitions 2. Historical  │
│  development and recent trends 3. Major challenges and opportunities 4. Notable applications or case studies 5. Future outlook and  │
│  potential developments                                                                                                             │
│  Make sure to organize your findings in a structured format with clear sections.                                                    │
│                                                                                                                                     │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: 275531a8-5763-456c-a168-3ea671677d42
    Status: Executing Task...
    └── 🔧 Used Search the internet with Serper (1)
╭────────────────────────────────────────────────────── 🔧 Agent Tool Execution ──────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  Agent: Senior Research Specialist for Artificial Intelligence in Healthcare                                                        │
│                                                                                                                                     │
│  Thought: Thought: To conduct thorough research on Artificial Intelligence in Healthcare, I need to start by gathering information  │
│  on key concepts and definitions. This will provide a foundation for understanding the historical development, recent trends,       │
│  challenges, opportunities, notable applications, and future outlook of AI in healthcare.                                           │
│                                                                                                                                     │
│  Using Tool: Search the internet with Serper                                                                                        │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────── Tool Input ─────────────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  "{\"search_query\": \"Artificial Intelligence in Healthcare definitions and concepts\"}"                                           │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────── Tool Output ────────────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  {'searchParameters': {'q': 'Artificial Intelligence in Healthcare definitions and concepts', 'type': 'search', 'num': 10,          │
│  'engine': 'google'}, 'organic': [{'title': 'What is Artificial Intelligence in Medicine? | IBM', 'link':                           │
│  'https://www.ibm.com/think/topics/artificial-intelligence-medicine', 'snippet': 'Artificial intelligence in medicine is the use    │
│  of machine learning models to help process medical data and give medical professionals important insights, improving health        │
│  outcomes and patient experiences .', 'position': 1}, {'title': 'Overview of artificial intelligence in medicine - PMC', 'link':    │
│  'https://pmc.ncbi.nlm.nih.gov/articles/PMC6691444/', 'snippet': 'This descriptive article gives a broad overview of AI in          │
│  medicine, dealing with the terms and concepts as well as the current and future applications of AI.', 'position': 2}, {'title':    │
│  'What Is AI in Healthcare? - Arm', 'link': 'https://www.arm.com/glossary/ai-in-healthcare', 'snippet': 'AI in healthcare is an     │
│  umbrella term to describe the application of machine learning (ML) algorithms and other cognitive technologies in medical          │
│  settings.', 'position': 3}, {'title': 'Artificial intelligence in healthcare: transforming the practice of ...', 'link':           │
│  'https://pmc.ncbi.nlm.nih.gov/articles/PMC8285156/', 'snippet': 'AI is a powerful and disruptive area of computer science, with    │
│  the potential to fundamentally transform the practice of medicine and the delivery of healthcare.', 'position': 4}, {'title': 'AI  │
│  in healthcare: Key terms to know | IMO Health', 'link':                                                                            │
│  'https://www.imohealth.com/resources/ai-in-healthcare-key-terms-to-know/', 'snippet': 'Artificial Intelligence (AI) ... AI refers  │
│  to the capability of machines and computer systems to simulate human intelligence processes, including ...', 'position': 5},       │
│  {'title': 'Artificial Intelligence (AI) in Healthcare & Medical Field', 'link':                                                    │
│  'https://www.foreseemed.com/artificial-intelligence-in-healthcare', 'snippet': 'AI in healthcare is expected to play a ma...       │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯





🚀 Crew: crew
└── 📋 Task: 275531a8-5763-456c-a168-3ea671677d42
    Status: Executing Task...
    ├── 🔧 Used Search the internet with Serper (1)
    └── ❌ LLM Failed


 An unknown error occurred. Please check the details below.

🚀 Crew: crew
└── 📋 Task: 275531a8-5763-456c-a168-3ea671677d42
    Assigned to: Senior Research Specialist for Artificial Intelligence in Healthcare

    Status: ❌ Failed
    ├── 🔧 Used Search the internet with Serper (1)
    └── ❌ LLM Failed
╭─────────────────────────────────────────────────────────── Task Failure ────────────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  Task Failed                                                                                                                        │
│  Name: 275531a8-5763-456c-a168-3ea671677d42                                                                                         │
│  Agent: Senior Research Specialist for Artificial Intelligence in Healthcare                                                        │
│                                                                                                                                     │
│  Tool Args:                                                                                                                         │
│                                                                                                                                     │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────── Crew Failure ────────────────────────────────────────────────────────────╮
│                                                                                                                                     │
│  Crew Execution Failed                                                                                                              │
│  Name: crew                                                                                                                         │
│  ID: ac865c67-8c12-48e9-aaad-367d349360dd                                                                                           │
│  Tool Args:                                                                                                                         │
│  Final Output:                                                                                                                      │
│                                                                                                                                     │
│                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Traceback (most recent call last):
IndexError: list index out of range

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/bin/run_crew", line 10, in <module>
    sys.exit(run())
             ~~~^^
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/src/research_crew/main.py", line 18, in run
    result = ResearchCrew().crew().kickoff(inputs=inputs)
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/crew.py", line 659, in kickoff
    result = self._run_sequential_process()
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/crew.py", line 768, in _run_sequential_process
    return self._execute_tasks(self.tasks)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/crew.py", line 871, in _execute_tasks
    task_output = task.execute_sync(
        agent=agent_to_use,
        context=context,
        tools=cast(List[BaseTool], tools_for_task),
    )
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/task.py", line 354, in execute_sync
    return self._execute_core(agent, context, tools)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/task.py", line 502, in _execute_core
    raise e  # Re-raise the exception after emitting the event
    ^^^^^^^
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/task.py", line 418, in _execute_core
    result = agent.execute_task(
        task=self,
        context=context,
        tools=tools,
    )
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agent.py", line 435, in execute_task
    raise e
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agent.py", line 411, in execute_task
    result = self._execute_without_timeout(task_prompt, task)
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agent.py", line 507, in _execute_without_timeout
    return self.agent_executor.invoke(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<4 lines>...
        }
        ^
    )["output"]
    ^
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agents/crew_agent_executor.py", line 125, in invoke
    raise e
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agents/crew_agent_executor.py", line 114, in invoke
    formatted_answer = self._invoke_loop()
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agents/crew_agent_executor.py", line 210, in _invoke_loop
    raise e
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/agents/crew_agent_executor.py", line 157, in _invoke_loop
    answer = get_llm_response(
        llm=self.llm,
    ...<2 lines>...
        printer=self._printer,
    )
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/utilities/agent_utils.py", line 160, in get_llm_response
    raise e
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/utilities/agent_utils.py", line 151, in get_llm_response
    answer = llm.call(
        messages,
        callbacks=callbacks,
    )
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/crewai/llm.py", line 956, in call
    return self._handle_non_streaming_response(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        params, callbacks, available_functions
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
An error occurred while running the crew: Command '['uv', 'run', 'run_crew']' returned non-zero exit status 1.
```

_Agents Are Fun!_

There isn't enough information printed to know what failed exactly. It prints what looks like reasonable response text from the LLM call, but then fails. The only clue is `IndexError: list index out of range`.

After some snooping around, I found that https://github.com/crewAIInc/crewAI/issues/2873#issuecomment-2899272854 describes the bug in `litellm` with a temporary patch. Hopefully `crewai` will update to a more recent version of `litellm` soon, where the bug is already fixed.

With this patch, the crew successfully executed (after running for many minutes) and wrote a reasonable-looking report, `output/report.md`.

### Exploring Other CLI Commands

In [this section](https://docs.crewai.com/en/guides/crews/first-crew#exploring-other-cli-commands), I tried `crewai test`. It appears to hard-code using `gImportError: cannot import name 'test' from 'research_crew.main' (/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/researcpt-4o-mini`, but appears to have failed before calling the LLM:

```
$ crewai test
Testing the crew for 3 iterations with model gpt-4o-mini
/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/lib/python3.13/site-packages/pydantic/fields.py:1093: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'required'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
  warn(
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/.venv/bin/test", line 4, in <module>
    from research_crew.main import test
ImportError: cannot import name 'test' from 'research_crew.main' (/Users/deanwampler/projects/ai/ai-toolkits-experiments/crewai/research_crew/src/research_crew/main.py)
An error occurred while testing the crew: Command '['uv', 'run', 'test', '3', 'gpt-4o-mini']' returned non-zero exit status 1.
```

There is no `test` in `src/research_crew/main.py`.

The [first crew](https://docs.crewai.com/en/guides/crews/first-crew) tutorial ends with suggestions for further exploration.

