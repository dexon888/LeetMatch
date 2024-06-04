import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Remove Link import
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import logo from '../assets/leetmatch.jpg';

const Auth = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSignup, setIsSignup] = useState(false);
    const navigate = useNavigate();
    const auth = getAuth();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            if (isSignup) {
                await createUserWithEmailAndPassword(auth, email, password);
            } else {
                await signInWithEmailAndPassword(auth, email, password);
            }
            navigate('/');
        } catch (error) {
            console.error('Error signing up:', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <img src={logo} alt="LeetMatch Logo" className="w-32 h-32 mb-4" />
            <form onSubmit={handleSignup} className="w-full max-w-sm">
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    className="border rounded p-2 w-full mb-4"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    className="border rounded p-2 w-full mb-4"
                />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">
                    {isSignup ? 'Sign Up' : 'Log In'}
                </button>
            </form>
            <div className="mt-4">
                {isSignup ? (
                    <p>
                        Already have an account?{' '}
                        <button onClick={() => setIsSignup(false)} className="text-blue-600 underline">
                            Log In
                        </button>
                    </p>
                ) : (
                    <p>
                        Don't have an account?{' '}
                        <button onClick={() => setIsSignup(true)} className="text-blue-600 underline">
                            Sign Up
                        </button>
                    </p>
                )}
            </div>
        </div>
    );
};

export default Auth;
