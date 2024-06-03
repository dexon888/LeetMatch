import React, { useState } from 'react';
import { getAuth, signOut } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/leetmatch.jpg';

function RecommendationForm() {
    const [url, setUrl] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const navigate = useNavigate();
    const auth = getAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('http://localhost:8000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });
        const data = await response.json();
        setRecommendations(data.recommendations || []);
    };

    const handleSignOut = () => {
        signOut(auth).then(() => {
            navigate('/auth');
        }).catch((error) => {
            console.error('Error signing out:', error);
        });
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <img src={logo} alt="LeetMatch Logo" className="w-32 h-32 mb-4" />
            <button onClick={handleSignOut} className="bg-red-500 text-white p-2 rounded mb-4">
                Sign Out
            </button>
            <form onSubmit={handleSubmit} className="w-full max-w-sm mb-4">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter LeetCode problem URL"
                    className="border rounded p-2 w-full mb-4"
                />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">
                    Get Recommendations
                </button>
            </form>
            <div className="recommendations-container">
                {recommendations.map((rec, index) => (
                    <a 
                        key={index}
                        href={`https://leetcode.com/problems/${rec.problem_name}/`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="recommendation-button p-2 rounded mb-2 inline-block text-center w-full"
                    >
                        {rec.problem_name} (Similarity: {rec.similarity.toFixed(4)})
                    </a>
                ))}
            </div>
        </div>
    );
}

export default RecommendationForm;
