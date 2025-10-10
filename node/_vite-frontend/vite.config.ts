// vite.config.js
import { resolve } from 'node:path'

export default {
   server: {
      proxy: {
         '/api': {
            target: 'http://localhost:8080',
            changeOrigin: true,
         },
      },
      fs: {
         allow: [
            './',
            '../../adobe'
         ]
      }
   },
   
   build: {
      rollupOptions: {
         input: {
            main  : resolve(__dirname, 'index.html'),
            report: resolve(__dirname, 'report.html')
         }
      }
   }
};