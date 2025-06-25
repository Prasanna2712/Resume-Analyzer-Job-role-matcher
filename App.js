import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [resume, setResume] = useState('');
  const [jd, setJD] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/match', {
        resume,
        jd
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Resume Analyzer & Job Matcher</h1>

      <textarea
        placeholder="Paste Resume Text Here"
        rows={8}
        value={resume}
        onChange={(e) => setResume(e.target.value)}
      />
      <textarea
        placeholder="Paste Job Description Here"
        rows={8}
        value={jd}
        onChange={(e) => setJD(e.target.value)}
      />

      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div className="result">
          <h3>Match Score: {result.match_score}%</h3>
          <h4>Missing Keywords:</h4>
          <ul>
            {result.missing_keywords.map((word, idx) => (
              <li key={idx}>{word}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
