import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Arquitectura de la sección 5.1 del Informe Técnico: en desarrollo, Vite
// corre en :5173 y reenvía /api al backend en :8000 (sin configurar CORS);
// para la entrega, el build se compila directamente a backend/static/ y
// FastAPI lo sirve desde el mismo puerto que la API.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
  },
})
