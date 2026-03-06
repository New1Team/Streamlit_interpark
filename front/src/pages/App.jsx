import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { Routes, Route } from "react-router";
import Sample from "@/pages/Sample.jsx";


const App = () => {
  const paths = [
   
    {path: "/", element: <Sample />},
   ]
  return (
    <>
        <Routes>
          { paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />) }
        </Routes>
    </>
  )
}

export default App