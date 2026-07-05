import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      '/auth': 'http://localhost:8000',
      '/workspaces': 'http://localhost:8000',
      '/collections': 'http://localhost:8000',
      '/requests': 'http://localhost:8000',
      '/users': 'http://localhost:8000',
      '/environments': 'http://localhost:8000',
    }
  }
})
