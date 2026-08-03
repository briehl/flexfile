export interface WorkoutT {
    filename: string,
    workout_type: string,
    exercises?: ExerciseT[]
}

export interface ExerciseT {
    name: string,
    reps: string,
    video: string | null
}