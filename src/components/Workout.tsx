import raw from '../assets/workout_days.json';
const data: WorkoutDay[] = raw;

interface WorkoutDay {
    [key: string]: Workout | undefined;
}


interface Workout {
    filename: string,
    workout_type: string,
    exercises?: Exercise[]
}

interface Exercise {
    name: string,
    reps: string,
    video: string | null
}

function Workout({day}: {day: number}) {
    const workoutIds = Object.keys(data[day]);
    const numWorkouts = workoutIds.length;
    const randoWorkout = workoutIds[Math.floor(Math.random() * numWorkouts)];
    const workout: Workout | undefined = data[day][randoWorkout];
    if (workout === undefined) {
        return (<>No workout found for date {randoWorkout}, please reload.</>)
    }
    return (
        <>
            <div>{JSON.stringify(workout)}</div>
        </>
    );
}

export default Workout;