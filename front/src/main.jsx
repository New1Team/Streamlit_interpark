import App from '@pages/App.jsx'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from "react-router";


createRoot(document.getElementById('root')).render(
  // <StrictMode>
    <BrowserRouter>
        
          <App />
      
      </BrowserRouter>
    
  // </StrictMode>,

)
