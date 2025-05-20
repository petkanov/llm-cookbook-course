# Detailed Bullet-Point Summary of Large Language Models (rLLMs) like ChatGPT

## Overview of Large Language Models (LLMs)

- Comprehensive intro to LLMs for general audience: how they work, are built, their strengths, and limitations.
- Goal: Provide mental models to understand tools like ChatGPT, which are "magical" yet have sharp edges.
- Key questions: What happens behind the text box? What generates responses? What are you interacting with?

## Building Large Language Models: The Pre-Training Stage
This is the full flow: 
from raw text collection → visualizing it → representing it in binary → compressing it with bytes → further optimizing with BPE → arriving at the token vocabulary used in state-of-the-art models like GPT-4 → giving tokens to the model → receiving response from the model

- **Data Collection and Preparation**
  - Trained on massive internet text datasets.
  - Example: FineWeb by Hugging Face (\~44 terabytes filtered).
  - Source: Common Crawl (2.7 billion pages since 2007).
  - Filtering: URL blocklists (malware, spam), HTML text extraction, language focus (e.g., &gt;65% English), de-duplication, PII removal.
  - Goal: Large, diverse, high-quality text corpus.

- **Visualization of Text Data**
  - The speaker selected the **first 200 web pages** as a sample.
  - All the text from these pages was **concatenated into one continuous block**.
  - This raw internet text is **massive** and filled with **patterns**.
  - The goal: use this **textual data to train neural networks** that can model how text flows.

- **Preparing Text for Neural Networks**
	-	Neural networks expect input as a one-dimensional sequence of symbols from a finite set (a vocabulary).
	-	Though text looks two-dimensional on screen, it is interpreted by the model as a linear, one-dimensional sequence.

- **Binary Representation – UTF-8 Encoding**
	-	Text is encoded using UTF-8, which converts characters into raw binary bits.
	-	Example: one bar shown corresponds to the first 8 bits (1 byte) of the text.
	-	Binary (0 and 1) is too granular and inefficient for language modeling:
	-	Long sequences with just 2 possible symbols (0 and 1).
	-	This is inefficient for neural networks due to limited sequence length.

- **Introducing Bytes (8-bit Grouping)**
	-	A naive compression method: group bits into bytes (8 bits).
	-	This reduces the sequence length by a factor of 8.
	-	Now there are 256 possible symbols (values from 0 to 255).
	-	These byte values can be thought of as unique symbols or emojis, not just numbers.

- **Optimizing Token Representation – Byte Pair Encoding (BPE)**
	-	Even with 256 symbols, further compression is beneficial.
	-	Use Byte Pair Encoding (BPE) to:
	  -	Find frequent adjacent byte pairs.
	  -	Replace them with a new symbol (e.g., ID 256, then 257, etc.). 
    This shortens the sequence further while increasing vocabulary size.
    The process is iterative and can continue to reduce sequence length.

- **Tokenization summary**
  - Text → tokens (unique IDs for text chunks) for neural processing.
  - Uses Byte Pair Encoding (BPE); GPT-4 has \~100,000 tokens.
  - Balances vocabulary size vs. sequence length.
  - Demonstrates tokenization using a tool called `Tiktokenizer`: how GPT-4 processes text by converting it into tokens and then back to text.

-	**Using Tiktokenizer Tool**
	-	User selects the cl100k_base tokenizer (GPT-4’s base model tokenizer).
	-	Example: Input "hello world" is tokenized into:
     "hello" → Token ID 15339 and " world" → Token ID 1917

- **Tokenization Behavior** 
    - Tokenization is case-sensitive. "Hello World" tokenizes differently than "hello world". Extra spaces between words change the token sequence.
    Example: Two spaces between "hello" and "world" generate a different token like 220.
	-	Token boundaries are not always intuitive and depend on tokenizer vocabulary.
- **Visualizing Tokens**
	-	Demonstrates that a line of text corresponds to a sequence of token IDs.
	-	Notes the model sees text as a 1D sequence of symbols (tokens) out of a vocabulary of 100,277 tokens.




- **Tokenizing a Dataset**
	•	A large dataset (e.g., FineWeb) contains 15 trillion tokens.
	•	This dataset is tokenized into a token sequences.
-	**Context Window for Training**
	•	A window of tokens (e.g., 4 tokens: this, bar, view, in) is selected as context.
	•	The goal is to predict the next token (e.g., "post" → ID 3962) given this context.
