#!/usr/bin/env python3
"""
Resume embedding from a specific batch number.
Usage: python3 embed_resume.py --start_batch 15
"""

import json
import torch
import argparse
from pathlib import Path
from FlagEmbedding import BGEM3FlagModel
import weaviate
from weaviate.classes.init import AdditionalConfig
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from tqdm import tqdm


MODEL_PATH = str(Path(__file__).parent.parent / 'models' / 'bge-m3')


def load_model():
    """Load BGE-M3 model."""
    print(f"Loading BGE-M3 from {MODEL_PATH}...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = BGEM3FlagModel(MODEL_PATH, use_fp16=True, devices=device)
    print(f"Model loaded on {device}")
    return model


def get_embeddings(texts, model, max_length=2048):
    """Get dense embeddings for a list of texts."""
    output = model.encode(texts, max_length=max_length, return_dense=True,
                          return_sparse=False, return_colbert_vecs=False)
    return output['dense_vecs'].tolist()


def setup_weaviate():
    """Setup Weaviate client and collection with 1024-dim vectors."""
    print("Setting up Weaviate...")
    data_path = str(Path(__file__).parent.parent / 'weaviate_data')

    client = weaviate.connect_to_embedded(
        headers={},
        persistence_data_path=data_path,
        additional_config=AdditionalConfig(timeout=(5, 120))
    )

    # Check if collection exists
    if not client.collections.exists("PhysicsChunks"):
        # Create collection with 1024-dim vectors
        collection = client.collections.create(
            name="PhysicsChunks",
            properties=[
                Property(name="book", data_type=DataType.TEXT),
                Property(name="chapter", data_type=DataType.TEXT),
                Property(name="section", data_type=DataType.TEXT),
                Property(name="title", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="type", data_type=DataType.TEXT),
                Property(name="chunkIndex", data_type=DataType.INT),
                Property(name="totalChunks", data_type=DataType.INT),
                Property(name="imagePaths", data_type=DataType.TEXT_ARRAY),
            ],
            vectorizer_config=Configure.Vectorizer.none(),
            vector_index_config=Configure.VectorIndex.hnsw(
                vector_cache_max_objects=10000,
            ),
        )
        print("Weaviate collection created (1024-dim)")
    else:
        collection = client.collections.get("PhysicsChunks")
        print("Weaviate collection already exists")

    return client, collection


def main():
    parser = argparse.ArgumentParser(description="Resume embedding from specific batch")
    parser.add_argument("--start_batch", type=int, default=0,
                       help="Batch number to start from (default: 0)")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent / 'merged'
    chunks_file = base_dir / 'chunks_combined.json'

    print(f"Loading chunks from {chunks_file}...")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    print(f"Loaded {len(chunks)} chunks")

    model = load_model()
    client, collection = setup_weaviate()

    batch_size = 32
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    start_batch = args.start_batch

    print(f"\nResuming from batch {start_batch}/{total_batches}")
    print(f"Skipping first {start_batch * batch_size} chunks")

    inserted = 0
    for batch_idx in tqdm(range(start_batch, total_batches), desc="Embedding batches", initial=start_batch, total=total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(chunks))
        batch_chunks = chunks[start_idx:end_idx]

        # Use content for embedding
        texts = [c['content'] for c in batch_chunks]
        embeddings = get_embeddings(texts, model)

        objects = []
        for chunk, emb in zip(batch_chunks, embeddings):
            objects.append(DataObject(
                properties={
                    "book": chunk['book'],
                    "chapter": str(chunk.get('chapter', '') or ''),
                    "section": str(chunk.get('section', '') or ''),
                    "title": chunk['title'],
                    "content": chunk['content'],
                    "type": chunk.get('type', 'content'),
                    "chunkIndex": chunk.get('chunk_index', 0),
                    "totalChunks": chunk.get('total_chunks', 1),
                    "imagePaths": chunk.get('images', []),
                },
                vector=emb,
            ))

        try:
            collection.data.insert_many(objects)
            inserted += len(objects)
        except Exception as e:
            print(f"\nError inserting batch {batch_idx}: {e}")
            continue

    print(f"\nDone! Inserted {inserted} chunks (batches {start_batch}-{total_batches-1})")

    # Count total in collection
    count = collection.aggregate.over_all(total_count=True)
    print(f"Total chunks in Weaviate: {count.total_count}")

    client.close()


if __name__ == '__main__':
    main()
