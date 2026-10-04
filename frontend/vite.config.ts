import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:18112',
      '/oauth2': 'http://localhost:18112',
      '/logout': 'http://localhost:18112',
    },
  },
});
