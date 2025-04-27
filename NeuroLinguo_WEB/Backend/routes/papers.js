// routes/papers.js
const express = require('express');
const router = express.Router();

router.get('/recommended', (req, res) => {
  const samplePapers = [
    {
      title: "A Survey on Transformer Architectures",
      authors: "Jane Doe, John Smith",
      abstract: "This paper provides a comprehensive overview of transformer-based architectures...",
      journal: "IEEE Transactions on Neural Networks",
      year: 2024,
      link: "https://arxiv.org/abs/2401.12345"
    },
    {
      title: "Efficient NLP with Low-Rank Adaptation",
      authors: "Emily Zhang",
      abstract: "Low-rank adaptation has shown promise in fine-tuning language models with fewer parameters...",
      journal: "ACL 2023",
      year: 2023,
      link: "https://arxiv.org/abs/2305.45678"
    },
    {
      title: "BERT: Pre-training of Deep Bidirectional Transformers",
      authors: "Jacob Devlin et al.",
      abstract: "We introduce BERT, a new language representation model...",
      journal: "NAACL 2019",
      year: 2019,
      link: "https://arxiv.org/abs/1810.04805"
    },
    {
      title: "A Survey on Transformer Architectures",
      authors: "Jane Doe, John Smith",
      abstract: "This paper provides a comprehensive overview of transformer-based architectures...",
      journal: "IEEE Transactions on Neural Networks",
      year: 2024,
      link: "https://arxiv.org/abs/2401.12345"
    },
    {
      title: "A Survey on Transformer Architectures",
      authors: "Jane Doe, John Smith",
      abstract: "This paper provides a comprehensive overview of transformer-based architectures...",
      journal: "IEEE Transactions on Neural Networks",
      year: 2024,
      link: "https://arxiv.org/abs/2401.12345"
    },
    {
      title: "A Survey on Transformer Architectures",
      authors: "Jane Doe, John Smith",
      abstract: "This paper provides a comprehensive overview of transformer-based architectures...",
      journal: "IEEE Transactions on Neural Networks",
      year: 2024,
      link: "https://arxiv.org/abs/2401.12345"
    },
  ];

  res.json(samplePapers);
});

module.exports = router;
