const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 }
    ],
    attendance: 82
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 76 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  },
  {
    name: "Aman",
    marks: [
      { subject: "Math", score: 86 },
      { subject: "English", score: 72 },
      { subject: "Science", score: 38 },
      { subject: "History", score: 65 },
      { subject: "Computer", score: 79 }
    ],
    attendance: 88
  },
  {
    name: "Riya",
    marks: [
      { subject: "Math", score: 67 },
      { subject: "English", score: 74 },
      { subject: "Science", score: 71 },
      { subject: "History", score: 70 },
      { subject: "Computer", score: 76 }
    ],
    attendance: 68
  }
];

// Function to calculate total marks for a student
function calculateTotalMarks(student) {
  let total = 0;

  for (let i = 0; i < student.marks.length; i++) {
    total += student.marks[i].score;
  }

  return total;
}

function calculateAverageMarks(student) {
  const total = calculateTotalMarks(student);
  return total / student.marks.length;
}

function getStudentGrade(student) {
  if (student.attendance < 75) {
    return "Fail (Low Attendance)";
  }

  for (let i = 0; i < student.marks.length; i++) {
    if (student.marks[i].score <= 40) {
      return `Fail (Failed in ${student.marks[i].subject})`;
    }
  }

  const average = calculateAverageMarks(student);

  if (average >= 85) {
    return "A";
  } else if (average >= 70) {
    return "B";
  } else if (average >= 50) {
    return "C";
  } else {
    return "Fail";
  }
}
