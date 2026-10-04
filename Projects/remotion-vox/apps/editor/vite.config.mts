import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react-swc';
import {fileURLToPath} from 'node:url';

// Editor dev server. publicDir = repo public/ so staticFile('projects/...')
// resolves identically in Player preview and `npx remotion render`.
export default defineConfig({
  root: fileURLToPath(new URL('.', import.meta.url)),
  publicDir: fileURLToPath(new URL('../../public', import.meta.url)),
  plugins: [react()],
  server: {
    port: 5599,
    strictPort: true,
    proxy: {
      '/api': 'http://127.0.0.1:7788',
    },
  },
});
