# Background

We submitted three version for round 2:
1. covidex.t5 - Rodrigo's T5 implementation ranked 2nd in automatic runs (only 0.001 away from first place)
2. covidex.sim - HNSW version
3. covidex.fuse - RRF of 1 and 2

I was able to re-produce covidex.sim. Here are some interesting findings.

# Observations

Table 1. Basic stats
           
|           | covidex.sim | covidex.t5 |
|-----------|-------------|------------|
| Judged@10 | 0.4971      | 0.937      |
| ndcg@10   | 0.3254      | 0.6250     |

> covidex.t5 was tagged as contributing to the pool hence more docs in covidex.t5 are judged. covidex.t5 performs so well that it almost doubled the score of covidex.sim.

Now if we removed all un-judged docs (based on qrels-rnd2.txt)

|           | covidex.sim | covidex.t5 |
|-----------|-------------|------------|
| Judged@10 | 1           | 1          |
| ndcg@10   | 0.5958      | 0.6499     |

> Naturally, both will have a Judged@10 of 1. We see a jumpy in ndcg@10 for both. covidex.t5 jumped by a little and covidx.sim jump by a lot. The increase in covidex.sim is large enough that it almost catches up to covidex.t5, but still 0.5 apart by ndcg@10. It seems to me that covidex.sim < covidex.t5 even if covidex.sim is tagged as contributing to the pool.

With un-judged docs removed, here's the per-topic breakdown.

|             |       topic | covidex.sim | covidex.t5 |
|-------------|-------------|-------------|------------|
|     ndcg@10 |         1   |     0.8358  |     0.3689 |
|     ndcg@10 |         2   |     1.0000  |     1.0000 |
|     ndcg@10 |         3   |     0.2842  |     0.6994 |
|     ndcg@10 |         4   |     0.5052  |     0.4938 |
|     ndcg@10 |         5   |     0.6482  |     0.7334 |
|     ndcg@10 |         6   |     0.8264  |     0.6959 |
|     ndcg@10 |         7   |     0.7663  |     0.3984 |
|     ndcg@10 |         8   |     0.2571  |     0.9266 |
|     ndcg@10 |         9   |     0.2999  |     0.6469 |
|     ndcg@10 |         10  |     0.9669  |     0.8514 |
|     ndcg@10 |         11  |     0.0000  |     0.8739 |
|     ndcg@10 |         12  |     0.5976  |     0.5554 |
|     ndcg@10 |         13  |     0.4725  |     0.3775 |
|     ndcg@10 |         14  |     0.2685  |     0.3485 |
|     ndcg@10 |         15  |     0.3716  |     0.0318 |
|     ndcg@10 |         16  |     0.2657  |     0.2203 |
|     ndcg@10 |         17  |     0.6235  |     0.5010 |
|     ndcg@10 |         18  |     0.4787  |     0.9608 |
|     ndcg@10 |         19  |     0.4612  |     0.0694 |
|     ndcg@10 |         20  |     0.4627  |     0.9653 |
|     ndcg@10 |         21  |     0.6146  |     0.6253 |
|     ndcg@10 |         22  |     0.7007  |     0.8459 |
|     ndcg@10 |         23  |     0.7819  |     0.8201 |
|     ndcg@10 |         24  |     0.4243  |     0.7569 |
|     ndcg@10 |         25  |     1.0000  |     1.0000 |
|     ndcg@10 |         26  |     0.9682  |     0.9017 |
|     ndcg@10 |         27  |     0.8076  |     1.0000 |
|     ndcg@10 |         28  |     0.9633  |     0.9682 |
|     ndcg@10 |         29  |     0.6985  |     0.4596 |
|     ndcg@10 |         30  |     0.5361  |     0.6873 |
|     ndcg@10 |         31  |     0.4419  |     0.4419 |
|     ndcg@10 |         32  |     0.4374  |     0.4374 |
|     ndcg@10 |         33  |     0.6792  |     0.6792 |
|     ndcg@10 |         34  |     0.4374  |     0.4374 |
|     ndcg@10 |         35  |     0.9682  |     0.9682 |

> Topic 31-35 are directly copied from covidex.t5 to covidex.sim since these topics are new in round 2 and covidex.sim relies on prior qrels to work. We've seen from the previous table that covidex.t5 performs better than covidex.sim overall. Notice that covidex.sim can significantly beat covidex.t5 in some topics (e.g. Topic 1 or Topic 19). Vice versa, covidex.t5 does the same in some other topics (e.g. Topic 8 or Topic 18).

Zooming into Topic 3, covidex.t5 beats covidex.sim by a long shot with a ndcg@10 of 0.6469 vs 0.2999.

| covidex.sim | rank | actual relevance | title |
|-------------|------|------------------|-------|
| aqwdg489    |    1 |                0 | A simple method to quantify country-specific effects of COVID-19 containment measures |
| 51g3vhcx    |    2 |                2 | Mathematical modeling of COVID-19 containment strategies with considerations for limited medical resources |
| 6ymuovl2    |    3 |                0 | COVID-19 Progression Timeline and Effectiveness of Response-to-Spread Interventions across the United States |
| od97az43    |    4 |                2 | Modelling the transmission dynamics of COVID-19 in six high burden countries |
| dufooku2    |    5 |                0 | The impact of current and future control measures on the spread of COVID-19 in Germany |

> Topic 9's question prompt is "how has COVID-19 affected Canada?" It seems like HNSW does a poor job finding relevant documents for this topic. It's really a hit or miss, but HNSW believes that these are the top 5 related documents to topic 9. Docs with rank 1, 3 & 5 are irrelevant since it's talking about other countries such as USA and Germany. HNSW believes its relevant since it's talking about how COVID-19 has affected countries in general. I'm guessing here the word vector embedding for Canada is very close to USA and Germany since these are all country related words. But with HNSW, there's no way to emphasize that we value the term "Canada" more than "the influence of COVID". SPECTER embedding is great at capturing the essense of documents' meaning in vector notations; we can't argue that it's wrong in this case. HNSW is not wrong either for calculating a simple L2 distance between two vectors. Maybe we need to utilize the embedding in a more fine-tune way to control the definition of relevancy to improve the performance of this method for round 3.


# Personal Reflection

This is my first round of TREC COVID. Throughout this process, I was quite confused with what's going on and how different pieces fit together. Looking back, I have a much clearer picture now with what to expect, what to do and what to focus on for the next round. Hopefully, I can start to make some suggestions on our approach and critically analyze why A performs better than B. 

I spent half a day today trying to replicate covid.sim, which is a strong signal for better software engineering practice. I need to improve my file/variable naming and organize my script/folder structure better (especially when running many experiments that are very similar but with different parameters). 

Special thanks to Rodrigo and Prof. Lin for guiding me throughout this process.

Onward to round 3 🚀
