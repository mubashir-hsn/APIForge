import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { Button } from './Button';

export function Modal({ isOpen, onClose, title, children, footer }) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
          onClick={onClose}
        />
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 10 }}
          className="relative bg-card w-full max-w-md rounded-2xl shadow-2xl border flex flex-col overflow-hidden"
        >
          <div className="flex items-center justify-between p-4 border-b bg-sidebar/50">
            <h3 className="font-semibold text-lg">{title}</h3>
            <button onClick={onClose} className="p-1 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="p-5">
            {children}
          </div>
          {footer && (
            <div className="p-4 border-t bg-sidebar/30 flex justify-end gap-2">
              {footer}
            </div>
          )}
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
