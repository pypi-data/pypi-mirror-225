import openai
import numpy as np


def AskGPT(model: str, context: list, temperature: float = 1) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=context,
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"]


def GetEmbedding(String: str) -> list:
    data = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=String
    )
    return data["data"][0]["embedding"]


def GetEmbeddingDistance(Embedding1: list, Embedding2: list) -> float:
    data1 = np.array(Embedding1)
    data2 = np.array(Embedding2)
    distance = np.linalg.norm(data1 - data2)
    return distance

