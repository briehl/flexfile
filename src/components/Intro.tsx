const days = [
  "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
]

function Intro({day}: {day: number}) {
  return(
    <>
      <div className="intro">
        Hey. It's {days[day]}. That means it's time for a
      </div>
    </>
  )
}

export default Intro;