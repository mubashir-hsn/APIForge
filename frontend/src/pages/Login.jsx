import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';
import { apiClient } from '@/api/client';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const res = await apiClient('/auth/login', { method: 'POST', body: { email, password } });
      setAuth({ email }, res.access_token);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md p-8 bg-card rounded-xl shadow-lg border"
      >
        <div className="text-center mb-8">
          <div className="w-10 h-10 bg-accent rounded-lg mx-auto mb-4 flex items-center justify-center">
            <span className="text-white font-bold text-lg">AP</span>
          </div>
          <h2 className="text-2xl font-semibold tracking-tight">Welcome back</h2>
          <p className="text-sm text-gray-500 mt-1">Sign in to your account</p>
        </div>

        {error && <div className="p-3 mb-4 text-sm text-red-500 bg-red-500/10 border border-red-500/20 rounded-md">{error}</div>}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5 text-gray-700 dark:text-gray-300">Email</label>
            <input 
              type="email" 
              required
              className="w-full bg-background border rounded-md px-3 py-2 text-sm focus:ring-1 focus:ring-accent outline-none"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="name@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5 text-gray-700 dark:text-gray-300">Password</label>
            <input 
              type="password" 
              required
              className="w-full bg-background border rounded-md px-3 py-2 text-sm focus:ring-1 focus:ring-accent outline-none"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          
          <Button type="submit" className="w-full mt-2" isLoading={isLoading}>
            Sign In
          </Button>
          
          <p className="text-center text-sm text-gray-500 mt-4">
            Don't have an account?{' '}
            <Link to="/register" className="text-accent hover:underline">
              Sign Up
            </Link>
          </p>
        </form>
      </motion.div>
    </div>
  );
}
