import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Briefcase, Folder, Settings, TerminalSquare } from 'lucide-react';

export default function Sidebar() {
  const location = useLocation();
  const links = [
    { name: 'Overview', to: '/', icon: LayoutDashboard },
    { name: 'API Builder', to: '/builder', icon: TerminalSquare },
    { name: 'Settings', to: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-[240px] bg-sidebar border-r flex flex-col h-full flex-shrink-0">
      <div className="h-14 px-4 flex items-center gap-2 border-b">
        <div className="w-6 h-6 rounded bg-accent flex items-center justify-center text-white font-bold text-xs">AP</div>
        <span className="font-semibold text-sm tracking-tight">API Platform</span>
      </div>
      
      <div className="p-3 py-4 flex-1 overflow-y-auto">
        <p className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Menu</p>
        <nav className="space-y-0.5">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.to;
            return (
              <Link 
                key={link.name} 
                to={link.to} 
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive ? 'bg-accent/10 text-accent' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200/50 dark:hover:bg-gray-800 hover:text-text'}`}
              >
                <Icon className="h-4 w-4" />
                {link.name}
              </Link>
            )
          })}
        </nav>
      </div>
    </aside>
  );
}
