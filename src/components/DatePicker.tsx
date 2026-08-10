function changeDate(date: Date, increment: number): Date {
    const newDate = new Date(date);
    newDate.setDate(newDate.getDate() + increment);
    return newDate;
}

function DatePicker({date, onDateChange}: {date: Date, onDateChange: Function}) {
    return (
        <>
            <button onClick={() => onDateChange(changeDate(date, -1))}>
                &lt;&lt;
            </button>
            <span className="current">
                {date.toLocaleDateString()}
            </span>
            <button onClick={() => onDateChange(changeDate(date, 1))}>
                &gt;&gt;
            </button>
        </>
    )
}

export default DatePicker;