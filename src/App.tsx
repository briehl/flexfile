import Intro from './components/Intro.tsx';
import Workout from './components/Workout.tsx';
import './App.css'

function App() {
  const now: Date = new Date();

  return(
    <>
      <div className="intro">
        <Intro day={now.getDay()}></Intro>
      </div>
      <div className="workout">
        <Workout date={now}></Workout>
      </div>
    </>
  )
}

export default App
