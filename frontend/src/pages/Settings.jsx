import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { useToast } from '@/store/useToast';
import { apiClient } from '@/api/client';
import { Button } from '@/components/ui/Button';
import { UserCircle, Mail, Briefcase } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Settings() {
  const { user, setAuth } = useAuthStore();
  const { addToast } = useToast();
  
  const [name, setName] = useState('');
  const [bio, setBio] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setBio(user.bio || '');
    }
  }, [user]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const updated = await apiClient('/users/', {
        method: 'PUT',
        body: { name, bio }
      });
      setAuth(updated, localStorage.getItem('token'));
      addToast('Profile updated successfully!', 'success');
    } catch (err) {
      addToast(err.message || 'Failed to update profile', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto w-full p-4 md:p-8">
      <h1 className="text-3xl font-bold mb-8">Account Settings</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="col-span-1 space-y-4">
          <div className="bg-card p-6 rounded-2xl border shadow-sm flex flex-col items-center text-center">
            <div className="w-24 h-24 bg-accent/10 text-accent rounded-full flex items-center justify-center text-3xl font-bold mb-4">
              {user?.name?.[0]?.toUpperCase()}
            </div>
            <h3 className="font-semibold text-lg">{user?.name}</h3>
            <p className="text-gray-500 text-sm">{user?.email}</p>
            <div className="mt-4 pt-4 border-t w-full flex justify-center gap-2">
               <span className="text-xs bg-sidebar px-2 py-1 rounded font-medium border">Pro Plan</span>
            </div>
          </div>
        </div>

        <div className="col-span-1 md:col-span-2">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="bg-card rounded-2xl border shadow-sm overflow-hidden">
            <div className="p-6 border-b">
              <h3 className="font-semibold text-lg">Public Profile</h3>
              <p className="text-sm text-gray-500 mt-1">This information will be displayed publicly.</p>
            </div>
            <form onSubmit={handleUpdate} className="p-6 space-y-5">
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <UserCircle className="w-4 h-4 text-gray-400" /> Full Name
                </label>
                <input 
                  type="text" 
                  value={name}
                  onChange={e => setName(e.target.value)}
                  className="w-full bg-background border rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-accent outline-none transition-all"
                />
              </div>
              
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <Mail className="w-4 h-4 text-gray-400" /> Email Address
                </label>
                <input 
                  type="email" 
                  value={user?.email || ''}
                  disabled
                  className="w-full bg-sidebar border border-transparent rounded-lg px-4 py-2.5 text-sm opacity-60 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <Briefcase className="w-4 h-4 text-gray-400" /> Bio
                </label>
                <textarea 
                  value={bio}
                  onChange={e => setBio(e.target.value)}
                  rows="3"
                  className="w-full bg-background border rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-accent outline-none transition-all resize-none"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>

              <div className="pt-2">
                <Button type="submit" isLoading={isLoading} className="px-8 shadow-md shadow-accent/20">
                  Save Changes
                </Button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
