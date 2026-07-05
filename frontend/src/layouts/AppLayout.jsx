import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import { useThemeStore } from '@/store/useThemeStore';
import { useToast } from '@/store/useToast';
import { apiClient } from '@/api/client';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { AnimatePresence, motion } from 'framer-motion';

function ToastContainer() {
  const toasts = useToast(s => s.toasts);
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      <AnimatePresence>
        {toasts.map(t => (
          <motion.div
            key={t.id}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className={`px-4 py-3 rounded-lg shadow-xl border flex items-center gap-3 ${t.type === 'error' ? 'bg-red-500 text-white border-red-600' : 'bg-card text-text'}`}
          >
            <span className="text-sm font-medium">{t.message}</span>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}

export default function AppLayout() {
  const { isAuthenticated, setAuth, logout } = useAuthStore();
  const { initTheme } = useThemeStore();
  const navigate = useNavigate();

  useEffect(() => {
    initTheme();
    if (!isAuthenticated) {
      navigate('/login');
    } else {
      apiClient('/auth/me')
        .then(res => {
          if (res.user) {
             setAuth(res.user, localStorage.getItem('token'));
          }
        })
        .catch(() => {
          logout();
          navigate('/login');
        });
    }
  }, [isAuthenticated, navigate, initTheme, setAuth, logout]);

  if (!isAuthenticated) return null;

  return (
    <div className="flex h-screen bg-background overflow-hidden selection:bg-accent/30">
      <Sidebar />
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
      <ToastContainer />
    </div>
  );
}
