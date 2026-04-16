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

function printStudentResults(studentList) {
  console.log("===== STUDENT TOTALS, AVERAGES, AND GRADES =====");

  for (let i = 0; i < studentList.length; i++) {
    const student = studentList[i];
    const total = calculateTotalMarks(student);
    const average = calculateAverageMarks(student);
    const grade = getStudentGrade(student);

    console.log(`${student.name} Total Marks: ${total}`);
    console.log(`${student.name} Average: ${average.toFixed(1)}`);
    console.log(`${student.name} Grade: ${grade}`);
    console.log("-----------------------------------");
  }
}


function getSubjectWiseHighest(studentList) {
  console.log("===== SUBJECT-WISE HIGHEST SCORES =====");

  const subjects = studentList[0].marks;

  for (let i = 0; i < subjects.length; i++) {
    const currentSubject = subjects[i].subject;
    let highestScore = -1;
    let highestScorer = "";

    for (let j = 0; j < studentList.length; j++) {
      const student = studentList[j];

      for (let k = 0; k < student.marks.length; k++) {
        if (
          student.marks[k].subject === currentSubject &&
          student.marks[k].score > highestScore
        ) {
          highestScore = student.marks[k].score;
          highestScorer = student.name;
        }
      }
    }

    console.log(`Highest in ${currentSubject}: ${highestScorer} (${highestScore})`);
  }
}

function getSubjectWiseAverage(studentList) {
  console.log("===== SUBJECT-WISE AVERAGE SCORES =====");

  const subjects = studentList[0].marks;

  for (let i = 0; i < subjects.length; i++) {
    const currentSubject = subjects[i].subject;
    let total = 0;

    for (let j = 0; j < studentList.length; j++) {
      const student = studentList[j];

      for (let k = 0; k < student.marks.length; k++) {
        if (student.marks[k].subject === currentSubject) {
          total += student.marks[k].score;
        }
      }
    }

    const average = total / studentList.length;
    console.log(`Average ${currentSubject} Score: ${average.toFixed(1)}`);
  }
}


function getClassTopper(studentList) {
  let topperName = "";
  let highestTotal = -1;

  for (let i = 0; i < studentList.length; i++) {
    const total = calculateTotalMarks(studentList[i]);

    if (total > highestTotal) {
      highestTotal = total;
      topperName = studentList[i].name;
    }
  }

  console.log("===== CLASS TOPPER =====");
  console.log(`Class Topper: ${topperName} with ${highestTotal} marks`);
}

// Main execution
printStudentResults(students);
getSubjectWiseHighest(students);
getSubjectWiseAverage(students);
getClassTopper(students);