-	**Input and Output of the Model**
	•	Input: Variable-length sequence of tokens (context).
	•	Output: A probability distribution over all 100,277 tokens (next-token prediction).
-	**Training Setup**
	•	The model initially has random weights, so its predictions are also random. 
    Example: 
    Token "Direction" might get 4% probability. 
    Token "post" might get 3% (correct answer).
	•	Training objective is to increase probability of the correct next token.
-	**Loss Function and Update**
	•	The model is updated to increase the score of the correct token and decrease others.
	•	Repeatedly feeding the same input after updates results in better predictions.

-	**Parallel Training**
	•	This process happens across many windows and tokens in parallel.
	•	The network is updated in batches during training.
	•	The goal is to match the model’s predicted token probabilities to the true statistical patterns in the training data.

- **Neural Network Training**
  - Predicts next token from context using Transformer architecture.
  - Adjusts billions of parameters to match training data patterns.
  - Process: Updates random parameters with token windows (e.g., 4-8,000 tokens).
  - Requires powerful GPUs due to computational intensity.

- **Inference**

  - Generates text by sampling next token from probability distribution.
  - Stochastic: Same input can yield different outputs.
  - Example: "| viewing single page" might become "| viewing single article" remixing training patterns, influenced by tollerances on 'Temperature' settings 







## Base Models and Their Capabilities
- **Base Models**

  - Pre-training output: Internet text simulators (e.g., GPT-2: 1.6B params; LLaMA 3: 45B params).
  - Not assistants; generate token sequences like training data.
  - Knowledge compressed in parameters (e.g., LLaMA 3 as internet "zip file").

- **In-Context Learning**

  - Adapts to tasks via prompt examples (e.g., translating "teacher" to "선생" in Korean).
  - Requires clever prompt design.

## Post-Training: Turning Base Models into Assistants

- **Post-Training Overview**

  - Makes base models task-specific (e.g., question-answering).
  - Less compute-heavy than pre-training, but vital.
  - Techniques: Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL).

- **Supervised Fine-Tuning (SFT)**

  - Trains on curated datasets (e.g., 1M Q&A pairs) to mimic experts.
  - Human labelers craft responses per guidelines (e.g., OpenAI’s).
  - Simulates a labeler’s response, not raw internet text.

- **Reinforcement Learning (RL)**

  - Rewards correct/desirable outputs.
  - **Verifiable Domains (Math, Code):**
    - Optimizes for correct answers (e.g., "thinking models" like o1, DeepSeek R1).
    - Runs indefinitely, finding novel strategies (e.g., AlphaGo’s Move 37).
  - **Unverifiable Domains (Creative Writing):**
    - Uses RL from Human Feedback (RLHF).
    - Humans rank outputs (e.g., Pelican jokes), training a reward model.
    - Limited by gaming: After \~hundreds of updates, produces nonsense (e.g., "the the the").
    - RLHF offers slight improvement, not pure RL’s "magic."

## Advanced Topics and Future Directions

- **Thinking Models**

  - RL-trained for reasoning (e.g., o1, DeepSeek R1); show internal monologues.
  - Some summarize reasoning (e.g., OpenAI) vs. full display.

- **Multimodality**

  - Will process audio, images, text natively (tokenizing spectrograms, patches).
  - Enables natural interactions (speech, visuals).

- **Longer Context Windows and Agents**

  - Larger token sequences (e.g., millions) for complex tasks.
  - Agents perform long tasks with supervision.

- **Test-Time Training**

  - Fixed post-training now; future may allow inference-time learning.

## Practical Considerations and Limitations

- **Hallucinations and Errors**

  - Fabricates info or fails oddly (e.g., 9.11 vs. 9.9).
  - "Swiss cheese" capability: Broad skills, random gaps.

- **Compute and Hardware**

  - Needs vast resources (e.g., 8x H100 GPUs at $3/GPU/hour).
  - Costs down (e.g., GPT-2: $40,000 in 2019 vs. \~$100 now).

## Accessing and Using LLMs

- **Proprietary:** OpenAI (ChatGPT), Google (Gemini), Anthropic (Claude).
- **Open-Weight:** DeepSeek, LLaMA (e.g., Together.ai).
- **Base Models:** Hyperbolic (LLaMA 3.1 405B base).
- **Local:** LM Studio for smaller models.

## Key Takeaways

- Built in stages: Pre-training (knowledge), SFT (responses), RL (reasoning).
- Powerful tools; verify outputs due to errors.
- Evolving toward multimodality, reasoning, agents.