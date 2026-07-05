import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '@/api/client';
import { useAuthStore } from '@/store/useAuthStore';
import { useWorkspaceStore } from '@/store/useWorkspaceStore';
import { Briefcase, Plus, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const { user } = useAuthStore();
  const { workspaces, setWorkspaces, setActiveWorkspace } = useWorkspaceStore();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newWsName, setNewWsName] = useState('');

  useEffect(() => {
    loadWorkspaces();
  }, []);

  const loadWorkspaces = async () => {
    try {
      const data = await apiClient('/workspaces/');
      setWorkspaces(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const createWorkspace = async () => {
    if (!newWsName.trim()) return;
    try {
      await apiClient('/workspaces/', { method: 'POST', body: { name: newWsName, description: '' } });
      setIsModalOpen(false);
      setNewWsName('');
      loadWorkspaces();
    } catch (e) {
      alert("Failed to create workspace");
    }
  };

  const openWorkspace = (id) => {
    setActiveWorkspace(id);
    navigate('/builder');
  };

  return (
    <div className="max-w-6xl mx-auto w-full p-4 md:p-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-10 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Welcome back{user?.name ? `, ${user.name}` : ''}</h1>
          <p className="text-gray-500 text-sm mt-1">Manage your API workspaces and collaborations.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} className="shadow-lg shadow-accent/20">
          <Plus className="h-4 w-4 mr-2" /> New Workspace
        </Button>
      </div>
      
      {isLoading ? (
        <div className="flex justify-center p-12"><span className="animate-pulse text-accent font-medium">Loading workspaces...</span></div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workspaces.map((ws, i) => (
            <motion.div 
              key={ws.id} 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="p-6 bg-card rounded-2xl border hover:border-accent hover:shadow-xl hover:shadow-accent/5 transition-all flex flex-col group cursor-pointer"
              onClick={() => openWorkspace(ws.id)}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-sidebar rounded-xl flex items-center justify-center border group-hover:bg-accent/10 group-hover:text-accent transition-colors">
                  <Briefcase className="h-5 w-5" />
                </div>
              </div>
              <h3 className="font-semibold text-lg">{ws.name}</h3>
              <p className="text-sm text-gray-500 mt-2 mb-6 flex-1">{ws.description || 'No description provided.'}</p>
              
              <div className="flex items-center text-accent font-medium text-sm group-hover:translate-x-1 transition-transform">
                Open Workspace <ArrowRight className="ml-2 h-4 w-4" />
              </div>
            </motion.div>
          ))}
          {workspaces.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-20 border-2 border-dashed rounded-2xl text-gray-500 bg-sidebar/30">
              <div className="w-16 h-16 bg-sidebar rounded-full flex items-center justify-center mb-4">
                <Briefcase className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="font-semibold text-lg text-text">No Workspaces Found</h3>
              <p className="text-sm mt-1 mb-6">Create your first workspace to get started</p>
              <Button onClick={() => setIsModalOpen(true)}>Create Workspace</Button>
            </div>
          )}
        </div>
      )}

      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
        title="Create New Workspace"
        footer={
          <>
            <Button variant="ghost" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={createWorkspace}>Create</Button>
          </>
        }
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Workspace Name</label>
            <input 
              autoFocus
              type="text" 
              value={newWsName}
              onChange={e => setNewWsName(e.target.value)}
              className="w-full bg-background border rounded-lg px-4 py-2 focus:ring-1 focus:ring-accent outline-none"
              placeholder="e.g. Production APIs"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
}
