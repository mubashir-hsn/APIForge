import { useThemeStore } from '@/store/useThemeStore';
import { useAuthStore } from '@/store/useAuthStore';
import { Moon, Sun, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/Button';

export default function Navbar() {
  const { theme, toggleTheme } = useThemeStore();
  const { logout, user } = useAuthStore();

  return (
    <header className="h-14 border-b flex items-center justify-between px-4 bg-background">
      <div className="flex items-center gap-2">
      </div>
      
      <div className="flex items-center gap-1.5">
        <Button variant="ghost" size="icon" onClick={toggleTheme} className="h-8 w-8 text-gray-500">
          {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
        <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center text-accent font-semibold ml-2 text-xs border border-accent/20">
          {user?.name?.[0]?.toUpperCase() || 'U'}
        </div>
        <Button variant="ghost" size="icon" onClick={logout} className="h-8 w-8 ml-1 text-gray-500 hover:text-red-500">
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
