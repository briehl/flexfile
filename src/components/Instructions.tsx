function typeToText(workoutType: string) {
    switch(workoutType) {
        case 'CARDIO':
            return "Go outside and get moving for half an hour, or do 4 sets of the following:";
        case 'MOBILITY':
            return "Do 2 or 3 sets of the following. Whatever you feel.";
        default:
            return "Move your ass!";
    }
}

function Instructions({workoutType}: {workoutType: string}) {
    return (
        <>{typeToText(workoutType)}</>
    );
}

export default Instructions;