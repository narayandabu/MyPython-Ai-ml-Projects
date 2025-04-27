import React, { useEffect, useState } from "react";
import axiosInstance from './utils/axiosInstance';
import "./styles/papers_display.css";

const PapersDisplay = ({ userEmail }) => {
  const [papers, setPapers] = useState([]);

  useEffect(() => {
    axiosInstance
      .get(`http://localhost:5000/api/papers/recommended?user=${userEmail}`)
      .then((res) => {
        setPapers(res.data);
      })
      .catch((err) => console.error("Failed to fetch papers:", err));
  }, [userEmail]);
  
  const renderPaperCard = (paper, index) => (
    console.log(index),
    <div key={index} className="paper-card">
      <h3 className="paper-title">{paper.title}</h3>
      <p className="paper-abstract">
        {paper.abstract.length > 250 ? paper.abstract.slice(0, 250) + "..." : paper.abstract}
      </p>
      <div className="paper-meta">
        <span><strong>Authors:</strong> {paper.authors}</span><br />
        <span><strong>Published in:</strong> {paper.journal} ({paper.year})</span><br />
        {paper.domain && (
          <span className="paper-badge">{paper.domain}</span>
        )}
      </div>
      <a
        href={paper.link}
        target="_blank"
        rel="noopener noreferrer"
        className="read-more"
      >
        Read Full Paper
      </a>
    </div>
  );
  return (
    <>
    <div className="papers-display-container">
      <h1 className="Main-title">📚 Papers</h1>
      <h2 className="section-title">📚 Today's Top Three</h2>
      <div className="papers-row-scroll">
            {papers.map((paper, index) => renderPaperCard(paper,index))}
      </div>
      <h1 className="section-title">📚 Recommended</h1>
      <div className="papers-row-scroll">
            {papers.map((paper, index) => renderPaperCard(paper,index))}
      </div>
      <h1 className="section-title">📚 More Papers</h1>
      {/* <div className="papers-row-scroll"> */}
      <div className="more-papers">
            {papers.map((paper, index) => renderPaperCard(paper,index))}
      </div>
    </div>
      <div></div>
    </>
  );
};
export default PapersDisplay;
