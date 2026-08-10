import Intro from './components/Intro.tsx';
import Workout from './components/Workout.tsx';
import DatePicker from './components/DatePicker.tsx';
import './App.css'
import { useState } from 'react';

function App() {
  const [date, setDate] = useState(new Date());

  function updateDate(newDate: Date) {
    setDate(newDate);
  }

  return(
    <>
      <div className="intro">
        <Intro day={date.getDay()}></Intro>
      </div>
      <div className="workout">
        <Workout date={date}></Workout>
      </div>
      <div className="date">
        <DatePicker date={date} onDateChange={updateDate}></DatePicker>
      </div>
    </>
  )
}

export default App;
