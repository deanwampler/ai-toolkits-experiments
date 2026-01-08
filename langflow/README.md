# README for Langflow Experiments

January 8, 2026

## Introduction

[Langflow](https://www.langflow.org/) ([docs](https://docs.langflow.org/)) is an open-source agent framework that IBM acquired when they acquired [DataStax](https://www.ibm.com/products/datastax).

## Getting Started

I [installed the desktop app](https://www.langflow.org/desktop) and started it.

I clicked the buttons to watch the repo and join the discord.

Then I clicked the button to create my first flow and selected "Simple Agent".

I followed the README instructions:
* Entered my OpenAI API key.
* Clicked _Playground_ above right.
* Entered "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need." (Typo: should be "give **me** a recipe...", but I started with the prompt as shown and I'll just continue to use it.)

Here is the result returned:

> Here are the recipes for the chocolate cake and apple pie:
> 
> ### Chocolate Cake Recipe (Hershey's Chocolate Cake)
> 
> **Ingredients:**
> 1. 2 cups white sugar
> 2. 1 ¾ cups all-purpose flour
> 3. ¾ cup unsweetened cocoa powder
> 4. 1 ½ teaspoons baking soda
> 5. 1 ½ teaspoons baking powder
> 6. 1 teaspoon salt
> 7. 2 large eggs
> 8. 1 cup milk
> 9. ½ cup vegetable oil
> 10. 2 teaspoons vanilla extract
> 11. 1 cup boiling water
> 12. **Frosting:**
>     - ¾ cup unsalted butter, at room temperature
>     - 5 ⅓ cups confectioners' sugar
>     - 1 ½ cups unsweetened cocoa powder
>     - ¼ cup milk
>     - 1 teaspoon vanilla extract
> 
> **Total Ingredients for Chocolate Cake:** 12 (cake) + 5 (frosting) = **17 > ingredients**
> 
> ### Apple Pie Recipe (Apple Pie by Grandma Ople)
> **Ingredients:**
> 1. 8 small Granny Smith apples
> 2. ½ cup unsalted butter
> 3. 3 tablespoons all-purpose flour
> 4. ½ cup white sugar
> 5. ½ cup packed brown sugar
> 6. ¼ cup water
> 7. 1 (9 inch) double-crust pie pastry, thawed
> 
> **Total Ingredients for Apple Pie:** 7 ingredients
> 
> ### Total Ingredients Combined
> - Chocolate Cake: 17 ingredients
> - Apple Pie: 7 ingredients
> 
> **Total Ingredients Needed:** 17 + 7 = **24 ingredients**
> 
> You will need a total of **24 ingredients** to make both the chocolate cake > and the apple pie. Enjoy your baking!

So, it worked well!

Let's try using Ollama instead of OpenAI. To do that, I start `ollama serve` in a terminal window, then in the UI, select "Ollama" in the _Model Provider_ control, "Refresh list" in the _Model Name_, then `gpt-oss:20b` in the _Model Name_.

I opened the _Playground_ again and typed "repeat the previous query", which appears to work, but I got the exact same result! Could it be that two OpenAI models return the same thing? Or, did it interpret my prompt to mean just return the previous result? 

> [!NOTE]
> It would be nice if the chat UI had history support to reuse previous prompts.

Let's try entering the exact same original query again. I got the same recipes, but some text is slightly different, especially about the number of ingredients and some minor formatting:

> **Chocolate Cake (Hershey’s Chocolate Cake)**  
> *Ingredients (cake only):*  
> 1. 2 cups white sugar  
> 2. 1 ¾ cups all‑purpose flour  
> 3. ¾ cup unsweetened cocoa powder  
> 4. 1 ½ tsp baking soda  
> 5. 1 ½ tsp baking powder  
> 6. 1 tsp salt  
> 7. 2 large eggs  
> 8. 1 cup milk  
> 9. ½ cup vegetable oil  
> 10. 2 tsp vanilla extract  
> 11. 1 cup boiling water  
> 
> *Frosting:*  
> 12. ¾ cup unsalted butter, softened  
> 13. 5 ⅓ cups confectioners’ sugar  
> 14. 1 ½ cups unsweetened cocoa powder  
> 15. ¼ cup milk  
> 16. 1 tsp vanilla extract  
> 
> **Total ingredients for chocolate cake:** **17**
> 
> ---
> 
> **Apple Pie (Grandma Ople’s Apple Pie)**  
> *Ingredients:*  
> 1. 8 small Granny Smith apples  
> 2. ½ cup unsalted butter  
> 3. 3 Tbsp all‑purpose flour  
> 4. ½ cup white sugar  
> 5. ½ cup packed brown sugar  
> 6. ¼ cup water  
> 7. 1 (9‑inch) double‑crust pie pastry, thawed  
> 
> **Total ingredients for apple pie:** **7**
> 
> ---
> 
> ### Combined Total
> 
> - Chocolate cake: 17 ingredients  
> - Apple pie: 7 ingredients  
> 
> **Total ingredients needed for both recipes:** **24**.

This suggests that using the prompt, "repeat the previous query", did cause it to just output the previous result, but using the same initial prompt shows that the two OpenAI models are very similar!

Let's try a different model, `llama3.2:3b`. Wow, this is all I got in return:

> You will need a total of 24 ingredients to make both the chocolate cake and the apple pie.

It didn't print the recipes. Let's try `granite4:small-h`. It took much longer than the other models, running for over a minute, and it returned nothing!

I'll stick with `gpt-oss:20b` for now.


### Sharing

Next to _Playground_ is a "_Share_" menu. Let's try it.

The first option is _API Access_, which presents Python, JavaScript, and cURL options. Here is the Python:

```python
import requests
import os
import uuid

api_key = 'YOUR_API_KEY_HERE'
url = "http://localhost:7860/api/v1/run/13e81448-428c-4037-b50c-30875384e68b"  # The complete API endpoint URL for this flow

# Request payload configuration
payload = {
    "output_type": "chat",
    "input_type": "chat",
    "input_value": "Hello, how are you?"
}
payload["session_id"] = str(uuid.uuid4())

headers = {"x-api-key": api_key}

try:
    # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes

    # Print response
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except ValueError as e:
    print(f"Error parsing response: {e}")
```

I saved this code in the file `simple_agent.py` so I can run it. I made several changes:
* Added `argparse` options for the port and prompt
* Changed the `payload["input_value"]` to my prompt above, by default, or an input prompt.
* Instead of hard-coding the API key, it is read from the environment.

There are no instructions for how to run this in the dialog, so I referred to the [docs](https://docs.langflow.org/get-started-installation#install-and-run-the-langflow-oss-python-package). I'll use `uv` and setup an environment with the `langflow` Python library installed:

```shell
$ uv init
$ rm main.py   # file created by init...
$ uv pip install langflow # installs a second copy of the GUI??
$ uv run langflow run     # runs the server and takes several minutes

✓ Initializing Langflow...
✓ Checking Environment...
■ Starting Core Services...2026-01-08T15:48:09.602532Z [warning  ] CORS: Using permissive defaults (all origins + credentials). Set LANGFLOW_CORS_ORIGINS for production. Stricter defaults in v2.0.
✓ Starting Core Services
✓ Connecting Database...
✓ Loading Components...
✓ Adding Starter Projects...
▣ Launching Langflow...2026-01-08T15:48:10.651920Z [info     ] Initializing alembic
□ Launching Langflow...2026-01-08T15:48:10.980949Z [warning  ] Column 'created_at' has type DATETIME in table 'apikey'
2026-01-08T15:48:10.981227Z [warning  ] Column 'created_at' has type DATETIME in table 'variable'
2026-01-08T15:48:10.981254Z [warning  ] Column 'updated_at' has type DATETIME in table 'variable'
□ Launching Langflow...The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec().
Break on __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__() to debug.
The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec().
# ... Last two lines repeated many times! ...

□ Launching Langflow.../Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/langflow/.venv/lib/python3.12/site-packages/lfx/schema/cross_module.py:48: PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated. Instead, you should access this attribute from the model class. Deprecated in Pydantic V2.11 to be removed in V3.0.
  if not hasattr(instance, "model_fields"):
/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/langflow/.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
  warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)
▢ Launching Langflow.../Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/langflow/.venv/lib/python3.12/site-packages/lfx/schema/cross_module.py:48: PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated. Instead, you should access this attribute from the model class. Deprecated in Pydantic V2.11 to be removed in V3.0.
  if not hasattr(instance, "model_fields"):
✓ Launching Langflow...

╭─────────────────────────────────────────────────────────────────────────╮
│                                                                         │
│  Welcome to Langflow                                                    │
│                                                                         │
│  🌟 GitHub: Star for updates → https://github.com/langflow-ai/langflow  │
│  💬 Discord: Join for support → https://discord.com/invite/EqksyE2EX9   │
│                                                                         │
│  We collect anonymous usage data to improve Langflow.                   │
│  To opt out, set: DO_NOT_TRACK=true in your environment.                │
│                                                                         │
│  🟢 Open Langflow → http://localhost:7861                               │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯
2026-01-08T15:48:57.013872Z [info     ] File _mcp_servers_cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.json saved successfully in flow cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.
2026-01-08T15:48:57.026914Z [info     ] File _mcp_servers_cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.json deleted successfully from flow cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.
2026-01-08T15:48:57.030183Z [info     ] File _mcp_servers_cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.json saved successfully in flow cb4d1d8f-9abe-49bd-a6e4-0afc42a2b61e.
```

Now the instructions say to open http://127.0.0.1:7860, but you can see in the console "exhaust" that the port is actually 7861. This is because I still have the desktop app running, so picking 7860 or 7861 picks which server. Let's try [http://127.0.0.1:7861](http://127.0.0.1:7861). This opens the same UI in a browser that is seen in the desktop app.

Next, I executed the app in a separate terminal, using the port for the desktop app:

```shell
$ uv run python simple-agent.py --port 7860 --verbose default

Simple Agent:
  port:   7860
  prompt: Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need.
  URL:    http://localhost:7860/api/v1/run/13e81448-428c-4037-b50c-30875384e68b
... JSON ...
```

Here is the JSON output, nicely formatted:

```json
{
  "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d",
  "outputs": [
    {
      "inputs": {
        "input_value": "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need."
      },
      "outputs": [
        {
          "results": {
            "message": {
              "text_key": "text",
              "data": {
                "timestamp": "2026-01-08 17:36:08 UTC",
                "sender": "Machine",
                "sender_name": "AI",
                "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d",
                "context_id": "",
                "text": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Granulated sugar | 2 cups (400 g) |\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n| Baking powder | 1 ½ tsp |\n| Baking soda | 1 ½ tsp |\n| Salt | 1 tsp |\n| Eggs | 2 large |\n| Whole milk | 1 cup (240 ml) |\n| Vegetable oil | ½ cup (120 ml) |\n| Vanilla extract | 2 tsp |\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n| Granulated sugar | ¾ cup (150 g) |\n| Brown sugar | ½ cup (100 g) |\n| Ground cinnamon | 2 tsp |\n| Ground nutmeg | ½ tsp |\n| Salt | ¼ tsp |\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n| Lemon juice | 2 tbsp |\n| Cornstarch | 2 tbsp |\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n|--------|--------------------------------|\n| Chocolate Cake | **11** |\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*",
                "files": [],
                "error": false,
                "edit": false,
                "properties": {
                  "text_color": null,
                  "background_color": null,
                  "edited": false,
                  "source": {
                    "id": "Agent-eQzLg",
                    "display_name": "Agent",
                    "source": "gpt-oss:20b"
                  },
                  "icon": "Bot",
                  "allow_markdown": false,
                  "positive_feedback": null,
                  "state": "complete",
                  "targets": []
                },
                "category": "message",
                "content_blocks": [
                  {
                    "title": "Agent Steps",
                    "contents": [
                      {
                        "type": "text",
                        "duration": 1,
                        "header": {
                          "title": "Input",
                          "icon": "MessageSquare"
                        },
                        "text": "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need."
                      },
                      {
                        "type": "text",
                        "duration": 8,
                        "header": {
                          "title": "Output",
                          "icon": "MessageSquare"
                        },
                        "text": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Granulated sugar | 2 cups (400 g) |\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n| Baking powder | 1 ½ tsp |\n| Baking soda | 1 ½ tsp |\n| Salt | 1 tsp |\n| Eggs | 2 large |\n| Whole milk | 1 cup (240 ml) |\n| Vegetable oil | ½ cup (120 ml) |\n| Vanilla extract | 2 tsp |\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n| Granulated sugar | ¾ cup (150 g) |\n| Brown sugar | ½ cup (100 g) |\n| Ground cinnamon | 2 tsp |\n| Ground nutmeg | ½ tsp |\n| Salt | ¼ tsp |\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n| Lemon juice | 2 tbsp |\n| Cornstarch | 2 tbsp |\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n|--------|--------------------------------|\n| Chocolate Cake | **11** |\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*"
                      }
                    ],
                    "allow_markdown": true,
                    "media_url": null
                  }
                ],
                "id": "6cc19030-36f5-46d8-8820-880bebd53a6b",
                "flow_id": "13e81448-428c-4037-b50c-30875384e68b",
                "duration": null
              },
              "default_value": "",
              "text": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Granulated sugar | 2 cups (400 g) |\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n| Baking powder | 1 ½ tsp |\n| Baking soda | 1 ½ tsp |\n| Salt | 1 tsp |\n| Eggs | 2 large |\n| Whole milk | 1 cup (240 ml) |\n| Vegetable oil | ½ cup (120 ml) |\n| Vanilla extract | 2 tsp |\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n| Granulated sugar | ¾ cup (150 g) |\n| Brown sugar | ½ cup (100 g) |\n| Ground cinnamon | 2 tsp |\n| Ground nutmeg | ½ tsp |\n| Salt | ¼ tsp |\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n| Lemon juice | 2 tbsp |\n| Cornstarch | 2 tbsp |\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n|--------|--------------------------------|\n| Chocolate Cake | **11** |\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*",
              "sender": "Machine",
              "sender_name": "AI",
              "files": [],
              "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d",
              "context_id": "",
              "timestamp": "2026-01-08T17:36:08+00:00",
              "flow_id": "13e81448-428c-4037-b50c-30875384e68b",
              "error": false,
              "edit": false,
              "properties": {
                "text_color": null,
                "background_color": null,
                "edited": false,
                "source": {
                  "id": "Agent-eQzLg",
                  "display_name": "Agent",
                  "source": "gpt-oss:20b"
                },
                "icon": "Bot",
                "allow_markdown": false,
                "positive_feedback": null,
                "state": "complete",
                "targets": []
              },
              "category": "message",
              "content_blocks": [
                {
                  "title": "Agent Steps",
                  "contents": [
                    {
                      "type": "text",
                      "duration": 1,
                      "header": {
                        "title": "Input",
                        "icon": "MessageSquare"
                      },
                      "text": "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need."
                    },
                    {
                      "type": "text",
                      "duration": 8,
                      "header": {
                        "title": "Output",
                        "icon": "MessageSquare"
                      },
                      "text": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Granulated sugar | 2 cups (400 g) |\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n| Baking powder | 1 ½ tsp |\n| Baking soda | 1 ½ tsp |\n| Salt | 1 tsp |\n| Eggs | 2 large |\n| Whole milk | 1 cup (240 ml) |\n| Vegetable oil | ½ cup (120 ml) |\n| Vanilla extract | 2 tsp |\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n| Granulated sugar | ¾ cup (150 g) |\n| Brown sugar | ½ cup (100 g) |\n| Ground cinnamon | 2 tsp |\n| Ground nutmeg | ½ tsp |\n| Salt | ¼ tsp |\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n| Lemon juice | 2 tbsp |\n| Cornstarch | 2 tbsp |\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n|--------|--------------------------------|\n| Chocolate Cake | **11** |\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*"
                    }
                  ],
                  "allow_markdown": true,
                  "media_url": null
                }
              ],
              "duration": null
            }
          },
          "artifacts": {
            "message": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n\n|------------|--------|\n\n| All‑purpose flour | 2 ½ cups (315 g) |\n\n| Granulated sugar | 2 cups (400 g) |\n\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n\n| Baking powder | 1 ½ tsp |\n\n| Baking soda | 1 ½ tsp |\n\n| Salt | 1 tsp |\n\n| Eggs | 2 large |\n\n| Whole milk | 1 cup (240 ml) |\n\n| Vegetable oil | ½ cup (120 ml) |\n\n| Vanilla extract | 2 tsp |\n\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n\n|------------|--------|\n\n| All‑purpose flour | 2 ½ cups (315 g) |\n\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n\n| Granulated sugar | ¾ cup (150 g) |\n\n| Brown sugar | ½ cup (100 g) |\n\n| Ground cinnamon | 2 tsp |\n\n| Ground nutmeg | ½ tsp |\n\n| Salt | ¼ tsp |\n\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n\n| Lemon juice | 2 tbsp |\n\n| Cornstarch | 2 tbsp |\n\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n\n|--------|--------------------------------|\n\n| Chocolate Cake | **11** |\n\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*",
            "sender": "Machine",
            "sender_name": "AI",
            "files": [],
            "type": "object"
          },
          "outputs": {
            "message": {
              "message": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Granulated sugar | 2 cups (400 g) |\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n| Baking powder | 1 ½ tsp |\n| Baking soda | 1 ½ tsp |\n| Salt | 1 tsp |\n| Eggs | 2 large |\n| Whole milk | 1 cup (240 ml) |\n| Vegetable oil | ½ cup (120 ml) |\n| Vanilla extract | 2 tsp |\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n|------------|--------|\n| All‑purpose flour | 2 ½ cups (315 g) |\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n| Granulated sugar | ¾ cup (150 g) |\n| Brown sugar | ½ cup (100 g) |\n| Ground cinnamon | 2 tsp |\n| Ground nutmeg | ½ tsp |\n| Salt | ¼ tsp |\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n| Lemon juice | 2 tbsp |\n| Cornstarch | 2 tbsp |\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n|--------|--------------------------------|\n| Chocolate Cake | **11** |\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*",
              "type": "text"
            }
          },
          "logs": {
            "message": []
          },
          "messages": [
            {
              "message": "**Chocolate Cake (Classic 9‑inch)**  \n\n| Ingredient | Amount |\n\n|------------|--------|\n\n| All‑purpose flour | 2 ½ cups (315 g) |\n\n| Granulated sugar | 2 cups (400 g) |\n\n| Unsweetened cocoa powder | ¾ cup (75 g) |\n\n| Baking powder | 1 ½ tsp |\n\n| Baking soda | 1 ½ tsp |\n\n| Salt | 1 tsp |\n\n| Eggs | 2 large |\n\n| Whole milk | 1 cup (240 ml) |\n\n| Vegetable oil | ½ cup (120 ml) |\n\n| Vanilla extract | 2 tsp |\n\n| Boiling water | 1 cup (240 ml) |\n\n**Apple Pie (Traditional 9‑inch)**  \n\n| Ingredient | Amount |\n\n|------------|--------|\n\n| All‑purpose flour | 2 ½ cups (315 g) |\n\n| Unsalted butter (cold, cubed) | 1 cup (227 g) |\n\n| Granulated sugar | ¾ cup (150 g) |\n\n| Brown sugar | ½ cup (100 g) |\n\n| Ground cinnamon | 2 tsp |\n\n| Ground nutmeg | ½ tsp |\n\n| Salt | ¼ tsp |\n\n| Apples (peeled, cored, sliced) | 6 cups (≈1.5 kg) |\n\n| Lemon juice | 2 tbsp |\n\n| Cornstarch | 2 tbsp |\n\n| Egg (for egg wash) | 1 large |\n\n---\n\n### Counting the ingredients\n\n| Recipe | Number of distinct ingredients |\n\n|--------|--------------------------------|\n\n| Chocolate Cake | **11** |\n\n| Apple Pie | **11** |\n\n**Total ingredients needed:** 11 + 11 = **22** distinct items.  \n\n*(If you prefer to combine the two butter entries in the pie recipe into one “butter” count, the total would be 21. The above count treats each distinct ingredient listed separately.)*",
              "sender": "Machine",
              "sender_name": "AI",
              "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d",
              "stream_url": null,
              "component_id": "ChatOutput-vBcbC",
              "files": [],
              "type": "text"
            }
          ],
          "timedelta": null,
          "duration": null,
          "component_display_name": "Chat Output",
          "component_id": "ChatOutput-vBcbC",
          "used_frozen_result": false
        }
      ]
    }
  ]
}
```

A slightly different answer than before...

Now try with the CLI server running on port 7861. I get the following interesting result:

```
Simple Agent:
  port:   7861
  prompt: Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need.
  URL:    http://localhost:7861/api/v1/run/13e81448-428c-4037-b50c-30875384e68b
<!doctype html>
<html lang="en">
  <head>
    <base href="/" />
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="./favicon.ico" />
    <link rel="manifest" href="./manifest.json" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Chivo:ital,wght@0,100..900;1,100..900&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
      rel="stylesheet"
    />
    <title>Langflow</title>
    <script type="module" crossorigin src="./assets/index-BVZrupat.js"></script>
    <link rel="stylesheet" crossorigin href="./assets/index-BFcc3mmE.css">
  </head>
  <body id="body" class="dark" style="width: 100%; height: 100%">
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div style="width: 100vw; height: 100vh" id="root"></div>
  </body>
</html>
```

It's possible this failed because the URL above came from my desktop app. Indeed, the server exhaust includes this message:

```
2026-01-08T16:18:43.485347Z [info     ] Client error during session scope: 404: Flow identifier 13e81448-428c-4037-b50c-30875384e68b not found
```

I would like to try again with the correct flow identifier, but I can't figure out what it is.


Let's go back to the _Share > API Access_ menu item and pick the cURL option:

```shell
curl --request POST \
     --url 'http://localhost:7860/api/v1/run/13e81448-428c-4037-b50c-30875384e68b?stream=false' \
     --header 'Content-Type: application/json' \
     --header "x-api-key: YOUR_API_KEY_HERE" \
     --data '{
       "output_type": "chat",
       "input_type": "chat",
       "input_value": "Hello, how are you?",
       "session_id": "YOUR_SESSION_ID_HERE"
     }'
```

> [!NOTE]
> There was an extra space after the `\` for the `--header "x-api-key: YOUR_API_KEY_HERE"` line.

Modified for my session ID (taken from previous output above), API key, and prompt:

```shell
curl --request POST \
     --url 'http://localhost:7860/api/v1/run/13e81448-428c-4037-b50c-30875384e68b?stream=false' \
     --header 'Content-Type: application/json' \
     --header "x-api-key: $LANGFLOW_API_KEY" \
     --data '{
       "output_type": "chat",
       "input_type": "chat",
       "input_value": "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need.",
       "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d"
     }'
```

The output looks basically the same as above.

This command can also be found in `simple-agent.sh`.

> [!TIP]
> I had a trailing comment after the `"session_id": "..."` that caused the following confusing error message (which may be from `curl`):
> ```json
> {
>     "detail":[
>         {
>             "type": "json_invalid",
>             "loc": ["body",320],
>             "msg": "JSON decode error",
>             "input": {},
>             "ctx": {
>                 "error": "Expecting property name enclosed in double quotes"
>             }
>         }
>     ]
> }
> ```

## Trying Other Things

Let's look at some more code. Here is the code for the agent:

```python
import json
import re

from langchain_core.tools import StructuredTool, Tool
from pydantic import ValidationError

from lfx.base.agents.agent import LCToolsAgentComponent
from lfx.base.agents.events import ExceptionWithMessageError
from lfx.base.models.model_input_constants import (
    ALL_PROVIDER_FIELDS,
    MODEL_DYNAMIC_UPDATE_FIELDS,
    MODEL_PROVIDERS_DICT,
    MODEL_PROVIDERS_LIST,
    MODELS_METADATA,
)
from lfx.base.models.model_utils import get_model_name
from lfx.components.helpers import CurrentDateComponent
from lfx.components.langchain_utilities.tool_calling import ToolCallingAgentComponent
from lfx.components.models_and_agents.memory import MemoryComponent
from lfx.custom.custom_component.component import get_component_toolkit
from lfx.custom.utils import update_component_build_config
from lfx.helpers.base_model import build_model_from_schema
from lfx.inputs.inputs import BoolInput, SecretStrInput, StrInput
from lfx.io import DropdownInput, IntInput, MessageTextInput, MultilineInput, Output, TableInput
from lfx.log.logger import logger
from lfx.schema.data import Data
from lfx.schema.dotdict import dotdict
from lfx.schema.message import Message
from lfx.schema.table import EditMode


def set_advanced_true(component_input):
    component_input.advanced = True
    return component_input


class AgentComponent(ToolCallingAgentComponent):
    display_name: str = "Agent"
    description: str = "Define the agent's instructions, then enter a task to complete using tools."
    documentation: str = "https://docs.langflow.org/agents"
    icon = "bot"
    beta = False
    name = "Agent"

    memory_inputs = [set_advanced_true(component_input) for component_input in MemoryComponent().inputs]

    # Filter out json_mode from OpenAI inputs since we handle structured output differently
    if "OpenAI" in MODEL_PROVIDERS_DICT:
        openai_inputs_filtered = [
            input_field
            for input_field in MODEL_PROVIDERS_DICT["OpenAI"]["inputs"]
            if not (hasattr(input_field, "name") and input_field.name == "json_mode")
        ]
    else:
        openai_inputs_filtered = []

    inputs = [
        DropdownInput(
            name="agent_llm",
            display_name="Model Provider",
            info="The provider of the language model that the agent will use to generate responses.",
            options=[*MODEL_PROVIDERS_LIST],
            value="OpenAI",
            real_time_refresh=True,
            refresh_button=False,
            input_types=[],
            options_metadata=[MODELS_METADATA[key] for key in MODEL_PROVIDERS_LIST if key in MODELS_METADATA],
            external_options={
                "fields": {
                    "data": {
                        "node": {
                            "name": "connect_other_models",
                            "display_name": "Connect other models",
                            "icon": "CornerDownLeft",
                        }
                    }
                },
            },
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="The API key to use for the model.",
            required=True,
        ),
        StrInput(
            name="base_url",
            display_name="Base URL",
            info="The base URL of the API.",
            required=True,
            show=False,
        ),
        StrInput(
            name="project_id",
            display_name="Project ID",
            info="The project ID of the model.",
            required=True,
            show=False,
        ),
        IntInput(
            name="max_output_tokens",
            display_name="Max Output Tokens",
            info="The maximum number of tokens to generate.",
            show=False,
        ),
        *openai_inputs_filtered,
        MultilineInput(
            name="system_prompt",
            display_name="Agent Instructions",
            info="System Prompt: Initial instructions and context provided to guide the agent's behavior.",
            value="You are a helpful assistant that can use tools to answer questions and perform tasks.",
            advanced=False,
        ),
        MessageTextInput(
            name="context_id",
            display_name="Context ID",
            info="The context ID of the chat. Adds an extra layer to the local memory.",
            value="",
            advanced=True,
        ),
        IntInput(
            name="n_messages",
            display_name="Number of Chat History Messages",
            value=100,
            info="Number of chat history messages to retrieve.",
            advanced=True,
            show=True,
        ),
        MultilineInput(
            name="format_instructions",
            display_name="Output Format Instructions",
            info="Generic Template for structured output formatting. Valid only with Structured response.",
            value=(
                "You are an AI that extracts structured JSON objects from unstructured text. "
                "Use a predefined schema with expected types (str, int, float, bool, dict). "
                "Extract ALL relevant instances that match the schema - if multiple patterns exist, capture them all. "
                "Fill missing or ambiguous values with defaults: null for missing values. "
                "Remove exact duplicates but keep variations that have different field values. "
                "Always return valid JSON in the expected format, never throw errors. "
                "If multiple objects can be extracted, return them all in the structured format."
            ),
            advanced=True,
        ),
        TableInput(
            name="output_schema",
            display_name="Output Schema",
            info=(
                "Schema Validation: Define the structure and data types for structured output. "
                "No validation if no output schema."
            ),
            advanced=True,
            required=False,
            value=[],
            table_schema=[
                {
                    "name": "name",
                    "display_name": "Name",
                    "type": "str",
                    "description": "Specify the name of the output field.",
                    "default": "field",
                    "edit_mode": EditMode.INLINE,
                },
                {
                    "name": "description",
                    "display_name": "Description",
                    "type": "str",
                    "description": "Describe the purpose of the output field.",
                    "default": "description of field",
                    "edit_mode": EditMode.POPOVER,
                },
                {
                    "name": "type",
                    "display_name": "Type",
                    "type": "str",
                    "edit_mode": EditMode.INLINE,
                    "description": ("Indicate the data type of the output field (e.g., str, int, float, bool, dict)."),
                    "options": ["str", "int", "float", "bool", "dict"],
                    "default": "str",
                },
                {
                    "name": "multiple",
                    "display_name": "As List",
                    "type": "boolean",
                    "description": "Set to True if this output field should be a list of the specified type.",
                    "default": "False",
                    "edit_mode": EditMode.INLINE,
                },
            ],
        ),
        *LCToolsAgentComponent.get_base_inputs(),
        # removed memory inputs from agent component
        # *memory_inputs,
        BoolInput(
            name="add_current_date_tool",
            display_name="Current Date",
            advanced=True,
            info="If true, will add a tool to the agent that returns the current date.",
            value=True,
        ),
    ]
    outputs = [
        Output(name="response", display_name="Response", method="message_response"),
    ]

    async def get_agent_requirements(self):
        """Get the agent requirements for the agent."""
        llm_model, display_name = await self.get_llm()
        if llm_model is None:
            msg = "No language model selected. Please choose a model to proceed."
            raise ValueError(msg)
        self.model_name = get_model_name(llm_model, display_name=display_name)

        # Get memory data
        self.chat_history = await self.get_memory_data()
        await logger.adebug(f"Retrieved {len(self.chat_history)} chat history messages")
        if isinstance(self.chat_history, Message):
            self.chat_history = [self.chat_history]

        # Add current date tool if enabled
        if self.add_current_date_tool:
            if not isinstance(self.tools, list):  # type: ignore[has-type]
                self.tools = []
            current_date_tool = (await CurrentDateComponent(**self.get_base_args()).to_toolkit()).pop(0)

            if not isinstance(current_date_tool, StructuredTool):
                msg = "CurrentDateComponent must be converted to a StructuredTool"
                raise TypeError(msg)
            self.tools.append(current_date_tool)

        # Set shared callbacks for tracing the tools used by the agent
        self.set_tools_callbacks(self.tools, self._get_shared_callbacks())

        return llm_model, self.chat_history, self.tools

    async def message_response(self) -> Message:
        try:
            llm_model, self.chat_history, self.tools = await self.get_agent_requirements()
            # Set up and run agent
            self.set(
                llm=llm_model,
                tools=self.tools or [],
                chat_history=self.chat_history,
                input_value=self.input_value,
                system_prompt=self.system_prompt,
            )
            agent = self.create_agent_runnable()
            result = await self.run_agent(agent)

            # Store result for potential JSON output
            self._agent_result = result

        except (ValueError, TypeError, KeyError) as e:
            await logger.aerror(f"{type(e).__name__}: {e!s}")
            raise
        except ExceptionWithMessageError as e:
            await logger.aerror(f"ExceptionWithMessageError occurred: {e}")
            raise
        # Avoid catching blind Exception; let truly unexpected exceptions propagate
        except Exception as e:
            await logger.aerror(f"Unexpected error: {e!s}")
            raise
        else:
            return result

    def _preprocess_schema(self, schema):
        """Preprocess schema to ensure correct data types for build_model_from_schema."""
        processed_schema = []
        for field in schema:
            processed_field = {
                "name": str(field.get("name", "field")),
                "type": str(field.get("type", "str")),
                "description": str(field.get("description", "")),
                "multiple": field.get("multiple", False),
            }
            # Ensure multiple is handled correctly
            if isinstance(processed_field["multiple"], str):
                processed_field["multiple"] = processed_field["multiple"].lower() in [
                    "true",
                    "1",
                    "t",
                    "y",
                    "yes",
                ]
            processed_schema.append(processed_field)
        return processed_schema

    async def build_structured_output_base(self, content: str):
        """Build structured output with optional BaseModel validation."""
        json_pattern = r"\{.*\}"
        schema_error_msg = "Try setting an output schema"

        # Try to parse content as JSON first
        json_data = None
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError:
            json_match = re.search(json_pattern, content, re.DOTALL)
            if json_match:
                try:
                    json_data = json.loads(json_match.group())
                except json.JSONDecodeError:
                    return {"content": content, "error": schema_error_msg}
            else:
                return {"content": content, "error": schema_error_msg}

        # If no output schema provided, return parsed JSON without validation
        if not hasattr(self, "output_schema") or not self.output_schema or len(self.output_schema) == 0:
            return json_data

        # Use BaseModel validation with schema
        try:
            processed_schema = self._preprocess_schema(self.output_schema)
            output_model = build_model_from_schema(processed_schema)

            # Validate against the schema
            if isinstance(json_data, list):
                # Multiple objects
                validated_objects = []
                for item in json_data:
                    try:
                        validated_obj = output_model.model_validate(item)
                        validated_objects.append(validated_obj.model_dump())
                    except ValidationError as e:
                        await logger.aerror(f"Validation error for item: {e}")
                        # Include invalid items with error info
                        validated_objects.append({"data": item, "validation_error": str(e)})
                return validated_objects

            # Single object
            try:
                validated_obj = output_model.model_validate(json_data)
                return [validated_obj.model_dump()]  # Return as list for consistency
            except ValidationError as e:
                await logger.aerror(f"Validation error: {e}")
                return [{"data": json_data, "validation_error": str(e)}]

        except (TypeError, ValueError) as e:
            await logger.aerror(f"Error building structured output: {e}")
            # Fallback to parsed JSON without validation
            return json_data

    async def json_response(self) -> Data:
        """Convert agent response to structured JSON Data output with schema validation."""
        # Always use structured chat agent for JSON response mode for better JSON formatting
        try:
            system_components = []

            # 1. Agent Instructions (system_prompt)
            agent_instructions = getattr(self, "system_prompt", "") or ""
            if agent_instructions:
                system_components.append(f"{agent_instructions}")

            # 2. Format Instructions
            format_instructions = getattr(self, "format_instructions", "") or ""
            if format_instructions:
                system_components.append(f"Format instructions: {format_instructions}")

            # 3. Schema Information from BaseModel
            if hasattr(self, "output_schema") and self.output_schema and len(self.output_schema) > 0:
                try:
                    processed_schema = self._preprocess_schema(self.output_schema)
                    output_model = build_model_from_schema(processed_schema)
                    schema_dict = output_model.model_json_schema()
                    schema_info = (
                        "You are given some text that may include format instructions, "
                        "explanations, or other content alongside a JSON schema.\n\n"
                        "Your task:\n"
                        "- Extract only the JSON schema.\n"
                        "- Return it as valid JSON.\n"
                        "- Do not include format instructions, explanations, or extra text.\n\n"
                        "Input:\n"
                        f"{json.dumps(schema_dict, indent=2)}\n\n"
                        "Output (only JSON schema):"
                    )
                    system_components.append(schema_info)
                except (ValidationError, ValueError, TypeError, KeyError) as e:
                    await logger.aerror(f"Could not build schema for prompt: {e}", exc_info=True)

            # Combine all components
            combined_instructions = "\n\n".join(system_components) if system_components else ""
            llm_model, self.chat_history, self.tools = await self.get_agent_requirements()
            self.set(
                llm=llm_model,
                tools=self.tools or [],
                chat_history=self.chat_history,
                input_value=self.input_value,
                system_prompt=combined_instructions,
            )

            # Create and run structured chat agent
            try:
                structured_agent = self.create_agent_runnable()
            except (NotImplementedError, ValueError, TypeError) as e:
                await logger.aerror(f"Error with structured chat agent: {e}")
                raise
            try:
                result = await self.run_agent(structured_agent)
            except (
                ExceptionWithMessageError,
                ValueError,
                TypeError,
                RuntimeError,
            ) as e:
                await logger.aerror(f"Error with structured agent result: {e}")
                raise
            # Extract content from structured agent result
            if hasattr(result, "content"):
                content = result.content
            elif hasattr(result, "text"):
                content = result.text
            else:
                content = str(result)

        except (
            ExceptionWithMessageError,
            ValueError,
            TypeError,
            NotImplementedError,
            AttributeError,
        ) as e:
            await logger.aerror(f"Error with structured chat agent: {e}")
            # Fallback to regular agent
            content_str = "No content returned from agent"
            return Data(data={"content": content_str, "error": str(e)})

        # Process with structured output validation
        try:
            structured_output = await self.build_structured_output_base(content)

            # Handle different output formats
            if isinstance(structured_output, list) and structured_output:
                if len(structured_output) == 1:
                    return Data(data=structured_output[0])
                return Data(data={"results": structured_output})
            if isinstance(structured_output, dict):
                return Data(data=structured_output)
            return Data(data={"content": content})

        except (ValueError, TypeError) as e:
            await logger.aerror(f"Error in structured output processing: {e}")
            return Data(data={"content": content, "error": str(e)})

    async def get_memory_data(self):
        # TODO: This is a temporary fix to avoid message duplication. We should develop a function for this.
        messages = (
            await MemoryComponent(**self.get_base_args())
            .set(
                session_id=self.graph.session_id,
                context_id=self.context_id,
                order="Ascending",
                n_messages=self.n_messages,
            )
            .retrieve_messages()
        )
        return [
            message for message in messages if getattr(message, "id", None) != getattr(self.input_value, "id", None)
        ]

    async def get_llm(self):
        if not isinstance(self.agent_llm, str):
            return self.agent_llm, None

        try:
            provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
            if not provider_info:
                msg = f"Invalid model provider: {self.agent_llm}"
                raise ValueError(msg)

            component_class = provider_info.get("component_class")
            display_name = component_class.display_name
            inputs = provider_info.get("inputs")
            prefix = provider_info.get("prefix", "")

            return self._build_llm_model(component_class, inputs, prefix), display_name

        except (AttributeError, ValueError, TypeError, RuntimeError) as e:
            await logger.aerror(f"Error building {self.agent_llm} language model: {e!s}")
            msg = f"Failed to initialize language model: {e!s}"
            raise ValueError(msg) from e

    def _build_llm_model(self, component, inputs, prefix=""):
        model_kwargs = {}
        for input_ in inputs:
            if hasattr(self, f"{prefix}{input_.name}"):
                model_kwargs[input_.name] = getattr(self, f"{prefix}{input_.name}")
        return component.set(**model_kwargs).build_model()

    def set_component_params(self, component):
        provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
        if provider_info:
            inputs = provider_info.get("inputs")
            prefix = provider_info.get("prefix")
            # Filter out json_mode and only use attributes that exist on this component
            model_kwargs = {}
            for input_ in inputs:
                if hasattr(self, f"{prefix}{input_.name}"):
                    model_kwargs[input_.name] = getattr(self, f"{prefix}{input_.name}")

            return component.set(**model_kwargs)
        return component

    def delete_fields(self, build_config: dotdict, fields: dict | list[str]) -> None:
        """Delete specified fields from build_config."""
        for field in fields:
            if build_config is not None and field in build_config:
                build_config.pop(field, None)

    def update_input_types(self, build_config: dotdict) -> dotdict:
        """Update input types for all fields in build_config."""
        for key, value in build_config.items():
            if isinstance(value, dict):
                if value.get("input_types") is None:
                    build_config[key]["input_types"] = []
            elif hasattr(value, "input_types") and value.input_types is None:
                value.input_types = []
        return build_config

    async def update_build_config(
        self, build_config: dotdict, field_value: str, field_name: str | None = None
    ) -> dotdict:
        # Iterate over all providers in the MODEL_PROVIDERS_DICT
        # Existing logic for updating build_config
        if field_name in ("agent_llm",):
            build_config["agent_llm"]["value"] = field_value
            provider_info = MODEL_PROVIDERS_DICT.get(field_value)
            if provider_info:
                component_class = provider_info.get("component_class")
                if component_class and hasattr(component_class, "update_build_config"):
                    # Call the component class's update_build_config method
                    build_config = await update_component_build_config(
                        component_class, build_config, field_value, "model_name"
                    )

            provider_configs: dict[str, tuple[dict, list[dict]]] = {
                provider: (
                    MODEL_PROVIDERS_DICT[provider]["fields"],
                    [
                        MODEL_PROVIDERS_DICT[other_provider]["fields"]
                        for other_provider in MODEL_PROVIDERS_DICT
                        if other_provider != provider
                    ],
                )
                for provider in MODEL_PROVIDERS_DICT
            }
            if field_value in provider_configs:
                fields_to_add, fields_to_delete = provider_configs[field_value]

                # Delete fields from other providers
                for fields in fields_to_delete:
                    self.delete_fields(build_config, fields)

                # Add provider-specific fields
                if field_value == "OpenAI" and not any(field in build_config for field in fields_to_add):
                    build_config.update(fields_to_add)
                else:
                    build_config.update(fields_to_add)
                # Reset input types for agent_llm
                build_config["agent_llm"]["input_types"] = []
                build_config["agent_llm"]["display_name"] = "Model Provider"
            elif field_value == "connect_other_models":
                # Delete all provider fields
                self.delete_fields(build_config, ALL_PROVIDER_FIELDS)
                # # Update with custom component
                custom_component = DropdownInput(
                    name="agent_llm",
                    display_name="Language Model",
                    info="The provider of the language model that the agent will use to generate responses.",
                    options=[*MODEL_PROVIDERS_LIST],
                    real_time_refresh=True,
                    refresh_button=False,
                    input_types=["LanguageModel"],
                    placeholder="Awaiting model input.",
                    options_metadata=[MODELS_METADATA[key] for key in MODEL_PROVIDERS_LIST if key in MODELS_METADATA],
                    external_options={
                        "fields": {
                            "data": {
                                "node": {
                                    "name": "connect_other_models",
                                    "display_name": "Connect other models",
                                    "icon": "CornerDownLeft",
                                },
                            }
                        },
                    },
                )
                build_config.update({"agent_llm": custom_component.to_dict()})
            # Update input types for all fields
            build_config = self.update_input_types(build_config)

            # Validate required keys
            default_keys = [
                "code",
                "_type",
                "agent_llm",
                "tools",
                "input_value",
                "add_current_date_tool",
                "system_prompt",
                "agent_description",
                "max_iterations",
                "handle_parsing_errors",
                "verbose",
            ]
            missing_keys = [key for key in default_keys if key not in build_config]
            if missing_keys:
                msg = f"Missing required keys in build_config: {missing_keys}"
                raise ValueError(msg)
        if (
            isinstance(self.agent_llm, str)
            and self.agent_llm in MODEL_PROVIDERS_DICT
            and field_name in MODEL_DYNAMIC_UPDATE_FIELDS
        ):
            provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
            if provider_info:
                component_class = provider_info.get("component_class")
                component_class = self.set_component_params(component_class)
                prefix = provider_info.get("prefix")
                if component_class and hasattr(component_class, "update_build_config"):
                    # Call each component class's update_build_config method
                    # remove the prefix from the field_name
                    if isinstance(field_name, str) and isinstance(prefix, str):
                        field_name_without_prefix = field_name.replace(prefix, "")
                    else:
                        field_name_without_prefix = field_name
                    build_config = await update_component_build_config(
                        component_class, build_config, field_value, field_name_without_prefix
                    )
        return dotdict({k: v.to_dict() if hasattr(v, "to_dict") else v for k, v in build_config.items()})

    async def _get_tools(self) -> list[Tool]:
        component_toolkit = get_component_toolkit()
        tools_names = self._build_tools_names()
        agent_description = self.get_tool_description()
        # TODO: Agent Description Depreciated Feature to be removed
        description = f"{agent_description}{tools_names}"

        tools = component_toolkit(component=self).get_tools(
            tool_name="Call_Agent",
            tool_description=description,
            # here we do not use the shared callbacks as we are exposing the agent as a tool
            callbacks=self.get_langchain_callbacks(),
        )
        if hasattr(self, "tools_metadata"):
            tools = component_toolkit(component=self, metadata=self.tools_metadata).update_tools_metadata(tools=tools)

        return tools

```

That's a lot. It's good that you _may_ not need to work this much, but it might make it difficult to build new custom agents or integrate third-party stuff. We'll see...

