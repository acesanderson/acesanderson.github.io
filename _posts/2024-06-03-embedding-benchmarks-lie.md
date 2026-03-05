⚡ gemini-3.1-pro-preview | You are a precise editorial critic. Your job is to identify AI-generated writing patterns in a blog ... | 
Cached (0.729s)
⚡ claude-opus-4-6 | You are a precise line editor. Revise the blog post draft based on the critique below.  Rules: - Fix... | Cached 
(0.034s)
Final Draft:
 

---
layout: default
title: "Embedding benchmarks lie (at least for your use case)"
date: 2024-06-03
---

# Embedding benchmarks lie (at least for your use case)

If you've spent any time building RAG systems, you've probably ended up on the MTEB
leaderboard at some point. It's the standard reference for embedding model performance:
a massive multilingual benchmark with dozens of tasks, thousands of papers citing it,
and a clean ranked list that makes it easy to just pick the top model and move on.

Tldr: you REALLY need to understand your own use case, and run your own tests. This
is especially true for embedding models.

---

## What I was building

I was building a course recommender for a library of 20,000+ online courses. The core
retrieval task: given a natural language query like "I want to learn about generative AI
for product managers," find the most relevant courses from the catalog.

This is a classic semantic search problem. You embed the query and the catalog entries,
then find nearest neighbors by cosine similarity. One design you have to make: which embedding model to use?

I started with the ChromaDB default, which is `all-minilm-l6-v2`. It worked fine. But
I'd read enough about embeddings to know that newer, larger models score significantly
higher on MTEB. The Salesforce `SFR-Embedding-Mistral` model, for example, was near the
top of the leaderboard at the time. So were a few Arctic models. Switching to one of
those should make my retrieval better, right?

So I decided to actually test it instead of assuming.

---

## The experiment

I set up a systematic evaluation across seven models:

- `all-minilm-l6-v2` (ChromaDB default)
- `all-minilm-latest` (newer version of the same family)
- `nomic-embed-text`
- `mxbai-embed-large`
- `snowflake-arctic-embed`
- `e5-large-v2`
- Salesforce `SFR-Embedding-Mistral`

For each model, I embedded the course catalog in two ways: using short descriptions
(title + one-line summary) and long descriptions (full course abstract). That gave me
fourteen collections to test.

One thing I ran into: ChromaDB has a built-in abstraction for custom embedding
models, but it requires you to pass the embedding model every time you access the
collection, which is a constant source of mismatches and silent errors. I bypassed it entirely
and used the Ollama Python client directly, generating embeddings with `ollama.embeddings`
for both ingestion and query. More explicit, fewer surprises.

Then I wrote thirteen evaluation queries. Some were specific skill queries ("Python
async programming"), some were broader topic queries ("machine learning for beginners"),
and some were role-based ("data engineering for analysts"). For each query, I retrieved the
top ten results from each collection, reviewed them manually, and scored them.

The harness itself was straightforward:

```python
results = {}
for i, query in enumerate(queries):
    print(f"Running query {i + 1} of {len(queries)}")
    query_results = {}
    for index, m in enumerate(models_iterator):
        print(f"\tRunning model {index + 1} of {len(models_iterator)}: {m[0]}.")
        for collection in m[1]:
            try:
                result = query_descriptions(query, n_results=10, collection=collection, model=m[0])
                query_results[m[0] + " " + collection] = result
            except:
                print(f"Error for model {m[0]} and collection {collection}.")
    results[query] = query_results
```

`models_iterator` is a list of `(model_name, [collection_names])` tuples — one entry
per model, with both the short and long description collection for each. The whole thing
ran overnight. I scored the results in a spreadsheet the next morning.

## The results

`all-minilm` won hands-down. Not a particular version — the difference between `l6` and `latest` was negligible — but the family as a whole, beating everything else in the field.

`nomic` was decent. `mxbai` got a C. `arctic`, `e5`, and Salesforce were genuinely
bad — returning irrelevant courses, misinterpreting queries, and in some cases returning
what looked like random results.

The MTEB rankings, if you checked them at the time, told essentially the opposite story.
The Salesforce model scored near the top. `all-minilm-l6` scored near the bottom.

## Why this happened

My best guess is that this is a record-length mismatch problem.

The MTEB benchmark includes tasks with long documents — retrieval from Wikipedia
paragraphs, semantic textual similarity between sentences, etc. The high-scoring models
are optimized to represent rich, lengthy text well.

My course descriptions are short. A typical entry is one or two sentences — catalog
copy, not academic prose. The queries are also short: five to ten words.

`all-minilm` was specifically designed for semantic matching of short records. It
dominates on tasks where both the query and the document are compact. The fancier models
may actually be penalized by the mismatch — they're looking for the kind of semantic
density that a one-line course title doesn't provide.

The `e5` and Salesforce models in particular strongly preferred short results that
matched the query length, regardless of actual relevance. If your query was six words,
you'd get back courses with six-word titles whether or not the content was relevant.

---

## The takeaway

The practical implication: before you commit to an embedding model for production, run
your own evaluation. You need:

1. A representative sample of your actual documents
2. A set of queries that reflect real usage
3. Some method of scoring results — even rough manual scoring works

This doesn't have to be elaborate. Mine was a spreadsheet. It took a few hours of
compute time and a morning of manual review.
