import { create } from 'zustand';

export const useWorkspaceStore = create((set) => ({
  workspaces: [],
  activeWorkspace: null,
  setWorkspaces: (workspaces) => set({ workspaces }),
  setActiveWorkspace: (id) => set({ activeWorkspace: id }),
}));
