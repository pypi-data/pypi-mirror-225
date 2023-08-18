# OpenAI Utility Library Documentation

## Overview

This library provides a set of utility functions to interact with the OpenAI API, specifically for querying GPT models and working with text embeddings.

## IMPORTANT, READ BELOW:

`IMPORTANT: WHEN YOU IMPORT THE PACKAGE, THE PACKAGE NAME IS openai_utils`

### Requirements

- `openai` Python package
- `numpy`

## Functions

### AskGPT

**Description**:
Queries the GPT model with the provided context and returns the model's response.

**Arguments**:
- `model (str)`: The identifier for the GPT model you wish to use.
- `context (list)`: A list of messages that you wish to send to the GPT model. The last message is typically from the user, and previous messages can provide context.

**Returns**:
- `str`: The model's response message.

**Example**:

```python
response = AskGPT("gpt-3.5-turbo", [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Who won the world cup in 2018?"}])
print(response)
```

### GetEmbedding

**Description**:
Generates a text embedding for the given string using the specified model.

**Arguments**:
- `String (str)`: The text for which you wish to generate an embedding.

**Returns**:
- `list`: A list of floats representing the text's embedding.

**Example**:

```python
embedding = GetEmbedding("Hello, world!")
print(embedding)
```

### GetEmbeddingDistance

**Description**:
Computes the difference between two embeddings. 

**Arguments**:
- `Embedding1 (list)`: The first embedding represented as a list of floats.
- `Embedding2 (list)`: The second embedding represented as a list of floats.

**Returns**:
- `float`: The absolute difference between the two embeddings.

**Example**:

```python
embedding1 = GetEmbedding("cat")
embedding2 = GetEmbedding("dog")
distance = GetEmbeddingDistance(embedding1, embedding2)
print(distance)
```

## Configuration

Before using the library, ensure that you have set the `api_key` variable to your OpenAI API key.

```python
api_key = "YOUR_API_KEY_HERE"
```

## Notes

Ensure that your OpenAI account has adequate API call limits and that you are aware of potential costs associated with making too many requests. Always consult OpenAI's official documentation for detailed information on models and API usage.

---

*End of Documentation*