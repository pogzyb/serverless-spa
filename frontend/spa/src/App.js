import './App.css';
import { Home } from './components/Home';
import { AppNav } from './components/Nav';

function App() {
  return (
    <div className="App">
      <AppNav/>
      <Home/>
    </div>
  );
}

export default App;
