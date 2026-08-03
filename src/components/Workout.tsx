import raw from '../assets/workout_days.json';
import type { WorkoutT, ExerciseT } from '../interfaces/Workout.tsx';
import Instructions from './Instructions.tsx';

const data: WorkoutDay[] = raw;

interface WorkoutDay {
    [key: string]: WorkoutT | undefined;
}


function Exercise({name, reps, video}: ExerciseT) {
    return (
        <>
            <div className="exercise">{name}</div>
            <div className="exercise">{reps}</div>
            <div className="exercise">{video}</div>
        </>
    );
}

function getWeek(date: Date) {
    const d = new Date(date.getTime());
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
    const week1 = new Date(d.getFullYear(), 0, 4);
    return 1 + Math.round(((d.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

function convertWorkoutType(type: string) {
    type = type.toLocaleUpperCase();
    switch(type) {
        case "CARDIO":
            return "cardio";
        case "MOBILITY":
            return "stretching and flexibility";
        default:
            return type;
    }
}

function Workout({date}: {date: Date}) {
    const day = date.getDay();
    const workoutIds = Object.keys(data[day]).sort();
    let week = getWeek(date);
    if (date.getFullYear() % 2 === 0) {
        week += 52;
    }
    const randoWorkout = workoutIds[week % workoutIds.length];
    const workout: WorkoutT | undefined = data[day][randoWorkout];
    if (workout === undefined) {
        return (<>No workout found for date {randoWorkout}, please reload or just go outside.</>);
    }
    let exercises = [<><div key="nope">No exercises given today. Make something up!</div></>];
    if (workout.exercises) {
        exercises = workout.exercises.map((exercise: ExerciseT) => (<Exercise key={exercise.name} {...exercise} />));
    }
    return (
        <>
            <div className="workoutType">{convertWorkoutType(workout.workout_type)} workout!</div>
            <div className="instructions">
                <Instructions workoutType={workout.workout_type} />
            </div>
            <div className="exerciseList">{exercises ? exercises : ""}</div>
        </>
    );
}

export default Workout;